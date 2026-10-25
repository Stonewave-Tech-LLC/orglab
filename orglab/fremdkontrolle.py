"""Fremdkontrolle der Ground Truth (CLAUDE.md Regel 12, D-018): Ein Nicht-Claude-Modell beurteilt eine geschichtete
Stichprobe des Materials blind und je Beleg einzeln. Abweichungen von der Generator-Wahrheit klärt Neo von Hand.

  python -m orglab.fremdkontrolle E-022 --dry      # nur Stichprobe und Prompt zeigen
  python -m orglab.fremdkontrolle E-022            # Aufrufe (OpenRouter), Bericht nach experimente/<E>/fremdkontrolle.md
  python -m orglab.fremdkontrolle E-020v4 --leck   # Lecktest: Kurzauftrag ohne Runbook, spec-reine Fehler sollen
                                                   # NICHT sicher als kaputt erkannt werden (Regel 17)

Der Prüfer sieht den Auftrag und alle drei Kanäle, nie `fault`, `finding` oder `signatures`. Mehr Information als die
Sonnet-Prüfer, weil hier gefragt ist, ob die Ground Truth stimmt und entscheidbar ist, nicht wie gut ein Prüfer ist.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Callable

from . import openrouter
from .evidence import CHANNEL_DESC, CHANNELS, EvidenceV2, generate_set_v2
from .runner import ROOT

CHECKER = "openai/gpt-6.1-sol"          # andere Modellfamilie; schon in E-017 (FAMILY_PANEL) benutzt
CHECKER_EFFORT = "high"                 # gründlich: es geht um die Wahrheit des Materials, nicht um Prüferverhalten

PROMPT_HEAD = ("A colleague finished the work item below. Afterwards, three independent observations of the system were "
               "collected. Decide whether the work item actually achieved its intended effect.")
PROMPT_TAIL = ('Answer with a JSON object only: {"works": true or false, "reason": "one or two sentences naming the '
               'decisive line(s)", "decidable": true or false}. Set "decidable" to false if the observations do not '
               "allow a confident decision either way.")


def build_prompt(ev: EvidenceV2, item_text: str | None = None, extra: str = "") -> str:
    parts = [PROMPT_HEAD, f"Work item: {item_text or ev.item}"]
    if extra:
        parts.append(extra)
    for ch in CHANNELS[ev.domain]:
        parts.append(f"Observation ({CHANNEL_DESC[ch]}):\n```\n{ev.channels[ch]}\n```")
    parts.append(PROMPT_TAIL)
    return "\n\n".join(parts)


def parse(text: str) -> dict[str, Any]:
    for m in reversed(list(re.finditer(r"\{[^{}]*\}", text or "", re.S))):
        try:
            d = json.loads(m.group(0))
        except json.JSONDecodeError:
            continue
        if isinstance(d.get("works"), bool):
            return d
    return {}


def stratified_sample(evs: list[EvidenceV2], per_fault: int, per_ok: int, tag: str) -> list[EvidenceV2]:
    """Je Domäne und Fehlerart `per_fault` kaputte Belege, je Domäne und Ok-Art `per_ok` Ok-Belege."""
    rng = random.Random(f"fremdkontrolle:{tag}")
    groups: dict[tuple, list[EvidenceV2]] = {}
    for e in evs:
        key = (e.domain, e.fault) if not e.works else (e.domain, e.kind)
        groups.setdefault(key, []).append(e)
    out = []
    for key in sorted(groups):
        g = sorted(groups[key], key=lambda e: e.id)
        out += rng.sample(g, min(per_ok if key[1].startswith("ok") else per_fault, len(g)))
    return out


def check(evs: list[EvidenceV2], out_dir: Path, purpose: str, prompt_fn: Callable[[EvidenceV2], str] = build_prompt,
          workers: int = 6, name: str = "fremdkontrolle") -> list[dict[str, Any]]:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{name}.jsonl"
    done = {json.loads(l)["id"] for l in path.read_text(encoding="utf-8").splitlines()} if path.exists() else set()

    def one(ev: EvidenceV2) -> dict[str, Any]:
        row: dict[str, Any] = {"id": ev.id, "domain": ev.domain, "kind": ev.kind, "fault": ev.fault, "truth": ev.works,
                               "model": CHECKER, "effort": CHECKER_EFFORT}
        for attempt in range(3):
            try:
                resp = openrouter.chat(CHECKER, [{"role": "user", "content": prompt_fn(ev)}], max_tokens=8000,
                                       purpose=purpose, estimate_usd=0.10, reasoning={"effort": CHECKER_EFFORT})
                text = resp["choices"][0]["message"].get("content") or ""
                d = parse(text)
                usage = resp.get("usage") or {}
                row.update(raw=text[-2000:], verdict=d.get("works"), reason=d.get("reason"), decidable=d.get("decidable"),
                           attempt=attempt, cost_usd=usage.get("cost"), completion_tokens=usage.get("completion_tokens"))
                if d:
                    break
            except openrouter.BudgetExceeded:
                raise
            except Exception as e:
                row.update(error=f"{type(e).__name__}: {str(e)[:200]}", attempt=attempt, verdict=None)
        return row

    todo = [e for e in evs if e.id not in done]
    with ThreadPoolExecutor(max_workers=workers) as pool, open(path, "a", encoding="utf-8") as fh:
        for row in pool.map(one, todo):
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            fh.flush()
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines()]


def report(rows: list[dict[str, Any]], evs: dict[str, EvidenceV2], title: str) -> str:
    agree = [r for r in rows if r.get("verdict") == r["truth"] and r.get("decidable") is not False]
    dis = [r for r in rows if r not in agree]
    cost = sum(float(r.get("cost_usd") or 0) for r in rows)
    L = [f"# {title}", "", f"Prüfer: `{CHECKER}` über OpenRouter, `reasoning.effort = {CHECKER_EFFORT}`, je Beleg einzeln, "
         "sieht Auftrag und alle drei Kanäle, keine Fehlerart und keinen Befundtext.", "",
         f"- Belege: {len(rows)}, Übereinstimmung mit der Generator-Wahrheit: {len(agree)}, **Abweichungen oder "
         f"'nicht entscheidbar': {len(dis)}**", f"- Kosten: {cost:.2f} $", "",
         "Jede Abweichung klärt Neo von Hand (Spalte 'Klärung'): Generatorfehler, Prüferfehler oder echte Mehrdeutigkeit. "
         "Der Hauptlauf startet erst, wenn alle geklärt sind.", ""]
    for r in sorted(dis, key=lambda r: r["id"]):
        ev = evs[r["id"]]
        L += [f"## {r['id']}", "", f"- Generator: {'ok' if r['truth'] else 'kaputt'} (`{r['fault']}`)",
              f"- Prüfer: {r.get('verdict')} (entscheidbar: {r.get('decidable')})", f"- Begründung: {r.get('reason')}",
              f"- Spur laut Generator: {ev.signatures or '—'}", "- **Klärung (Neo):** ", "",
              "<details><summary>Beleg</summary>", "", "```", build_prompt(ev), "```", "", "</details>", ""]
    L += ["## Alle Urteile", "", "| Beleg | Fehlerart | Wahrheit | Prüfer | entscheidbar |", "|---|---|---|---|---|"]
    L += [f"| {r['id']} | {r['fault']} | {r['truth']} | {r.get('verdict')} | {r.get('decidable')} |"
          for r in sorted(rows, key=lambda r: r["id"])]
    return "\n".join(L)


# Material je Experiment: (Belege, Stichprobe, Datenordner, Ergebnisordner)
def _e022() -> tuple[list[EvidenceV2], list[EvidenceV2], Path, Path]:
    from . import e022
    evs = generate_set_v2(e022.SEEDS)
    return evs, stratified_sample(evs, per_fault=2, per_ok=2, tag="E-022"), e022.DATA, ROOT / "experimente" / e022.EXPERIMENT


def _e020v4() -> tuple[list, list, Path, Path]:
    from . import evidence_v4
    evs = evidence_v4.generate_set(E020_SEEDS)
    exp = ROOT / "experimente" / "E-020-realitaet-in-dosen"
    return evs, stratified_sample(evs, per_fault=3, per_ok=2, tag="E-020v4"), ROOT / "daten" / "E-020-realitaet-in-dosen", exp


E020_SEEDS = range(6000, 6024)        # frische Hauptlauf-Seeds für E-020 auf Material v4 (Entwurf v3)
E024_SEEDS = range(7000, 7024)        # frische Seeds für den Bestätigungslauf E-024 (Material v4.3 unverändert)
E024 = "E-024-bestaetigung-massstab"


def _e024() -> tuple[list, list, Path, Path]:
    from . import evidence_v4
    evs = evidence_v4.generate_set(E024_SEEDS)
    # Ablage in einem Unterordner: verblindung.py liest nur daten/<E>/*.jsonl, und diese Zeilen tragen ein model-Feld
    return evs, stratified_sample(evs, per_fault=3, per_ok=2, tag=E024), ROOT / "daten" / E024 / "material", ROOT / "experimente" / E024


MATERIAL = {"E-022": _e022, "E-020v4": _e020v4, "E-024": _e024}

# --- Einzelkanal (Lehre aus E-020): sieht der Prüfer nur EINEN Kanal, wie bei ZUGANG = 0, ist der Beleg dann entscheidbar? ---
SINGLE_HEAD = ("A colleague finished the work item below. Afterwards, one observation of the system was collected. "
               "Decide whether the work item actually achieved its intended effect, based on this observation.")


def build_prompt_single(ev: EvidenceV2) -> str:
    from .e020v3 import presented_channel
    ch = presented_channel(ev)
    return "\n\n".join([SINGLE_HEAD, f"Work item: {ev.item}",
                        f"Observation ({CHANNEL_DESC[ch]}):\n```\n{ev.channels[ch]}\n```", PROMPT_TAIL])


def single_report(rows: list[dict[str, Any]], evs: dict[str, Any], title: str) -> str:
    """Je Fehlerart × vorgelegter Kanal: stimmt GPT mit der Wahrheit überein und hält den Beleg für entscheidbar?"""
    from .e020v3 import presented_channel
    bad = [r for r in rows if not (r.get("verdict") == r["truth"] and r.get("decidable") is not False)]
    groups: dict[tuple, list] = {}
    for r in rows:
        groups.setdefault((r["fault"] if not r["truth"] else r["kind"], presented_channel(evs[r["id"]])), []).append(r)
    cost = sum(float(r.get("cost_usd") or 0) for r in rows)
    L = [f"# {title}", "", f"Prüfer: `{CHECKER}`, `reasoning.effort = {CHECKER_EFFORT}`, je Beleg einzeln. Sieht den **vollen "
         "Auftrag mit Sollwerten** und **nur den einen Kanal**, der bei ZUGANG = 0 vorgelegt wird (Kanal = Seed mod 3).", "",
         f"- Belege: {len(rows)} (alle), **nicht übereinstimmend oder nicht entscheidbar: {len(bad)}**, Kosten {cost:.2f} $",
         "- Diese Belege gelten im Bestätigungslauf als **einzeln nicht entscheidbar** und werden in der vorab festgelegten "
         "Zusatzanalyse ausgeschlossen (Liste unten, `einzelkanal-ausschluss.json`).", "",
         "| Fehlerart bzw. Ok-Art | Kanal | n | übereinstimmend und entscheidbar |", "|---|---|---|---|"]
    for k in sorted(groups):
        g = groups[k]
        good = sum(r not in bad for r in g)
        L.append(f"| {k[0]} | {k[1]} | {len(g)} | {good} |")
    L += ["", "## Nicht übereinstimmend oder nicht entscheidbar", "", "| Beleg | Wahrheit | Prüfer | entscheidbar | Begründung |",
          "|---|---|---|---|---|"]
    L += [f"| {r['id']} | {'ok' if r['truth'] else r['fault']} | {r.get('verdict')} | {r.get('decidable')} | "
          f"{(r.get('reason') or r.get('error') or '').replace('|', '/')} |" for r in sorted(bad, key=lambda r: r["id"])]
    return "\n".join(L)


def leak_report(rows: list[dict[str, Any]], title: str) -> str:
    """Lecktest: Der Prüfer sieht nur den Kurzauftrag. Bei spec-reinen Fehlern sollte er unsicher sein oder irren."""
    from .evidence_v4 import PRIMARY
    prim = [r for r in rows if r["fault"] in PRIMARY]
    caught = [r for r in prim if r.get("verdict") is False and r.get("decidable") is not False]
    L = [f"# {title}", "", f"Prüfer: `{CHECKER}`, `reasoning.effort = {CHECKER_EFFORT}`, je Beleg einzeln, sieht nur den "
         "**Kurzauftrag** (ohne Sollwerte) und alle drei Kanäle, kein Runbook.", "",
         f"- Spec-reine kaputte Belege: {len(prim)}, davon **ohne Sollwert sicher als kaputt erkannt: {len(caught)}** "
         f"({len(caught) / max(len(prim), 1):.0%})",
         "- Vorab festgelegtes Kriterium (Entwurf v3): höchstens 25 % je Fehlerart. Liegt eine Fehlerart darüber, ist sie "
         "nicht spec-rein und fällt aus der Primärmenge (oder der Generator wird nachgebessert).", "",
         "| Fehlerart | n | sicher erkannt ohne Sollwert |", "|---|---|---|"]
    for f in PRIMARY:
        fr = [r for r in prim if r["fault"] == f]
        c = sum(r in caught for r in fr)
        L.append(f"| {f} | {len(fr)} | {c} ({c / max(len(fr), 1):.0%}) |")
    ok = [r for r in rows if r["truth"]]
    L += ["", f"Ok-Belege (Gegenprobe): {len(ok)}, davon als kaputt beurteilt: {sum(r.get('verdict') is False for r in ok)}",
          "", "| Beleg | Fehlerart | Prüfer | entscheidbar | Begründung |", "|---|---|---|---|---|"]
    L += [f"| {r['id']} | {r['fault']} | {r.get('verdict')} | {r.get('decidable')} | {(r.get('reason') or '').replace('|', '/')} |"
          for r in sorted(rows, key=lambda r: r["id"])]
    return "\n".join(L)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("experiment", choices=sorted(MATERIAL))
    p.add_argument("--dry", action="store_true")
    p.add_argument("--leck", action="store_true", help="Kurzauftrag ohne Sollwerte (nur Material v4)")
    p.add_argument("--einzelkanal", action="store_true", help="alle Belege, nur der bei ZUGANG = 0 vorgelegte Kanal (Material v4)")
    a = p.parse_args()
    evs, sample, data, exp = MATERIAL[a.experiment]()
    if a.einzelkanal:
        if a.dry:
            print(build_prompt_single(evs[0]))
            return
        exp.mkdir(parents=True, exist_ok=True)
        rows = check(evs, data, purpose=f"{a.experiment} Einzelkanal", prompt_fn=build_prompt_single, name="einzelkanal")
        text = single_report(rows, {e.id: e for e in evs}, f"{a.experiment}: Fremdkontrolle je Einzelkanal (Regel 12, Lehre E-020)")
        (exp / "fremdkontrolle-einzelkanal.md").write_text(text, encoding="utf-8")
        bad = sorted(r["id"] for r in rows if not (r.get("verdict") == r["truth"] and r.get("decidable") is not False))
        (exp / "einzelkanal-ausschluss.json").write_text(json.dumps(bad, indent=1), encoding="utf-8")
        print(text.split("\n## ")[0])
        return
    print(f"[Fremdkontrolle {a.experiment}] Stichprobe {len(sample)} von {len(evs)} Belegen: "
          f"{sum(not e.works for e in sample)} kaputt, {sum(e.works for e in sample)} ok", flush=True)
    prompt_fn = (lambda e: build_prompt(e, item_text=e.item_short)) if a.leck else build_prompt
    if a.leck:
        # Lecktest: je spec-reiner Fehlerart 6 kaputte Belege, dazu je Domäne und Ok-Art 2 Ok-Belege als Gegenprobe
        from .evidence_v4 import PRIMARY
        sample = stratified_sample([e for e in evs if e.works or e.fault in PRIMARY], per_fault=6, per_ok=2, tag="leck")
        print(f"[Lecktest] {len(sample)} Belege: {sum(not e.works for e in sample)} spec-rein kaputt, "
              f"{sum(e.works for e in sample)} ok", flush=True)
    if a.dry:
        print(prompt_fn(sample[0]))
        return
    if a.leck:
        rows = check(sample, data, purpose=f"{a.experiment} Lecktest", prompt_fn=prompt_fn, name="lecktest")
        text = leak_report(rows, f"{a.experiment}: Lecktest ohne Sollwerte (Regel 17)")
        (exp / "lecktest.md").write_text(text, encoding="utf-8")
        print(text.split("\n| Beleg")[0])
        return
    rows = check(sample, data, purpose=f"{a.experiment} Fremdkontrolle")
    text = report(rows, {e.id: e for e in evs}, f"{a.experiment}: Fremdkontrolle der Ground Truth (Regel 12)")
    (exp / "fremdkontrolle.md").write_text(text, encoding="utf-8")
    print(text.split("\n## ")[0])


if __name__ == "__main__":
    main()
