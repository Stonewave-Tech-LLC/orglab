"""Blinde Fremdkodierung der Wave-Fälle (`notizen/28-wave-faelle`, D-019) durch ein Nicht-Claude-Modell.

  python -m orglab.kodierung_fremd --dry     # nur den Prompt zeigen
  python -m orglab.kodierung_fremd           # ein Aufruf, Ergebnis nach notizen/28-wave-faelle/03-kodierung-gpt.md

Das Modell bekommt nur die 14 Fälle und das Kodierbuch, nicht den Abschnitt "Herkunft und Einschränkungen". Dort steht
unsere Hypothese ("Status grün, eine Zahl widerspricht"), und die soll den Kodierer nicht lenken. Ebenso wenig sieht es
Claudes versiegelte Kodierung.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time

from . import openrouter
from .runner import ROOT

FOLDER = ROOT / "notizen" / "28-wave-faelle"
RAW = ROOT / "daten" / "wave-kodierung"
MODEL = "openai/gpt-6.1-sol"
EFFORT = "high"
FIELDS = ("K0", "K1", "K2", "K3", "K4", "K5", "K6", "K7")


def material() -> tuple[str, str]:
    text = (FOLDER / "00-faelle-und-kodierbuch.md").read_text(encoding="utf-8")
    cases = text.split("## Die Fälle")[1].split("## Kodierbuch")[0].split("\n", 1)[1].strip()
    book = text.split("## Kodierbuch")[1].split("**Verfahren:**")[0].split("\n", 1)[1].strip()
    return cases, book


def build_prompt() -> str:
    cases, book = material()
    return "\n\n".join([
        "Du kodierst 14 kurze Fallbeschreibungen aus einem Software-Team, in dem KI-Agenten Arbeit erledigen und prüfen. "
        "Wende das Kodierbuch genau an: je Fall und Feld genau einen der erlaubten Werte. Kodiere nur, was der Text "
        "hergibt. 'unklar' bzw. 'unbekannt' ist ausdrücklich besser als Raten. Gib zu jedem Wert einen Beleg aus dem "
        "Text in 2 bis 6 Wörtern an.",
        "## Kodierbuch\n\n" + book,
        "## Fälle\n\n" + cases,
        'Antworte nur mit einem JSON-Objekt der Form {"1": {"K0": {"v": "<Wert>", "b": "<Beleg>"}, "K1": {...}, ..., '
        '"K7": {...}}, "2": {...}, ..., "14": {...}}. Verwende die Werte exakt wie im Kodierbuch geschrieben.',
    ])


def parse(text: str) -> dict:
    m = re.search(r"\{.*\}", text or "", re.S)
    return json.loads(m.group(0)) if m else {}


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("--dry", action="store_true")
    a = p.parse_args()
    prompt = build_prompt()
    if a.dry:
        print(prompt)
        return
    resp = openrouter.chat(MODEL, [{"role": "user", "content": prompt}], max_tokens=16000,
                           purpose="Wave-Kodierung Fremdkodierer", estimate_usd=0.5, reasoning={"effort": EFFORT})
    text = resp["choices"][0]["message"].get("content") or ""
    usage = resp.get("usage") or {}
    RAW.mkdir(parents=True, exist_ok=True)
    (RAW / "gpt-roh.json").write_text(json.dumps({"model": MODEL, "effort": EFFORT, "time": time.strftime("%Y-%m-%d %H:%M"),
                                                   "prompt": prompt, "raw": text, "usage": usage}, ensure_ascii=False, indent=1),
                                      encoding="utf-8")
    codes = parse(text)
    L = ["# Kodierung GPT (blind, Fremdkodierer)", "",
         f"- **Modell:** `{MODEL}` über OpenRouter, `reasoning.effort = {EFFORT}`, ein Aufruf, {time.strftime('%Y-%m-%d %H:%M')}",
         "- **Sah:** nur die 14 Fälle und das Kodierbuch. **Nicht:** den Abschnitt mit unserer Hypothese, Claudes oder Aces Kodierung.",
         f"- **Kosten:** {float(usage.get('cost') or 0):.3f} $ · Rohantwort: `daten/wave-kodierung/gpt-roh.json`", "",
         "| Fall | " + " | ".join(FIELDS) + " |", "|---|" + "---|" * len(FIELDS)]
    for n in range(1, 15):
        c = codes.get(str(n), {})
        L.append(f"| {n} | " + " | ".join(f"{(c.get(k) or {}).get('v', '–')}" for k in FIELDS) + " |")
    L += ["", "## Belege", ""]
    for n in range(1, 15):
        c = codes.get(str(n), {})
        L.append(f"- **Fall {n}:** " + "; ".join(f"{k} {(c.get(k) or {}).get('b', '–')}" for k in FIELDS))
    (FOLDER / "03-kodierung-gpt.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L[:22]))


if __name__ == "__main__":
    main()
