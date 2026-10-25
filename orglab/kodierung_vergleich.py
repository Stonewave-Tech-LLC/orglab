"""Vergleich der drei Kodierungen der Wave-Fälle (D-019): Übereinstimmung je Feld, Cohens κ paarweise, strittige Zellen.

  python -m orglab.kodierung_vergleich             # schreibt notizen/28-wave-faelle/05-vergleich.md und daten/wave-kodierung/vergleich.json
  python -m orglab.kodierung_vergleich ergebnis    # Endstand K0/K2/K5 mit Neos Schlichtung → 06-endstand.md

Quellen: Claude `01-kodierung-claude.md` (Tabelle), GPT `daten/wave-kodierung/gpt-roh.json`, Ace `daten/wave-kodierung/ace-roh.json`.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from itertools import combinations

from .kodierung_fremd import FIELDS, FOLDER, RAW, parse

CASES = [str(n) for n in range(1, 15)]


def claude() -> dict[str, dict[str, dict[str, str]]]:
    out: dict[str, dict[str, dict[str, str]]] = {}
    for line in (FOLDER / "01-kodierung-claude.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\| (\d+) [^|]*\|(.*)\|\s*$", line)
        if m:
            vals = [v.strip() for v in m.group(2).split("|")]
            out[m.group(1)] = {k: {"v": v, "b": ""} for k, v in zip(FIELDS, vals)}
    return out


def from_raw(name: str) -> dict:
    d = json.loads((RAW / f"{name}-roh.json").read_text(encoding="utf-8"))
    return parse(d["raw"])


def kappa(a: list[str], b: list[str]) -> float | None:
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n ** 2
    return None if pe == 1 else (po - pe) / (1 - pe)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    raters = {"Claude": claude(), "GPT": from_raw("gpt"), "Ace": from_raw("ace")}
    val = lambda r, n, k: ((raters[r].get(n) or {}).get(k) or {}).get("v", "–")
    L = ["# Wave-Fälle: Vergleich der drei Kodierungen (D-019)", "",
         "Claude und Ace sind vermutlich dieselbe Modellfamilie und kannten die Hypothese. Die Paare mit GPT zählen mehr.", "",
         "## Übereinstimmung je Feld", "",
         "| Feld | alle drei gleich | Claude–GPT | Claude–Ace | GPT–Ace |", "|---|---|---|---|---|"]
    disputed = []
    for k in FIELDS:
        same = sum(len({val(r, n, k) for r in raters}) == 1 for n in CASES)
        cells = []
        for a, b in combinations(raters, 2):
            xa, xb = [val(a, n, k) for n in CASES], [val(b, n, k) for n in CASES]
            po = sum(x == y for x, y in zip(xa, xb)) / len(CASES)
            kp = kappa(xa, xb)
            cells.append(f"{po:.0%} (κ {kp:.2f})" if kp is not None else f"{po:.0%} (κ –)")
        L.append(f"| {k} | {same}/14 | " + " | ".join(cells) + " |")
        disputed += [(n, k) for n in CASES if len({val(r, n, k) for r in raters}) > 1]
    L += ["", f"## Strittige Zellen ({len(disputed)} von {14 * len(FIELDS)})", "",
          "| Fall | Feld | Claude | GPT | Ace |", "|---|---|---|---|---|"]
    L += [f"| {n} | {k} | {val('Claude', n, k)} | {val('GPT', n, k)} | {val('Ace', n, k)} |" for n, k in disputed]
    (FOLDER / "05-vergleich.md").write_text("\n".join(L), encoding="utf-8")
    (RAW / "vergleich.json").write_text(json.dumps(raters, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n".join(L[:16]))
    print(f"\nStrittig: {len(disputed)} Zellen")


def ergebnis() -> str:
    """Endstand K0/K2/K5: Konsens der drei Kodierer, sonst Neos Schlichtung (`daten/wave-kodierung/neo-schlichtung.json`)."""
    raters = json.loads((RAW / "vergleich.json").read_text(encoding="utf-8"))
    neo = json.loads((RAW / "neo-schlichtung.json").read_text(encoding="utf-8"))["decisions"]
    final, source = {}, {}
    for n in CASES:
        for k in ("K0", "K2", "K5"):
            vs = {((raters[r].get(n) or {}).get(k) or {}).get("v") for r in raters}
            final[n, k], source[n, k] = (vs.pop(), "Konsens") if len(vs) == 1 else (neo.get(f"{n}|{k}", "offen"), "Neo")
    L = ["# Wave-Fälle: Endstand K0, K2, K5 (D-019)", "",
         "**Status: Hinweis.** n = 14, von Ace aus dem Gedächtnis ausgewählt (Auswahlverzerrung). Neo hat 15 strittige Zellen "
         "geschlichtet und seine Entscheidungen selbst als **nicht sicher** eingestuft. Claude und Ace sind vermutlich dieselbe "
         "Modellfamilie.", "",
         "| Fall | K0 Art | K2 Beleg | K5 grün/Zahl widerspricht |", "|---|---|---|---|"]
    for n in CASES:
        L.append(f"| {n} | " + " | ".join(final[n, k] + (" *(Neo)*" if source[n, k] == "Neo" else "") for k in ("K0", "K2", "K5")) + " |")
    by = Counter(final[n, "K0"] for n in CASES)
    L += ["", "## Auszählung (deskriptiv)", "", "Art: " + ", ".join(f"{v} {c}" for v, c in by.most_common()), ""]
    for art in ("übersehen", "fehlalarm"):
        ns = [n for n in CASES if final[n, "K0"] == art]
        k2, k5 = Counter(final[n, "K2"] for n in ns), Counter(final[n, "K5"] for n in ns)
        L.append(f"- **{art}** ({len(ns)} Fälle): Beleg " + ", ".join(f"{v} {c}" for v, c in k2.most_common())
                 + " · grün/Zahl widerspricht " + ", ".join(f"{v} {c}" for v, c in k5.most_common()))
    text = "\n".join(L)
    (FOLDER / "06-endstand.md").write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    if sys.argv[1:] == ["ergebnis"]:
        sys.stdout.reconfigure(encoding="utf-8")
        print(ergebnis())
    else:
        main()
