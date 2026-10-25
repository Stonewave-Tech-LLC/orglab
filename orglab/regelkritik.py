"""Regelkritik durch ein Modell-Panel (notizen/31): Welche Fehlerarten fangen die Projektregeln strukturell nicht?

  python -m orglab.regelkritik --dry       # Prompt zeigen
  python -m orglab.regelkritik run         # 20 Modelle, je ein Aufruf
  python -m orglab.regelkritik cluster     # anonymisiert von einem Nicht-Claude-Modell zu Themen bündeln lassen
  python -m orglab.regelkritik report      # Auswertung → notizen/31-regelkritik-panel.md (Abschnitt Ergebnis)

Die Modelle sehen nur CLAUDE.md, nicht notizen/30. Dort steht unsere eigene Vermutung (schleichende Konvergenz),
und die würde alle Antworten in dieselbe Richtung lenken.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations

from . import openrouter
from .runner import ROOT

DATA = ROOT / "daten" / "regelkritik"
NOTE = ROOT / "notizen" / "31-regelkritik-panel.md"
CLAUDE_FAMILY = ("anthropic/claude-opus-5.5", "anthropic/claude-sonnet-5.5", "anthropic/claude-haiku-5.5")
PANEL = (
    "openai/gpt-6.1-sol", "openai/gpt-6-astra", "google/gemini-4-argon", "google/gemini-3.8-flash", "x-ai/grok-4.7",
    "deepseek/deepseek-v4-pro-0813", "qwen/qwen3.8-max-0902", "moonshotai/kimi-k3", "mistralai/mistral-large-4-0",
    "meta/muse-spark-1.3", "z-ai/glm-5.3-prime", "minimax/minimax-m3", "cohere/command-a-plus", "amazon/nova-premier-v1",
    "stepfun/step-5-preview", "xiaomi/mimo-v2.6-pro", "thinkingmachines/inkling",
) + CLAUDE_FAMILY
CLUSTERER = "google/gemini-4-argon"     # bündelt anonymisierte Antworten, kennt die Herkunft nicht

QUESTION = """Ein kleines Forschungsteam besteht aus einem Menschen, der Forschungsmethodik gerade erst lernt, und einem KI-Modell. Die KI schreibt Code, Testmaterial, Auswertungen, Zusammenfassungen und auch die Arbeitsregeln. Die Regeln unten (die Datei CLAUDE.md des Projekts) wurden schrittweise aus Fehlern abgeleitet, die im Projekt bemerkt wurden.

Frage: Welche Fehlerarten fangen diese Regeln strukturell NICHT? Uns interessieren besonders Fehler, die keine der Regeln sichtbar machen würde, auch wenn alle Regeln eingehalten werden.

Nenne 3 bis 6 solche blinden Flecken. Je blinden Fleck:
- "name": kurzer Name
- "szenario": ein konkretes Beispiel, wie der Fehler in diesem Projekt passieren könnte
- "warum_unentdeckt": welche Regel ihn eigentlich fangen sollte und warum sie es nicht tut
- "gegenmassnahme": eine Gegenmaßnahme, die nicht davon abhängt, dass die KI ihren Fehler selbst bemerkt

Sei konkret und auf dieses Projekt bezogen, nicht allgemein. Antworte auf Deutsch und nur mit einem JSON-Array dieser Objekte.

--- CLAUDE.md ---
"""


def prompt() -> str:
    return QUESTION + (ROOT / "CLAUDE.md").read_text(encoding="utf-8")


def parse_array(text: str) -> list[dict]:
    m = re.search(r"\[.*\]", text or "", re.S)
    try:
        arr = json.loads(m.group(0)) if m else []
    except json.JSONDecodeError:
        return []
    return [x for x in arr if isinstance(x, dict) and x.get("name")]


def run(max_tokens: int = 8000, retry_empty: bool = False) -> None:
    """retry_empty: nur Modelle erneut fragen, deren letzte Antwort leer war (z. B. Denkbudget aufgebraucht)."""
    DATA.mkdir(parents=True, exist_ok=True)
    out = DATA / "antworten.jsonl"
    last = {}
    if out.exists():
        for l in out.read_text(encoding="utf-8").splitlines():
            r = json.loads(l)
            last[r["model"]] = r
    done = {m for m, r in last.items() if r["items"] or not retry_empty or "end of its life" in r.get("error", "")}
    p = prompt()

    def one(model: str) -> dict:
        row = {"model": model, "time": time.strftime("%Y-%m-%d %H:%M")}
        for attempt in range(2):
            try:
                resp = openrouter.chat(model, [{"role": "user", "content": p}], max_tokens=max_tokens,
                                       purpose="Regelkritik-Panel", estimate_usd=0.5)
                text = resp["choices"][0]["message"].get("content") or ""
                usage = resp.get("usage") or {}
                row.update(raw=text, items=parse_array(text), cost_usd=usage.get("cost"),
                           completion_tokens=usage.get("completion_tokens"), attempt=attempt)
                if row["items"]:
                    break
            except openrouter.BudgetExceeded:
                raise
            except Exception as e:
                row.update(error=f"{type(e).__name__}: {str(e)[:200]}", items=[], attempt=attempt)
        return row

    with ThreadPoolExecutor(max_workers=6) as pool, open(out, "a", encoding="utf-8") as fh:
        for row in pool.map(one, [m for m in PANEL if m not in done]):
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            fh.flush()
            print(f"{row['model']}: {len(row['items'])} blinde Flecken {row.get('error', '')}", flush=True)


def load() -> list[dict]:
    rows = [json.loads(l) for l in (DATA / "antworten.jsonl").read_text(encoding="utf-8").splitlines()]
    last = {r["model"]: r for r in rows}           # letzter Versuch je Modell
    return [last[m] for m in PANEL if m in last and last[m]["items"]]


def cluster() -> None:
    rows = load()
    rng = random.Random(31)
    items = [(r["model"], it) for r in rows for it in r["items"]]
    rng.shuffle(items)
    key = {f"B{n:03d}": (m, it) for n, (m, it) in enumerate(items, 1)}
    listing = "\n".join(f"{k}: {it.get('name')} – {it.get('warum_unentdeckt', '')[:400]}" for k, (m, it) in key.items())
    instr = ("Unten stehen blinde Flecken, die verschiedene Gutachter in den Arbeitsregeln eines Forschungsprojekts gefunden "
             "haben, jeweils mit ID, Name und Begründung. Bündle sie zu 8 bis 15 inhaltlichen Themen. Jede ID gehört zu genau "
             "einem Thema. Fasse nur gleichartige Einwände zusammen, nicht bloß ähnlich klingende. Antworte nur mit JSON: "
             '{"themen": [{"titel": "...", "beschreibung": "ein Satz", "ids": ["B001", ...]}, ...]}\n\n' + listing)
    resp = openrouter.chat(CLUSTERER, [{"role": "user", "content": instr}], max_tokens=12000,
                           purpose="Regelkritik-Clustering", estimate_usd=0.5)
    text = resp["choices"][0]["message"].get("content") or ""
    m = re.search(r"\{.*\}", text, re.S)
    (DATA / "cluster.json").write_text(json.dumps({"clusterer": CLUSTERER, "key": {k: {"model": v[0], **v[1]} for k, v in key.items()},
                                                   "raw": text, "themen": json.loads(m.group(0))["themen"] if m else []},
                                                  ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(key)} blinde Flecken, Clustering gespeichert")


def report() -> str:
    c = json.loads((DATA / "cluster.json").read_text(encoding="utf-8"))
    models = [r["model"] for r in load()]
    themes_of: dict[str, set[int]] = defaultdict(set)
    assigned = set()
    for i, t in enumerate(c["themen"]):
        for bid in t["ids"]:
            if bid in c["key"]:
                themes_of[c["key"][bid]["model"]].add(i)
                assigned.add(bid)
    jac = lambda a, b: len(themes_of[a] & themes_of[b]) / max(len(themes_of[a] | themes_of[b]), 1)
    pairs = lambda ms: [jac(a, b) for a, b in combinations(ms, 2)]
    claude = [m for m in models if m in CLAUDE_FAMILY]
    other = [m for m in models if m not in CLAUDE_FAMILY]
    mean = lambda xs: sum(xs) / len(xs) if xs else float("nan")
    cross = [jac(a, b) for a in claude for b in other]
    L = ["## Ergebnis (automatisch, `python -m orglab.regelkritik report`)", "",
         f"- Modelle mit verwertbarer Antwort: {len(models)} von {len(PANEL)} · blinde Flecken: {len(c['key'])} "
         f"(zugeordnet: {len(assigned)}) · Themen: {len(c['themen'])} · Clustering: `{c['clusterer']}`, anonymisiert",
         f"- Themen-Überlappung (Jaccard, Mittel): innerhalb Claude {mean(pairs(claude)):.2f} · innerhalb Nicht-Claude "
         f"{mean(pairs(other)):.2f} · Claude gegen Nicht-Claude {mean(cross):.2f}", "",
         "| Thema | genannt von (Modelle) | davon Claude | Beschreibung |", "|---|---|---|---|"]
    rows = []
    for i, t in enumerate(c["themen"]):
        ms = sorted({c["key"][b]["model"] for b in t["ids"] if b in c["key"]})
        rows.append((len(ms), t, ms))
    for n, t, ms in sorted(rows, key=lambda x: -x[0]):
        L.append(f"| {t['titel']} | {n} | {sum(m in CLAUDE_FAMILY for m in ms)} | {t.get('beschreibung', '')} |")
    L += ["", "**Einzelstimmen** (Themen, die nur ein Modell nennt):", ""]
    for n, t, ms in rows:
        if n == 1:
            L.append(f"- {t['titel']} ({ms[0]})")
    L += ["", "Kosten: " + f"{sum(float(r.get('cost_usd') or 0) for r in load()):.2f} $ Panel"]
    text = "\n".join(L)
    note = NOTE.read_text(encoding="utf-8")
    note = note.split("## Ergebnis")[0].rstrip() + "\n\n" + text + "\n"
    NOTE.write_text(note, encoding="utf-8")
    return text


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("cmd", nargs="?", choices=["run", "cluster", "report"])
    p.add_argument("--dry", action="store_true")
    p.add_argument("--retry-empty", action="store_true", help="leere Antworten mit 32.000 Tokens Budget wiederholen")
    a = p.parse_args()
    if a.dry or not a.cmd:
        print(prompt()[:1500])
    elif a.cmd == "run":
        run(32000, True) if a.retry_empty else run()
    elif a.cmd == "cluster":
        cluster()
    else:
        print(report())


if __name__ == "__main__":
    main()
