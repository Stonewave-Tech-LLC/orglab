"""E-017: Faktorielles Prüfer-Panel (Information × Stil/Verfahren × Erfahrung), siehe experimente/E-017-faktorielles-panel/prereg.md.

  python -m orglab.factorial dryrun                       # Prompts aller Zellen für 2 Belege, ohne API-Aufrufe
  python -m orglab.factorial calibrate --iteration 1      # Stufe 0: Sonnet, I0/S0/E0, jeder Kanal einzeln
  python -m orglab.factorial calibrate-report --iteration 1
  python -m orglab.factorial run --model anthropic/claude-sonnet-5.5

Rohdaten: daten/E-017-faktorielles-panel/ (append-only, fortsetzbar). Alle Aufrufe über OpenRouter mit Tagesbudget.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import re
import statistics as st
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from . import openrouter
from .evidence import CHANNEL_DESC, CHANNELS, EvidenceV2, as_dict, generate_set_v2
from .runner import ROOT

EXPERIMENT = "E-017-faktorielles-panel"
DATA = ROOT / "daten" / EXPERIMENT
SONNET = "anthropic/claude-sonnet-5.5"
FAMILY_PANEL = (SONNET, "openai/gpt-6.1-sol", "google/gemini-4-argon")

MAIN_SEEDS = range(2000, 2020)
CALIBRATION_SEEDS = range(1000, 1010)
EPISODE_SEEDS = range(500, 700)
EPISODES_PER_PROMPT = 6

INFO = ("I0", "I1")          # gleicher Kanal / verschiedene Kanäle
STYLE = ("S0", "S1", "S2")   # neutral / Etiketten-Persona / Verfahrens-Persona
EXPERIENCE = ("E0", "E1", "E2")  # keine / gleiche / disjunkte Rohepisoden
CELLS = [f"{i}-{s}-{e}" for i, s, e in itertools.product(INFO, STYLE, EXPERIENCE)]

# Etiketten-Personas: nur Name, Hintergrund, Temperament. Bewusst ohne Wörter wie careful/skeptical/thorough (prereg S1).
PERSONAS = (
    "You are Jonas Berger, an operations engineer from Graz with twelve years of experience. "
    "You are calm, friendly and like a good joke.",
    "You are Priya Raman, a team lead who moved from Bangalore to Vienna. "
    "You are energetic, direct and enjoy mentoring new colleagues.",
    "You are Tomás Ortega, a former musician who switched careers into IT. "
    "You are relaxed, quiet and love cooking.",
)
# Verfahrens-Personas (S2): verschiedene Prüfmethoden
PROCEDURES = (
    "Review method: first name three concrete ways this work item could have failed even though it may look fine. "
    "Then check the output for each of them.",
    "Review method: before you read the output, write down what you would expect to see in it if the intended "
    "effect was achieved. Then compare the output against your expectation.",
    "Review method: find every place where the output states the same fact more than once or where it can be "
    "compared with the work item (a version, an ID, an address, a count). Check that they all agree.",
)

JSON_SPEC = '{"works": true or false, "confidence": number between 0 and 1, "reason": "one short sentence"}'


def channel_for(ev: EvidenceV2, info: str, position: int) -> str:
    """I0: alle drei sehen denselben Kanal (rotiert über Belege). I1: Position k sieht Kanal (k + Seed) mod 3."""
    chans = CHANNELS[ev.domain]
    seed = int(ev.id.rsplit("-", 1)[1])
    return chans[seed % 3] if info == "I0" else chans[(position + seed) % 3]


# --- Erfahrung: Rohepisoden ------------------------------------------------------

_POOL: tuple[list[EvidenceV2], list[EvidenceV2]] | None = None


def _pool() -> tuple[list[EvidenceV2], list[EvidenceV2]]:
    global _POOL
    if _POOL is None:
        evs = generate_set_v2(EPISODE_SEEDS)
        _POOL = ([e for e in evs if e.works], [e for e in evs if not e.works])
    return _POOL


def episodes_for(ev: EvidenceV2, experience: str, position: int) -> list[tuple[EvidenceV2, str]]:
    """E1: ein Set pro Beleg, das alle drei teilen. E2: drei disjunkte Sets. Je 3 ok + 3 kaputt, Kanal zufällig."""
    return episodes_for_key(ev.id, experience, position)


def episodes_for_key(key: str, experience: str, position: int) -> list[tuple[EvidenceV2, str]]:
    """Wie episodes_for, aber für einen beliebigen Schlüssel (E-019: ein Set pro Stapel statt pro Beleg)."""
    if experience == "E0":
        return []
    oks, fails = _pool()
    half = EPISODES_PER_PROMPT // 2
    rng = random.Random(f"episodes:{key}")
    k = 1 if experience == "E1" else 3
    ok_draw, fail_draw = rng.sample(oks, half * k), rng.sample(fails, half * k)
    slot = 0 if experience == "E1" else position
    chosen = ok_draw[slot * half:(slot + 1) * half] + fail_draw[slot * half:(slot + 1) * half]
    rng2 = random.Random(f"episodes:{key}:{slot}")
    rng2.shuffle(chosen)
    return [(e, rng2.choice(CHANNELS[e.domain])) for e in chosen]


def _block(ev: EvidenceV2, channel: str) -> str:
    return f"Work item: {ev.item}\n\nSystem output ({CHANNEL_DESC[channel]}):\n```\n{ev.channels[channel]}\n```"


def build_prompt(ev: EvidenceV2, cell: str, position: int, blind: bool = False) -> tuple[str, str]:
    """Liefert (Prompt, Kanal). Bewusst als echte Arbeitssituation formuliert, ohne "Test"/"Benchmark" (CLAUDE.md §8)."""
    info, style, experience = cell.split("-")[:3]
    channel = channel_for(ev, info, position)
    parts = []
    if style == "S1":
        parts.append(PERSONAS[position])
    parts.append("You are reviewing whether a completed work item actually achieved its intended effect. "
                 "Base your judgment only on the system output shown for it.")
    eps = episodes_for(ev, experience, position)
    if eps:
        lines = ["For reference, here are earlier work items you reviewed, with what was found out later:"]
        for n, (e, ch) in enumerate(eps, 1):
            lines.append(f"\n--- Earlier item {n}\n{_block(e, ch)}\nFound out later: {e.finding}")
        parts.append("\n".join(lines))
    shown = ev
    if blind:
        # Positivkontrolle (prereg): Fehlerspur aus dem gezeigten Kanal entfernen
        text = "\n".join(l for l in ev.channels[channel].splitlines() if ev.signatures.get(channel, "\0") not in l)
        shown = EvidenceV2(**{**ev.__dict__, "channels": {**ev.channels, channel: text}})
    if style == "S2":
        parts.append(PROCEDURES[position])   # vor dem Beleg, damit "commit first" überhaupt möglich ist
    parts.append(("Now the current work item.\n\n" if eps else "") + _block(shown, channel))
    if style == "S2":
        parts.append(f"Apply the review method briefly, then end your answer with one line of JSON only: {JSON_SPEC}")
    else:
        parts.append(f"Respond with JSON only: {JSON_SPEC}")
    return "\n\n".join(parts), channel


def parse_last_json(text: str) -> tuple[bool | None, float | None]:
    """Nimmt das letzte JSON-Objekt der Antwort (der E-016-Parser bricht bei Text vor dem JSON)."""
    for m in reversed(list(re.finditer(r"\{[^{}]*\}", text or ""))):
        try:
            d = json.loads(m.group(0))
        except json.JSONDecodeError:
            continue
        works, conf = d.get("works"), d.get("confidence")
        if isinstance(works, bool):
            return works, float(conf) if isinstance(conf, (int, float)) else None
    return None, None


def judge(model: str, ev: EvidenceV2, cell: str, position: int, blind: bool = False) -> dict[str, Any]:
    prompt, channel = build_prompt(ev, cell, position, blind)
    out: dict[str, Any] = {"id": ev.id, "cell": cell, "position": position, "model": model, "channel": channel,
                           "kind": ev.kind, "domain": ev.domain, "fault": ev.fault, "subtlety": ev.subtlety,
                           "truth": ev.works}
    msgs = [{"role": "user", "content": prompt}]
    for attempt in range(3):     # technisch fehlgeschlagene Aufrufe bis zu zweimal wiederholen (prereg)
        try:
            try:
                resp = openrouter.chat(model, msgs, max_tokens=1500, purpose=f"{EXPERIMENT} {cell}", estimate_usd=0.02,
                                       reasoning={"effort": "low"})
            except RuntimeError as e:
                if "HTTP 400" not in str(e):
                    raise
                resp = openrouter.chat(model, msgs, max_tokens=1500, purpose=f"{EXPERIMENT} {cell} (no reasoning)",
                                       estimate_usd=0.02)
            text = resp["choices"][0]["message"].get("content") or ""
            works, conf = parse_last_json(text)
            usage = resp.get("usage") or {}
            out.update(verdict=works, confidence=conf, raw=text[-600:], cost_usd=usage.get("cost"), attempt=attempt,
                       prompt_tokens=usage.get("prompt_tokens"), completion_tokens=usage.get("completion_tokens"))
            if works is not None:
                return out
        except openrouter.BudgetExceeded:
            raise
        except Exception as e:
            out.update(verdict=None, error=f"{type(e).__name__}: {str(e)[:200]}", attempt=attempt)
    return out


def _execute(path: Path, jobs: list[tuple], workers: int) -> None:
    """jobs: (model, ev, cell, position, blind). Schreibt append-only, überspringt Erledigtes."""
    done = set()
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            j = json.loads(line)
            if j.get("verdict") is not None:
                done.add((j["model"], j["id"], j["cell"], j["position"]))
    todo = [j for j in jobs if (j[0], j[1].id, j[2], j[3]) not in done]
    print(f"[E-017] {len(jobs)} Urteile geplant, offen {len(todo)} | heute {openrouter.spent_today():.2f} $ "
          f"von {openrouter.daily_budget():.2f} $", flush=True)
    n = 0
    with ThreadPoolExecutor(max_workers=workers) as pool, open(path, "a", encoding="utf-8") as fh:
        futs = [pool.submit(judge, *j) for j in todo]
        for f in as_completed(futs):
            try:
                r = f.result()
            except openrouter.BudgetExceeded as e:
                print(f"[E-017] STOPP: {e}", flush=True)
                pool.shutdown(cancel_futures=True)
                break
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            fh.flush()
            n += 1
            if n % 100 == 0:
                print(f"[E-017] {n}/{len(todo)} | heute {openrouter.spent_today():.2f} $", flush=True)
    print(f"[E-017] fertig, {n} neue Urteile, heute {openrouter.spent_today():.2f} $", flush=True)


# --- Stufe 0: Kalibrierung -------------------------------------------------------------

def calibrate(iteration: int, model: str, workers: int) -> None:
    """Jeder Beleg, jeder Kanal einzeln, neutral, ohne Erfahrung (I0/S0/E0 mit Kanal = Position)."""
    DATA.mkdir(parents=True, exist_ok=True)
    evs = generate_set_v2(CALIBRATION_SEEDS)
    tag = "" if model == SONNET else "-" + model.split("/")[1]
    (DATA / f"kalibrierung-{iteration}{tag}-belege.jsonl").write_text(
        "\n".join(json.dumps(as_dict(e), ensure_ascii=False) for e in evs), encoding="utf-8")
    # Kalibrierung braucht jeden Kanal: "I1" mit Position 0–2 deckt alle drei Kanäle ab, S0/E0 hält den Rest neutral.
    jobs = [(model, e, "I1-S0-E0", p, False) for e in evs for p in range(3)]
    _execute(DATA / f"kalibrierung-{iteration}{tag}.jsonl", jobs, workers)


def calibrate_report(iteration: int, model: str) -> str:
    tag = "" if model == SONNET else "-" + model.split("/")[1]
    js = [j for j in map(json.loads, (DATA / f"kalibrierung-{iteration}{tag}.jsonl").read_text(encoding="utf-8").splitlines())]
    valid = [j for j in js if j.get("verdict") is not None]
    err = lambda xs: st.fmean(int(j["verdict"] != j["truth"]) for j in xs) if xs else float("nan")
    lines = [f"# E-017 Kalibrierung, Iteration {iteration} ({model})", "",
             f"Urteile: {len(js)}, gültig: {len(valid)}, unparsbar/Fehler: {len(js) - len(valid)}", "",
             f"**Einzelfehlerrate gesamt: {err(valid):.3f}** (Ziel 0,10–0,40)", "", "## Nach Kanal", "",
             "| Domäne | Kanal | n | Fehlerrate |", "|---|---|---|---|"]
    chan_rates = []
    for d, chans in CHANNELS.items():
        for c in chans:
            xs = [j for j in valid if j["channel"] == c]
            chan_rates.append(err(xs))
            lines.append(f"| {d} | {c} | {len(xs)} | {err(xs):.3f} |")
    pos_rates = [err([j for j in valid if j["position"] == p]) for p in range(3)]
    lines += ["", f"Kanalbalance (Position = Kanalindex, über Domänen): {', '.join(f'{r:.3f}' for r in pos_rates)} "
              f"→ Spanne {max(pos_rates) - min(pos_rates):.3f} (Ziel ≤ 0,20, also ±0,10)",
              f"Spanne über alle 9 Kanäle: {max(chan_rates) - min(chan_rates):.3f} (nur deskriptiv)", "",
              "## Nach Art und Subtilität", "", "| Art | subtlety | n | Fehlerrate |", "|---|---|---|---|"]
    for k in sorted({j["kind"] for j in valid}):
        for s in (1, 2, 3):
            xs = [j for j in valid if j["kind"] == k and j["subtlety"] == s]
            if xs:
                lines.append(f"| {k} | {s} | {len(xs)} | {err(xs):.3f} |")
    oks, fails = [j for j in valid if j["truth"]], [j for j in valid if not j["truth"]]
    lines += ["", f"Ok-Belege (Fehlalarm): {err(oks):.3f} · Fail-Belege (übersehen): {err(fails):.3f} (beide Ziel ≥ 0,03)",
              "", "## Nach Fehlerart", ""]
    for f in sorted({j["fault"] for j in valid}):
        lines.append(f"- {f}: {err([j for j in valid if j['fault'] == f]):.3f}")
    cost = sum(float(j.get("cost_usd") or 0) for j in js)
    lines += ["", f"Kosten: {cost:.2f} $", "", "## Falsch beurteilte Urteile (für die Stichprobenprüfung, Kriterium 4)", ""]
    for j in [j for j in valid if j["verdict"] != j["truth"]][:40]:
        lines.append(f"- {j['id']} · {j['channel']} · Wahrheit {'ok' if j['truth'] else 'kaputt'} · "
                     f"Konf. {j.get('confidence')} · {(j.get('raw') or '').strip()[-160:]!r}")
    text = "\n".join(lines)
    (DATA / f"kalibrierung-{iteration}{tag}-bericht.md").write_text(text, encoding="utf-8")
    return text


# --- Hauptlauf -------------------------------------------------------------------------

def main_jobs(model: str) -> list[tuple]:
    evs = generate_set_v2(MAIN_SEEDS)
    jobs = [(model, e, c, p, False) for e in evs for c in CELLS for p in range(3)]
    if model == SONNET:
        jobs += [(model, e, "I0-S0-E0-AA", p, False) for e in evs for p in range(3)]       # A/A-Kontrolle
        jobs += [(model, e, "I0-S0-E0-BLIND", p, p == 2) for e in evs for p in range(3)]   # Positivkontrolle
    return jobs


def family_jobs() -> list[tuple]:
    """Zusatzarm: Position k = Modell k (Sonnet, GPT, Gemini), S0/E0, I0 und I1."""
    evs = generate_set_v2(MAIN_SEEDS)
    return [(FAMILY_PANEL[p], e, f"{i}-S0-E0-FAM", p, False) for e in evs for i in INFO for p in range(3)]


def run(model: str, family: bool, workers: int) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "belege.jsonl").write_text(
        "\n".join(json.dumps(as_dict(e), ensure_ascii=False) for e in generate_set_v2(MAIN_SEEDS)), encoding="utf-8")
    _execute(DATA / "judgments.jsonl", family_jobs() if family else main_jobs(model), workers)


def dryrun() -> str:
    """Prompts aller Zellen für 2 Belege, ohne API-Aufrufe, zum Gegenlesen."""
    evs = generate_set_v2(range(2000, 2001), domains=("coding", "business"), kinds=("fail_subtle",))
    out = []
    for e in evs:
        for c in CELLS + ["I0-S0-E0-BLIND"]:
            for p in range(3):
                prompt, ch = build_prompt(e, c, p, blind=c.endswith("BLIND") and p == 2)
                out.append(f"\n\n######## {e.id} · {c} · Position {p} · Kanal {ch}\n\n{prompt}")
    DATA.mkdir(parents=True, exist_ok=True)
    path = DATA / "dryrun-prompts.md"
    path.write_text("".join(out), encoding="utf-8")
    return str(path)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["dryrun", "calibrate", "calibrate-report", "run"])
    p.add_argument("--iteration", type=int, default=1)
    p.add_argument("--model", default=SONNET)
    p.add_argument("--family", action="store_true", help="Zusatzarm mit drei Modellfamilien")
    p.add_argument("--workers", type=int, default=8)
    a = p.parse_args()
    if a.cmd == "dryrun":
        print(dryrun())
    elif a.cmd == "calibrate":
        calibrate(a.iteration, a.model, a.workers)
        print(calibrate_report(a.iteration, a.model))
    elif a.cmd == "calibrate-report":
        print(calibrate_report(a.iteration, a.model))
    else:
        run(a.model, a.family, a.workers)


if __name__ == "__main__":
    main()
