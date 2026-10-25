"""Schwierigkeitslandkarte: Was macht Prüfaufgaben für starke Modelle schwer? Explorative Auswertung aller
Kalibrierungsläufe von E-017 und E-019 (nicht präregistriert, nur aus den Rohdaten).

  python -m orglab.landkarte          # schreibt notizen/20-schwierigkeitslandkarte.md

Ungültige Läufe (Generatorfehler, mehrdeutige Ground Truth) fließen nicht in die Hauptzahlen ein; der mehrdeutige
zero_traffic-Lauf wird nur für den Spezifikationsvergleich gesondert gezeigt.
"""

from __future__ import annotations

import json
import math
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

from .runner import ROOT

E17, E19 = ROOT / "daten" / "E-017-faktorielles-panel", ROOT / "daten" / "E-019-stapel-panel"
SONNET, HAIKU = "anthropic/claude-sonnet-5.5", "anthropic/claude-haiku-5.5"

# (Kürzel, Datei, Modus, Material, Reasoning, gültig, Grund)
RUNS = [
    ("E17-K1", E17 / "kalibrierung-1.jsonl", "einzeln", "v2.0", "low", False, "Rauschen veränderte Daten (Generatorfehler)"),
    ("E17-K2", E17 / "kalibrierung-2.jsonl", "einzeln", "v2.1", "low", True, ""),
    ("E17-K3", E17 / "kalibrierung-3.jsonl", "einzeln", "v2.2", "low", True, ""),
    ("E17-K3-Haiku", E17 / "kalibrierung-3-claude-haiku-5.5.jsonl", "einzeln", "v2.2", "low", True, ""),
    ("E19-L1-v2-ungültig", E19 / "judgments-kalibrierung-L1-lauf1-generatorfehler.jsonl", "Stapel 8", "v2.2", "low", False,
     "Routinezeilen widersprüchlich (Generatorfehler)"),
    ("E19-L1-v2", E19 / "judgments-kalibrierung-L1.jsonl", "Stapel 8", "v2.3", "low", True, ""),
    ("E19-L2-v2", E19 / "judgments-kalibrierung-L2.jsonl", "Stapel 12", "v2.3", "low", True, ""),
    ("E19-L3-v2", E19 / "judgments-kalibrierung-L3.jsonl", "Stapel 12", "v2.3", "aus", True, ""),
    ("E19-L1-v3-mehrdeutig", E19 / "judgments-kalibrierung-L1-v3-lauf1-mehrdeutig.jsonl", "Stapel 8", "v3.0", "low", False,
     "zero_traffic ohne übliche Last im Auftrag (mehrdeutig)"),
    ("E19-L1-v3", E19 / "judgments-kalibrierung-L1-v3.jsonl", "Stapel 8", "v3.1", "low", True, ""),
    ("E19-L2-v3", E19 / "judgments-kalibrierung-L2-v3.jsonl", "Stapel 12", "v3.1", "low", True, ""),
    ("E19-L3-v3", E19 / "judgments-kalibrierung-L3-v3.jsonl", "Stapel 12", "v3.1", "aus", True, ""),
]

# Welche Art von Abgleich verlangt die Fehlerspur?
TRACE = {
    "stale_process": "Identität mit Auftrag abgleichen (Commit, Adresse, Betrag)",
    "wrong_recipient": "Identität mit Auftrag abgleichen (Commit, Adresse, Betrag)",
    "amount_mismatch": "Identität mit Auftrag abgleichen (Commit, Adresse, Betrag)",
    "db_down": "Status grün, eine Zahl widerspricht",
    "cache_down": "Status grün, eine Zahl widerspricht",
    "zero_traffic": "Status grün, eine Zahl widerspricht",
    "empty_attachment": "Status grün, eine Zahl widerspricht",
    "weights_broken": "Status grün, eine Zahl widerspricht",
    "row_loss": "Menge mit Auftrag abgleichen (Zeilen, Duplikate, Spalten)",
    "duplicates_kept": "Menge mit Auftrag abgleichen (Zeilen, Duplikate, Spalten)",
    "column_loss": "Menge mit Auftrag abgleichen (Zeilen, Duplikate, Spalten)",
    "bounced": "Zustand ohne Fehlerwort (zurückgestellt, ausstehend)",
}


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def rate(xs: list[dict]) -> str:
    k, n = sum(j["verdict"] != j["truth"] for j in xs), len(xs)
    if not n:
        return "–"
    lo, hi = wilson(k, n)
    return f"{k / n:.3f} [{lo:.2f}; {hi:.2f}] (n={n})"


def load() -> list[dict]:
    out = []
    for tag, path, mode, mat, effort, valid, why in RUNS:
        if not path.exists():
            continue
        last: dict[tuple, dict] = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            j = json.loads(line)
            last[(j["id"], j.get("cell"), j.get("position"), j.get("channel"))] = j
        for j in last.values():
            if j.get("verdict") is None:
                continue
            out.append({**j, "run": tag, "mode": mode, "material": mat, "effort": effort, "valid": valid,
                        "model": j.get("model", SONNET)})
    return out


def report() -> str:
    js = load()
    son = [j for j in js if j["valid"] and j["model"] == SONNET]
    miss = lambda xs: [j for j in xs if not j["truth"]]
    fa = lambda xs: [j for j in xs if j["truth"]]
    L = ["# Schwierigkeitslandkarte: Was macht Prüfaufgaben für Sonnet 5.5 schwer?", "",
         "> **Korrektur 23.10. (E-021, KORREKTUR_E021):** \"Reasoning aus\" bedeutet hier die Standardeinstellung mit adaptivem, verborgenem Reasoning, \"low\" bedeutet gedrosseltes Reasoning. Aussagen \"Reasoning erhöht Fehlalarme\" sind umzudrehen (H-037).", "",
         "**Stand:** 22.10.2026 · **explorativ**, nicht präregistriert · Skript: `python -m orglab.landkarte`",
         "Daten: alle Kalibrierungsläufe aus E-017 und E-019. Ungültige Läufe werden nur dort gezeigt, wo es ausdrücklich steht.",
         "Raten mit 95-%-Wilson-Intervall. Urteile desselben Belegs über Kanäle oder Läufe sind nicht unabhängig, die "
         "Intervalle sind deshalb zu eng. Lies sie als Größenordnung.", "",
         "## 1. Überblick je Lauf", "",
         "| Lauf | Modus | Material | Reasoning | gültig | Fehlerrate | Fehlalarm | übersehen |", "|---|---|---|---|---|---|---|---|"]
    for tag, _, mode, mat, effort, valid, why in RUNS:
        xs = [j for j in js if j["run"] == tag]
        if not xs:
            continue
        r = lambda ys: f"{st.fmean(int(j['verdict'] != j['truth']) for j in ys):.3f}" if ys else "–"
        L.append(f"| {tag} | {mode} | {mat} | {effort} | {'ja' if valid else 'nein: ' + why} | {r(xs)} | {r(fa(xs))} | {r(miss(xs))} |")

    total = len(son)
    L += ["", f"Gültige Sonnet-Urteile gesamt: **{total}**, davon Fehler: {sum(j['verdict'] != j['truth'] for j in son)}.", "",
          "## 2. Übersehen je Fehlerart (Sonnet, alle gültigen Läufe)", "",
          "| Fehlerart | Art der Spur | Übersehensrate [95-%-KI] |", "|---|---|---|"]
    by_fault = defaultdict(list)
    for j in miss(son):
        by_fault[j["fault"]].append(j)
    for f, xs in sorted(by_fault.items(), key=lambda kv: -st.fmean(int(j["verdict"] != j["truth"]) for j in kv[1])):
        L.append(f"| `{f}` | {TRACE.get(f, '?')} | {rate(xs)} |")

    L += ["", "## 3. Nach Art der Spur zusammengefasst", "", "| Art der Spur | Übersehensrate |", "|---|---|"]
    by_trace = defaultdict(list)
    for j in miss(son):
        by_trace[TRACE.get(j["fault"], "?")].append(j)
    for t, xs in sorted(by_trace.items(), key=lambda kv: -st.fmean(int(j["verdict"] != j["truth"]) for j in kv[1])):
        L.append(f"| {t} | {rate(xs)} |")

    L += ["", "## 4. Reasoning: low gegen aus (gleiches Material, Stapel 12)", "",
          "| Material | Reasoning | Fehlalarm | übersehen |", "|---|---|---|---|"]
    for mat in ("v2.3", "v3.1"):
        for eff in ("low", "aus"):
            xs = [j for j in son if j["material"] == mat and j["effort"] == eff and j["mode"] == "Stapel 12"]
            L.append(f"| {mat} | {eff} | {rate(fa(xs))} | {rate(miss(xs))} |")

    L += ["", "## 5. Fehlalarme: wo entstehen sie? (Sonnet, Reasoning low, gültige Läufe)", "",
          "| Domäne | Kanal | Fehlalarm |", "|---|---|---|"]
    low = [j for j in son if j["effort"] == "low"]
    by_ch = defaultdict(list)
    for j in fa(low):
        by_ch[(j["domain"], j["channel"])].append(j)
    for (d, c), xs in sorted(by_ch.items(), key=lambda kv: -st.fmean(int(j["verdict"] != j["truth"]) for j in kv[1])):
        L.append(f"| {d} | {c} | {rate(xs)} |")

    L += ["", "## 6. Einzelbeleg gegen Stapel (Sonnet, Reasoning low, Material v2)", "",
          "Achtung: Das Material unterscheidet sich zwischen den Läufen in Details (v2.1–v2.3), deshalb nur grob vergleichbar.", "",
          "| Modus | Fehlalarm | übersehen |", "|---|---|---|"]
    for mode in ("einzeln", "Stapel 8", "Stapel 12"):
        xs = [j for j in low if j["mode"] == mode and j["material"].startswith("v2")]
        L.append(f"| {mode} | {rate(fa(xs))} | {rate(miss(xs))} |")

    L += ["", "## 7. Subtilität der Spur (Sonnet, alle gültigen Läufe)", "", "| subtlety | Fehlalarm | übersehen |", "|---|---|---|"]
    for s in (1, 2, 3):
        xs = [j for j in son if j["subtlety"] == s]
        L.append(f"| {s} | {rate(fa(xs))} | {rate(miss(xs))} |")

    L += ["", "## 8. Position im Stapel (Sonnet, Stapel 12)", "", "| Reasoning | Slot 1–4 | Slot 5–8 | Slot 9–12 |", "|---|---|---|---|"]
    for eff in ("low", "aus"):
        xs = [j for j in son if j["mode"] == "Stapel 12" and j["effort"] == eff]
        L.append(f"| {eff} | " + " | ".join(rate([j for j in xs if lo <= j["slot"] <= hi]) for lo, hi in ((1, 4), (5, 8), (9, 12))) + " |")

    L += ["", "## 9. Konfidenz: Sind die Fehler sicher vorgetragen? (Sonnet, alle gültigen Läufe)", "",
          "| angegebene Konfidenz | Anteil aller Urteile | Fehlerrate |", "|---|---|---|"]
    for lo, hi in ((0, 0.7), (0.7, 0.85), (0.85, 0.95), (0.95, 1.01)):
        xs = [j for j in son if j.get("confidence") is not None and lo <= j["confidence"] < hi]
        L.append(f"| {lo:.2f}–{min(hi, 1):.2f} | {len(xs) / max(total, 1):.2f} | {rate(xs)} |")
    wrong = [j for j in son if j["verdict"] != j["truth"] and j.get("confidence") is not None]
    if wrong:
        L.append("")
        L.append(f"Median-Konfidenz der falschen Urteile: {st.median(j['confidence'] for j in wrong):.2f} · "
                 f"der richtigen: {st.median(j['confidence'] for j in son if j['verdict'] == j['truth'] and j.get('confidence') is not None):.2f}")

    L += ["", "### 9b. Eskalationskurve: Mensch prüft nur Urteile unter einer Konfidenzschwelle", "",
          "Bezug `notizen/14` (Verlässlichkeit pro Mensch-Minute). Annahme: Der Mensch beurteilt eskalierte Belege fehlerfrei.", "",
          "| Schwelle | eskaliert (Anteil Belege) | davon gefangene Fehler | Restfehlerrate ohne Mensch |", "|---|---|---|---|"]
    rated = [j for j in son if j.get("confidence") is not None]
    errs = sum(j["verdict"] != j["truth"] for j in rated)
    for thr in (0.6, 0.7, 0.8, 0.85, 0.9, 0.95):
        esc = [j for j in rated if j["confidence"] < thr]
        caught = sum(j["verdict"] != j["truth"] for j in esc)
        L.append(f"| < {thr:.2f} | {len(esc) / len(rated):.2f} | {caught / max(errs, 1):.2f} | {(errs - caught) / len(rated):.3f} |")

    L += ["", "## 10. Spezifikation: derselbe Fehler mit und ohne Sollwert im Auftrag (`zero_traffic`)", "",
          "| Auftrag | Übersehensrate |", "|---|---|"]
    amb = [j for j in js if j["run"] == "E19-L1-v3-mehrdeutig" and j["fault"] == "zero_traffic"]
    clear = [j for j in son if j["fault"] == "zero_traffic"]
    L += [f"| ohne übliche Last (ungültiger Lauf, Ground Truth mehrdeutig) | {rate(amb)} |",
          f"| mit \"normally handles ~N requests/min\" | {rate(clear)} |"]

    L += ["", "## 11. Haiku gegen Sonnet (gleiches Material, Einzelbeleg, E-017 K3)", "", "| Modell | Fehlalarm | übersehen |", "|---|---|---|"]
    for m, name in ((SONNET, "Sonnet 5.5"), (HAIKU, "Haiku 5.5")):
        xs = [j for j in js if j["run"].startswith("E17-K3") and j["model"] == m]
        L.append(f"| {name} | {rate(fa(xs))} | {rate(miss(xs))} |")
    return "\n".join(L)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    text = report()
    (ROOT / "notizen" / "20-schwierigkeitslandkarte.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
