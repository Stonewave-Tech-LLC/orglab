"""Prüfer 3b: GPT schreibt aus README, FRAGEN und Methodenbericht ein Analyseskript (Schritt 1) und deutet dessen
Ausgabe (Schritt 2). Das Skript führt Claude erst nach dem Lesen isoliert aus (python -I)."""
import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"<home>\Desktop\AI Workspace\social-skills-benchmark")
from orglab import openrouter

P = Path(r"<home>\Recherche\pruefer-3")
G = Path(r"<home>\Recherche\pruefer-3-gpt")
MODEL = "openai/gpt-6.1-sol"
docs = "\n\n".join(f"=== {n} ===\n" + (P / n).read_text(encoding="utf-8") for n in ("FRAGEN.md", "daten/README_DATEN.md", "recherche.md"))
samples = []
for f in sorted((P / "daten").glob("*.jsonl")):
    lines = f.read_text(encoding="utf-8").splitlines()[:2]
    samples.append(f"=== {f.name} (erste 2 Zeilen, lange Felder gekürzt) ===\n" + "\n".join(l[:1500] for l in lines))

def ask(prompt, purpose):
    r = openrouter.chat(MODEL, [{"role": "user", "content": prompt}], max_tokens=32000, purpose=purpose,
                        estimate_usd=1.0, reasoning={"effort": "high"})
    return r["choices"][0]["message"].get("content") or ""

if sys.argv[1] == "skript":
    prompt = ("Du bist ein unabhängiger Datenanalyst. Unten stehen ein Auftrag (FRAGEN.md), eine Datenbeschreibung und ein "
              "Methodenbericht, danach Beispielzeilen der Rohdaten. Schreib EIN Python-3-Skript, nur Standardbibliothek, das "
              "das Datenverzeichnis als einziges Argument nimmt, NICHTS schreibt, keine Netzwerkaufrufe macht und alle "
              "Zahlen ausgibt, die du brauchst, um die sechs Fragen zu beantworten (Tabellen als Text). Berücksichtige den "
              "Methodenbericht: Skala (Prozentpunkte UND Logit), keine Zirkelschlüsse bei der Schwierigkeit (Seeds 6000 und "
              "7000 sind getrennte Datensätze), Bootstrap über Belege, zufallskorrigierte Fehlerübereinstimmung. Schreib "
              "oben im Skript als Kommentar deinen Analyseplan, inklusive welche Ergebnisse welche Lesart stützen würden. "
              "Antworte nur mit dem Skript in einem ```python-Block.\n\n" + docs + "\n\n" + "\n\n".join(samples))
    text = ask(prompt, "Prüfer 3b Skript")
    m = re.search(r"```python\n(.*?)```", text, re.S)
    (G / "analyse_gpt.py").write_text(m.group(1) if m else "# keine Code-Antwort\n" + text[-2000:], encoding="utf-8")
    print("Skript:", "ja" if m else "NEIN", len(m.group(1)) if m else 0)
else:
    out = (G / "analyse_ausgabe.txt").read_text(encoding="utf-8")
    code = (G / "analyse_gpt.py").read_text(encoding="utf-8")
    prompt = ("Du bist derselbe unabhängige Datenanalyst. Unten stehen Auftrag, Datenbeschreibung, Methodenbericht, dein "
              "Analyseskript und seine Ausgabe. Schreib den Bericht auf Deutsch: je Frage die Antwort mit Zahlen und "
              "Unsicherheit, markiere, was explorativ ist, und schließe mit 'Was ich daraus schließen würde, und was nicht'. "
              "Formuliere nichts stärker, als die Zahlen hergeben. Benenne Schwächen deines eigenen Skripts.\n\n" + docs +
              "\n\n=== analyse_gpt.py ===\n" + code + "\n\n=== Ausgabe ===\n" + out)
    (G / "bericht_gpt.md").write_text(ask(prompt, "Prüfer 3b Bericht"), encoding="utf-8")
    print("Bericht geschrieben")
