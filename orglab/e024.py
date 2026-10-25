"""E-024: Bestätigungslauf zu E-023 (Stufe Bestätigung). Präregistrierung: experimente/E-024-bestaetigung-massstab/prereg.md

Design wie E-020 v3/E-023 (Material v4.3, 8 Zellen, Prompts, Werkzeuge), **frische Seeds 7000–7023**, beide Modelle.
Geprüft werden fünf gerichtete Vorhersagen für Haiku: V1 (fehlender Sollwert), W1 (Wechselwirkung mit Sonnet),
C1/C2 (Kanal-Werkzeuge verdrängen das Nachschlagen und erhöhen dadurch das Übersehen), F1 (Selbstauskunft erhöht Fehlalarme).

  python -m orglab.e024 pilot                 # nur Technik, Seeds 1600–1601, beide Modelle
  python -m orglab.e024 run                   # Hauptlauf (erst nach Freigabe und Grok-Gutachten)
  python -m orglab.verblindung verblinden E-024-bestaetigung-massstab --feld model \
      --arme anthropic/claude-sonnet-5.5 anthropic/claude-haiku-5.5 --weg completion_tokens cost_usd final lookup_topics error
  python -m orglab.e024 verblindet            # Auswertung der verblindeten Kopie (Arme A/B) → auswertung-verblindet.md
  python -m orglab.verblindung entblinden E-024-bestaetigung-massstab
  python -m orglab.e024 analyze               # entblindet: Entscheidungen je Vorhersage, Profil je Modell
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

from . import e020v3 as base
from . import openrouter
from .evidence_v4 import as_dict, generate_set
from .factorial import SONNET
from .runner import ROOT

EXPERIMENT = "E-024-bestaetigung-massstab"
DATA = ROOT / "daten" / EXPERIMENT
EXPDIR = ROOT / "experimente" / EXPERIMENT
HAIKU = "anthropic/claude-haiku-5.5"
MODELS = (SONNET, HAIKU)
SEEDS = range(7000, 7024)
PILOT_SEEDS = range(1600, 1602)
COST_STOP = 60.0
MIN_SEEDS = 16
# Vorhersagewerte (prereg): deutlich unter den E-023-Schätzungen, weil entdeckte Effekte beim Nachmessen meist schrumpfen
NEED = {"V1": 0.10, "W1": 0.10, "C1": 0.20, "C2": 0.10, "F1": 0.02}
# Fremdkontrolle 47/48: Zähler über die Laufzeit ergibt 113/min gegen Normband 120–180 (echte Mehrdeutigkeit)
GRENZFAELLE = ["coding-ok_clear-7009"]


def run(seeds: range, tag: str, workers: int) -> None:
    """Beide Modelle, seedweise Warteschlange (Seed für Seed, je Seed beide Modelle), Kostenstopp über beide."""
    DATA.mkdir(parents=True, exist_ok=True)
    evs = generate_set(seeds)
    (DATA / f"belege{tag}.jsonl").write_text("\n".join(json.dumps(as_dict(e), ensure_ascii=False) for e in evs), encoding="utf-8")
    jpath, tpath = DATA / f"judgments{tag}.jsonl", DATA / f"transcripts{tag}.jsonl"
    done, spent = set(), 0.0
    if jpath.exists():
        for line in jpath.read_text(encoding="utf-8").splitlines():
            j = json.loads(line)
            spent += float(j.get("cost_usd") or 0)
            if j.get("verdict") is not None:
                done.add((j["model"], j["id"], j["cell"]))
    order = sorted(evs, key=lambda e: (int(e.id.rsplit("-", 1)[1]), e.id))
    jobs = [(m, e, c) for e in order for m in MODELS for c in base.CELLS if (m, e.id, c) not in done]
    print(f"[E-024] {len(evs) * len(base.CELLS) * len(MODELS)} Prüfungen, offen {len(jobs)} | heute "
          f"{openrouter.spent_today():.2f} $", flush=True)
    n = 0
    with ThreadPoolExecutor(max_workers=workers) as pool, open(jpath, "a", encoding="utf-8") as fj, \
            open(tpath, "a", encoding="utf-8") as ft:
        futs = [pool.submit(base.judge, e, c, m) for m, e, c in jobs]
        for f in as_completed(futs):
            try:
                row, tr = f.result()
            except openrouter.BudgetExceeded as e:
                print(f"[E-024] STOPP: {e}", flush=True)
                pool.shutdown(cancel_futures=True)
                break
            tr["model"] = row["model"]
            fj.write(json.dumps(row, ensure_ascii=False) + "\n")
            ft.write(json.dumps(tr, ensure_ascii=False) + "\n")
            fj.flush(); ft.flush()
            spent += float(row.get("cost_usd") or 0)
            n += 1
            if spent > COST_STOP:
                print(f"[E-024] STOPP: Kosten {spent:.2f} $ > {COST_STOP} $", flush=True)
                pool.shutdown(cancel_futures=True)
                break
            if n % 200 == 0:
                print(f"[E-024] {n}/{len(jobs)} | Experiment {spent:.2f} $", flush=True)
    print(f"[E-024] fertig, {n} neue Prüfungen, Experiment {spent:.2f} $", flush=True)


# --- Auswertung (arbeitet mit echten Modellnamen oder verblindeten Armen A/B gleichermaßen) -------------------------------

def prepare(js: list[dict]) -> tuple[dict[str, list[dict]], set[int]]:
    """Letzter Datensatz je (Arm, Beleg, Zelle); nur Seeds, die in ALLEN Armen vollständig sind (Paarung über Modelle)."""
    last: dict[tuple, dict] = {}
    for j in js:
        last[(j["model"], j["id"], j["cell"])] = j
    arms: dict[str, list[dict]] = defaultdict(list)
    for (arm, _, _), j in last.items():
        arms[arm].append(j)
    seeds = set.intersection(*(base.complete_seeds(v, 12) for v in arms.values())) if arms else set()
    return {a: [j for j in v if j["seed"] in seeds and j.get("verdict") is not None] for a, v in arms.items()}, seeds


def per_item(js: list[dict], select, factor: str, value, keep=None) -> dict[str, float]:
    """Je Beleg: Mittel von `value` in Stufe 1 minus Stufe 0 von `factor`, über die übrigen Zellen gemittelt.
    `select(j)` wählt die Zeilen (z. B. nur SPEC = 1), `keep(id)` die Belege."""
    by: dict[str, dict[int, list[float]]] = defaultdict(lambda: {0: [], 1: []})
    for j in js:
        if select(j) and (keep is None or keep(j["id"])):
            by[j["id"]][j[factor]].append(float(value(j)))
    return {i: st.fmean(v[1]) - st.fmean(v[0]) for i, v in by.items() if v[0] and v[1]}


def miss(j: dict) -> int:
    return int(j["verdict"] is True)


def contrasts(js: list[dict], keep=None, f1_exclude: set[str] | frozenset = frozenset()) -> dict[str, dict[str, float]]:
    """Die fünf Kontraste je Beleg für EIN Modell (W1 entsteht erst aus zwei Modellen).
    F1 nur auf Ok-Belegen, die auch mit EINEM Kanal entscheidbar sind (Abweichung vor dem Start: `f1_exclude` =
    Einzelkanal-Ausschluss). Sonst wäre ein "kaputt" für unbelegbaren Erfolg als Fehlalarm gezählt."""
    f1_keep = lambda i: i not in f1_exclude and (keep is None or keep(i))
    broken_prim = lambda j: not j["truth"] and j["primary"]
    return {
        # V1: Übersehen SPEC 1 − 0, spec-reine kaputte Belege
        "V1": per_item(js, broken_prim, "SP", miss, keep),
        # C1: Nachschlagen ZUGANG 0 − 1 bei SPEC = 1, alle Belege (positiv = Kanal-Werkzeuge verdrängen das Nachschlagen)
        "C1": {i: -v for i, v in per_item(js, lambda j: j["SP"] == 1, "ZU", lambda j: j["looked_up"]).items()},
        # C2: Übersehen ZUGANG 1 − 0 bei SPEC = 1, spec-reine kaputte Belege
        "C2": per_item(js, lambda j: j["SP"] == 1 and broken_prim(j), "ZU", miss, keep),
        # F1: Fehlalarm AUSKUNFT 1 − 0, Ok-Belege
        "F1": per_item(js, lambda j: j["truth"], "AU", lambda j: j["verdict"] is False, f1_keep),
    }


def label(lo: float, hi: float, q: float, need: float, descriptive: bool, weak: bool = False) -> str:
    """Entscheidungsregel laut prereg (Abschnitt Vorhersagen). Bestätigt = nachgewiesen (untere Grenze > 0 und q ≤ 0,05),
    auch wenn kleiner als vorhergesagt. F1 (schwache Power) heißt ohne Nachweis nur "nicht bestätigt", nie "widerlegt"."""
    if descriptive:
        return "nur deskriptiv"
    if lo > 0 and q <= 0.05:
        return ("BESTÄTIGT (Vorhersagewert nicht ausgeschlossen)" if hi >= need
                else "BESTÄTIGT, aber kleiner als vorhergesagt (Größe beachten)")
    if weak:
        return "nicht bestätigt (schwache Power, kein Widerlegen)"
    if hi < 0.02:
        return "nicht bestätigt: praktisch null (widerlegt)"
    if hi < need:
        return "nicht bestätigt: Vorhersagewert ausgeschlossen (widerlegt)"
    return "nicht bestätigt: nicht entschieden"


SEEDS_BOOT = {"V1": 241, "W1": 242, "C1": 243, "C2": 244, "F1": 245}
SEEDS_P = {"V1": 251, "W1": 252, "C1": 253, "C2": 254, "F1": 255}


def evaluate(arms: dict[str, list[dict]], target: str, other: str, keep=None, descriptive: bool = False,
             f1_exclude: set[str] | frozenset = frozenset()) -> dict[str, dict]:
    """Fünf Vorhersagen für `target` (Haiku), W1 = target − other gepaart je Beleg. BH über alle fünf."""
    ct, co = contrasts(arms[target], keep, f1_exclude), contrasts(arms[other], keep, f1_exclude)
    vals = {k: list(ct[k].values()) for k in ("V1", "C1", "C2", "F1")}
    common = sorted(set(ct["V1"]) & set(co["V1"]))
    vals["W1"] = [ct["V1"][i] - co["V1"][i] for i in common]
    out = {}
    for k in ("V1", "W1", "C1", "C2", "F1"):
        m, lo, hi = base.boot(vals[k], SEEDS_BOOT[k])
        out[k] = {"m": m, "lo": lo, "hi": hi, "n": len(vals[k]), "p": base.p_greater(vals[k], SEEDS_P[k])}
    q = base.bh({k: v["p"] for k, v in out.items()})
    for k, v in out.items():
        v["q"] = q[k]
        v["label"] = label(v["lo"], v["hi"], v["q"], NEED[k], descriptive, k == "F1")
        v["other"] = st.fmean(co[k].values()) if k != "W1" and co[k] else float("nan")
    return out


TEXT = {"V1": "Übersehen SPEC 1 − 0 (spec-rein)", "W1": "V1 Ziel − V1 Vergleich, gepaart je Beleg",
        "C1": "Nachschlagen ZUGANG 0 − 1 bei SPEC = 1", "C2": "Übersehen ZUGANG 1 − 0 bei SPEC = 1 (spec-rein)",
        "F1": "Fehlalarm AUSKUNFT 1 − 0 (Ok-Belege)"}


def table(res: dict[str, dict], target: str, other: str) -> list[str]:
    L = [f"| Nr | Kontrast | Ziel = {target} [95-%-KI] | q | Vorhersage | Etikett | Vergleich = {other} |", "|---|---|---|---|---|---|---|"]
    for k, v in res.items():
        L.append(f"| {k} | {TEXT[k]} | **{v['m']:+.3f}** [{v['lo']:+.3f}; {v['hi']:+.3f}] (n = {v['n']}) | {v['q']:.4f} | "
                 f"≥ {NEED[k]:+.2f} | {v['label']} | {v['other']:+.3f} |")
    return L


def exclusion() -> set[str]:
    p = EXPDIR / "einzelkanal-ausschluss.json"
    if not p.exists():
        raise FileNotFoundError(f"{p} fehlt: ohne Einzelkanal-Ausschluss ist F1 nicht wie präregistriert auswertbar")
    return set(json.loads(p.read_text(encoding="utf-8")))


def manipulation_check(js: list[dict]) -> dict[str, dict]:
    """Je Arm, auf allen Zeilen vor dem Filtern: run_check bei ZUGANG = 1 im Mittel, höchster Ausfallanteil je Zelle.
    Verrät das Modell nicht (beide Modelle fragen laut Pilot 3,0 ab)."""
    last: dict[tuple, dict] = {}
    for j in js:
        last[(j["model"], j["id"], j["cell"])] = j
    out = {}
    for arm in sorted({k[0] for k in last}):
        rows = [j for (a, _, _), j in last.items() if a == arm]
        zu1 = [j for j in rows if j["ZU"] == 1]
        n_cell = len(SEEDS) * 12
        fails = {c: n_cell - sum(1 for j in rows if j["cell"] == c and j.get("verdict") is not None) for c in base.CELLS}
        rc = st.fmean(j["n_checks"] for j in zu1) if zu1 else 0.0
        mx = max(fails.values()) / n_cell
        out[arm] = {"run_check": rc, "max_ausfall": mx, "ok": rc >= 1 and mx <= 0.05}
    return out


def analyze_blind(js: list[dict]) -> str:
    """Verblindet: Arme heißen A und B. Beide Zuordnungen werden vollständig berechnet, entschieden wird nach dem Entblinden."""
    arms, seeds = prepare(js)
    names = sorted(arms)
    desc = len(seeds) < MIN_SEEDS
    ex = exclusion()
    mc = manipulation_check(js)
    L = ["# E-024 Auswertung, VERBLINDET (automatisch erzeugt)", "",
         f"Arme: {', '.join(names)}. Vollständige Seeds (in allen Armen): {len(seeds)}. Gültige Urteile je Arm: "
         + ", ".join(f"{a} {len(v)}" for a, v in arms.items()), "",
         "Manipulationscheck je Arm (prereg: run_check bei ZUGANG=1 im Mittel ≥ 1, Ausfälle ≤ 5 % je Zelle): "
         + "; ".join(f"{a}: run_check {m['run_check']:.2f}, max. Ausfall je Zelle {m['max_ausfall']:.1%} → "
                     f"{'bestanden' if m['ok'] else 'GESCHEITERT (nur deskriptiv)'}" for a, m in mc.items()), ""]
    if desc:
        L += [f"**Weniger als {MIN_SEEDS} vollständige Seeds: nur deskriptiv.**", ""]
    desc = desc or not all(m["ok"] for m in mc.values())
    for t in names:
        o = [a for a in names if a != t][0]
        L += [f"## Falls {t} = Haiku (Ziel) und {o} = Sonnet (Vergleich)", ""]
        L += table(evaluate(arms, t, o, descriptive=desc, f1_exclude=ex), t, o)
        L += ["", f"Ohne die {len(ex)} einzeln nicht entscheidbaren Belege (vorab festgelegt, sekundär):", ""]
        L += table(evaluate(arms, t, o, keep=lambda i: i not in ex, descriptive=desc, f1_exclude=ex), t, o)
        L += ["", f"Ohne Grenzfall {GRENZFAELLE} (vorab festgelegt):", ""]
        L += table(evaluate(arms, t, o, keep=lambda i: i not in GRENZFAELLE, descriptive=desc, f1_exclude=ex), t, o)
        L += [""]
    return "\n".join(L)


def profile(js: list[dict]) -> dict[str, float]:
    ok = [j for j in js if j.get("verdict") is not None]
    toks = sorted(j["completion_tokens"] for j in ok)
    sp1 = [j for j in ok if j["SP"] == 1]
    zu1 = [j for j in ok if j["ZU"] == 1]
    return {"n": len(js), "ausfaelle": len(js) - len(ok), "tokens": toks[len(toks) // 2] if toks else 0,
            "nachgeschlagen_sp1": st.fmean(j["looked_up"] for j in sp1) if sp1 else float("nan"),
            "run_check_zu1": st.fmean(j["n_checks"] for j in zu1) if zu1 else float("nan")}


def analyze(js: list[dict]) -> str:
    """Entblindet: Entscheidungen für Haiku, Profil und Manipulationscheck je Modell."""
    arms, seeds = prepare(js)
    desc = len(seeds) < MIN_SEEDS
    ex = exclusion()
    L = ["# E-024 Auswertung, entblindet (automatisch erzeugt)", "", f"Vollständige Seeds (beide Modelle): {len(seeds)}", "",
         "## Vorab festgelegte Vorhersagen für Haiku 5.5 (BH über alle fünf)", ""]
    L += table(evaluate(arms, HAIKU, SONNET, descriptive=desc, f1_exclude=ex), "Haiku", "Sonnet")
    L += ["", f"## Sekundär: ohne die {len(ex)} einzeln nicht entscheidbaren Belege", ""]
    L += table(evaluate(arms, HAIKU, SONNET, keep=lambda i: i not in ex, descriptive=desc, f1_exclude=ex), "Haiku", "Sonnet")
    L += ["", f"## Sekundär: ohne Grenzfall {GRENZFAELLE}", ""]
    L += table(evaluate(arms, HAIKU, SONNET, keep=lambda i: i not in GRENZFAELLE, descriptive=desc, f1_exclude=ex), "Haiku", "Sonnet")
    L += ["", "## Deskriptiv: F1 auf ALLEN Ok-Belegen (wie in E-023, vermischt Fehlalarm und Weigerung bei unbelegbarem Erfolg)", ""]
    L += table(evaluate(arms, HAIKU, SONNET, descriptive=True), "Haiku", "Sonnet")
    L += ["", "## Manipulationscheck und Profil je Modell (alle Zeilen, vor dem Filtern)", "",
          "| Modell | Prüfungen | Ausfälle | Tokens (Median) | nachgeschlagen bei SPEC=1 | run_check bei ZUGANG=1 |", "|---|---|---|---|---|---|"]
    raw: dict[str, list[dict]] = defaultdict(list)
    for j in base.latest([dict(j, cell=f"{j['model']}|{j['cell']}") for j in js]):
        raw[j["model"]].append(j)
    for m in MODELS:
        p = profile(raw[m])
        L.append(f"| {m} | {p['n']} | {p['ausfaelle']} | {p['tokens']} | {p['nachgeschlagen_sp1']:.2f} | {p['run_check_zu1']:.2f} |")
    L += ["", "## Diagnose (deskriptiv, ohne BH): ZUGANG 1 − 0 auf Übersehen bei SPEC = 0, spec-rein", ""]
    for m in MODELS:
        d = per_item(arms[m], lambda j: j["SP"] == 0 and not j["truth"] and j["primary"], "ZU", miss)
        mm, lo, hi = base.boot(list(d.values()), 246)
        L.append(f"- {m}: {mm:+.3f} [{lo:+.3f}; {hi:+.3f}] (n = {len(d)})")
    for m in MODELS:
        _, text = base.analyze_data([j for j in js if j["model"] == m and j["seed"] in seeds])
        L += ["", f"## Alle E-020-Kontraste für {m} (deskriptiv, zum Vergleich mit E-020/E-023)", "",
              text.split("## Vorab festgelegte Kontraste")[1].split("## Zellen")[0].strip()]
    return "\n".join(L)


# --- Synthetische Daten (Tests, Power) -------------------------------------------------------------------------------

def synthetic(evs, model: str, v1: float, crowd: float, fa_up: float, seed: int, base_miss: float = 0.06,
              base_fa: float = 0.03, base_look: float = 0.95) -> list[dict]:
    """Haiku-artiges Verhalten: Ohne Nachschlagen wird bei SPEC = 1 ein spec-reiner Fehler übersehen.
    v1 = Zusatz-Übersehen bei SPEC = 1, crowd = Rückgang des Nachschlagens mit Kanal-Werkzeugen, fa_up = Fehlalarm-Zuwachs unter AU."""
    rng = random.Random(seed)
    js = []
    for ev in evs:
        for c in base.CELLS:
            cc = base.parse_cell(c)
            look = rng.random() < (base_look - (crowd if cc["ZU"] and cc["SP"] else 0.0))
            if ev.works:
                err = rng.random() < base_fa + (fa_up if cc["AU"] else 0.0)
            else:
                p = base_miss + (v1 if cc["SP"] and ev.primary else 0.0)
                if cc["SP"] and ev.primary and not look:
                    p = 0.9
                err = rng.random() < p
            js.append({"model": model, "id": ev.id, "seed": int(ev.id[-4:]), "cell": c, **cc, "truth": ev.works,
                       "primary": ev.primary, "fault": ev.fault, "verdict": (not ev.works) if err else ev.works,
                       "looked_up": look, "n_checks": 3 if cc["ZU"] else 0, "confidence": 0.9, "completion_tokens": 600,
                       "page_returned": look, "right_section": look, "cost_usd": 0.0})
    return js


def power(n_sims: int = 30, seeds: range = SEEDS) -> dict[str, float]:
    """Halbierte E-023-Effekte (V1 +0,12, Verdrängung 0,22, Fehlalarm +0,02) gegen Sonnet ohne Effekte."""
    evs = generate_set(seeds)
    old = base.B
    base.B = 1000
    hits: dict[str, int] = defaultdict(int)
    try:
        for k in range(n_sims):
            js = synthetic(evs, HAIKU, 0.12, 0.22, 0.02, seed=900 + k) + synthetic(evs, SONNET, 0.0, 0.0, 0.0, seed=950 + k)
            arms, _ = prepare(js)
            for key, v in evaluate(arms, HAIKU, SONNET, f1_exclude=exclusion()).items():
                hits[key] += v["label"].startswith("BESTÄTIGT")
    finally:
        base.B = old
    return {k: v / n_sims for k, v in hits.items()}


def load(path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["pilot", "run", "verblindet", "analyze", "power"])
    p.add_argument("--workers", type=int, default=6)
    a = p.parse_args()
    if a.cmd == "pilot":
        run(PILOT_SEEDS, "-pilot", a.workers)
    elif a.cmd == "run":
        run(SEEDS, "", a.workers)
    elif a.cmd == "verblindet":
        text = analyze_blind(load(DATA / "verblindet" / "judgments.jsonl"))
        (EXPDIR / "auswertung-verblindet.md").write_text(text, encoding="utf-8")
        print(text)
    elif a.cmd == "analyze":
        text = analyze(load(DATA / "judgments.jsonl"))
        (EXPDIR / "auswertung.md").write_text(text, encoding="utf-8")
        print(text)
    else:
        print(power())


if __name__ == "__main__":
    main()
