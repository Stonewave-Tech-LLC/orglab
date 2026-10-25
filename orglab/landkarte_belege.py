"""Schwierigkeitslandkarte, Neuberechnung nach dem Grok-Gutachten (notizen/23 §3–4, §7 Punkt 2). Explorativ.

  python -m orglab.landkarte_belege        # schreibt notizen/20b-landkarte-belegebene.md

Unterschiede zu orglab.landkarte:
1. Einheit ist der Beleg, nicht das Urteil: Raten je Beleg mitteln, Bootstrap über Belege, getrennt je Lauf.
2. Reasoning-Kontrast gepaart über identische Belege (Stapel 12, gleicher Materialstand, L2 gegen L3).
3. Eskalation out-of-sample: Schwelle auf Material v2 gewählt, auf v3 geprüft.
4. Vergleich mit einer beobachtbaren Regel (Domäne × Kanal) bei gleichem Eskalationsanteil. Groks wörtlicher
   Vorschlag "eskaliere Fehlerart X" ist nicht umsetzbar, weil die Fehlerart vor der Prüfung unbekannt ist.
5. Prävalenz: dieselben Kennzahlen bei 5 % statt 50 % kaputter Belege (Umgewichtung).
"""

from __future__ import annotations

import random
import statistics as st
import sys
from collections import defaultdict

from .landkarte import SONNET, load
from .runner import ROOT

B = 2000


def boot_ci(values: list[float], b: int = B, seed: int = 0) -> tuple[float, float]:
    if not values:
        return float("nan"), float("nan")
    rng = random.Random(seed)
    n = len(values)
    means = sorted(st.fmean(rng.choices(values, k=n)) for _ in range(b))
    return means[int(0.025 * b)], means[int(0.975 * b) - 1]


def fmt(values: list[float]) -> str:
    if not values:
        return "–"
    lo, hi = boot_ci(values)
    return f"{st.fmean(values):.3f} [{lo:.3f}; {hi:.3f}] (Belege={len(values)})"


def item_rates(js: list[dict]) -> dict[str, float]:
    by = defaultdict(list)
    for j in js:
        by[j["id"]].append(int(j["verdict"] != j["truth"]))
    return {k: st.fmean(v) for k, v in by.items()}


def report() -> str:
    js = [j for j in load() if j["valid"] and j["model"] == SONNET]
    runs = sorted({j["run"] for j in js})
    L = ["# Schwierigkeitslandkarte auf Belegebene (Neuberechnung nach Grok-Gutachten)", "",
         "> **Korrektur 23.10. (E-021, KORREKTUR_E021):** \"Reasoning aus\" bedeutet hier die Standardeinstellung mit adaptivem, verborgenem Reasoning, \"low\" bedeutet gedrosseltes Reasoning. Aussagen \"Reasoning erhöht Fehlalarme\" sind umzudrehen (H-037).", "",
         "**Stand:** 23.10.2026, nachts · **explorativ** · Skript `python -m orglab.landkarte_belege` · Daten wie `notizen/20`.",
         f"Einheit ist der **Beleg** (Fehlerrate je Beleg über seine Urteile gemittelt), Bootstrap über Belege ({B} Ziehungen), "
         "getrennt je Lauf. Damit sind die Intervalle ehrlicher als in `notizen/20`.", "",
         "## 1. Je Lauf: Fehlalarm und Übersehen auf Belegebene", "",
         "| Lauf | Fehlalarm (ok-Belege) | Übersehen (kaputte Belege) | Urteile je Beleg |", "|---|---|---|---|"]
    for r in runs:
        xs = [j for j in js if j["run"] == r]
        ok = item_rates([j for j in xs if j["truth"]])
        bad = item_rates([j for j in xs if not j["truth"]])
        per = len(xs) / max(len({j["id"] for j in xs}), 1)
        L.append(f"| {r} | {fmt(list(ok.values()))} | {fmt(list(bad.values()))} | {per:.1f} |")

    L += ["", "## 2. Reasoning low gegen aus, gepaart über identische Belege (Stapel 12)", "",
          "Differenz = low − aus je Beleg. Positiv heißt: mit Reasoning mehr Fehler.", "",
          "| Material | Δ Fehlalarm (ok-Belege) | Δ Übersehen (kaputte Belege) |", "|---|---|---|"]
    for mat, (r_low, r_off) in {"v2.3": ("E19-L2-v2", "E19-L3-v2"), "v3.1": ("E19-L2-v3", "E19-L3-v3")}.items():
        low = [j for j in js if j["run"] == r_low]
        off = [j for j in js if j["run"] == r_off]
        out = []
        for truth in (True, False):
            a, b = item_rates([j for j in low if j["truth"] == truth]), item_rates([j for j in off if j["truth"] == truth])
            out.append(fmt([a[k] - b[k] for k in a if k in b]))
        L.append(f"| {mat} | {out[0]} | {out[1]} |")

    # --- Eskalation out-of-sample
    rated = [j for j in js if j.get("confidence") is not None]
    train = [j for j in rated if j["material"].startswith("v2")]
    test = [j for j in rated if j["material"].startswith("v3")]
    errs = lambda xs: sum(j["verdict"] != j["truth"] for j in xs)
    target = 0.25
    thr_candidates = sorted({j["confidence"] for j in train})
    best = None
    for t in thr_candidates:
        esc = [j for j in train if j["confidence"] < t]
        if len(esc) / len(train) <= target:
            best = t
    best = best if best is not None else min(thr_candidates)

    def evaluate(xs: list[dict], esc_rule) -> tuple[float, float, float]:
        esc = [j for j in xs if esc_rule(j)]
        e_all, e_esc = errs(xs), errs(esc)
        return len(esc) / len(xs), e_esc / max(e_all, 1), (e_all - e_esc) / len(xs)

    L += ["", "## 3. Eskalation nach Konfidenz: Schwelle auf v2 gewählt, auf v3 geprüft", "",
          f"Gewählt wurde die höchste Schwelle mit höchstens {target:.0%} Eskalation auf v2: **Konfidenz < {best:.2f}**.", "",
          "| Daten | eskaliert | gefangene Fehler | Restfehlerrate |", "|---|---|---|---|"]
    for name, xs in (("v2 (Training)", train), ("v3 (Test)", test)):
        a, c, r = evaluate(xs, lambda j: j["confidence"] < best)
        L.append(f"| {name} | {a:.2f} | {c:.2f} | {r:.3f} |")
    L += ["", "Getrennt nach Modus und Reasoning (alle Läufe, gleiche Schwelle):", "",
          "| Modus | Reasoning | eskaliert | gefangene Fehler |", "|---|---|---|---|"]
    for mode in ("einzeln", "Stapel 8", "Stapel 12"):
        for eff in ("low", "aus"):
            xs = [j for j in rated if j["mode"] == mode and j["effort"] == eff]
            if xs:
                a, c, _ = evaluate(xs, lambda j: j["confidence"] < best)
                L.append(f"| {mode} | {eff} | {a:.2f} | {c:.2f} |")

    # --- Beobachtbare Regel: Domäne × Kanal, gleiche Eskalationsquote
    cell_err = defaultdict(list)
    for j in train:
        cell_err[(j["domain"], j["channel"])].append(int(j["verdict"] != j["truth"]))
    ranked = sorted(cell_err, key=lambda c: -st.fmean(cell_err[c]))
    L += ["", "## 4. Konfidenz gegen eine beobachtbare Regel bei ähnlichem Eskalationsanteil", "",
          "Die Regel eskaliert ganze Kanäle (Domäne × Kanal), sortiert nach Fehlerrate auf v2. Ein Kanal umfasst etwa 11 % "
          "der Urteile, deshalb werden 1, 2 und 3 Kanäle gezeigt. Reihenfolge der Kanäle: "
          f"{', '.join(f'{d}/{c}' for d, c in ranked[:3])}.", "",
          "| Daten | Regel | eskaliert | gefangene Fehler |", "|---|---|---|---|"]
    for name, xs in (("v2 (Training)", train), ("v3 (Test)", test)):
        a, c, _ = evaluate(xs, lambda j: j["confidence"] < best)
        L.append(f"| {name} | Konfidenz < {best:.2f} | {a:.2f} | {c:.2f} |")
        for k in (1, 2, 3):
            cells = set(ranked[:k])
            a, c, _ = evaluate(xs, lambda j, cells=cells: (j["domain"], j["channel"]) in cells)
            L.append(f"| {name} | Kanal-Regel ({k} Kanäle) | {a:.2f} | {c:.2f} |")

    # --- Prävalenz 5 %
    def weighted(xs: list[dict], prev: float, rule_fn) -> tuple[float, float, float]:
        w = lambda j: (prev / 0.5) if not j["truth"] else ((1 - prev) / 0.5)
        tot = sum(w(j) for j in xs)
        esc = sum(w(j) for j in xs if rule_fn(j))
        e_all = sum(w(j) for j in xs if j["verdict"] != j["truth"])
        e_esc = sum(w(j) for j in xs if j["verdict"] != j["truth"] and rule_fn(j))
        alarms = [j for j in xs if j["verdict"] is False]
        true_alarms = sum(w(j) for j in alarms if not j["truth"])
        ppv = true_alarms / max(sum(w(j) for j in alarms), 1e-9)
        return esc / tot, e_esc / max(e_all, 1e-9), ppv

    L += ["", "## 5. Prävalenz: dieselben Läufe bei 50 % gegen 5 % kaputter Belege (Umgewichtung)", "",
          "PPV = Anteil echter Fehler unter den 'kaputt'-Urteilen des Prüfers. **Achtung (Grok-Gutachten 2):** Die Spalte 'gefangene Fehler' ist der Anteil *aller* Fehler (Übersehen und Fehlalarm), den die Eskalation erfasst. Er verschiebt sich mit der Zusammensetzung und ist **keine** Sensitivität. Maßgeblich für die Praxis ist die PPV.", "",
          "| Modus/Reasoning | Prävalenz | eskaliert | gefangene Fehler | PPV der Alarme |", "|---|---|---|---|---|"]
    for mode, eff in (("einzeln", "low"), ("Stapel 12", "low"), ("Stapel 12", "aus")):
        xs = [j for j in rated if j["mode"] == mode and j["effort"] == eff]
        for prev in (0.5, 0.05):
            a, c, ppv = weighted(xs, prev, lambda j: j["confidence"] < best)
            L.append(f"| {mode} / {eff} | {prev:.0%} | {a:.2f} | {c:.2f} | {ppv:.2f} |")
    return "\n".join(L)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    text = report()
    (ROOT / "notizen" / "20b-landkarte-belegebene.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
