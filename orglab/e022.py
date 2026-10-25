"""E-022: Reasoning-Dosis und Fehlalarme bei der Stapelprüfung (Bestätigung von H-037 mit gemessener Manipulation).
Prereg: experimente/E-022-reasoning-dosis/prereg.md

  python -m orglab.e022 dryrun        # Prompttext (für alle Arme gleich) nach experimente/E-022…/dryrun-prompt.md
  python -m orglab.e022 run           # erst nach Fremdkontrolle und Neos Freigabe
  python -m orglab.e022 analyze

Prompt, Parser und Aufruf aus orglab.batch unverändert (wie E-021). Neu gegenüber E-021: vier Arme, Cluster-Bootstrap
über Stapel (Regel 13), Manipulationscheck als Bedingung (Regel 10), nur vollständige Stapel gehen in die Auswertung.
"""

from __future__ import annotations

import argparse
import json
import random
import statistics as st
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from . import openrouter
from .batch import build_batch_prompt, judge_batch, make_batches
from .evidence import as_dict, generate_set_v2
from .factorial import SONNET
from .runner import ROOT

EXPERIMENT = "E-022-reasoning-dosis"
DATA = ROOT / "daten" / EXPERIMENT
SEEDS = range(5000, 5024)
# Arm -> Wert für reasoning.effort; None = Parameter weggelassen (adaptives Reasoning, E-021)
ARMS: dict[str, str | None] = {"low": "low", "medium": "medium", "high": "high", "ohne": None}
CELL = "I1-S0-E0"
POSITIONS = 3
THRESHOLD = 0.80          # Eskalationsschwelle, vorab festgelegt aus notizen/20b §3 (E-019 v2)
B = 10_000
RELEVANT = 0.05           # P1-Relevanzgrenze
NONINF = 0.03             # P2-Grenze
MC_RATIO = 1.5            # Manipulationscheck: Median-Tokens high ≥ 1,5 × low
COST_STOP = 10.0          # Abbruch, damit der Lauf unter der Grenze für externe Kritik bleibt (Regel 18)


def arm_of(effort: str | None) -> str:
    return next(a for a, e in ARMS.items() if e == effort)


def batches() -> list[tuple[str, list]]:
    return make_batches(generate_set_v2(SEEDS), 12, "e022")


def run(workers: int) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    evs = generate_set_v2(SEEDS)
    (DATA / "belege.jsonl").write_text("\n".join(json.dumps(as_dict(e), ensure_ascii=False) for e in evs), encoding="utf-8")
    bs = make_batches(evs, 12, "e022")
    calls_p, judg_p = DATA / "calls.jsonl", DATA / "judgments.jsonl"
    done = set()
    if calls_p.exists():
        for line in calls_p.read_text(encoding="utf-8").splitlines():
            c = json.loads(line)
            if c.get("parsed", 0) >= c["size"] * 0.95:
                done.add((c["batch"], c["position"], arm_of(c["effort"])))
    # Stapelweise Reihenfolge: Der Pool arbeitet die Warteschlange in dieser Reihenfolge ab, sodass bei Abbruch
    # fast nur vollständige Stapel (alle Arme × Positionen) vorliegen. Ausgewertet werden nur vollständige.
    jobs = [(arm, bid, b, p) for bid, b in bs for p in range(POSITIONS) for arm in ARMS if (bid, p, arm) not in done]
    print(f"[E-022] {len(bs) * POSITIONS * len(ARMS)} Aufrufe geplant, offen {len(jobs)} | heute {openrouter.spent_today():.2f} $",
          flush=True)
    spent = _spent()
    with ThreadPoolExecutor(max_workers=workers) as pool, open(calls_p, "a", encoding="utf-8") as fc, \
            open(judg_p, "a", encoding="utf-8") as fj:
        futs = [pool.submit(judge_batch, SONNET, bid, b, CELL, p, ARMS[arm]) for arm, bid, b, p in jobs]
        n = 0
        for f in as_completed(futs):
            try:
                call, rows = f.result()
            except openrouter.BudgetExceeded as e:
                print(f"[E-022] STOPP: {e}", flush=True)
                pool.shutdown(cancel_futures=True)
                break
            fc.write(json.dumps(call, ensure_ascii=False) + "\n")
            fj.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
            fc.flush(); fj.flush()
            spent += float(call.get("cost_usd") or 0)
            n += 1
            if spent > COST_STOP:
                print(f"[E-022] STOPP: Kosten {spent:.2f} $ > {COST_STOP} $", flush=True)
                pool.shutdown(cancel_futures=True)
                break
            if n % 24 == 0:
                print(f"[E-022] {n}/{len(jobs)} | Experiment {spent:.2f} $ | heute {openrouter.spent_today():.2f} $", flush=True)
    print(f"[E-022] fertig | Experiment {spent:.2f} $", flush=True)


def _spent() -> float:
    p = DATA / "calls.jsonl"
    return sum(float(json.loads(l).get("cost_usd") or 0) for l in p.read_text(encoding="utf-8").splitlines()) if p.exists() else 0.0


def dryrun() -> str:
    bid, b = batches()[0]
    out = ["# E-022 Dry-Run: exakter Prompttext (Regel 16)", "",
           "Der Text ist in allen vier Armen identisch. Die Arme unterscheiden sich nur im API-Parameter "
           "`reasoning.effort` (low, medium, high, weggelassen). Gezeigt: Stapel 1, Positionen 0–2 (jede Position sieht "
           "je Beleg einen anderen Kanal).", ""]
    for p in range(POSITIONS):
        prompt, _ = build_batch_prompt(bid, b, CELL, p)
        out += [f"## {bid}, Position {p}", "", "````", prompt, "````", ""]
    text = "\n".join(out)
    (ROOT / "experimente" / EXPERIMENT / "dryrun-prompt.md").write_text(text, encoding="utf-8")
    return text


# --- Auswertung (vor dem ersten Lauf festgelegt, mit tests/test_e022.py an synthetischen Daten geprüft) -------------

def load() -> tuple[list[dict], list[dict]]:
    calls = [json.loads(l) for l in (DATA / "calls.jsonl").read_text(encoding="utf-8").splitlines()]
    js = [json.loads(l) for l in (DATA / "judgments.jsonl").read_text(encoding="utf-8").splitlines()]
    return calls, js


def complete_batches(calls: list[dict]) -> set[str]:
    """Stapel, für die jeder Arm an jeder Position einen Aufruf mit ≥ 95 % geparsten Urteilen hat."""
    ok = defaultdict(set)
    for c in calls:
        if c.get("parsed", 0) >= c["size"] * 0.95:
            ok[c["batch"]].add((arm_of(c["effort"]), c["position"]))
    need = {(a, p) for a in ARMS for p in range(POSITIONS)}
    return {b for b, s in ok.items() if need <= s}


def latest(js: list[dict]) -> list[dict]:
    """Letztes Urteil je (Arm, Beleg, Position); Wiederholungen ersetzen frühere Versuche."""
    last: dict[tuple, dict] = {}
    for j in js:
        j = dict(j, arm=arm_of(j["effort"]))
        last[(j["arm"], j["id"], j["position"])] = j
    return list(last.values())


def item_rates(js: list[dict], arm: str, truth: bool) -> dict[str, tuple[str, float]]:
    """Je Beleg: (Stapel, Fehlerrate über seine gültigen Urteile). truth=True → Fehlalarm, False → Übersehen."""
    by: dict[str, list[int]] = defaultdict(list)
    batch: dict[str, str] = {}
    for j in js:
        if j["arm"] == arm and j["truth"] == truth and j["verdict"] is not None:
            by[j["id"]].append(int(j["verdict"] != j["truth"]))
            batch[j["id"]] = j["batch"]
    return {k: (batch[k], st.fmean(v)) for k, v in by.items()}


def paired(a: dict[str, tuple[str, float]], b: dict[str, tuple[str, float]]) -> dict[str, list[float]]:
    """Differenzen a − b je Beleg, gruppiert nach Stapel (Cluster)."""
    out: dict[str, list[float]] = defaultdict(list)
    for k in sorted(a):
        if k in b:
            out[a[k][0]].append(a[k][1] - b[k][1])
    return dict(out)


def cluster_boot(clusters: dict[str, list[float]], seed: int) -> tuple[float, float, float, float, float]:
    """Mittel über Belege; Bootstrap zieht Stapel mit Zurücklegen. Liefert Mittel, 5./95. Perzentil (einseitige
    95-%-Grenzen), 2,5./97,5. Perzentil (zweiseitiges 95-%-KI)."""
    keys = sorted(clusters)
    sums = [sum(clusters[k]) for k in keys]
    ns = [len(clusters[k]) for k in keys]
    mean = sum(sums) / max(sum(ns), 1)
    rng = random.Random(seed)
    means = []
    for _ in range(B):
        idx = [rng.randrange(len(keys)) for _ in keys]
        n = sum(ns[i] for i in idx)
        means.append(sum(sums[i] for i in idx) / n if n else 0.0)
    means.sort()
    q = lambda p: means[min(int(p * B), B - 1)]
    return mean, q(0.05), q(0.95), q(0.025), q(0.975)


def rate_ci(r: dict[str, tuple[str, float]], seed: int) -> tuple[float, float, float]:
    cl: dict[str, list[float]] = defaultdict(list)
    for b, v in r.values():
        cl[b].append(v)
    m, _, _, lo, hi = cluster_boot(dict(cl), seed)
    return m, lo, hi


def manipulation_check(calls: list[dict], keep: set[str]) -> tuple[bool, dict[str, float]]:
    med = {a: st.median([c.get("completion_tokens") or 0 for c in calls
                         if arm_of(c["effort"]) == a and c["batch"] in keep] or [0]) for a in ARMS}
    ok = med["low"] < med["medium"] < med["high"] and med["high"] >= MC_RATIO * med["low"]
    return ok, med


def ppv(js: list[dict], prev: float) -> float:
    """Anteil echter Fehler unter den Alarmen ("works": false), umgewichtet von 50 % auf Prävalenz prev."""
    w = lambda j: (prev / 0.5) if not j["truth"] else ((1 - prev) / 0.5)
    alarms = [j for j in js if j["verdict"] is False]
    return sum(w(j) for j in alarms if not j["truth"]) / max(sum(w(j) for j in alarms), 1e-9)


def analyze_data(calls: list[dict], js: list[dict]) -> tuple[dict[str, Any], str]:
    keep = complete_batches(calls)
    js = [j for j in latest(js) if j["batch"] in keep]
    valid = [j for j in js if j["verdict"] is not None]
    res: dict[str, Any] = {"complete_batches": len(keep)}
    L = ["# E-022 Ergebnis (automatisch erzeugt)", "",
         f"Vollständige Stapel: {len(keep)} von {len({c['batch'] for c in calls})}. Urteile: {len(js)}, gültig: {len(valid)}", ""]
    for arm in ARMS:
        a = [j for j in js if j["arm"] == arm]
        L.append(f"- Arm {arm}: {len(a)} Urteile, fehlend {1 - sum(j['verdict'] is not None for j in a) / max(len(a), 1):.3f}")

    mc_ok, med = manipulation_check(calls, keep)
    res["mc_ok"], res["median_tokens"] = mc_ok, med
    L += ["", "## Manipulationscheck (Bedingung, Regel 10)", "",
          "Median Completion-Tokens je Aufruf: " + ", ".join(f"{a} {v:.0f}" for a, v in med.items()),
          f"Kriterium low < medium < high und high ≥ {MC_RATIO} × low → **{'bestanden' if mc_ok else 'NICHT bestanden'}**"]

    fa = {a: item_rates(js, a, True) for a in ARMS}
    ms = {a: item_rates(js, a, False) for a in ARMS}
    m1, lo1, _, _, _ = cluster_boot(paired(fa["low"], fa["high"]), seed=221)
    m2, _, hi2, _, _ = cluster_boot(paired(ms["high"], ms["low"]), seed=222)
    p1_ok, p2_ok = (lo1 > 0 and m1 > 0), hi2 <= NONINF
    res.update(p1=m1, p1_lo=lo1, p1_ok=p1_ok, p1_relevant=m1 >= RELEVANT, p2=m2, p2_hi=hi2, p2_ok=p2_ok)
    res["h037"] = p1_ok and p2_ok and mc_ok
    if p1_ok and p2_ok and not mc_ok:
        verdict = "Kontrast erfüllt, aber Manipulationscheck gescheitert → H-037 NICHT bestätigt; Befund gilt nur unter der tatsächlichen Manipulation"
    else:
        verdict = "BESTÄTIGT" if res["h037"] else "NICHT bestätigt"
    L += ["", "## Primär (Cluster-Bootstrap über Stapel, einseitig 95 %)", "",
          f"- **P1** Δ Fehlalarm (low − high) = **{m1:+.3f}**, untere Grenze {lo1:+.3f} → {'erfüllt' if p1_ok else 'NICHT erfüllt'}"
          f" (Relevanz ≥ +{RELEVANT}: {'ja' if m1 >= RELEVANT else 'nein'}; ok-Belege {sum(len(v) for v in paired(fa['low'], fa['high']).values())})",
          f"- **P2** Δ Übersehen (high − low) = **{m2:+.3f}**, obere Grenze {hi2:+.3f} (Grenze +{NONINF}) → {'erfüllt' if p2_ok else 'NICHT erfüllt'}",
          f"- **H-037: {verdict}** (P1, P2 und Manipulationscheck gemeinsam)"]

    L += ["", "## Sekundär (vorab festgelegt, nicht konfirmatorisch)", "",
          "S1 Dosis: Raten je Arm (Mittel über Belege, zweiseitiges 95-%-KI über Stapel)", "",
          "| Arm | Median-Tokens | Fehlalarm | Übersehen | PPV bei 50 % | PPV bei 5 % |", "|---|---|---|---|---|---|"]
    res["fa"], res["miss"] = {}, {}
    for i, a in enumerate(ARMS):
        f, flo, fhi = rate_ci(fa[a], 230 + i)
        m, mlo, mhi = rate_ci(ms[a], 240 + i)
        res["fa"][a], res["miss"][a] = f, m
        va = [j for j in valid if j["arm"] == a]
        L.append(f"| {a} | {med[a]:.0f} | {f:.3f} [{flo:.3f}; {fhi:.3f}] | {m:.3f} [{mlo:.3f}; {mhi:.3f}] | "
                 f"{ppv(va, 0.5):.2f} | {ppv(va, 0.05):.2f} |")
    mono = res["fa"]["low"] > res["fa"]["medium"] >= res["fa"]["high"]
    L.append(f"\nErwartung FA(low) > FA(medium) ≥ FA(high): {'ja' if mono else 'nein'}")
    d, _, _, dlo, dhi = cluster_boot(paired(fa["ohne"], fa["high"]), seed=250)
    L.append(f"\nS2 Δ Fehlalarm (ohne − high) = {d:+.3f} [{dlo:+.3f}; {dhi:+.3f}] (E-021-Probe: gleich)")
    L += ["", f"S3 Eskalation bei Konfidenz < {THRESHOLD:.2f}", "", "| Arm | eskaliert | gefangene Fehler |", "|---|---|---|"]
    for a in ARMS:
        va = [j for j in valid if j["arm"] == a and j.get("confidence") is not None]
        esc = [j for j in va if j["confidence"] < THRESHOLD]
        errs = sum(j["verdict"] != j["truth"] for j in va)
        L.append(f"| {a} | {len(esc) / max(len(va), 1):.2f} | {sum(j['verdict'] != j['truth'] for j in esc) / max(errs, 1):.2f} |")
    L += ["", "S4 Fehlalarm je Domäne", "", "| Domäne | " + " | ".join(ARMS) + " |", "|---|" + "---|" * len(ARMS)]
    for dom in sorted({j["domain"] for j in valid}):
        cells = []
        for a in ARMS:
            r = [int(j["verdict"] != j["truth"]) for j in valid if j["arm"] == a and j["truth"] and j["domain"] == dom]
            cells.append(f"{st.fmean(r):.3f}" if r else "–")
        L.append(f"| {dom} | " + " | ".join(cells) + " |")
    flagged = sorted(k for k in fa["low"] if all(fa[a].get(k, ("", 0))[1] == 1 for a in ARMS))
    cost = sum(float(c.get("cost_usd") or 0) for c in calls)
    L += ["", f"Generatorfehler-Regel: ok-Belege in allen Armen und Kanälen als kaputt beurteilt: {flagged or 'keine'}",
          f"Kosten: {cost:.2f} $"]
    res["flagged"], res["cost"] = flagged, cost
    return res, "\n".join(L)


def analyze() -> str:
    calls, js = load()
    _, text = analyze_data(calls, js)
    (DATA / "auswertung.md").write_text(text, encoding="utf-8")
    return text


def transcripts() -> None:
    calls, _ = load()
    rng = random.Random(2022)
    out = ["# E-022 Transkripte (2 zufällige Stapel-Antworten je Arm, Pflichtlektüre)", ""]
    for arm in ARMS:
        cs = [c for c in calls if arm_of(c["effort"]) == arm and c.get("raw")]
        for c in rng.sample(cs, min(2, len(cs))):
            out += [f"## Arm {arm} · {c['batch']} · Position {c['position']}", "", "```", c["raw"][-3000:], "```", ""]
    (ROOT / "experimente" / EXPERIMENT / "transkripte.md").write_text("\n".join(out), encoding="utf-8")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["dryrun", "run", "analyze"])
    p.add_argument("--workers", type=int, default=6)
    a = p.parse_args()
    if a.cmd == "dryrun":
        print(dryrun()[:2000])
    elif a.cmd == "run":
        run(a.workers)
    else:
        print(analyze())
        transcripts()


if __name__ == "__main__":
    main()
