"""Naive Baseline ohne LLM (Grok-Gutachten §6/§7): Wie viel der "Prüfleistung" ist Stringvergleich?

  python -m orglab.baseline_naiv          # schreibt notizen/27-naive-baseline.md

Material: Generator v3.1, Kalibrierungsseeds 1200–1211, jeder Beleg in jedem Kanal einzeln, also dieselben Einheiten
wie E-019 L1/L2/L3 v3 (Sonnet). Die Regeln sind festgelegt, bevor ihr Ergebnis berechnet wurde.

Ehrliche Einordnung: Der Autor der Regeln kennt die Sprache des Generators. B2 ist deshalb eine *informierte*
Heuristik und eher eine Obergrenze dessen, was einfacher Textabgleich schafft, als ein fairer Gegner.
"""

from __future__ import annotations

import json
import re
import statistics as st
import sys
from collections import defaultdict

from .evidence import CHANNELS, generate_set_v2
from .runner import ROOT

SEEDS = range(1200, 1212)
SONNET_RUNS = {"L1 (Stapel 8, low)": "judgments-kalibrierung-L1-v3.jsonl", "L2 (Stapel 12, low)": "judgments-kalibrierung-L2-v3.jsonl",
               "L3 (Stapel 12, aus)": "judgments-kalibrierung-L3-v3.jsonl"}

# B1: Widerspruch zum Auftrag. Ein Kennzeichen derselben Art kommt im Kanal vor, aber mit anderem Wert.
ID_PATTERNS = {
    "version": r"\bv?(\d+\.\d+\.\d+)\b",
    "commit": r"\b([0-9a-f]{7})\b",
    "email": r"([a-z0-9.\-]+@[a-z0-9.\-]+\.[a-z]{2,})",
    "betrag": r"(€ ?[\d,]+\.\d{2})",
}
# B2: generische Warnwörter (aus Betriebs-Alltag; teilweise Generator-Sprache, siehe Moduldoc)
RED = re.compile(r"\b(error|fail(ed|ure)?|refused|bounced|deferred|expired|pending|mismatch|unreachable|degraded|timed? ?out|"
                 r"denied|exception|nan|syn-sent)\b|✗|\b0/\d+\b|\b0 kB\b|\(0 pages\)|: 0$|dropped 0 ", re.I | re.M)


def b1(item: str, text: str) -> bool:
    """True = 'funktioniert' (kein Widerspruch gefunden)."""
    for pat in ID_PATTERNS.values():
        want = set(re.findall(pat, item, re.I))
        if not want:
            continue
        seen = set(re.findall(pat, text, re.I))
        if seen and not (seen & want):
            return False
        if pat == ID_PATTERNS["email"] and seen - want:
            return False
    return True


def b2(item: str, text: str) -> bool:
    return not RED.search(text)


def b3(item: str, text: str) -> bool:
    return b1(item, text) and b2(item, text)


def report() -> str:
    evs = generate_set_v2(SEEDS)
    rows = []
    for e in evs:
        for ch in CHANNELS[e.domain]:
            rows.append({"id": e.id, "truth": e.works, "fault": e.fault, "domain": e.domain, "channel": ch,
                         "B1": b1(e.item, e.channels[ch]), "B2": b2(e.item, e.channels[ch]), "B3": b3(e.item, e.channels[ch])})
    err = lambda xs, k: st.fmean(int(x[k] != x["truth"]) for x in xs) if xs else float("nan")
    oks, fails = [r for r in rows if r["truth"]], [r for r in rows if not r["truth"]]
    L = ["# Naive Baseline ohne LLM: Wie viel ist Stringvergleich?", "",
         "**Stand:** 23.10.2026, nachts · explorativ · Skript `python -m orglab.baseline_naiv` · Anlass: Grok-Gutachten §6 und §7.",
         "Material: Generator v3.1, Seeds 1200–1211 (144 Belege × 3 Kanäle = 432 Einzelurteile), dieselben Einheiten wie die Sonnet-Kalibrierung E-019 v3.", "",
         "**Regeln** (vor der Berechnung festgelegt):",
         "- **B1 Widerspruch:** Kommt im Kanal ein Kennzeichen derselben Art wie im Auftrag vor (Version, 7-stelliger Hash, "
         "E-Mail, €-Betrag), aber keines mit dem Wert aus dem Auftrag, gilt der Beleg als kaputt.",
         "- **B2 Warnwörter:** error, fail, refused, bounced, deferred, expired, pending, mismatch, unreachable, degraded, "
         "timeout, NaN, SYN-SENT, ✗, `0/N`, `0 kB`, `(0 pages)`, `dropped 0`. Diese Liste ist **informiert**: Ich kenne die Sprache des Generators.",
         "- **B3** = B1 oder B2.", "",
         "## Gesamt", "", "| Prüfer | Fehlalarm | übersehen | Fehlerrate |", "|---|---|---|---|"]
    for k in ("B1", "B2", "B3"):
        L.append(f"| {k} | {err(oks, k):.3f} | {err(fails, k):.3f} | {err(rows, k):.3f} |")
    son = {}
    for name, f in SONNET_RUNS.items():
        p = ROOT / "daten" / "E-019-stapel-panel" / f
        if p.exists():
            js = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines()]
            js = [j for j in js if j["verdict"] is not None]
            son[name] = js
            L.append(f"| Sonnet {name} | {st.fmean(int(j['verdict'] != j['truth']) for j in js if j['truth']):.3f} | "
                     f"{st.fmean(int(j['verdict'] != j['truth']) for j in js if not j['truth']):.3f} | "
                     f"{st.fmean(int(j['verdict'] != j['truth']) for j in js):.3f} |")
    L += ["", "## Übersehen je Fehlerart", "", "| Fehlerart | B1 | B2 | B3 | Sonnet L2 |", "|---|---|---|---|---|"]
    son_l2 = son.get("L2 (Stapel 12, low)", [])
    for f in sorted({r["fault"] for r in fails}):
        xs = [r for r in fails if r["fault"] == f]
        sj = [j for j in son_l2 if j["fault"] == f]
        s = f"{st.fmean(int(j['verdict'] != j['truth']) for j in sj):.2f}" if sj else "–"
        L.append(f"| `{f}` | {err(xs, 'B1'):.2f} | {err(xs, 'B2'):.2f} | {err(xs, 'B3'):.2f} | {s} |")
    L += ["", "## Fehlalarm je Domäne und Kanal (B3)", "", "| Domäne/Kanal | B3 Fehlalarm |", "|---|---|"]
    by = defaultdict(list)
    for r in oks:
        by[(r["domain"], r["channel"])].append(r)
    for (d, c), xs in sorted(by.items()):
        L.append(f"| {d}/{c} | {err(xs, 'B3'):.2f} |")
    return "\n".join(L)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    text = report()
    (ROOT / "notizen" / "27-naive-baseline.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
