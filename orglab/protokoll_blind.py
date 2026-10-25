"""Blinde Kodierung des Fehlerprotokolls (notizen/30): Richtung und Fehlerquelle, durch ein Nicht-Claude-Modell.

  python -m orglab.protokoll_blind --dry
  python -m orglab.protokoll_blind          # Ergebnis nach daten/protokoll-blind/<Zeitstempel>.json

Der Kodierer sieht je Eintrag nur "Was", "Wer", "Gefunden durch" und den Wortlaut der betroffenen These, nie Claudes eigene
Einschätzung (Spalten "Richtung (Claude)" und "Quelle (Claude)").
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time

from . import openrouter
from .runner import ROOT

MODEL, EFFORT = "openai/gpt-6.1-sol", "high"
OUT = ROOT / "daten" / "protokoll-blind"

# Vorausschauende Einträge ohne Claudes Spalten; These im Wortlaut (hypothesen.md bzw. Kontext)
EINTRAEGE = [
    {"wann": "23.10. ~10:50",
     "was": "The frozen analysis script of a confirmatory experiment did not implement a preregistered rule "
            "('with fewer than 16 complete batches, report only descriptively, not confirmatorily').",
     "wer": "Claude (wrote the script)", "gefunden": "two other models (GPT, Gemini) that re-implemented the analysis from the preregistration only",
     "these": "H-037: Throttled reasoning (effort: low) increases the false alarm rate of reviewers compared with normal "
              "(adaptive) reasoning, without lowering the miss rate."},
    {"wann": "23.10. ~11:45",
     "was": "Claude proposed a 'secure' blinding variant (the human picks the random number) and claimed it was safe, but "
            "on a shared machine the number would have passed through Claude's hands anyway.",
     "wer": "Claude", "gefunden": "the human asked 'why does this need a human if it is just a dice roll?'",
     "these": "Rule proposal: blinded analysis protects the analysis from unconscious bias."},
    {"wann": "23.10. ~13:15",
     "was": "In a report, a summary line stated '14 entries, I 7, S 6, Z 3, K 2', but the report's own table had 24 rows "
            "with different category counts.",
     "wer": "Ace (another agent)", "gefunden": "Claude recounted the table",
     "these": "Monolith benchmark analysis: which category of breakpoints dominated (infrastructure most frequent, integration most costly)."},
]

PROMPT = """You code entries of an error log from a small research team (a human and AI agents). For each entry, decide two things, independently:

1. "richtung": If the error had NOT been caught, would it have pushed the results or claims toward SUPPORTING the named thesis ("pro"), toward CONTRADICTING it ("contra"), or neither ("neutral")? Use "unklar" if you cannot tell.
2. "quelle": What was the source of the error?
   - "Z" chance / slip (inattention, miscount, typo)
   - "I" missing information (the one who erred lacked a fact about the world, a provider, data, or documentation)
   - "K" context bias (what the one who erred had in mind, such as a hypothesis or their own plan, colored the judgment)
   - "M" model bias (a blind spot that other instances of the same model or model family would share)
   - "S" specification gap (a rule or plan says something, the implementation does not do it)
   - "U" unclear

Give a reason of at most 20 words for each. Answer only with JSON: [{{"wann": "...", "richtung": "...", "richtung_grund": "...", "quelle": "...", "quelle_grund": "..."}}, ...]

Entries:
{entries}
"""


def build() -> str:
    return PROMPT.format(entries=json.dumps(EINTRAEGE, ensure_ascii=False, indent=1))


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("--dry", action="store_true")
    a = p.parse_args()
    prompt = build()
    if a.dry:
        print(prompt)
        return
    resp = openrouter.chat(MODEL, [{"role": "user", "content": prompt}], max_tokens=8000, purpose="Protokoll blind",
                           estimate_usd=0.2, reasoning={"effort": EFFORT})
    text = resp["choices"][0]["message"].get("content") or ""
    m = re.search(r"\[.*\]", text, re.S)
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f"{time.strftime('%Y%m%d-%H%M')}.json"
    out.write_text(json.dumps({"model": MODEL, "effort": EFFORT, "prompt": prompt, "raw": text,
                               "codes": json.loads(m.group(0)) if m else None, "usage": resp.get("usage")},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
