"""E-023: E-020 v3 mit Haiku 5.5 statt Sonnet 5.5 (Modell × Harness, H-038). Präregistrierung: experimente/E-023-haiku-dosen/prereg.md

Alles wie E-020 v3: Material v4.3, Seeds 6000–6023, 8 Zellen, Prompts, Werkzeuge, Auswertung `e020v3.analyze_data`.
Einzige Änderung ist das Prüfer-Modell. Dazu kommt die Wechselwirkung Modell × Faktor gegen die Sonnet-Daten aus E-020,
gepaart je Beleg (gleiche Belege, gleiche Zellen).

  python -m orglab.e023 pilot       # nur Technik, Seeds 1400–1401 (wie E-020 Pilot 3)
  python -m orglab.e023 run         # Hauptlauf, Seeds 6000–6023 (erst nach Freigabe)
  python -m orglab.e023 analyze

Hinweis: `e020v3.judge` schreibt "E-020-realitaet-in-dosen v3 <Zelle>" als Zweck ins OpenRouter-Ledger. Die Haiku-Aufrufe
sind dort am Feld `model` erkennbar.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from . import e020v3 as base
from . import openrouter
from .evidence_v4 import EvidenceV4, as_dict, generate_set
from .runner import ROOT

EXPERIMENT = "E-023-haiku-dosen"
DATA = ROOT / "daten" / EXPERIMENT
HAIKU = "anthropic/claude-haiku-5.5"
COST_STOP = 15.0
PILOT_SEEDS = range(1400, 1402)
# Materialbefund E-020 (ergebnis.md): einzeln vorgelegt nicht entscheidbar. Vorab festgelegt: mit und ohne berichten.
UNENTSCHEIDBAR = {("db_down", "deploy"), ("low_traffic", "sockets")}
FAKTOREN = {"V1 SPEC (spec-rein)": ("SP", True), "V2 AUSKUNFT": ("AU", False), "ZUGANG": ("ZU", False)}


def undecidable_ids(evs: list[EvidenceV4]) -> list[str]:
    return [ev.id for ev in evs if (ev.fault, base.presented_channel(ev)) in UNENTSCHEIDBAR]


def run(seeds: range, tag: str, workers: int, model: str = HAIKU) -> None:
    """Wie `e020v3.run`, mit eigenem Datenordner und Modell (E-020 bleibt eingefroren)."""
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
                done.add((j["id"], j["cell"]))
    order = sorted(evs, key=lambda e: (int(e.id.rsplit("-", 1)[1]), e.id))
    jobs = [(e, c) for e in order for c in base.CELLS if (e.id, c) not in done]
    print(f"[E-023] {len(evs) * len(base.CELLS)} Prüfungen, offen {len(jobs)}, Modell {model} | heute "
          f"{openrouter.spent_today():.2f} $", flush=True)
    n = 0
    with ThreadPoolExecutor(max_workers=workers) as pool, open(jpath, "a", encoding="utf-8") as fj, \
            open(tpath, "a", encoding="utf-8") as ft:
        futs = [pool.submit(base.judge, e, c, model) for e, c in jobs]
        for f in as_completed(futs):
            try:
                row, tr = f.result()
            except openrouter.BudgetExceeded as e:
                print(f"[E-023] STOPP: {e}", flush=True)
                pool.shutdown(cancel_futures=True)
                break
            fj.write(json.dumps(row, ensure_ascii=False) + "\n")
            ft.write(json.dumps(tr, ensure_ascii=False) + "\n")
            fj.flush(); ft.flush()
            spent += float(row.get("cost_usd") or 0)
            n += 1
            if spent > COST_STOP:
                print(f"[E-023] STOPP: Kosten {spent:.2f} $ > {COST_STOP} $", flush=True)
                pool.shutdown(cancel_futures=True)
                break
            if n % 200 == 0:
                print(f"[E-023] {n}/{len(jobs)} | Experiment {spent:.2f} $", flush=True)
    print(f"[E-023] fertig, {n} neue Prüfungen, Experiment {spent:.2f} $", flush=True)


def contrast_by_item(js: list[dict], factor: str, primary_only: bool) -> dict[str, float]:
    """Je kaputtem Beleg: Übersehen in Stufe 1 minus Stufe 0 des Faktors, gemittelt über die übrigen Faktoren."""
    by: dict[str, dict[int, list[int]]] = defaultdict(lambda: {0: [], 1: []})
    for j in js:
        if not j["truth"] and j.get("verdict") is not None and (j["primary"] or not primary_only):
            by[j["id"]][j[factor]].append(int(j["verdict"] is True))
    return {i: sum(v[1]) / len(v[1]) - sum(v[0]) / len(v[0]) for i, v in by.items() if v[0] and v[1]}


def clean(js: list[dict]) -> list[dict]:
    """Wie analyze_data: letzter Datensatz je Paar, nur vollständige Seeds, nur gültige Urteile."""
    js = base.latest(js)
    seeds = base.complete_seeds(js, 12)
    return [j for j in js if j["seed"] in seeds and j.get("verdict") is not None]


def interaction(haiku: list[dict], sonnet: list[dict], exclude: list[str] | None = None) -> dict[str, tuple]:
    """Wechselwirkung Modell × Faktor: je Beleg (Haiku-Kontrast − Sonnet-Kontrast), Bootstrap über gemeinsame Belege."""
    ex = set(exclude or [])
    h, s = clean(haiku), clean(sonnet)
    out = {}
    for k, (factor, prim) in FAKTOREN.items():
        ch, cs = contrast_by_item(h, factor, prim), contrast_by_item(s, factor, prim)
        common = sorted((set(ch) & set(cs)) - ex)
        diffs = [ch[i] - cs[i] for i in common]
        m, lo, hi = base.boot(diffs, 231)
        mh, _, _ = base.boot([ch[i] for i in common], 232)
        ms, _, _ = base.boot([cs[i] for i in common], 233)
        out[k] = (mh, ms, m, lo, hi, len(common))
    return out


def model_profile(js: list[dict]) -> dict[str, float]:
    """Manipulationscheck und Beschreibung je Modell: Tokens, Nachschlagen bei SPEC=1, Abfragen bei ZUGANG=1, Ausfälle."""
    js = base.latest(js)
    ok = [j for j in js if j.get("verdict") is not None]
    sp1 = [j for j in ok if j["SP"] == 1]
    zu1 = [j for j in ok if j["ZU"] == 1]
    toks = sorted(j["completion_tokens"] for j in ok)
    return {"n": len(js), "ausfaelle": len(js) - len(ok), "tokens_median": toks[len(toks) // 2] if toks else 0,
            "nachgeschlagen_sp1": sum(j["looked_up"] for j in sp1) / len(sp1) if sp1 else float("nan"),
            "run_check_zu1": sum(j["n_checks"] for j in zu1) / len(zu1) if zu1 else float("nan"),
            "fehlalarm": sum(j["verdict"] is False for j in ok if j["truth"]) / max(1, sum(j["truth"] for j in ok)),
            "uebersehen": sum(j["verdict"] is True for j in ok if not j["truth"]) / max(1, sum(not j["truth"] for j in ok))}


def analyze_both(haiku: list[dict], sonnet: list[dict]) -> str:
    evs = generate_set(base.MAIN_SEEDS)
    und = undecidable_ids(evs)
    _, text = base.analyze_data(haiku)
    text = text.replace("# E-020 v3 Auswertung", "# E-023 Auswertung (Haiku 5.5, Design E-020 v3)", 1)
    L = [text, "", "## Vorab festgelegt: ohne die einzeln nicht entscheidbaren Belege (E-020 Materialbefund)", "",
         f"Ausgeschlossen ({len(und)}): {', '.join(und)}", ""]
    r2, _ = base.analyze_data(haiku, exclude=und)
    L += [f"- V1 {r2['v1']:+.3f} [{r2['v1_lo']:+.3f}; {r2['v1_hi']:+.3f}] → {r2['v1_label']}",
          f"- V2 {r2['v2']:+.3f} [{r2['v2_lo']:+.3f}; {r2['v2_hi']:+.3f}] → {r2['v2_label']}", ""]
    L += ["## Profil je Modell (Manipulationscheck, deskriptiv)", "",
          "| Modell | Prüfungen | Ausfälle | Tokens (Median) | nachgeschlagen bei SPEC=1 | run_check bei ZUGANG=1 | Fehlalarm | Übersehen |",
          "|---|---|---|---|---|---|---|---|"]
    for name, js in (("Haiku 5.5", haiku), ("Sonnet 5.5 (E-020)", sonnet)):
        p = model_profile(js)
        L.append(f"| {name} | {p['n']} | {p['ausfaelle']} | {p['tokens_median']} | {p['nachgeschlagen_sp1']:.2f} | "
                 f"{p['run_check_zu1']:.2f} | {p['fehlalarm']:.3f} | {p['uebersehen']:.3f} |")
    for title, ex in (("alle Belege", None), ("ohne die einzeln nicht entscheidbaren Belege", und)):
        L += ["", f"## Wechselwirkung Modell × Faktor ({title}): Haiku-Effekt − Sonnet-Effekt, gepaart je Beleg", "",
              "| Kontrast | Effekt Haiku | Effekt Sonnet | Differenz [95-%-KI] | Belege |", "|---|---|---|---|---|"]
        for k, (mh, ms, m, lo, hi, n) in interaction(haiku, sonnet, ex).items():
            L.append(f"| {k} | {mh:+.3f} | {ms:+.3f} | **{m:+.3f}** [{lo:+.3f}; {hi:+.3f}] | {n} |")
    return "\n".join(L)


def load(path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def analyze(tag: str = "") -> str:
    text = analyze_both(load(DATA / f"judgments{tag}.jsonl"), load(base.DATA / "judgments.jsonl"))
    (DATA / f"auswertung{tag}.md").write_text(text, encoding="utf-8")
    return text


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["pilot", "run", "analyze"])
    p.add_argument("--workers", type=int, default=6)
    p.add_argument("--tag", default="")
    a = p.parse_args()
    if a.cmd == "pilot":
        run(PILOT_SEEDS, "-pilot", a.workers)
    elif a.cmd == "run":
        run(base.MAIN_SEEDS, "", a.workers)
    else:
        print(analyze(a.tag))


if __name__ == "__main__":
    main()
