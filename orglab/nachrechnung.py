"""Doppelte Buchführung (notizen/31, Empfehlung): Ein Modell anderer Familie schreibt die Auswertung eines Experiments
neu, nur aus der Präregistrierung und Beispielzeilen der Rohdaten, ohne Claudes Auswertecode.

  python -m orglab.nachrechnung E-022-reasoning-dosis            # Fremdmodelle schreiben je ein Skript (wird NICHT ausgeführt)
  python -I daten/<E>/nachrechnung/<modell>.py daten/<E>          # erst nach Lesen des Codes von Hand ausführen

Wo die Präregistrierung etwas offen lässt, muss das Fremdmodell selbst wählen und die Wahl im Feld "choices" nennen.
Diese Stellen sind Forscher-Freiheitsgrade, die eigentlich in die Präregistrierung gehört hätten (Regel 16).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time

from . import openrouter
from .runner import ROOT

MODELS = ("openai/gpt-6.1-sol", "google/gemini-4-argon")

TASK = """Below is the preregistration (in German) of a completed experiment, followed by the first lines of each raw data file. Write ONE self-contained Python 3 script (standard library only) that recomputes the preregistered primary analysis from the raw data. You do not have the original analysis code, and you must not guess what it does: implement what the preregistration specifies.

The script:
- takes the data directory as its only command-line argument and reads calls.jsonl and judgments.jsonl from it (one JSON object per line)
- writes nothing, makes no network calls, and prints exactly one JSON object to stdout with these keys:
  n_complete_batches, median_completion_tokens (per arm), manipulation_check_passed,
  p1_estimate, p1_lower_bound_one_sided_95, p2_estimate, p2_upper_bound_one_sided_95,
  false_alarm_rate (per arm), miss_rate (per arm), h_confirmed,
  choices (a list of strings: every decision you had to make because the preregistration left it open or ambiguous)
- uses a fixed random seed and the number of bootstrap draws stated in the preregistration

Arm names: the field "effort" is "low", "medium", "high", or null (= the arm the preregistration calls "ohne"). In judgments, "truth" true means the item really worked, "verdict" is the reviewer's judgment (true = works, false = broken, null = missing).

Answer with the script in a single ```python code block, nothing else.

=== PREREGISTRATION ===
{prereg}

=== FIRST 3 LINES OF calls.jsonl (field "raw" shortened) ===
{calls}

=== FIRST 3 LINES OF judgments.jsonl ===
{judgments}
"""


TASK_E020 = """Below is the preregistration (in German) of a completed experiment, including its dated deviations ("Abweichungen"), which are binding: where a deviation replaces an earlier section (e.g. the decision rule or the V2 secondary analysis), follow the deviation. Then the first lines of the raw data file. Write ONE self-contained Python 3 script (standard library only) that recomputes the preregistered primary analysis (V1, V2, V3) from the raw data. You do not have the original analysis code, and you must not guess what it does: implement what the preregistration specifies.

The script:
- takes the data directory as its only command-line argument and reads judgments.jsonl from it (one JSON object per line, one line per item x cell)
- writes nothing, makes no network calls, and prints exactly one JSON object to stdout with these keys:
  n_complete_seeds, v1_estimate, v1_ci95, v1_label, v2_estimate, v2_ci95, v2_label, v3_estimate, v3_ci95,
  miss_rate (per cell), false_alarm_rate (per cell),
  choices (a list of strings: every decision you had to make because the preregistration left it open or ambiguous)
- uses a fixed random seed and the number of bootstrap draws stated in the preregistration

Fields: "cell" is e.g. "SP1-ZU0-AU1" (SP = SPEC, ZU = ZUGANG, AU = AUSKUNFT, also given as integer fields "SP", "ZU", "AU"). "truth" true means the item really worked, "verdict" is the reviewer's judgment (true = works, false = broken, null = missing). "primary" true marks the spec-pure broken items ("spec-rein"). "n_checks" is the number of run_check calls. "seed" is the material seed, "id" the item.

Answer with the script in a single ```python code block, nothing else.

=== PREREGISTRATION ===
{prereg}

=== FIRST 3 LINES OF judgments.jsonl ===
{judgments}
"""


TASK_E024 = """Below is the preregistration (in German) of a completed confirmatory experiment, then the first lines of the raw data file. Write ONE self-contained Python 3 script (standard library only) that recomputes the preregistered primary analysis (the five predictions V1, W1, C1, C2, F1) from the raw data. You do not have the original analysis code, and you must not guess what it does: implement what the preregistration specifies.

The script:
- takes the data directory as its only command-line argument and reads judgments.jsonl from it (one JSON object per line, one line per model x item x cell)
- writes nothing, makes no network calls, and prints exactly one JSON object to stdout with these keys:
  n_complete_seeds, and for each of V1, W1, C1, C2, F1: <name>_estimate, <name>_ci95, <name>_q, <name>_label;
  plus sonnet_v1, sonnet_c1, sonnet_c2, sonnet_f1 (the same contrasts for the comparison model),
  choices (a list of strings: every decision you had to make because the preregistration left it open or ambiguous)
- uses the fixed random seeds and the number of bootstrap draws stated in the preregistration

Fields: "model" is "anthropic/claude-haiku-5.5" (target) or "anthropic/claude-sonnet-5.5" (comparison). "cell" is e.g. "SP1-ZU0-AU1" (also integer fields "SP", "ZU", "AU"). "truth" true means the item really worked, "verdict" is the reviewer's judgment (true = works, false = broken, null = missing). "primary" true marks spec-pure broken items. "looked_up" is whether the reviewer queried the runbook. "seed" is the material seed, "id" the item.

Answer with the script in a single ```python code block, nothing else.

=== PREREGISTRATION ===
{prereg}

=== FIRST 3 LINES OF judgments.jsonl ===
{judgments}
"""


def build_prompt(exp: str) -> str:
    if exp.startswith("E-024"):
        prereg = (ROOT / "experimente" / exp / "prereg.md").read_text(encoding="utf-8")
        judg = (ROOT / "daten" / exp / "judgments.jsonl").read_text(encoding="utf-8").splitlines()[:3]
        return TASK_E024.format(prereg=prereg, judgments="\n".join(judg))
    if exp.startswith("E-023"):                     # Design E-020 v3 mit Haiku: beide Präregistrierungen, Haiku-Rohdaten
        prereg = ((ROOT / "experimente" / "E-020-realitaet-in-dosen" / "prereg-v3.md").read_text(encoding="utf-8")
                  + "\n\n=== E-023 (same design, model changed; applies on top of the above) ===\n\n"
                  + (ROOT / "experimente" / exp / "prereg.md").read_text(encoding="utf-8"))
        judg = (ROOT / "daten" / exp / "judgments.jsonl").read_text(encoding="utf-8").splitlines()[:3]
        return TASK_E020.format(prereg=prereg, judgments="\n".join(judg))
    if exp.startswith("E-020"):                     # Fassung 3: Präregistrierung samt Abweichungen (Entscheidungsregel)
        prereg = (ROOT / "experimente" / exp / "prereg-v3.md").read_text(encoding="utf-8")
        judg = (ROOT / "daten" / exp / "v3" / "judgments.jsonl").read_text(encoding="utf-8").splitlines()[:3]
        return TASK_E020.format(prereg=prereg, judgments="\n".join(judg))
    prereg = (ROOT / "experimente" / exp / "prereg.md").read_text(encoding="utf-8").split("## Abweichungen")[0]
    data = ROOT / "daten" / exp
    calls = []
    for line in (data / "calls.jsonl").read_text(encoding="utf-8").splitlines()[:3]:
        c = json.loads(line)
        c["raw"] = (c.get("raw") or "")[:80] + " …"
        calls.append(json.dumps(c, ensure_ascii=False))
    judg = (data / "judgments.jsonl").read_text(encoding="utf-8").splitlines()[:3]
    return TASK.format(prereg=prereg, calls="\n".join(calls), judgments="\n".join(judg))


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("experiment")
    p.add_argument("--dry", action="store_true")
    a = p.parse_args()
    prompt = build_prompt(a.experiment)
    if a.dry:
        print(prompt)
        return
    out = ROOT / "daten" / a.experiment / "nachrechnung"
    out.mkdir(parents=True, exist_ok=True)
    (out / "prompt.md").write_text(prompt, encoding="utf-8")
    for model in MODELS:
        resp = openrouter.chat(model, [{"role": "user", "content": prompt}], max_tokens=32000,
                               purpose=f"{a.experiment} Nachrechnung", estimate_usd=1.0)
        text = resp["choices"][0]["message"].get("content") or ""
        m = re.search(r"```python\n(.*?)```", text, re.S)
        name = model.split("/")[1]
        (out / f"{name}.py").write_text(m.group(1) if m else "# keine Code-Antwort\n", encoding="utf-8")
        (out / f"{name}-meta.json").write_text(json.dumps({"model": model, "time": time.strftime("%Y-%m-%d %H:%M"),
                                                           "usage": resp.get("usage"), "raw_tail": text[-500:]},
                                                          ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{model}: {'Skript' if m else 'KEIN Skript'} ({len(m.group(1)) if m else 0} Zeichen)", flush=True)


if __name__ == "__main__":
    main()
