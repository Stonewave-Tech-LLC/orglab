"""E-026: Bestätigung von E-025 (H-041, H-042), Stufe Bestätigung. Präregistrierung: experimente/E-026-bestaetigung-vertrauen/prereg.md

Gleiche Bedingungen wie E-025 (Material v4.3, Auszug, 8 Zellen, Prompts, Modelle, ein Aufruf je Prüfung), frische Seeds
9000–9015. Die Prompts baut weiter `e025.build_prompt`, damit sich nichts unbemerkt ändert.

Neu gegenüber E-025 (Lehren aus dem ersten Harness-Lauf):
  - Jede Zeile trägt `norm_im_prompt` und `dritte_antwort_im_prompt`, gelesen aus dem TATSÄCHLICH gesendeten Prompt.
    Der Manipulationscheck "N und T" ist damit aus den Daten nachrechenbar (Neo: ein Check, den Rechner B nicht
    nachrechnen kann, ist kein Check im gleichen Sinne).
  - Der Preis der dritten Antwort wird als Trefferquote gemessen (B4), nicht als Bestätigungsrate (E-025 K3 übersah ihn).
  - Die Auswertung rechnet je Zuordnung "Ziel = Sonnet" (wie E-024 mit "Ziel = Haiku"), weil B1 ein Modellkontrast ist.

  python -m orglab.e026 dryrun | material | pilot | run | power
  python -m orglab.e026 blind-json <datei>     # Rechner A im Harness
"""

from __future__ import annotations

import argparse
import json
import random
import re
import statistics as st
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from . import e025, openrouter
from .e025 import CELLS, NE, NORM, boot, bh, build_prompt, confirm, counted, p_greater, parse_cell, prepare
from .evidence_v4 import as_dict, generate_set
from .runner import ROOT

EXPERIMENT = "E-026-bestaetigung-vertrauen"
DATA = ROOT / "daten" / EXPERIMENT
EXPDIR = ROOT / "experimente" / EXPERIMENT
SONNET, HAIKU = e025.SONNET, e025.HAIKU
MODELS = (SONNET, HAIKU)
SEEDS = range(9000, 9016)
PILOT_SEEDS = range(1702, 1704)
COST_STOP = 60.0
MIN_ITEMS = 144
GAP_MAX = e025.GAP_MAX
PRIMARY = ("B1", "B2", "B3", "B4")
NEED = {"B1": 0.08, "B2": 0.05, "B3": 0.05, "B4": 0.08}
SEEDS_BOOT = {"B1": 441, "B2": 442, "B3": 443, "B4": 444, "K0Z": 445, "K0V": 446, "R1V": 447, "R2V": 448, "B4Z": 449}
SEEDS_P = {"B1": 451, "B2": 452, "B3": 453, "B4": 454}
TRI_MARK = '"not established"'


def prompt_flags(prompt: str) -> dict[str, bool]:
    """Was im gesendeten Prompt wirklich stand (nicht, was die Zelle verspricht)."""
    return {"norm_im_prompt": NORM in prompt, "dritte_antwort_im_prompt": TRI_MARK in prompt}


def judge(ev, cell: str, model: str) -> tuple[dict[str, Any], dict[str, Any]]:
    row, tr = e025.judge(ev, cell, model)
    row.update(prompt_flags(tr["messages"][0]["content"]))
    return row, tr


def run(seeds: range, tag: str, workers: int, out_dir: Path = DATA) -> None:
    """Wie e025.run: seedweise, beide Modelle je Seed, Kostenstopp, fortsetzbar, Ausfälle werden nicht wiederholt."""
    out_dir.mkdir(parents=True, exist_ok=True)
    evs = generate_set(seeds)
    (out_dir / f"belege{tag}.jsonl").write_text("\n".join(json.dumps(as_dict(e), ensure_ascii=False) for e in evs),
                                                encoding="utf-8")
    jpath, tpath = out_dir / f"judgments{tag}.jsonl", out_dir / f"transcripts{tag}.jsonl"
    done, spent = set(), 0.0
    if jpath.exists():
        for line in jpath.read_text(encoding="utf-8").splitlines():
            j = json.loads(line)
            spent += float(j.get("cost_usd") or 0)
            done.add((j["model"], j["id"], j["cell"]))
    order = sorted(evs, key=lambda e: (int(e.id.rsplit("-", 1)[1]), e.id))
    jobs = [(m, e, c) for e in order for m in MODELS for c in CELLS if (m, e.id, c) not in done]
    print(f"[{EXPERIMENT}] {len(evs) * len(CELLS) * len(MODELS)} Prüfungen, offen {len(jobs)}", flush=True)
    n = 0
    with ThreadPoolExecutor(max_workers=workers) as pool, open(jpath, "a", encoding="utf-8") as fj, \
            open(tpath, "a", encoding="utf-8") as ft:
        futs = [pool.submit(judge, e, c, m) for m, e, c in jobs]
        for f in as_completed(futs):
            try:
                row, tr = f.result()
            except openrouter.BudgetExceeded as e:
                print(f"[{EXPERIMENT}] STOPP: {e}", flush=True)
                pool.shutdown(cancel_futures=True)
                break
            fj.write(json.dumps(row, ensure_ascii=False) + "\n")
            ft.write(json.dumps(tr, ensure_ascii=False) + "\n")
            fj.flush(); ft.flush()
            spent += float(row.get("cost_usd") or 0)
            n += 1
            if spent > COST_STOP:
                print(f"[{EXPERIMENT}] STOPP: Kosten {spent:.2f} $ > {COST_STOP} $", flush=True)
                pool.shutdown(cancel_futures=True)
                break
            if n % 200 == 0:
                print(f"[{EXPERIMENT}] {n}/{len(jobs)} | {spent:.2f} $", flush=True)
    print(f"[{EXPERIMENT}] fertig, {n} neue Prüfungen, {spent:.2f} $", flush=True)


def material(out_dir: Path = DATA, workers: int = 6) -> None:
    """Fremdkontrolle wie E-025 (VOLL und AUSZUG), auf den E-026-Seeds."""
    out_dir.mkdir(parents=True, exist_ok=True)
    sample = e025.material_sample(generate_set(SEEDS))

    def one(job):
        ev, d = job
        row = {"id": ev.id, "D": d, "truth": ev.works, "fault": ev.fault, "model": e025.CHECKER, "effort": "high"}
        try:
            resp = openrouter.chat(e025.CHECKER, [{"role": "user", "content": e025.check_prompt(ev, d)}], max_tokens=16000,
                                   purpose=f"{EXPERIMENT} Fremdkontrolle", estimate_usd=0.1, reasoning={"effort": "high"})
            text = resp["choices"][0]["message"].get("content") or ""
            m = list(re.finditer(r"\{[^{}]*\}", text))
            dd = json.loads(m[-1].group(0)) if m else {}
            row.update(verdict=dd.get("works"), decidable=dd.get("decidable"), reason=dd.get("reason"),
                       cost_usd=(resp.get("usage") or {}).get("cost"))
        except openrouter.BudgetExceeded:
            raise
        except Exception as e:
            row.update(verdict=None, decidable=None, error=f"{type(e).__name__}: {str(e)[:200]}")
        return row

    with ThreadPoolExecutor(max_workers=workers) as pool:
        rows = list(pool.map(one, [(e, d) for e in sample for d in (0, 1)]))
    (out_dir / "material.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows), encoding="utf-8")
    print(json.dumps(e025.material_summary(rows), ensure_ascii=False))


# --- Auswertung (vor dem Pilot festgelegt, tests/test_e026.py) ------------------------------------------------

def correct(j: dict) -> bool:
    return j["verdict"] == j["truth"]


def per_arm(rows: list[dict]) -> dict[str, dict[str, float]]:
    """Je Beleg für EIN Arm: K0 (Bestätigung im AUSZUG N0T0), R1, R2 (wie E-025), KV (Preis der dritten Antwort bei
    voller Evidenz: Treffer D0-N0-T0 minus D0-N0-T1, positiv = kostet Treffer)."""
    c = e025.contrasts(rows)
    by: dict[str, dict[str, float]] = defaultdict(dict)
    for j in rows:
        if j["cell"] in ("D0-N0-T0", "D0-N0-T1"):
            by[j["id"]][j["cell"]] = float(correct(j))
    kv = {i: v["D0-N0-T0"] - v["D0-N0-T1"] for i, v in by.items() if len(v) == 2}
    return {"K0": c["K0"], "R1": c["R1"], "R2": c["R2"], "KV": kv}


def manipulation_check(js_all: list[dict], arms: dict[str, list[dict]]) -> dict[str, dict]:
    """Wie E-025 (Ausfälle, VOLL informativ, AUSZUG uninformativ) plus, jetzt aus den Daten: Norm und dritte Antwort
    standen genau in den Zellen im Prompt, deren Name es sagt."""
    base = e025.manipulation_check(js_all, arms)
    for arm in base:
        rows = [j for j in js_all if j["model"] == arm]
        flags_ok = bool(rows) and all(j.get("norm_im_prompt") is bool(j["N"]) and
                                      j.get("dritte_antwort_im_prompt") is bool(j["T"]) for j in rows)
        base[arm]["prompt_wie_zelle"] = flags_ok
        base[arm]["ok"] = base[arm]["ok"] and flags_ok
    return base


def label(lo: float, hi: float, q: float, need: float, descriptive: bool) -> str:
    """Wie E-024 (Stufe Bestätigung)."""
    if descriptive:
        return "nur deskriptiv"
    if lo > 0 and q <= 0.05:
        return ("BESTÄTIGT (Vorhersagewert nicht ausgeschlossen)" if hi >= need
                else "BESTÄTIGT, aber kleiner als vorhergesagt")
    if hi < 0.02:
        return "nicht bestätigt: praktisch null (widerlegt)"
    if hi < need:
        return "nicht bestätigt: Vorhersagewert ausgeschlossen (widerlegt)"
    return "nicht bestätigt: nicht entschieden"


def _r(vals: list[float], seed: int) -> dict:
    m, lo, hi = boot(vals, seed)
    nan = lambda x: None if isinstance(x, float) and x != x else x
    return {"estimate": nan(m), "ci95": [nan(lo), nan(hi)], "n": len(vals), "q": None, "label": "deskriptiv",
            "confirmed": False, "comparison": None}


def evaluate(js: list[dict]) -> dict:
    """Je Zuordnung "Ziel = t" (t wäre Sonnet), Vergleich = der andere Arm (wäre Haiku). BH über B1–B4 je Zuordnung.
      B1  K0(Ziel) − K0(Vergleich), gepaart je Beleg            (H-042)
      B2  R1(Ziel): Senkung durch die Evidenznorm                 (H-041)
      B3  R2(Ziel): Senkung durch die dritte Antwort              (H-041)
      B4  KV(Vergleich): Preis der dritten Antwort bei voller Evidenz beim Vergleichsmodell
    Deskriptiv: K0 beider Arme, R1/R2 des Vergleichs, KV des Ziels, "not established"-Anteile."""
    arms, items = prepare(js)
    mc = manipulation_check(js, arms)
    desc = len(items) < MIN_ITEMS or not all(m["ok"] for m in mc.values())
    c = {a: per_arm(rows) for a, rows in arms.items()}
    res: dict[str, dict] = {}
    for t in sorted(arms):
        o = next(a for a in sorted(arms) if a != t)
        common = sorted(set(c[t]["K0"]) & set(c[o]["K0"]))
        vals = {"B1": [c[t]["K0"][i] - c[o]["K0"][i] for i in common],
                "B2": [c[t]["R1"][i] for i in sorted(c[t]["R1"])], "B3": [c[t]["R2"][i] for i in sorted(c[t]["R2"])],
                "B4": [c[o]["KV"][i] for i in sorted(c[o]["KV"])]}
        r = {k: _r(v, SEEDS_BOOT[k]) for k, v in vals.items()}
        q = bh({k: p_greater(v, SEEDS_P[k]) for k, v in vals.items()})
        for k in PRIMARY:
            r[k]["q"] = q[k]
            lo, hi = r[k]["ci95"]
            r[k]["label"] = label(lo if lo is not None else float("nan"), hi if hi is not None else float("nan"),
                                  q[k], NEED[k], desc)
            r[k]["confirmed"] = r[k]["label"].startswith("BESTÄTIGT")
        r["K0Z"] = _r([c[t]["K0"][i] for i in sorted(c[t]["K0"])], SEEDS_BOOT["K0Z"])
        r["K0V"] = _r([c[o]["K0"][i] for i in sorted(c[o]["K0"])], SEEDS_BOOT["K0V"])
        r["R1V"] = _r([c[o]["R1"][i] for i in sorted(c[o]["R1"])], SEEDS_BOOT["R1V"])
        r["R2V"] = _r([c[o]["R2"][i] for i in sorted(c[o]["R2"])], SEEDS_BOOT["R2V"])
        r["B4Z"] = _r([c[t]["KV"][i] for i in sorted(c[t]["KV"])], SEEDS_BOOT["B4Z"])
        res[t] = r
    return {"n_complete_seeds": e025.complete_seeds(items), "n_complete_items": len(items), "manipulation_check": mc,
            "manipulation_check_passed": {a: m["ok"] for a, m in mc.items()}, "descriptive_only": desc,
            "assignments": res}


# --- Synthetische Daten, Power --------------------------------------------------------------------------------

def synthetic(evs, model: str, k0: float, voll_ne: float, seed: int, acc: float = 0.97) -> list[dict]:
    """Bestätigung im AUSZUG nur bei N0T0 (Rate k0), sonst "kaputt" bzw. "not established" (wie in E-025).
    Bei voller Evidenz: Treffer acc, bei T1 zusätzlich mit Rate voll_ne "not established"."""
    rng = random.Random(seed)
    js = []
    for ev in evs:
        for cell in CELLS:
            cc = parse_cell(cell)
            if cc["D"]:
                v = True if (not cc["N"] and not cc["T"] and rng.random() < k0) else (NE if cc["T"] else False)
            elif cc["T"] and rng.random() < voll_ne:
                v = NE
            else:
                v = ev.works if rng.random() < acc else (not ev.works)
            js.append({"model": model, "id": ev.id, "seed": int(ev.id[-4:]), "cell": cell, **cc, "truth": ev.works,
                       "verdict": v, "parse_ok": True, "finish_reason": "stop", "confidence": 0.8,
                       "norm_im_prompt": bool(cc["N"]), "dritte_antwort_im_prompt": bool(cc["T"])})
    return js


def power(n_sims: int = 30, factor: float = 0.5) -> dict[str, float]:
    """Effekte = factor × E-025 (Sonnet K0 0,23, Haiku K0 0,02, Haikus "not established" bei voller Evidenz 0,22)."""
    evs = generate_set(SEEDS)
    old = e025.B
    e025.B = 1000
    hits: dict[str, int] = defaultdict(int)
    try:
        for k in range(n_sims):
            js = (synthetic(evs, "S", 0.23 * factor, 0.06 * factor, 700 + k)
                  + synthetic(evs, "H", 0.02 * factor, 0.22 * factor, 750 + k))
            res = evaluate(js)["assignments"]["S"]
            for key in PRIMARY:
                hits[key] += res[key]["confirmed"]
    finally:
        e025.B = old
    return {k: hits[k] / n_sims for k in PRIMARY}


def load(path) -> list[dict]:
    return [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]


def dryrun() -> str:
    """Exakte Prompts (Regel 16). Dieselbe Funktion wie in E-025 (`e025.build_prompt`), Beispiele aus Seed 9000."""
    evs = generate_set(range(9000, 9001))
    picks = [next(e for e in evs if e.domain == d and not e.works) for d in ("coding", "business", "research")]
    out = [f"# {EXPERIMENT}: Dry-Run, exakte Prompts (Regel 16)", "",
           "Gleiche Prompts wie E-025 (`orglab.e025.build_prompt`), nur andere Seeds. "
           f"Modelle {SONNET} und {HAIKU} über OpenRouter, ohne `reasoning`, `max_tokens` {e025.MAX_TOKENS}.", ""]
    for c in CELLS:
        out += [f"## {c} (Beispiel {picks[0].id}, Fehlerart {picks[0].fault})", "", "````", build_prompt(picks[0], c),
                "````", ""]
    for ev in picks[1:]:
        out += [f"## Auszug {ev.id} (Fehlerart {ev.fault}, Zelle D1-N0-T0)", "", "````", build_prompt(ev, "D1-N0-T0"),
                "````", ""]
    return "\n".join(out)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["dryrun", "material", "pilot", "run", "blind-json", "power"])
    p.add_argument("datei", nargs="?")
    p.add_argument("--workers", type=int, default=8)
    p.add_argument("--out")
    a = p.parse_args()
    out = Path(a.out) if a.out else DATA
    if a.cmd == "dryrun":
        EXPDIR.mkdir(parents=True, exist_ok=True)
        (EXPDIR / "dryrun.md").write_text(dryrun(), encoding="utf-8")
    elif a.cmd == "material":
        material(out)
    elif a.cmd == "pilot":
        run(PILOT_SEEDS, "-pilot", a.workers, out)
    elif a.cmd == "run":
        run(SEEDS, "", a.workers, out)
    elif a.cmd == "power":
        print(json.dumps(power(), ensure_ascii=False))
    else:
        print(json.dumps(evaluate(load(a.datei)), ensure_ascii=False))


if __name__ == "__main__":
    main()
