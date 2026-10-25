"""E-019: Stapel-Panel – ein Prüfer beurteilt B Belege in einem Aufruf (Aufmerksamkeitsknappheit).
Präregistrierung: experimente/E-019-stapel-panel/prereg.md. Faktoren, Personas, Verfahren, Episoden aus orglab.factorial.

  python -m orglab.batch dryrun --step L2
  python -m orglab.batch calibrate --step L1            # Leiter L1 → L2 → L3, erste erfüllte Stufe wird eingefroren
  python -m orglab.batch calibrate-report --step L1
  python -m orglab.batch run --step L2                  # Hauptlauf (erst nach Neos Freigabe)

Rohdaten: daten/E-019-stapel-panel/ – calls*.jsonl (eine Zeile pro Aufruf, Rohantwort) und judgments*.jsonl (eine Zeile pro Beleg).
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import re
import statistics as st
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from . import openrouter
from .evidence import CHANNEL_DESC, EvidenceV2, as_dict, generate_set_v2
from .factorial import CELLS, FAMILY_PANEL, PERSONAS, PROCEDURES, SONNET, channel_for, episodes_for_key
from .runner import ROOT

EXPERIMENT = "E-019-stapel-panel"
DATA = ROOT / "daten" / EXPERIMENT
MAIN_SEEDS = range(2000, 2024)
CALIBRATION_SEEDS = range(1200, 1212)   # Material v3 (D-016); v2-Kalibrierung lief auf 1100–1111
MATERIAL = "v3"
LADDER = {"L1": (8, "low"), "L2": (12, "low"), "L3": (12, None)}   # (Stapelgröße, Reasoning-Effort)

ARRAY_SPEC = '[{"item": 1, "works": true or false, "confidence": number between 0 and 1}, ...] with exactly one entry per item'


def make_batches(evs: list[EvidenceV2], size: int, tag: str) -> list[tuple[str, list[EvidenceV2]]]:
    """Einmal per Seed mischen, dann in Stapel teilen. Zusammensetzung und Reihenfolge gelten für alle Zellen (gepaart)."""
    order = list(evs)
    random.Random(f"E-019-stapel:{tag}").shuffle(order)
    n = len(order) - len(order) % size
    return [(f"{tag}-b{i // size:02d}", order[i:i + size]) for i in range(0, n, size)]


def build_batch_prompt(batch_id: str, batch: list[EvidenceV2], cell: str, position: int, blind: bool = False) -> tuple[str, list[str]]:
    """Liefert (Prompt, Kanal je Beleg). Formulierung als echte Arbeitssituation (CLAUDE.md §8)."""
    info, style, experience = cell.split("-")[:3]
    parts = []
    if style == "S1":
        parts.append(PERSONAS[position])
    parts.append(f"You have {len(batch)} completed work items to review in this session. For each one, judge whether it "
                 "actually achieved its intended effect. Base each judgment only on the system output shown for that item.")
    if style == "S2":
        parts.append(PROCEDURES[position] + " Apply this method to every item.")
    eps = episodes_for_key(batch_id, experience, position)
    if eps:
        lines = ["For reference, here are earlier work items you reviewed, with what was found out later:"]
        for n, (e, ch) in enumerate(eps, 1):
            lines.append(f"\n--- Earlier item {n}\nWork item: {e.item}\n\nSystem output ({CHANNEL_DESC[ch]}):\n```\n"
                         f"{e.channels[ch]}\n```\nFound out later: {e.finding}")
        parts.append("\n".join(lines))
    channels, items = [], []
    for n, ev in enumerate(batch, 1):
        ch = channel_for(ev, info, position)
        text = ev.channels[ch]
        if blind and ev.signatures.get(ch):
            text = "\n".join(l for l in text.splitlines() if ev.signatures[ch] not in l)
        channels.append(ch)
        items.append(f"### Item {n}\nWork item: {ev.item}\n\nSystem output ({CHANNEL_DESC[ch]}):\n```\n{text}\n```")
    parts.append(("Now the items to review.\n\n" if eps else "") + "\n\n".join(items))
    if style == "S2":
        parts.append(f"Apply the review method briefly to each item, then end your answer with a JSON array only: {ARRAY_SPEC}")
    else:
        parts.append(f"Respond with a JSON array only: {ARRAY_SPEC}")
    return "\n\n".join(parts), channels


def parse_array(text: str) -> dict[int, tuple[bool, float | None]]:
    """Letztes JSON-Array der Antwort; Einträge ohne gültiges item/works fehlen."""
    text = text or ""
    end = text.rfind("]")
    for start in [m.start() for m in re.finditer(r"\[", text[:end + 1])][::-1]:
        try:
            arr = json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            continue
        if isinstance(arr, list) and arr and all(isinstance(x, dict) for x in arr):
            out = {}
            for x in arr:
                if isinstance(x.get("item"), int) and isinstance(x.get("works"), bool):
                    c = x.get("confidence")
                    out[x["item"]] = (x["works"], float(c) if isinstance(c, (int, float)) else None)
            return out
    return {}


def judge_batch(model: str, batch_id: str, batch: list[EvidenceV2], cell: str, position: int, effort: str | None,
                blind: bool = False) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    prompt, channels = build_batch_prompt(batch_id, batch, cell, position, blind)
    call: dict[str, Any] = {"batch": batch_id, "cell": cell, "position": position, "model": model, "effort": effort,
                            "size": len(batch)}
    msgs = [{"role": "user", "content": prompt}]
    parsed: dict[int, tuple[bool, float | None]] = {}
    for attempt in range(3):     # technisch fehlgeschlagene oder unparsbare Aufrufe bis zu zweimal wiederholen
        try:
            extra = {"reasoning": {"effort": effort}} if effort else {}
            resp = openrouter.chat(model, msgs, max_tokens=4000, purpose=f"{EXPERIMENT} {cell}", estimate_usd=0.15, **extra)
            text = resp["choices"][0]["message"].get("content") or ""
            parsed = parse_array(text)
            usage = resp.get("usage") or {}
            call.update(raw=text[-6000:], cost_usd=usage.get("cost"), attempt=attempt, parsed=len(parsed),
                        prompt_tokens=usage.get("prompt_tokens"), completion_tokens=usage.get("completion_tokens"))
            if len(parsed) >= len(batch) * 0.95:
                break
        except openrouter.BudgetExceeded:
            raise
        except Exception as e:
            call.update(error=f"{type(e).__name__}: {str(e)[:200]}", attempt=attempt, parsed=0)
    rows = []
    for n, (ev, ch) in enumerate(zip(batch, channels), 1):
        works, conf = parsed.get(n, (None, None))
        rows.append({"id": ev.id, "batch": batch_id, "slot": n, "cell": cell, "position": position, "model": model,
                     "effort": effort, "channel": ch, "kind": ev.kind, "domain": ev.domain, "fault": ev.fault,
                     "subtlety": ev.subtlety, "truth": ev.works, "verdict": works, "confidence": conf})
    return call, rows


def _execute(tag: str, jobs: list[tuple], effort: str | None, workers: int) -> None:
    """jobs: (model, batch_id, batch, cell, position, blind). Append-only, Erledigtes (≥ 95 % geparst) wird übersprungen."""
    calls_p, judg_p = DATA / f"calls{tag}.jsonl", DATA / f"judgments{tag}.jsonl"
    done = set()
    if calls_p.exists():
        for line in calls_p.read_text(encoding="utf-8").splitlines():
            c = json.loads(line)
            if c.get("parsed", 0) >= c["size"] * 0.95:
                done.add((c["model"], c["batch"], c["cell"], c["position"]))
    todo = [j for j in jobs if (j[0], j[1], j[3], j[4]) not in done]
    print(f"[E-019] {len(jobs)} Aufrufe geplant, offen {len(todo)} | heute {openrouter.spent_today():.2f} $ "
          f"von {openrouter.daily_budget():.2f} $", flush=True)
    n = 0
    with ThreadPoolExecutor(max_workers=workers) as pool, open(calls_p, "a", encoding="utf-8") as fc, \
            open(judg_p, "a", encoding="utf-8") as fj:
        futs = [pool.submit(judge_batch, m, bid, b, c, p, effort, blind) for m, bid, b, c, p, blind in todo]
        for f in as_completed(futs):
            try:
                call, rows = f.result()
            except openrouter.BudgetExceeded as e:
                print(f"[E-019] STOPP: {e}", flush=True)
                pool.shutdown(cancel_futures=True)
                break
            fc.write(json.dumps(call, ensure_ascii=False) + "\n")
            fj.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
            fc.flush(); fj.flush()
            n += 1
            if n % 20 == 0:
                print(f"[E-019] {n}/{len(todo)} Aufrufe | heute {openrouter.spent_today():.2f} $", flush=True)
    print(f"[E-019] fertig, {n} neue Aufrufe, heute {openrouter.spent_today():.2f} $", flush=True)


def _tag(step: str, model: str, calibration: bool) -> str:
    return (f"-kalibrierung-{step}-{MATERIAL}" if calibration else "") + ("" if model == SONNET else "-" + model.split("/")[1])


# --- Stufe 0: Kalibrierungsleiter ------------------------------------------------------

def calibrate(step: str, model: str, workers: int) -> None:
    size, effort = LADDER[step]
    DATA.mkdir(parents=True, exist_ok=True)
    evs = generate_set_v2(CALIBRATION_SEEDS)
    tag = _tag(step, model, True)
    (DATA / f"belege{tag}.jsonl").write_text("\n".join(json.dumps(as_dict(e), ensure_ascii=False) for e in evs), encoding="utf-8")
    batches = make_batches(evs, size, "kal")
    _execute(tag, [(model, bid, b, "I1-S0-E0", p, False) for bid, b in batches for p in range(3)], effort, workers)


def _load(tag: str) -> tuple[list[dict], list[dict]]:
    calls = [json.loads(l) for l in (DATA / f"calls{tag}.jsonl").read_text(encoding="utf-8").splitlines()]
    js = [json.loads(l) for l in (DATA / f"judgments{tag}.jsonl").read_text(encoding="utf-8").splitlines()]
    # bei Wiederholungen eines Aufrufs zählt der letzte Datensatz
    last: dict[tuple, dict] = {}
    for j in js:
        last[(j["model"], j["id"], j["cell"], j["position"])] = j
    return calls, list(last.values())


def calibrate_report(step: str, model: str) -> str:
    tag = _tag(step, model, True)
    calls, js = _load(tag)
    valid = [j for j in js if j["verdict"] is not None]
    err = lambda xs: st.fmean(int(j["verdict"] != j["truth"]) for j in xs) if xs else float("nan")
    size, effort = LADDER[step]
    rate = err(valid)
    pos_rates = [err([j for j in valid if j["position"] == p]) for p in range(3)]
    oks, fails = [j for j in valid if j["truth"]], [j for j in valid if not j["truth"]]
    fault_miss = {f: err([j for j in fails if j["fault"] == f]) for f in sorted({j["fault"] for j in fails})}
    wrong = [j for j in valid if j["verdict"] != j["truth"]]
    per_item = collections.Counter(j["id"] for j in wrong)
    top_share = max(per_item.values()) / len(wrong) if wrong else 0.0
    parse_fail = 1 - len(valid) / len(js) if js else 1.0
    half = size / 2
    front, back = err([j for j in valid if j["slot"] <= half]), err([j for j in valid if j["slot"] > half])
    crit = {
        "1 Fehlerrate 0,10–0,40": 0.10 <= rate <= 0.40,
        "2 Kanalbalance ≤ 0,20": max(pos_rates) - min(pos_rates) <= 0.20,
        "3 Fehlalarm und Übersehen ≥ 0,03": err(oks) >= 0.03 and err(fails) >= 0.03,
        "4 ≥ Hälfte der Fehlerarten ≥ 0,05 und kein Beleg > 5 % der Fehler (D-016)":
            sum(v >= 0.05 for v in fault_miss.values()) >= len(fault_miss) / 2 and top_share <= 0.05,
        "6 Parse-Ausfall ≤ 5 %": parse_fail <= 0.05,
    }
    lines = [f"# E-019 Kalibrierung {step}, Material {MATERIAL} (B={size}, Reasoning={effort or 'aus'}, {model})", "",
             f"Aufrufe: {len(calls)}, Urteile: {len(js)}, gültig: {len(valid)} (Parse-Ausfall {parse_fail:.3f})", "",
             f"**Einzelfehlerrate: {rate:.3f}** · Fehlalarm {err(oks):.3f} · Übersehen {err(fails):.3f}", "",
             f"Kanalpositionen: {', '.join(f'{r:.3f}' for r in pos_rates)}",
             f"Position im Stapel (V8-Vorschau): vordere Hälfte {front:.3f}, hintere Hälfte {back:.3f}", "",
             "Übersehensrate je Fehlerart: " + ", ".join(f"{k} {v:.3f}" for k, v in fault_miss.items()),
             f"Größter Anteil eines einzelnen Belegs an allen Fehlern: {top_share:.3f}", "", "## Kriterien", ""]
    lines += [f"- {'✔' if ok else '✘'} {name}" for name, ok in crit.items()]
    lines += ["- (5 Stichprobe: von Hand, siehe unten)", "",
              f"**Alle automatischen Kriterien erfüllt: {'JA' if all(crit.values()) else 'NEIN'}**", "",
              "## Fehlerrate je Art und Subtilität", ""]
    for k in sorted({j["kind"] for j in valid}):
        lines.append(f"- {k}: {err([j for j in valid if j['kind'] == k]):.3f}")
    lines += ["", f"Kosten: {sum(float(c.get('cost_usd') or 0) for c in calls):.2f} $", "",
              "## Falsch beurteilte Belege (für die Stichprobe)", ""]
    for j in wrong[:40]:
        lines.append(f"- {j['id']} · {j['channel']} · Slot {j['slot']} · Wahrheit {'ok' if j['truth'] else 'kaputt'} · Konf. {j['confidence']}")
    text = "\n".join(lines)
    (DATA / f"kalibrierung-{step}-{MATERIAL}{_tag(step, model, False)}-bericht.md").write_text(text, encoding="utf-8")
    return text


# --- Hauptlauf -------------------------------------------------------------------------

def main_jobs(step: str, model: str, family: bool) -> list[tuple]:
    size, _ = LADDER[step]
    batches = make_batches(generate_set_v2(MAIN_SEEDS), size, "main")
    if family:
        return [(FAMILY_PANEL[p], bid, b, f"{i}-S0-E0-FAM", p, False) for bid, b in batches for i in ("I0", "I1") for p in range(3)]
    jobs = [(model, bid, b, c, p, False) for bid, b in batches for c in CELLS for p in range(3)]
    if model == SONNET:
        jobs += [(model, bid, b, "I0-S0-E0-AA", p, False) for bid, b in batches for p in range(3)]
        jobs += [(model, bid, b, "I0-S0-E0-BLIND", p, p == 2) for bid, b in batches for p in range(3)]
    return jobs


def run(step: str, model: str, family: bool, workers: int) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "belege.jsonl").write_text(
        "\n".join(json.dumps(as_dict(e), ensure_ascii=False) for e in generate_set_v2(MAIN_SEEDS)), encoding="utf-8")
    _execute(_tag(step, model, False), main_jobs(step, model, family), LADDER[step][1], workers)


def dryrun(step: str) -> str:
    size, _ = LADDER[step]
    bid, batch = make_batches(generate_set_v2(MAIN_SEEDS), size, "main")[0]
    out = []
    for c in CELLS + ["I0-S0-E0-BLIND"]:
        for p in range(3):
            prompt, chans = build_batch_prompt(bid, batch, c, p, blind=c.endswith("BLIND") and p == 2)
            out.append(f"\n\n######## {bid} · {c} · Position {p} · Kanäle {chans}\n\n{prompt}")
    DATA.mkdir(parents=True, exist_ok=True)
    path = DATA / f"dryrun-{step}.md"
    path.write_text("".join(out), encoding="utf-8")
    return str(path)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["dryrun", "calibrate", "calibrate-report", "run"])
    p.add_argument("--step", choices=list(LADDER), default="L1")
    p.add_argument("--model", default=SONNET)
    p.add_argument("--family", action="store_true")
    p.add_argument("--workers", type=int, default=6)
    a = p.parse_args()
    if a.cmd == "dryrun":
        print(dryrun(a.step))
    elif a.cmd == "calibrate":
        calibrate(a.step, a.model, a.workers)
        print(calibrate_report(a.step, a.model))
    elif a.cmd == "calibrate-report":
        print(calibrate_report(a.step, a.model))
    else:
        run(a.step, a.model, a.family, a.workers)


if __name__ == "__main__":
    main()
