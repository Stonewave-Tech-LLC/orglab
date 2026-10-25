"""E-021: Reasoning und Fehlalarme bei der Stapelprüfung (Bestätigung von H-036). Prereg: experimente/E-021-reasoning-fehlalarme/prereg.md

  python -m orglab.e021 run
  python -m orglab.e021 analyze

Nutzt Prompt, Parser und Aufruf aus orglab.batch unverändert. Rohdaten: daten/E-021-reasoning-fehlalarme/.
"""

from __future__ import annotations

import argparse
import json
import random
import statistics as st
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from . import openrouter
from .batch import judge_batch, make_batches
from .evidence import as_dict, generate_set_v2
from .factorial import SONNET
from .runner import ROOT

EXPERIMENT = "E-021-reasoning-fehlalarme"
DATA = ROOT / "daten" / EXPERIMENT
SEEDS = range(4000, 4024)
ARMS = {"low": "low", "aus": None}
CELL = "I1-S0-E0"
THRESHOLD = 0.80          # vorab festgelegt aus notizen/20b §3 (E-019 v2)
B = 10_000


def run(workers: int) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    evs = generate_set_v2(SEEDS)
    (DATA / "belege.jsonl").write_text("\n".join(json.dumps(as_dict(e), ensure_ascii=False) for e in evs), encoding="utf-8")
    batches = make_batches(evs, 12, "e021")
    calls_p, judg_p = DATA / "calls.jsonl", DATA / "judgments.jsonl"
    done = set()
    if calls_p.exists():
        for line in calls_p.read_text(encoding="utf-8").splitlines():
            c = json.loads(line)
            if c.get("parsed", 0) >= c["size"] * 0.95:
                done.add((c["batch"], c["position"], c["effort"] or "aus"))
    jobs = [(arm, bid, b, p) for bid, b in batches for p in range(3) for arm in ARMS if (bid, p, arm) not in done]
    print(f"[E-021] {len(batches) * 3 * len(ARMS)} Aufrufe geplant, offen {len(jobs)} | heute {openrouter.spent_today():.2f} $", flush=True)
    with ThreadPoolExecutor(max_workers=workers) as pool, open(calls_p, "a", encoding="utf-8") as fc, \
            open(judg_p, "a", encoding="utf-8") as fj:
        futs = {pool.submit(judge_batch, SONNET, bid, b, CELL, p, ARMS[arm]): arm for arm, bid, b, p in jobs}
        n = 0
        for f in as_completed(futs):
            try:
                call, rows = f.result()
            except openrouter.BudgetExceeded as e:
                print(f"[E-021] STOPP: {e}", flush=True)
                pool.shutdown(cancel_futures=True)
                break
            fc.write(json.dumps(call, ensure_ascii=False) + "\n")
            fj.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
            fc.flush(); fj.flush()
            n += 1
            if n % 24 == 0:
                print(f"[E-021] {n}/{len(jobs)} | heute {openrouter.spent_today():.2f} $", flush=True)
    print(f"[E-021] fertig | heute {openrouter.spent_today():.2f} $", flush=True)


# --- Auswertung (vor dem ersten Lauf festgelegt) ------------------------------------------

def _load() -> tuple[list[dict], list[dict]]:
    calls = [json.loads(l) for l in (DATA / "calls.jsonl").read_text(encoding="utf-8").splitlines()]
    last: dict[tuple, dict] = {}
    for l in (DATA / "judgments.jsonl").read_text(encoding="utf-8").splitlines():
        j = json.loads(l)
        j["arm"] = j["effort"] or "aus"
        last[(j["arm"], j["id"], j["position"])] = j
    return calls, list(last.values())


def item_rate(js: list[dict], arm: str, truth: bool) -> dict[str, float]:
    by = defaultdict(list)
    for j in js:
        if j["arm"] == arm and j["truth"] == truth and j["verdict"] is not None:
            by[j["id"]].append(int(j["verdict"] != j["truth"]))
    return {k: st.fmean(v) for k, v in by.items()}


def paired_diff(a: dict[str, float], b: dict[str, float]) -> list[float]:
    return [a[k] - b[k] for k in sorted(a) if k in b]


def one_sided(values: list[float], seed: int = 21) -> tuple[float, float, float]:
    """Mittelwert, untere und obere Grenze des einseitigen 95-%-KI (5. bzw. 95. Perzentil), Anteil Ziehungen ≤ 0."""
    rng = random.Random(seed)
    n = len(values)
    means = sorted(st.fmean(rng.choices(values, k=n)) for _ in range(B))
    return st.fmean(values), means[int(0.05 * B)], means[int(0.95 * B) - 1], sum(m <= 0 for m in means) / B


def analyze() -> str:
    calls, js = _load()
    valid = [j for j in js if j["verdict"] is not None]
    L = ["# E-021 Ergebnis (automatisch erzeugt)", "",
         f"Aufrufe: {len(calls)}, Urteile: {len(js)}, gültig: {len(valid)}", ""]
    for arm in ARMS:
        a = [j for j in js if j["arm"] == arm]
        miss = 1 - sum(j["verdict"] is not None for j in a) / max(len(a), 1)
        L.append(f"- Arm {arm}: {len(a)} Urteile, fehlend {miss:.3f}")
    fa = {arm: item_rate(js, arm, True) for arm in ARMS}
    ms = {arm: item_rate(js, arm, False) for arm in ARMS}
    d1 = paired_diff(fa["low"], fa["aus"])
    m1, lo1, hi1, p1 = one_sided(d1)
    d2 = paired_diff(ms["aus"], ms["low"])
    m2, lo2, hi2, _ = one_sided(d2, seed=22)
    p1_ok = lo1 > 0 and m1 > 0
    p2_ok = hi2 <= 0.03
    L += ["", "## Primär", "",
          f"- **FA(low)** = {st.fmean(fa['low'].values()):.3f}, **FA(aus)** = {st.fmean(fa['aus'].values()):.3f} (ok-Belege: {len(d1)})",
          f"- **P1** Δ Fehlalarm (low − aus) = **{m1:+.3f}**, einseitiges 95-%-KI untere Grenze {lo1:+.3f}, Bootstrap-p = {p1:.4f} "
          f"→ {'erfüllt' if p1_ok else 'NICHT erfüllt'} (Relevanz ≥ +0,05: {'ja' if m1 >= 0.05 else 'nein'})",
          f"- **Miss(low)** = {st.fmean(ms['low'].values()):.3f}, **Miss(aus)** = {st.fmean(ms['aus'].values()):.3f} (kaputte Belege: {len(d2)})",
          f"- **P2** Δ Übersehen (aus − low) = **{m2:+.3f}**, obere Grenze des einseitigen 95-%-KI {hi2:+.3f} (Grenze +0,03) "
          f"→ {'erfüllt' if p2_ok else 'NICHT erfüllt'}",
          f"- **H-036: {'BESTÄTIGT' if p1_ok and p2_ok else 'NICHT bestätigt'}** (P1 und P2 gemeinsam)"]
    # Sekundär S1/S2
    L += ["", "## Sekundär", "", f"S1: Eskalation bei Konfidenz < {THRESHOLD:.2f} (Schwelle vorab festgelegt)", "",
          "| Arm | eskaliert | gefangene Fehler | PPV der Alarme bei 50 % | PPV bei 5 % |", "|---|---|---|---|---|"]
    for arm in ARMS:
        a = [j for j in valid if j["arm"] == arm and j.get("confidence") is not None]
        esc = [j for j in a if j["confidence"] < THRESHOLD]
        errs = [j for j in a if j["verdict"] != j["truth"]]
        caught = sum(1 for j in esc if j["verdict"] != j["truth"])

        def ppv(prev: float) -> float:
            w = lambda j: (prev / 0.5) if not j["truth"] else ((1 - prev) / 0.5)
            alarms = [j for j in a if j["verdict"] is False]
            return sum(w(j) for j in alarms if not j["truth"]) / max(sum(w(j) for j in alarms), 1e-9)

        L.append(f"| {arm} | {len(esc) / max(len(a), 1):.2f} | {caught / max(len(errs), 1):.2f} | {ppv(0.5):.2f} | {ppv(0.05):.2f} |")
    L += ["", "S3: Fehlalarm je Domäne/Kanal", "", "| Domäne/Kanal | low | aus |", "|---|---|---|"]
    cells = sorted({(j["domain"], j["channel"]) for j in valid})
    for d, c in cells:
        r = {arm: [int(j["verdict"] != j["truth"]) for j in valid if j["arm"] == arm and j["truth"] and j["domain"] == d and j["channel"] == c]
             for arm in ARMS}
        L.append(f"| {d}/{c} | {st.fmean(r['low']) if r['low'] else float('nan'):.3f} | {st.fmean(r['aus']) if r['aus'] else float('nan'):.3f} |")
    toks = {arm: [c.get("completion_tokens") or 0 for c in calls if (c["effort"] or "aus") == arm] for arm in ARMS}
    L += ["", f"Manipulationscheck, Completion-Tokens je Aufruf: low {st.fmean(toks['low']):.0f}, aus {st.fmean(toks['aus']):.0f}",
          f"Kosten: {sum(float(c.get('cost_usd') or 0) for c in calls):.2f} $"]
    # Generatorfehler-Regel
    flagged = [k for k in fa["low"] if fa["low"].get(k) == 1 and fa["aus"].get(k) == 1]
    L += ["", f"Generatorfehler-Regel: ok-Belege in beiden Armen in allen 3 Kanälen als kaputt beurteilt: {flagged or 'keine'}"]
    text = "\n".join(L)
    (DATA / "auswertung.md").write_text(text, encoding="utf-8")
    return text


def transcripts() -> None:
    calls, _ = _load()
    rng = random.Random(2021)
    out = ["# E-021 Transkripte (2 zufällige Stapel-Antworten je Arm, Pflichtlektüre)", ""]
    for arm in ARMS:
        cs = [c for c in calls if (c["effort"] or "aus") == arm and c.get("raw")]
        for c in rng.sample(cs, min(2, len(cs))):
            out += [f"## Arm {arm} · {c['batch']} · Position {c['position']}", "", "```", c["raw"][-3000:], "```", ""]
    (ROOT / "experimente" / EXPERIMENT / "transkripte.md").write_text("\n".join(out), encoding="utf-8")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["run", "analyze"])
    p.add_argument("--workers", type=int, default=6)
    a = p.parse_args()
    if a.cmd == "run":
        run(a.workers)
    else:
        print(analyze())
        transcripts()


if __name__ == "__main__":
    main()
