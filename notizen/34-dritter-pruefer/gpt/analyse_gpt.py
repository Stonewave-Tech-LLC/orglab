#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ANALYSEPLAN – vor dem Einlesen der Ergebnisdaten
# ============================================================
# Dieser Kommentar ersetzt analyseplan.md: Der Auftrag verbietet Dateiausgaben.
# Der Plan ist keine historische Präregistrierung. Alle Tabellen, auch Null-
# ergebnisse, werden ausgegeben; automatische Auffälligkeitsprüfungen heißen
# ausdrücklich "Diagnostik", nicht bestätigte Entdeckungen.
#
# 1. Daten prüfen; Seeds 6000 und 7000 als verschiedene Belege behandeln.
#    Primär zählt ein ungültiges Urteil als Misserfolg. Zusätzlich vollständige
#    gültige Paare/Blöcke analysieren. Keine stillschweigende Deduplizierung der
#    Prüferurteile. GPT-Wiederholungen nach einer ergebnisblinden Regel behandeln.
#
# 2. Je Datensatz, Modell und Zelle: Urteile, Fehler nach Wahrheit, Konfidenz,
#    Kalibrierung, Nachschlagen, richtige Runbook-Sektion, Kanalabfragen, Aufwand.
#    Modelle auf denselben Belegen/Zellen paaren. Unterschiede in Werkzeugnutzung
#    sind beobachtetes Verhalten, keine nachgewiesenen kausalen Mediatoren.
#
# 3. Vollständige faktorielle Kontraste für SP, ZU, AU einschließlich aller
#    Wechselwirkungen: Prozentpunkte UND marginale Logit-Kontraste. Für Haupt-
#    effekte wird über die jeweils anderen Faktoren gemittelt. Für Interaktionen
#    werden Differenzen von Differenzen bzw. die dreifache Differenz berechnet.
#    Schichten: Wahrheit, Domäne, kind, fault, primary, subtlety; ferner vor
#    Ergebnisbetrachtung definierte Längenschichten. Verhaltenskontraste insgesamt.
#    Ein SP-Schaden besonders bei primary-Fehlern, verbunden mit fehlendem
#    Nachschlagen, wäre mit Sollwertbeschaffung als Engpass vereinbar.
#    Ein ZU-Nutzen mit mehreren abgefragten Kanälen wäre mit Evidenzbeschaffung
#    vereinbar. AU-bedingtes häufigeres "works", insbesondere bei kaputten
#    Belegen, wäre mit Zustimmung/Ankern vereinbar; zusätzliche Promptlänge ist
#    damit aber nicht experimentell getrennt.
#
# 4. Empirische Schwierigkeit pro Beleg = Fehlerrate über den balancierten
#    Acht-Zellen-Plan; keine präzise Rasch-Kalibrierung mit nur zwei Modellen.
#    Pro Beleg keine scheinbaren Bootstrap-CIs aus seinen acht Bedingungen.
#    Ähnlichkeit der Schwierigkeiten: Pearson/Spearman über vollständige Belege
#    und über Belegtypen, mit Beleg-Bootstrap.
#
#    NICHT Schwierigkeit eines 6000-Belegs auf einen vermeintlich identischen
#    7000-Beleg übertragen! Unabhängige Schwierigkeit wird nur auf Typebene
#    übertragen: (domain, kind, fault, primary, subtlety), ohne Seed/ID.
#    Je Richtung 6000->7000 und 7000->6000 sowie je Modell wird die Erfolgs-
#    wahrscheinlichkeit eines Typs ausschließlich im Quelldatensatz geschätzt.
#    Nicht übertragbare Typen werden ausgewiesen, nicht imputiert.
#    Dies prüft Typ-Schwierigkeit, nicht unabhängige individuelle Schwierigkeit.
#
#    Zusätzlich ein kleines bedingtes logistisches Modell für diskordante
#    Urteilspaare eines Faktors: log odds(Verbesserung statt Verschlechterung)
#    ~ externe Erfolgs-Logits + externe Grenznähe 4*p*(1-p) + Kontext.
#    Ein zweites Modell kontrolliert Domäne, kind und primary. Bootstrap zieht
#    Quell- und Zielbelege unabhängig und schätzt die Schwierigkeit erneut.
#    Ein Logit-Interaktionsterm ungleich null wäre stärkere Evidenz für
#    Effektmodifikation als ein bloßes Prozentpunktmuster. Verschwinden solche
#    Terme bei Kontrolle des Typs, spricht das für Aufgabenkomposition.
#    Das ist ein regularisiertes matched-pair-Modell, kein voll identifiziertes
#    gemischtes IRT-Modell und kein Nachweis eines individuellen Grenzmechanismus.
#    Innerhalb eines exakten Typs ist externe Typ-Schwierigkeit konstant.
#
# 5. Fehlerübereinstimmung: vollständige gepaarte 2x2-Tabellen, Cohen-kappa,
#    Phi, gemeinsame Fehler relativ zur Unabhängigkeit, Orakel-Obergrenze.
#    Bootstrap immer über Belege, alle Zellen/Modelle eines Belegs gemeinsam.
#    Auswertung insgesamt und geschichtet; gültige Urteile als Sensitivität.
#    Zusätzlich Residualkorrelation nach unabhängig geschätztem Typ×Zell-Risiko.
#    Positive kappa/exzessive Doppelfehler stützen gemeinsame Fehlermengen.
#    Residualkorrelation kann weiterhin ungemessene individuelle Schwierigkeit
#    enthalten; sie beweist keine direkte Abhängigkeit der Modelle.
#
# 6. GPT-Einzelkanal: Entscheidbarkeit ist ein externes Modellurteil, kein Gold.
#    GPT selbst gegen truth prüfen. ZU=0 nach decidable, SP und AU aufschlüsseln;
#    SP=0 ist wegen GPTs vollständigem Sollwertauftrag der passendere Vergleich.
#    Effekte von SP, ZU, AU innerhalb der GPT-Gruppen und deren Differenzen
#    ausgeben. ZU-Nutzen besonders bei "nicht entscheidbar" wäre mit einem
#    Einzelkanal-Engpass vereinbar; GPT-Fehler/Typkomposition sind Alternativen.
#
# 7. Gegenproben: unabhängiger zweiter Datensatz, gültige Urteile, Fehlerrichtung,
#    Aufgabenart, Längen, Runbook-Rücklauf, Kanalabdeckung, Aufwand und technische
#    Auffälligkeiten. Werkzeugzahl >=6 ist KEIN Nachweis von sechs Werkzeugrunden;
#    hohe Tokenzahl ist nur ein Budgetproxy. Modell und Laufzeit sind bei 6000
#    teilweise vermengt; 7000 mildert, beseitigt aber nicht alle Driftprobleme.
#
# Inferenz: deterministischer Perzentil-Bootstrap über Belege, nicht Zeilen.
# Keine p-Wert-Auswahl, keine Unterdrückung von Nullbefunden. CIs sind punktweise,
# nicht multiplikationskorrigiert; die zahlreichen Untergruppen sind explorativ.
# Ein Beleg-Bootstrap misst Variation zwischen Belegen, nicht die unbekannte
# Wiederholungsschwankung eines einzelnen LLM-Laufs. Kleine Gruppen und perfekte
# Trefferquoten können degenerierte Bootstrapintervalle liefern.
# Logits erhalten eine explizite 0.5-Korrektur; Prozentpunkte bleiben unkorrigiert.
#
# Aufruf: python3 analyse.py /pfad/zu/daten
# Nur Standardbibliothek; keine Dateien schreiben, keine Netzwerkzugriffe.

import sys
sys.dont_write_bytecode = True

import collections
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import statistics


B = 499
B_REG = 199
MASTER_SEED = 20261023
FACTORS = ("SP", "ZU", "AU")
CELLS = tuple(itertools.product((0, 1), repeat=3))
ACTIVE_SETS = tuple(
    a for k in (1, 2, 3) for a in itertools.combinations(range(3), k)
)
TYPE_FIELDS = ("domain", "kind", "fault", "primary", "subtlety")
BATCHES = ("6000", "7000")
MISSING = "<fehlend>"


def fatal(message):
    raise ValueError(message)


def is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def num(x):
    return float(x) if is_number(x) else None


def boolean_number(x):
    return float(x) if isinstance(x, bool) else None


def fmt(x):
    if x is None:
        return "NA"
    if isinstance(x, bool):
        return "true" if x else "false"
    if isinstance(x, int):
        return str(x)
    if isinstance(x, float):
        return "NA" if not math.isfinite(x) else "%.6g" % x
    return str(x).replace("\t", " ").replace("\r", " ").replace("\n", " ")


def table(title, headers, rows):
    print("\n### " + title)
    print("\t".join(map(fmt, headers)))
    for row in rows:
        print("\t".join(map(fmt, row)))


def mean(values):
    values = [x for x in values if x is not None]
    return math.fsum(values) / len(values) if values else None


def pct(a, b):
    return 100.0 * a / b if b else None


def ratio(a, b):
    return a / b if b else None


def logit_corrected(successes, trials):
    if trials <= 0:
        return None
    return math.log((successes + 0.5) / (trials - successes + 0.5))


def sigmoid(x):
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-min(x, 700.0)))
    e = math.exp(max(x, -700.0))
    return e / (1.0 + e)


def quantile(values, q):
    values = sorted(x for x in values if x is not None and math.isfinite(x))
    if not values:
        return None
    p = (len(values) - 1) * q
    lo = int(p)
    hi = min(lo + 1, len(values) - 1)
    return values[lo] + (values[hi] - values[lo]) * (p - lo)


def interval(values):
    good = [x for x in values if x is not None and math.isfinite(x)]
    return quantile(good, 0.025), quantile(good, 0.975), len(good)


def rng_for(tag):
    digest = hashlib.sha256((str(MASTER_SEED) + "|" + str(tag)).encode("utf-8")).digest()
    return random.Random(int.from_bytes(digest[:16], "big"))


def sums(vectors):
    if not vectors:
        return ()
    out = [0.0] * len(vectors[0])
    for v in vectors:
        for j, value in enumerate(v):
            out[j] += value
    return tuple(out)


def compressed_sampler(vectors):
    counts = collections.Counter(tuple(v) for v in vectors)
    values = list(counts)
    weights = [counts[v] for v in values]
    return values, weights, len(vectors)


def draw_sum(sampler, rng):
    values, weights, n = sampler
    counts = collections.Counter(rng.choices(range(len(values)), weights=weights, k=n))
    out = [0.0] * len(values[0])
    for i, count in counts.items():
        v = values[i]
        for j, value in enumerate(v):
            out[j] += count * value
    return tuple(out)


def bootstrap(vectors, function, tag, repetitions=B):
    """Eine Vektorzeile pro Beleg. Ganze Vektoren gemeinsam resampeln."""
    vectors = list(vectors)
    if not vectors:
        return (), (), (), (), ()
    point = tuple(function(sums(vectors)))
    draws = [[] for _ in point]
    sampler = compressed_sampler(vectors)
    rng = rng_for(tag)
    for _ in range(repetitions):
        estimate = function(draw_sum(sampler, rng))
        for j, value in enumerate(estimate):
            draws[j].append(value)
    cis = [interval(x) for x in draws]
    return (
        point,
        tuple(x[0] for x in cis),
        tuple(x[1] for x in cis),
        tuple(x[2] for x in cis),
        tuple(draws),
    )


def ci_columns(result, index):
    if not result[0]:
        return (None, None, None, 0)
    return (
        result[0][index], result[1][index],
        result[2][index], result[3][index],
    )


def pearson_from_sums(n, sx, sy, sxx, syy, sxy):
    if n <= 1:
        return None
    vx = sxx - sx * sx / n
    vy = syy - sy * sy / n
    if vx <= 1e-12 or vy <= 1e-12:
        return None
    return max(-1.0, min(1.0, (sxy - sx * sy / n) / math.sqrt(vx * vy)))


def pearson(xs, ys):
    n = len(xs)
    return pearson_from_sums(
        n, math.fsum(xs), math.fsum(ys),
        math.fsum(x*x for x in xs), math.fsum(y*y for y in ys),
        math.fsum(x*y for x, y in zip(xs, ys)),
    )


def ranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    result = [0.0] * len(values)
    k = 0
    while k < len(order):
        end = k + 1
        while end < len(order) and values[order[end]] == values[order[k]]:
            end += 1
        rank = (k + end - 1) / 2.0 + 1.0
        for j in range(k, end):
            result[order[j]] = rank
        k = end
    return result


def correlation_bootstrap(pairs, tag):
    if not pairs:
        return (None,) * 8
    def calc(sample):
        xs = [x for x, _ in sample]
        ys = [y for _, y in sample]
        return pearson(xs, ys), pearson(ranks(xs), ranks(ys))
    point = calc(pairs)
    rng = rng_for(tag)
    draws = [[], []]
    for _ in range(B):
        sample = [pairs[rng.randrange(len(pairs))] for _ in pairs]
        for j, value in enumerate(calc(sample)):
            draws[j].append(value)
    a, b = interval(draws[0]), interval(draws[1])
    return (point[0], a[0], a[1], a[2], point[1], b[0], b[1], b[2])


def read_jsonl(path):
    result = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except Exception as exc:
                fatal("%s:%d: ungültiges JSON: %s" % (path.name, line_number, exc))
            if not isinstance(value, dict):
                fatal("%s:%d: JSON-Objekt erwartet" % (path.name, line_number))
            value["_source"] = path.name
            value["_line"] = line_number
            result.append(value)
    return result


def type_key(row):
    return tuple(fmt(row.get(field, MISSING)) for field in TYPE_FIELDS)


def type_label(key):
    return "|".join("%s=%s" % x for x in zip(TYPE_FIELDS, key))


def cell_label(cell):
    return "-".join("%s%d" % (f, v) for f, v in zip(FACTORS, cell))


def active_label(active):
    return ":".join(FACTORS[i] for i in active)


def item_maps(rows):
    result = collections.defaultdict(dict)
    for row in rows:
        result[row["id"]][row["_cell"]] = row
    return dict(result)


def row_metric(row, metric):
    if metric == "acc":
        return row["_acc"]
    if metric == "acc_valid":
        return row["_acc"] if row["_valid"] else None
    if metric == "invalid":
        return float(not row["_valid"])
    if metric == "yes":
        return float(row["verdict"] is True)
    if metric in ("looked_up", "page_returned", "right_section"):
        return boolean_number(row.get(metric))
    if metric == "confidence":
        return row["_confidence"] if row["_valid"] else None
    if metric == "high_conf_error":
        c = row["_confidence"]
        return float(c >= 0.9 and not row["_acc"]) if row["_valid"] and c is not None else None
    if metric == "no_check":
        c = num(row.get("n_checks"))
        return float(c == 0) if c is not None else None
    if metric == "all_three":
        c = num(row.get("distinct_checks"))
        return float(c == 3) if c is not None else None
    return num(row.get(metric))


BINARY_METRICS = {
    "acc", "acc_valid", "invalid", "yes", "looked_up", "page_returned",
    "right_section", "high_conf_error", "no_check", "all_three",
}
BEHAVIOR_METRICS = (
    "invalid", "yes", "looked_up", "page_returned", "right_section",
    "n_checks", "distinct_checks", "no_check", "all_three", "confidence",
    "n_tool_calls", "completion_tokens", "cost_usd",
)


def contrast_vectors(items, active, metric="acc"):
    """Nur vollständige aktive Blöcke; die übrigen Faktoren sind gepaart."""
    inactive = tuple(i for i in range(3) if i not in active)
    patterns = tuple(itertools.product((0, 1), repeat=len(active)))
    result = {}
    for item_id, cells in items.items():
        values = [0.0] * len(patterns)
        blocks = 0
        for context in itertools.product((0, 1), repeat=len(inactive)):
            block = []
            for pattern in patterns:
                cell = [0, 0, 0]
                for i, value in zip(inactive, context):
                    cell[i] = value
                for i, value in zip(active, pattern):
                    cell[i] = value
                row = cells.get(tuple(cell))
                block.append(row_metric(row, metric) if row is not None else None)
            if any(value is None for value in block):
                continue
            blocks += 1
            for j, value in enumerate(block):
                values[j] += value
        if blocks:
            result[item_id] = (float(blocks),) + tuple(values)
    return result


def contrast_function(active, binary=True):
    patterns = tuple(itertools.product((0, 1), repeat=len(active)))
    signs = tuple((-1.0) ** (len(active) - sum(p)) for p in patterns)
    def calculate(total):
        n = total[0]
        if n <= 0:
            return (None, None) if binary else (None,)
        effect = math.fsum(sign * value / n for sign, value in zip(signs, total[1:]))
        if not binary:
            return (effect,)
        logits = math.fsum(
            sign * logit_corrected(value, n)
            for sign, value in zip(signs, total[1:])
        )
        return 100.0 * effect, logits
    return calculate


def contrast_report(items, active, tag, metric="acc"):
    units = contrast_vectors(items, active, metric)
    binary = metric in BINARY_METRICS
    result = bootstrap(
        units.values(), contrast_function(active, binary), tag
    )
    blocks = int(sum(v[0] for v in units.values()))
    return units, result, blocks


def summary(rowset):
    n = len(rowset)
    valid = [r for r in rowset if r["_valid"]]
    intact = [r for r in rowset if r["truth"]]
    broken = [r for r in rowset if not r["truth"]]
    looked = [r for r in rowset if r.get("looked_up") is True]
    pages = [r for r in rowset if r.get("page_returned") is True]
    confrows = [r for r in valid if r["_confidence"] is not None]
    high = [r for r in confrows if r["_confidence"] >= 0.9]
    correct = sum(r["_acc"] for r in rowset)
    fp = sum(r["verdict"] is True for r in broken)
    fn = sum(r["verdict"] is False for r in intact)
    return (
        len({r["id"] for r in rowset}), n, len(valid), int(correct),
        pct(correct, n), pct(correct, len(valid)),
        n - len(valid), pct(n - len(valid), n),
        len(broken), fp, pct(fp, len(broken)),
        len(intact), fn, pct(fn, len(intact)),
        pct(sum(r["verdict"] is True for r in rowset), n),
        pct(sum(r.get("looked_up") is True for r in rowset), n),
        pct(sum(r.get("page_returned") is True for r in looked), len(looked)),
        pct(sum(r.get("right_section") is True for r in pages), len(pages)),
        pct(sum(r.get("right_section") is True for r in rowset), n),
        mean([num(r.get("n_checks")) for r in rowset]),
        mean([num(r.get("distinct_checks")) for r in rowset]),
        mean([r["_confidence"] for r in confrows]),
        len(confrows),
        mean([(r["_confidence"] - r["_acc"])**2 for r in confrows]),
        len(high), pct(sum(not r["_acc"] for r in high), len(high)),
        mean([num(r.get("n_tool_calls")) for r in rowset]),
        mean([num(r.get("completion_tokens")) for r in rowset]),
        mean([num(r.get("cost_usd")) for r in rowset]),
        math.fsum(num(r.get("cost_usd")) or 0 for r in rowset),
    )


SUMMARY_HEADERS = (
    "n_Belege", "n_Zeilen", "n_gueltig", "n_korrekt",
    "korrekt_pct_alle", "korrekt_pct_gueltige",
    "n_ungueltig", "ungueltig_pct",
    "n_kaputt", "n_falsch_works", "falsch_works_pct_kaputt",
    "n_intakt", "n_falsch_kaputt", "falsch_kaputt_pct_intakt",
    "works_pct_alle", "lookup_pct_alle",
    "page_pct_lookup", "right_pct_page", "right_pct_alle",
    "checks_M", "verschiedene_checks_M",
    "Konfidenz_M", "n_Konfidenz", "Brier_Konfidenz",
    "n_Konf_ge_0.9", "Fehler_pct_Konf_ge_0.9",
    "tool_calls_M", "tokens_M", "USD_M", "USD_Summe",
)


def calibration(rows, prefix):
    output = []
    for j in range(10):
        selected = [
            r for r in rows
            if r["_valid"] and r["_confidence"] is not None
            and min(9, int(r["_confidence"] * 10)) == j
        ]
        confidence = mean([r["_confidence"] for r in selected])
        accuracy = mean([r["_acc"] for r in selected])
        output.append(prefix + (
            "%.1f-%.1f%s" % (j/10, (j+1)/10, "]" if j == 9 else ")"),
            len(selected), confidence, accuracy,
            confidence - accuracy if selected else None,
        ))
    usable = [r for r in rows if r["_valid"] and r["_confidence"] is not None]
    ece = 0.0
    for row in output:
        n, c, a = row[-4], row[-3], row[-2]
        if n:
            ece += n * abs(c - a)
    output.append(prefix + ("ECE_10_Bins", len(usable), None, None,
                            ece / len(usable) if usable else None))
    return output


def strata_for(items, references):
    result = [("gesamt", items)]
    for field in ("truth",) + TYPE_FIELDS:
        groups = collections.defaultdict(dict)
        for item_id, cells in items.items():
            row = next(iter(cells.values()))
            groups[fmt(row.get(field, MISSING))][item_id] = cells
        for value in sorted(groups):
            result.append(("%s=%s" % (field, value), groups[value]))
    # Längen hängen nur an den Belegen, nicht an beobachteten Urteilen.
    for label, field in (("Auftrag_kurz_Laenge", "_short_len"),
                         ("Sollwert_Zusatzlaenge", "_norm_len")):
        values = [references[i][field] for i in items if i in references]
        if not values:
            continue
        median = statistics.median(values)
        for low in (True, False):
            group = {
                i: c for i, c in items.items()
                if i in references and
                ((references[i][field] <= median) if low else
                 (references[i][field] > median))
            }
            result.append(("%s%s%s" % (label, "<=" if low else ">", fmt(median)), group))
    return result


def complete_score(cells):
    if set(cells) != set(CELLS):
        return None
    return sum(cells[c]["_acc"] for c in CELLS), 8


def train_type_scores(items, weights=None):
    scores = collections.defaultdict(lambda: [0.0, 0.0, 0.0])
    for j, (item_id, cells) in enumerate(items.items()):
        score = complete_score(cells)
        if score is None:
            continue
        w = weights[j] if weights is not None else 1
        if not w:
            continue
        key = type_key(next(iter(cells.values())))
        scores[key][0] += w * score[0]
        scores[key][1] += w * score[1]
        scores[key][2] += w
    return {
        key: (s, n, count, (s + 0.5) / (n + 1.0))
        for key, (s, n, count) in scores.items()
    }


def overlap_vector(cells_a, cells_b, valid_only=False):
    # Reihenfolge: beide korrekt, nur A falsch, nur B falsch, beide falsch.
    counts = [0.0] * 4
    for cell in sorted(set(cells_a) & set(cells_b)):
        a, b = cells_a[cell], cells_b[cell]
        if valid_only and not (a["_valid"] and b["_valid"]):
            continue
        ea, eb = int(not a["_acc"]), int(not b["_acc"])
        index = 3 if ea and eb else 1 if ea else 2 if eb else 0
        counts[index] += 1
    return tuple(counts)


def overlap_stats(counts):
    n00, n10, n01, n11 = counts
    n = sum(counts)
    if not n:
        return (None,) * 13
    ea, eb = (n10+n11)/n, (n01+n11)/n
    observed = (n00+n11)/n
    expected = ea*eb + (1-ea)*(1-eb)
    kappa = (observed-expected)/(1-expected) if expected < 1-1e-12 else None
    phi_den = math.sqrt(ea*(1-ea)*eb*(1-eb))
    phi = (n11/n-ea*eb)/phi_den if phi_den > 1e-12 else None
    double = n11/n
    return (
        ea, eb, observed, expected, kappa, phi, double, ea*eb,
        double-ea*eb, ratio(double, ea*eb),
        ratio(n11, n10+n11), ratio(n11, n01+n11),
        1-double,
    )


def solve_linear(matrix, rhs):
    n = len(rhs)
    a = [list(matrix[i]) + [rhs[i]] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda i: abs(a[i][col]))
        if abs(a[pivot][col]) < 1e-12:
            return None
        a[col], a[pivot] = a[pivot], a[col]
        value = a[col][col]
        for j in range(col, n+1):
            a[col][j] /= value
        for i in range(col+1, n):
            factor = a[i][col]
            if factor:
                for j in range(col, n+1):
                    a[i][j] -= factor*a[col][j]
    x = [0.0]*n
    for i in range(n-1, -1, -1):
        x[i] = a[i][n] - sum(a[i][j]*x[j] for j in range(i+1, n))
    return x


def softplus(x):
    return max(x, 0.0) + math.log1p(math.exp(-abs(x)))


def fit_binomial(rows, dimension, ridge=0.1):
    """rows: (sparse x, improvements, deteriorations); schwache feste Ridge."""
    if not rows or sum(w+l for _, w, l in rows) == 0:
        return None
    beta = [0.0]*dimension

    def objective(b):
        out = -0.5*ridge*sum(v*v for v in b)
        for sparse, wins, losses in rows:
            eta = sum(b[j]*x for j, x in sparse)
            out += wins*eta - (wins+losses)*softplus(eta)
        return out

    old = objective(beta)
    for _ in range(50):
        gradient = [-ridge*x for x in beta]
        hessian = [[0.0]*dimension for _ in range(dimension)]
        for j in range(dimension):
            hessian[j][j] = ridge
        for sparse, wins, losses in rows:
            n = wins+losses
            if n <= 0:
                continue
            eta = sum(beta[j]*x for j, x in sparse)
            p = sigmoid(eta)
            residual, weight = wins-n*p, n*p*(1-p)
            for a, (j, xj) in enumerate(sparse):
                gradient[j] += xj*residual
                for k, xk in sparse[a:]:
                    hessian[j][k] += weight*xj*xk
        for j in range(dimension):
            for k in range(j):
                hessian[j][k] = hessian[k][j]
        step = solve_linear(hessian, gradient)
        if step is None:
            return None
        scale = 1.0
        accepted = False
        while scale >= 1.0/1024:
            candidate = [x+scale*d for x, d in zip(beta, step)]
            value = objective(candidate)
            if value >= old-1e-10:
                accepted = True
                break
            scale *= 0.5
        if not accepted:
            return None
        beta, old = candidate, value
        if max(abs(scale*d) for d in step) < 1e-7:
            return beta
    return None


def multinomial_counts(n, rng):
    result = [0]*n
    for _ in range(n):
        result[rng.randrange(n)] += 1
    return result


def conditional_regression(source_items, target_items, factor, tag):
    """Externe Type-Schwierigkeit; Quell- und Zielbootstrap unabhängig."""
    source_list = list(source_items.items())
    target_list = list(target_items.items())
    other = tuple(i for i in range(3) if i != factor)
    domains = sorted({fmt(next(iter(c.values())).get("domain", MISSING))
                      for _, c in target_list})
    kinds = sorted({fmt(next(iter(c.values())).get("kind", MISSING))
                    for _, c in target_list})
    source_records = []
    for item_id, cells in source_list:
        score = complete_score(cells)
        key = type_key(next(iter(cells.values())))
        source_records.append((key, score))

    target_records = []
    all_pairs = 0
    for item_id, cells in target_list:
        row = next(iter(cells.values()))
        key = type_key(row)
        records = []
        for context in itertools.product((0, 1), repeat=2):
            c0 = [0, 0, 0]
            for index, value in zip(other, context):
                c0[index] = value
            c1 = list(c0)
            c1[factor] = 1
            a, b = cells.get(tuple(c0)), cells.get(tuple(c1))
            if a is None or b is None:
                continue
            all_pairs += 1
            if a["_acc"] != b["_acc"]:
                records.append((key, context, int(b["_acc"] > a["_acc"]),
                                int(b["_acc"] < a["_acc"])))
        target_records.append(records)

    names = (
        ["Intercept", "externer_Erfolgslogit", "Grenznaehe_4p1mp",
         FACTORS[other[0]], FACTORS[other[1]],
         FACTORS[other[0]]+":"+FACTORS[other[1]]]
        + ["domain="+x for x in domains[1:]]
        + ["kind="+x for x in kinds[1:]]
        + ["primary"]
    )

    def build_and_fit(source_weights, target_weights, adjusted):
        totals = collections.defaultdict(lambda: [0.0, 0.0])
        for weight, (key, score) in zip(source_weights, source_records):
            if weight and score is not None:
                totals[key][0] += weight*score[0]
                totals[key][1] += weight*score[1]
        pairs = collections.defaultdict(lambda: [0.0, 0.0])
        for weight, records in zip(target_weights, target_records):
            if not weight:
                continue
            for key, context, wins, losses in records:
                if key in totals:
                    pairs[(key, context)][0] += weight*wins
                    pairs[(key, context)][1] += weight*losses
        rows = []
        for (key, context), (wins, losses) in pairs.items():
            s, n = totals[key]
            p = (s+0.5)/(n+1.0)
            z = math.log(p/(1-p))
            x = [1.0, z, 4*p*(1-p), float(context[0]),
                 float(context[1]), float(context[0]*context[1])]
            if adjusted:
                x += [float(key[0] == d) for d in domains[1:]]
                x += [float(key[1] == k) for k in kinds[1:]]
                x += [float(key[3] == "true")]
            sparse = [(j, value) for j, value in enumerate(x) if value]
            rows.append((sparse, wins, losses))
        dimension = len(names) if adjusted else 6
        return fit_binomial(rows, dimension), sum(w+l for _, w, l in rows)

    sw = [1]*len(source_records)
    tw = [1]*len(target_records)
    raw, raw_n = build_and_fit(sw, tw, False)
    adjusted, adjusted_n = build_and_fit(sw, tw, True)
    draws = [[] for _ in names]
    rng = rng_for(tag)
    for _ in range(B_REG):
        s = multinomial_counts(len(source_records), rng)
        t = multinomial_counts(len(target_records), rng)
        fit, _ = build_and_fit(s, t, True)
        for j in range(len(names)):
            draws[j].append(fit[j] if fit is not None else None)
    rows = []
    for j, name in enumerate(names):
        lo, hi, good = interval(draws[j])
        rows.append((
            name, raw[j] if raw is not None and j < 6 else None,
            adjusted[j] if adjusted is not None else None, lo, hi, good,
        ))
    return all_pairs, raw_n, adjusted_n, rows


def residual_units(source_a, source_b, target_a, target_b, selected_cell=None):
    # Unsicherheit dieser CIs ist ausdrücklich bedingt auf die Quellschätzung.
    probabilities = []
    for source in (source_a, source_b):
        totals = collections.defaultdict(lambda: [0.0, 0.0])
        for cells in source.values():
            for cell, row in cells.items():
                key = (type_key(row), cell)
                totals[key][0] += 1-row["_acc"]
                totals[key][1] += 1
        probabilities.append({
            key: (s+0.5)/(n+1.0) for key, (s, n) in totals.items()
        })
    output = []
    for item_id in sorted(set(target_a) & set(target_b)):
        total = [0.0]*10
        for cell in sorted(set(target_a[item_id]) & set(target_b[item_id])):
            if selected_cell is not None and cell != selected_cell:
                continue
            a, b = target_a[item_id][cell], target_b[item_id][cell]
            key = (type_key(a), cell)
            if key not in probabilities[0] or key not in probabilities[1]:
                continue
            pa, pb = probabilities[0][key], probabilities[1][key]
            ea, eb = 1-a["_acc"], 1-b["_acc"]
            ra, rb = ea-pa, eb-pb
            values = (1, ra, rb, ra*ra, rb*rb, ra*rb,
                      ea*eb, pa*pb, ea, eb)
            for j, value in enumerate(values):
                total[j] += value
        if total[0]:
            output.append(tuple(total))
    return output


def residual_stats(total):
    n, sa, sb, saa, sbb, sab, both, expected, _, _ = total
    if not n:
        return (None,)*6
    return (
        pearson_from_sums(n, sa, sb, saa, sbb, sab),
        sab/n, sa/n, sb/n, both/n, expected/n,
    )


def paired_metric_units(items_a, items_b, metric, only_cell=None):
    output = []
    for item_id in sorted(set(items_a) & set(items_b)):
        n = sa = sb = 0.0
        for cell in sorted(set(items_a[item_id]) & set(items_b[item_id])):
            if only_cell is not None and cell != only_cell:
                continue
            a = row_metric(items_a[item_id][cell], metric)
            b = row_metric(items_b[item_id][cell], metric)
            if a is not None and b is not None:
                n += 1
                sa += a
                sb += b
        if n:
            output.append((n, sa, sb))
    return output


def paired_metric_function(metric):
    binary = metric in BINARY_METRICS
    scale = 100.0 if binary else 1.0
    def function(total):
        n, a, b = total
        if not n:
            return (None,)*4
        return (
            scale*a/n, scale*b/n, scale*(a-b)/n,
            logit_corrected(a, n)-logit_corrected(b, n) if binary else None,
        )
    return function


def effect_difference(items_a, items_b, active, tag):
    # Vorab gemeinsame Zellen wählen, damit dieselben Blöcke verglichen werden.
    ca, cb = {}, {}
    for item_id in set(items_a) & set(items_b):
        common = set(items_a[item_id]) & set(items_b[item_id])
        ca[item_id] = {c: items_a[item_id][c] for c in common}
        cb[item_id] = {c: items_b[item_id][c] for c in common}
    va = contrast_vectors(ca, active)
    vb = contrast_vectors(cb, active)
    units = []
    for item_id in sorted(set(va) & set(vb)):
        if va[item_id][0] != vb[item_id][0]:
            fatal("Interner Fehler: unterschiedlich gepaarte Faktorblöcke")
        units.append(va[item_id]+vb[item_id])
    width = 1+2**len(active)
    calc = contrast_function(active)
    def function(total):
        a, b = calc(total[:width]), calc(total[width:])
        return a[0]-b[0], a[1]-b[1]
    return bootstrap(units, function, tag), len(units)


def independent_difference(result_a, result_b):
    if not result_a[0] or not result_b[0]:
        return (None,)*8
    output = []
    for j in (0, 1):
        diffs = [
            a-b if a is not None and b is not None else None
            for a, b in zip(result_a[4][j], result_b[4][j])
        ]
        lo, hi, good = interval(diffs)
        output.extend((result_a[0][j]-result_b[0][j], lo, hi, good))
    return tuple(output)


def main(directory):
    references = {}
    file_counts = []
    for batch in BATCHES:
        path = directory / ("belege_seeds%s.jsonl" % batch)
        records = read_jsonl(path)
        file_counts.append((path.name, len(records)))
        for record in records:
            item_id = record.get("id")
            if not isinstance(item_id, str) or item_id in references:
                fatal("Fehlende/doppelte Beleg-ID in %s" % path.name)
            truth = record.get("works", record.get("truth"))
            if not isinstance(truth, bool):
                fatal("Beleg ohne boolesche Wahrheit: " + item_id)
            record["truth"] = truth
            record["_batch"] = batch
            record["_short_len"] = len(str(record.get("item_short", "")))
            record["_norm_len"] = len(str(record.get("item", ""))) - record["_short_len"]
            references[item_id] = record

    filenames = (
        ("6000", "urteile_seeds6000_sonnet.jsonl"),
        ("6000", "urteile_seeds6000_haiku.jsonl"),
        ("7000", "urteile_seeds7000_beide.jsonl"),
    )
    judgments = []
    seen = set()
    diagnostics = collections.Counter()
    field_missing = collections.Counter()
    metadata_by_item = {}
    for batch, filename in filenames:
        records = read_jsonl(directory / filename)
        file_counts.append((filename, len(records)))
        for row in records:
            item_id = row.get("id")
            if item_id not in references:
                fatal("Urteil ohne zugehörigen Beleg: %r" % item_id)
            ref = references[item_id]
            if ref["_batch"] != batch:
                fatal("Datensatzübergreifende ID-Zuordnung: " + item_id)
            if not isinstance(row.get("truth"), bool) or row["truth"] != ref["truth"]:
                fatal("Widersprüchliche Wahrheit: " + item_id)
            for field in TYPE_FIELDS:
                if field not in row and field in ref:
                    row[field] = ref[field]
                if field in row and field in ref and row[field] != ref[field]:
                    fatal("Widersprüchliches Belegmerkmal %s: %s" % (field, item_id))
            key = type_key(row)
            if item_id in metadata_by_item and metadata_by_item[item_id] != key:
                fatal("Belegmerkmale variieren zwischen Urteilen: " + item_id)
            metadata_by_item[item_id] = key
            cell = []
            for field in FACTORS:
                value = row.get(field)
                if value not in (0, 1) or value is None:
                    fatal("Ungültiger Faktor %s bei %s" % (field, item_id))
                cell.append(int(value))
            cell = tuple(cell)
            if row.get("cell") != cell_label(cell):
                fatal("cell und Faktoren widersprechen sich: " + item_id)
            model = row.get("model")
            if not isinstance(model, str):
                fatal("Fehlender Modellname: " + item_id)
            duplicate_key = (batch, model, item_id, cell)
            if duplicate_key in seen:
                fatal("Doppeltes Prüferurteil: %r" % (duplicate_key,))
            seen.add(duplicate_key)
            verdict = row.get("verdict")
            row["_valid"] = isinstance(verdict, bool)
            row["_acc"] = float(row["_valid"] and verdict == row["truth"])
            row["_cell"] = cell
            row["_batch"] = batch
            confidence = num(row.get("confidence"))
            row["_confidence"] = confidence if confidence is not None and 0 <= confidence <= 1 else None
            if confidence is not None and not 0 <= confidence <= 1:
                diagnostics[(batch, model, "Konfidenz_ausserhalb_0_1")] += 1
            if not row["_valid"]:
                diagnostics[(batch, model, "ungueltiges_Urteil")] += 1
            if cell[1] == 0 and (num(row.get("n_checks")) or 0) != 0:
                diagnostics[(batch, model, "ZU0_mit_run_check")] += 1
            if cell[1] == 1 and row.get("presented") is not None:
                diagnostics[(batch, model, "ZU1_mit_presented")] += 1
            distinct, checks = num(row.get("distinct_checks")), num(row.get("n_checks"))
            if distinct is not None and (distinct < 0 or distinct > 3):
                diagnostics[(batch, model, "distinct_checks_ausserhalb_0_3")] += 1
            if distinct is not None and checks is not None and distinct > checks:
                diagnostics[(batch, model, "distinct_checks_groesser_checks")] += 1
            if (num(row.get("completion_tokens")) or 0) >= 3900:
                diagnostics[(batch, model, "Tokenproxy_ge3900_kein_Abbruchnachweis")] += 1
            if (num(row.get("n_tool_calls")) or 0) >= 6:
                diagnostics[(batch, model, "Toolproxy_ge6_kein_Rundennachweis")] += 1
            if row.get("right_section") is True and row.get("page_returned") is not True:
                diagnostics[(batch, model, "right_ohne_page")] += 1
            for field in ("confidence", "n_checks", "distinct_checks", "looked_up",
                          "page_returned", "right_section", "n_tool_calls",
                          "completion_tokens", "cost_usd", "lookup_topics"):
                if row.get(field) is None:
                    field_missing[(batch, model, field)] += 1
            judgments.append(row)

    models = sorted({r["model"] for r in judgments})
    if len(models) != 2:
        fatal("Genau zwei Prüfmodelle erwartet, gefunden: %r" % models)
    # Explizite Vorzeichenrichtung: Sonnet minus Haiku, sofern Namen erkennbar.
    if any("sonnet" in m.lower() for m in models):
        models.sort(key=lambda m: (0 if "sonnet" in m.lower() else 1, m))
    model_a, model_b = models

    rows_by = {}
    items_by = {}
    for batch in BATCHES:
        for model in models:
            selected = [r for r in judgments if r["_batch"] == batch and r["model"] == model]
            if not selected:
                fatal("Leere Datensatz-Modell-Kombination: %s %s" % (batch, model))
            rows_by[(batch, model)] = selected
            items_by[(batch, model)] = item_maps(selected)

    gpt_records = read_jsonl(directory / "gpt_einzelkanal_seeds7000.jsonl")
    file_counts.append(("gpt_einzelkanal_seeds7000.jsonl", len(gpt_records)))
    gpt_candidates = collections.defaultdict(list)
    gpt_raw_fallback = 0
    for g in gpt_records:
        item_id = g.get("id")
        if item_id not in references or references[item_id]["_batch"] != "7000":
            fatal("GPT-ID außerhalb der 7000-Belege: %r" % item_id)
        if not isinstance(g.get("decidable"), bool) and isinstance(g.get("raw"), str):
            try:
                raw = json.loads(g["raw"])
            except (ValueError, TypeError):
                raw = {}
            if isinstance(raw, dict) and isinstance(raw.get("decidable"), bool):
                g["decidable"] = raw["decidable"]
                gpt_raw_fallback += 1
            if not isinstance(g.get("verdict"), bool) and isinstance(raw, dict):
                if isinstance(raw.get("works"), bool):
                    g["verdict"] = raw["works"]
        if "truth" in g and g["truth"] != references[item_id]["truth"]:
            fatal("GPT-Wahrheit widerspricht Beleg: " + item_id)
        gpt_candidates[item_id].append(g)
    gpt = {}
    for item_id, candidates in gpt_candidates.items():
        # Frühester entscheidbarkeitsgültiger Versuch, sonst frühester Versuch.
        # Keine Auswahl nach Richtigkeit oder danach, ob decidable true ist.
        candidates.sort(key=lambda g: (
            0 if isinstance(g.get("decidable"), bool) else 1,
            num(g.get("attempt")) if num(g.get("attempt")) is not None else 0,
            g["_line"],
        ))
        gpt[item_id] = candidates[0]

    presented_by_id = collections.defaultdict(set)
    for r in judgments:
        if r["_batch"] == "7000" and r["ZU"] == 0:
            presented_by_id[r["id"]].add(fmt(r.get("presented")))
    ambiguous_channels = set()
    explicit_gpt_mismatch = set()
    for item_id, values in presented_by_id.items():
        if len(values) != 1 or next(iter(values)) in ("None", MISSING):
            ambiguous_channels.add(item_id)
        chosen = gpt.get(item_id)
        if chosen is not None:
            channel = chosen.get("presented", chosen.get("channel"))
            if channel is not None and fmt(channel) not in values:
                explicit_gpt_mismatch.add(item_id)
    unusable_gpt = ambiguous_channels | explicit_gpt_mismatch

    print("ANALYSE: vollständig auf stdout; keine Datei- oder Netzwerkoperationen.")
    print("Datensätze werden getrennt analysiert. A=%s; B=%s." % (model_a, model_b))
    print("Alle Modellunterschiede: A minus B. Faktoreffekt: Stufe 1 minus 0.")
    print("B=%d Beleg-Bootstraps; B_REG=%d unabhängige Quell-/Ziel-Bootstraps." % (B, B_REG))
    print("CIs: punktweise 95%-Perzentilintervalle; NA = nicht definiert/verfügbar.")
    print("Primär: ungültig = Fehler. Logits: (Erfolge+0.5)/(Misserfolge+0.5).")
    print("Binäre Verhaltenskontraste in Prozentpunkten, andere in Originaleinheiten.")
    print("Konfidenz wird als Sicherheit im gewählten Urteil interpretiert.")
    print("Keine automatische Umrechnung von Konfidenzen außerhalb [0,1].")
    print("Viele Untergruppen: explorativ, keine korrigierten Bestätigungstests.")
    print("Kein Beleg-Bootstrap kann die fehlenden Wiederholungsläufe ersetzen.")

    table("Dateien", ("Datei", "JSON_Zeilen"), file_counts)
    coverage = []
    for batch in BATCHES:
        ids = {i for i, ref in references.items() if ref["_batch"] == batch}
        for model in models:
            items = items_by[(batch, model)]
            coverage.append((
                batch, model, len(ids), len(items), len(rows_by[(batch, model)]),
                len(ids)*8, sum(set(c) == set(CELLS) for c in items.values()),
                len(ids-set(items)),
            ))
    table("Datenabdeckung", ("Datensatz", "Modell", "n_Referenzbelege",
          "n_beurteilte_Belege", "n_Urteile", "erwartete_Urteile",
          "n_vollstaendige_Achtzellenbelege", "n_fehlende_Belege"), coverage)
    table("Diagnostik: automatisch bemerkte Auffälligkeiten, keine bestätigten Befunde",
          ("Datensatz", "Modell", "Pruefung", "n"),
          [key+(value,) for key, value in sorted(diagnostics.items())])
    table("Fehlende Felder", ("Datensatz", "Modell", "Feld", "n"),
          [key+(value,) for key, value in sorted(field_missing.items())])
    table("GPT-Zuordnungsdiagnostik", ("Pruefung", "n"), (
        ("Rohzeilen", len(gpt_records)),
        ("gewaehlte_Belege", len(gpt)),
        ("verworfene_Wiederholungen", len(gpt_records)-len(gpt)),
        ("decidable_aus_raw_rekonstruiert", gpt_raw_fallback),
        ("mehrdeutiger_vorgelegter_Kanal", len(ambiguous_channels)),
        ("expliziter_GPT_Kanalwiderspruch", len(explicit_gpt_mismatch)),
        ("7000_Referenzen_ohne_GPT", sum(
            ref["_batch"] == "7000" and i not in gpt for i, ref in references.items())),
    ))
    print("GPT ohne explizites Kanalfeld: Kanalgleichheit nur laut Datenbeschreibung angenommen.")

    summaries = []
    calibrations = []
    topic_counts = collections.Counter()
    for batch in BATCHES:
        for model in models:
            rows = rows_by[(batch, model)]
            for cell in (None,) + CELLS:
                selected = rows if cell is None else [r for r in rows if r["_cell"] == cell]
                label = "alle" if cell is None else cell_label(cell)
                summaries.append((batch, model, label)+summary(selected))
                calibrations.extend(calibration(selected, (batch, model, label)))
            for row in rows:
                topics = row.get("lookup_topics")
                if isinstance(topics, list):
                    for topic in topics:
                        topic_counts[(batch, model, fmt(topic))] += 1
    table("Q1: Urteile und Vorgehen je Zelle",
          ("Datensatz", "Modell", "Zelle")+SUMMARY_HEADERS, summaries)
    table("Q1: Kalibrierung; Konfidenz minus Trefferquote",
          ("Datensatz", "Modell", "Zelle", "Bin", "n",
           "Konfidenz_M", "Trefferquote", "Luecke_oder_ECE"), calibrations)

    topics_output = []
    for batch in BATCHES:
        for model in models:
            counts = [(topic, n) for (b, m, topic), n in topic_counts.items()
                      if b == batch and m == model]
            counts.sort(key=lambda x: (-x[1], x[0]))
            topics_output.extend((batch, model, topic, n) for topic, n in counts[:20])
            topics_output.append((batch, model, "REST_nicht_top20_Aufrufe",
                                  sum(n for _, n in counts[20:])))
    table("Q1: Häufigste exakte lookup_topics, rein deskriptiv",
          ("Datensatz", "Modell", "Topic", "n_Nennungen"), topics_output)

    model_comparisons = []
    model_effect_gaps = []
    for batch in BATCHES:
        ia, ib = items_by[(batch, model_a)], items_by[(batch, model_b)]
        for cell in (None,) + CELLS:
            label = "alle" if cell is None else cell_label(cell)
            for metric in ("acc",)+BEHAVIOR_METRICS:
                units = paired_metric_units(ia, ib, metric, cell)
                result = bootstrap(units, paired_metric_function(metric),
                                   ("Modellvergleich", batch, label, metric))
                point = result[0] if result[0] else (None,)*4
                model_comparisons.append((
                    batch, label, metric, len(units), int(sum(v[0] for v in units)),
                    point[0], point[1],
                ) + ci_columns(result, 2) + ci_columns(result, 3))
        for active in ACTIVE_SETS:
            result, n = effect_difference(ia, ib, active, ("Modell_Effektluecke", batch, active))
            model_effect_gaps.append((batch, active_label(active), n)
                                     + ci_columns(result, 0)+ci_columns(result, 1))
    table("Q1: Gepaarter Modellvergleich A minus B",
          ("Datensatz", "Zelle", "Metrik", "n_Belege", "n_Zellpaare", "A", "B",
           "Delta", "CI_lo", "CI_hi", "B_gueltig",
           "Delta_Logit", "Logit_CI_lo", "Logit_CI_hi", "B_Logit"), model_comparisons)
    table("Q2: Unterschied der Faktoreffekte A minus B",
          ("Datensatz", "Kontrast", "n_Belege",
           "Delta_pp", "CI_lo", "CI_hi", "B_gueltig",
           "Delta_Logit", "Logit_CI_lo", "Logit_CI_hi", "B_Logit"), model_effect_gaps)

    effect_rows = []
    behavior_rows = []
    strata_summaries = []
    primary_results = {}
    for batch in BATCHES:
        for model in models:
            items = items_by[(batch, model)]
            for stratum, selected in strata_for(items, references):
                if not selected:
                    continue
                flat = [r for cells in selected.values() for r in cells.values()]
                strata_summaries.append((batch, model, stratum)+summary(flat))
                for active in ACTIVE_SETS:
                    units, result, blocks = contrast_report(
                        selected, active, ("Faktor", batch, model, stratum, active)
                    )
                    effect_rows.append((batch, model, stratum, active_label(active),
                                        len(units), blocks)
                                       + ci_columns(result, 0)+ci_columns(result, 1))
                    if stratum == "gesamt":
                        primary_results[(batch, model, active)] = result
            # Sensitivität mit nur vollständig gültigen aktiven Blöcken.
            for active in ACTIVE_SETS:
                units, result, blocks = contrast_report(
                    items, active, ("gueltige_Bloecke", batch, model, active),
                    "acc_valid"
                )
                effect_rows.append((batch, model, "nur_gueltige_Bloecke",
                                    active_label(active), len(units), blocks)
                                   + ci_columns(result, 0)+ci_columns(result, 1))
            for active in ((0,), (1,), (2,)):
                for metric in BEHAVIOR_METRICS:
                    units, result, blocks = contrast_report(
                        items, active, ("Verhalten", batch, model, active, metric), metric
                    )
                    behavior_rows.append((batch, model, active_label(active), metric,
                                          len(units), blocks)+ci_columns(result, 0))
    table("Q2/Q6: Ausgangslagen nach Belegmerkmalen",
          ("Datensatz", "Modell", "Schicht")+SUMMARY_HEADERS, strata_summaries)
    table("Q2: Alle faktoriellen Genauigkeitskontraste",
          ("Datensatz", "Modell", "Schicht", "Kontrast", "n_Belege",
           "n_vollstaendige_Bloecke",
           "Effekt_pp", "CI_lo", "CI_hi", "B_gueltig",
           "Effekt_Logit", "Logit_CI_lo", "Logit_CI_hi", "B_Logit"), effect_rows)
    table("Q2: Faktoreffekte auf Vorgehen und Aufwand",
          ("Datensatz", "Modell", "Faktor", "Metrik", "n_Belege",
           "n_Bloecke", "Effekt", "CI_lo", "CI_hi", "B_gueltig"), behavior_rows)

    batch_differences = []
    scale_rows = []
    for model in models:
        for active in ACTIVE_SETS:
            a = primary_results[("7000", model, active)]
            b = primary_results[("6000", model, active)]
            batch_differences.append((model, active_label(active))
                                     + independent_difference(a, b))
        for batch in BATCHES:
            for active in ((0,), (1,), (2,)):
                result = primary_results[(batch, model, active)]
                delta = result[0][1] if result[0] else None
                for p0 in (0.05, 0.2, 0.5, 0.8, 0.95):
                    p1 = sigmoid(math.log(p0/(1-p0))+delta) if delta is not None else None
                    scale_rows.append((batch, model, active_label(active), delta,
                                       p0, p1, 100*(p1-p0) if p1 is not None else None))
    table("Q6: Replikationsunterschied 7000 minus 6000, UNABHÄNGIGE Belege",
          ("Modell", "Kontrast", "Differenz_pp", "CI_lo", "CI_hi", "B_gueltig",
           "Differenz_Logit", "Logit_CI_lo", "Logit_CI_hi", "B_Logit"), batch_differences)
    table("Q6: Reiner Skalenmechanismus bei konstantem beobachtetem Haupt-Logiteffekt",
          ("Datensatz", "Modell", "Faktor", "konstantes_Delta_Logit",
           "hypothetisches_p0", "p1", "erwartete_pp"),
          scale_rows)
    print("Die Skalentabelle ist eine mathematische Illustration, keine Anpassung an einzelne Belege.")

    difficulty_rows = []
    difficulty_corr = []
    type_difficulty = []
    for batch in BATCHES:
        for model in models:
            items = items_by[(batch, model)]
            for item_id in sorted(items):
                cells = items[item_id]
                score = complete_score(cells)
                s = sum(r["_acc"] for r in cells.values())
                n = len(cells)
                row = next(iter(cells.values()))
                signature = "".join(
                    "-" if c not in cells else
                    "?" if not cells[c]["_valid"] else
                    "C" if cells[c]["_acc"] else "E"
                    for c in CELLS
                )
                difficulty_rows.append((
                    batch, model, item_id, type_label(type_key(row)), n,
                    score is not None, 1-s/n, logit_corrected(n-s, n),
                    signature,
                    mean([r["_confidence"] for r in cells.values() if r["_valid"]]),
                    sum(r.get("looked_up") is True for r in cells.values()),
                    sum(r.get("right_section") is True for r in cells.values()),
                ))
            for key, (s, n, count, p) in sorted(train_type_scores(items).items()):
                type_difficulty.append((batch, model, type_label(key), int(count),
                                        int(n), 1-s/n, 1-p, math.log((1-p)/p)))
        ia, ib = items_by[(batch, model_a)], items_by[(batch, model_b)]
        pairs = []
        for item_id in sorted(set(ia) & set(ib)):
            a, b = complete_score(ia[item_id]), complete_score(ib[item_id])
            if a and b:
                pairs.append((1-a[0]/a[1], 1-b[0]/b[1]))
        difficulty_corr.append((batch, "Belege", len(pairs))
                               + correlation_bootstrap(pairs, ("Schwierigkeit", batch)))
        # Typkorrelation: CIs durch Belege, nicht durch vermeintlich unabhängige Zellen.
        paired_ids = [
            i for i in sorted(set(ia) & set(ib))
            if complete_score(ia[i]) and complete_score(ib[i])
        ]
        records = []
        for item_id in paired_ids:
            key = type_key(next(iter(ia[item_id].values())))
            records.append((key, complete_score(ia[item_id])[0],
                            complete_score(ib[item_id])[0]))
        def type_corr(records_sample):
            totals = collections.defaultdict(lambda: [0, 0, 0])
            for key, sa, sb in records_sample:
                totals[key][0] += sa
                totals[key][1] += sb
                totals[key][2] += 8
            xs = [1-a/n for a, b, n in totals.values()]
            ys = [1-b/n for a, b, n in totals.values()]
            return pearson(xs, ys), pearson(ranks(xs), ranks(ys)), len(xs)
        point = type_corr(records)
        draws = [[], []]
        rng = rng_for(("Typkorrelation", batch))
        for _ in range(B):
            sample = [records[rng.randrange(len(records))] for _ in records] if records else []
            values = type_corr(sample)
            draws[0].append(values[0])
            draws[1].append(values[1])
        c0, c1 = interval(draws[0]), interval(draws[1])
        difficulty_corr.append((batch, "Typen_Belegbootstrap", point[2],
                                point[0], c0[0], c0[1], c0[2],
                                point[1], c1[0], c1[1], c1[2]))
    table("Q3: Schwierigkeit jedes Belegs; Zellreihenfolge " +
          ",".join(cell_label(c) for c in CELLS),
          ("Datensatz", "Modell", "ID", "Typ", "n_Zellen", "vollstaendig",
           "empirische_Fehlerrate", "Fehler_Logit_korrigiert",
           "C_richtig_E_falsch_?_ungueltig_-_fehlend",
           "Konfidenz_M", "n_lookup", "n_right"), difficulty_rows)
    table("Q3: Schwierigkeit jedes Typs; nur vollständige Achtzellenbelege",
          ("Datensatz", "Modell", "Typ", "n_Belege", "n_Urteile",
           "empirische_Fehlerrate", "gegl_Fehlerrate", "Fehler_Logit"),
          type_difficulty)
    table("Q3: Ähnlichkeit der Schwierigkeiten zwischen A und B",
          ("Datensatz", "Ebene", "n_Einheiten",
           "Pearson", "CI_lo", "CI_hi", "B_Pearson",
           "Spearman", "CI_lo", "CI_hi", "B_Spearman"), difficulty_corr)

    transfer_rows = []
    difficulty_effects = []
    regression_rows = []
    regression_coverage = []
    for source_batch, target_batch in (("6000", "7000"), ("7000", "6000")):
        for model in models:
            source = items_by[(source_batch, model)]
            target = items_by[(target_batch, model)]
            scores = train_type_scores(source)
            target_groups = collections.defaultdict(dict)
            bins = collections.defaultdict(dict)
            for item_id, cells in target.items():
                key = type_key(next(iter(cells.values())))
                target_groups[key][item_id] = cells
                if key not in scores:
                    bins["nicht_uebertragbar"][item_id] = cells
                else:
                    p = scores[key][3]
                    label = "leicht_p_ge0.8" if p >= 0.8 else "schwer_p_le0.2" if p <= 0.2 else "mittel"
                    bins[label][item_id] = cells
            for key in sorted(target_groups):
                group = target_groups[key]
                complete = [complete_score(c) for c in group.values()]
                complete = [c for c in complete if c is not None]
                s = sum(c[0] for c in complete)
                n = sum(c[1] for c in complete)
                train = scores.get(key)
                transfer_rows.append((
                    source_batch+"->"+target_batch, model, type_label(key),
                    train[2] if train else 0, train[3] if train else None,
                    len(group), len(complete), s/n if n else None,
                    (s/n-train[3]) if n and train else None,
                ))
            for label, group in sorted(bins.items()):
                for active in ((0,), (1,), (2,)):
                    units, result, blocks = contrast_report(
                        group, active, ("unabhaengige_Bins", source_batch,
                                        target_batch, model, label, active)
                    )
                    difficulty_effects.append((
                        source_batch+"->"+target_batch, model, label,
                        active_label(active), len(units), blocks
                    ) + ci_columns(result, 0)+ci_columns(result, 1))
            for factor in range(3):
                pairs, nraw, nadj, coefficients = conditional_regression(
                    source, target, factor,
                    ("bedingte_Logitregression", source_batch, target_batch, model, factor)
                )
                regression_coverage.append((
                    source_batch+"->"+target_batch, model, FACTORS[factor],
                    len(source), len(target), pairs, nraw, nadj,
                ))
                regression_rows.extend(
                    (source_batch+"->"+target_batch, model, FACTORS[factor])+c
                    for c in coefficients
                )
    table("Q3: Unabhängige Typ-Schwierigkeit und Zielkalibrierung",
          ("Quelle_Ziel", "Modell", "Typ", "n_Quellbelege",
           "p_Erfolg_Quelle_geglaettet", "n_Zielbelege",
           "n_vollstaendige_Zielbelege", "p_Erfolg_Ziel", "Ziel_minus_Quelle"),
          transfer_rows)
    table("Q3: Faktoreffekte nach ausschließlich extern festgelegten Schwierigkeitsbins",
          ("Quelle_Ziel", "Modell", "externe_Schicht", "Faktor",
           "n_Zielbelege", "n_Bloecke",
           "Effekt_pp", "CI_lo", "CI_hi", "B_gueltig",
           "Effekt_Logit", "Logit_CI_lo", "Logit_CI_hi", "B_Logit"),
          difficulty_effects)
    print("Bin-CIs sind bedingt auf die Quell-Bineinteilung; die folgenden Regressions-CIs")
    print("schätzen dagegen Quellschwierigkeit und Zielmodell in jedem Bootstrap neu.")
    table("Q3: Informationsbasis der bedingten Logitmodelle",
          ("Quelle_Ziel", "Modell", "Faktor", "n_Quellbelege", "n_Zielbelege",
           "n_vollstaendige_Zellpaare", "n_nutzbare_diskordante_Paare_roh",
           "n_nutzbare_diskordante_Paare_adjustiert"), regression_coverage)
    table("Q3: Bedingte Logit-Effektmodifikation; Ridge=0.1 auf alle Koeffizienten",
          ("Quelle_Ziel", "Modell", "Faktor", "Term", "Koeff_ohne_Typkontrollen",
           "Koeff_mit_domain_kind_primary", "Bootstrap_CI_lo",
           "Bootstrap_CI_hi", "B_erfolgreich"), regression_rows)
    print("Logitmodell-Ziel: Verbesserung versus Verschlechterung unter diskordanten Paaren.")
    print("Grenznähe=4*p*(1-p), Erfolgslogit=log(p/(1-p)); p stammt nur aus der Quelle.")
    print("Keine exakten Typ-Fixed-Effects der Faktoreffekte: diese würden den typkonstanten")
    print("Schwierigkeitseffekt vollständig absorbieren. Geringe Erfolgszahlen sind Warnzeichen.")

    overlap_rows = []
    for batch in BATCHES:
        ia, ib = items_by[(batch, model_a)], items_by[(batch, model_b)]
        for valid_only in (False, True):
            # Schichtungen sind marginale Schichten, nicht zusätzliche Laufreplikate.
            selections = [("alle", None, None)]
            selections += [(cell_label(c), "cell", c) for c in CELLS]
            for field in ("truth",)+TYPE_FIELDS:
                values = sorted({fmt(next(iter(c.values())).get(field, MISSING))
                                 for c in ia.values()})
                selections += [(field+"="+v, field, v) for v in values]
            for label, field, value in selections:
                vectors = []
                for item_id in sorted(set(ia) & set(ib)):
                    a, b = ia[item_id], ib[item_id]
                    if field == "cell":
                        a = {value: a[value]} if value in a else {}
                        b = {value: b[value]} if value in b else {}
                    elif field is not None:
                        row = next(iter(a.values()))
                        if fmt(row.get(field, MISSING)) != value:
                            continue
                    v = overlap_vector(a, b, valid_only)
                    if sum(v):
                        vectors.append(v)
                result = bootstrap(vectors, overlap_stats,
                                   ("Fehleruebereinstimmung", batch, valid_only, label))
                total = sums(vectors)
                point = result[0] if result[0] else (None,)*13
                overlap_rows.append((
                    batch, "nur_beide_gueltig" if valid_only else "ungueltig_als_Fehler",
                    label, len(vectors), int(sum(total)) if total else 0,
                ) + (tuple(int(x) for x in total) if total else (0,0,0,0)) + (
                    point[0], point[1], point[2], point[3],
                ) + ci_columns(result, 4) + ci_columns(result, 5) + (
                    point[6], point[7],
                ) + ci_columns(result, 8) + (
                    point[9], point[10], point[11], point[12],
                ))
    table("Q4: Zufallskorrigierte Fehlerübereinstimmung",
          ("Datensatz", "Umgang_ungueltig", "Schicht", "n_Belege", "n_Zellpaare",
           "beide_korrekt", "nur_A_falsch", "nur_B_falsch", "beide_falsch",
           "Fehlerrate_A", "Fehlerrate_B", "Uebereinstimmung", "Zufallserwartung",
           "Kappa", "CI_lo", "CI_hi", "B_Kappa",
           "Phi", "CI_lo", "CI_hi", "B_Phi",
           "Doppelfehler", "Doppelfehler_unabhaengig",
           "Exzess", "CI_lo", "CI_hi", "B_Exzess",
           "Doppelfehler_Ratio", "P_B_Fehler_gegeben_A_Fehler",
           "P_A_Fehler_gegeben_B_Fehler", "Orakel_Trefferquote"), overlap_rows)

    residual_rows = []
    for source_batch, target_batch in (("6000", "7000"), ("7000", "6000")):
        for cell in (None,)+CELLS:
            units = residual_units(
                items_by[(source_batch, model_a)], items_by[(source_batch, model_b)],
                items_by[(target_batch, model_a)], items_by[(target_batch, model_b)], cell
            )
            result = bootstrap(units, residual_stats,
                               ("Residualkorrelation", source_batch, target_batch, cell))
            point = result[0] if result[0] else (None,)*6
            residual_rows.append((
                source_batch+"->"+target_batch, "alle" if cell is None else cell_label(cell),
                len(units), int(sum(v[0] for v in units)),
            )+ci_columns(result, 0)+ci_columns(result, 1)+tuple(point[2:]))
    table("Q4: Residuen nach externem Typ×Zell-Fehlerrisiko; CIs bedingt auf Quelle",
          ("Quelle_Ziel", "Zelle", "n_Zielbelege", "n_Zellpaare",
           "Residualkorrelation", "CI_lo", "CI_hi", "B_gueltig",
           "M_Residuenprodukt", "CI_lo", "CI_hi", "B_gueltig",
           "M_Residuum_A", "M_Residuum_B", "beobachtete_Doppelfehler",
           "erwartetes_Produkt_externer_Risiken"), residual_rows)

    gpt_quality = []
    gpt_grouped = collections.defaultdict(list)
    for item_id, chosen in gpt.items():
        ref = references[item_id]
        row = dict(chosen)
        row["truth"] = ref["truth"]
        row["_acc"] = float(isinstance(chosen.get("verdict"), bool)
                            and chosen["verdict"] == ref["truth"])
        dec = fmt(chosen.get("decidable")) if isinstance(chosen.get("decidable"), bool) else "unbekannt"
        gpt_grouped[("gesamt", dec)].append(row)
        for field in ("truth", "domain", "kind", "fault"):
            value = ref.get(field, next(
                (r.get(field, MISSING) for r in rows_by[("7000", model_a)] if r["id"] == item_id),
                MISSING,
            ))
            gpt_grouped[(field+"="+fmt(value), dec)].append(row)
    for (stratum, dec), group in sorted(gpt_grouped.items()):
        valid = sum(isinstance(r.get("verdict"), bool) for r in group)
        correct = sum(r["_acc"] for r in group)
        gpt_quality.append((stratum, dec, len(group), valid, int(correct),
                            pct(correct, len(group)), pct(correct, valid),
                            sum(r.get("verdict") is True for r in group)))
    table("Q5: GPT ist selbst ein fehlbarer Prüfer",
          ("Schicht", "decidable", "n_Belege", "n_gueltig", "n_korrekt",
           "korrekt_pct_alle", "korrekt_pct_gueltig", "n_works"), gpt_quality)

    def gpt_label(item_id):
        if item_id in unusable_gpt:
            return "Kanalzuordnung_unsicher"
        chosen = gpt.get(item_id)
        if chosen is None or not isinstance(chosen.get("decidable"), bool):
            return "unbekannt"
        return "entscheidbar" if chosen["decidable"] else "nicht_entscheidbar"

    gpt_summaries = []
    gpt_effects = []
    gpt_interactions = []
    for model in models:
        items = items_by[("7000", model)]
        groups = collections.defaultdict(dict)
        for item_id, cells in items.items():
            groups[gpt_label(item_id)][item_id] = cells
        stored = {}
        for label, group in sorted(groups.items()):
            for sp, au in itertools.product((0, 1), repeat=2):
                selected = [
                    cells[(sp,0,au)] for cells in group.values() if (sp,0,au) in cells
                ]
                gpt_summaries.append((model, label, sp, au)+summary(selected))
            for active in ((0,), (1,), (2,)):
                units, result, blocks = contrast_report(
                    group, active, ("GPT_Effekte", model, label, active)
                )
                stored[(label, active)] = result
                gpt_effects.append((model, label, "alle_Kontexte", active_label(active),
                                    len(units), blocks)
                                   + ci_columns(result, 0)+ci_columns(result, 1))
                if active in ((0,), (2,)):
                    single = {
                        i: {c: r for c, r in cells.items() if c[1] == 0}
                        for i, cells in group.items()
                    }
                    units, result, blocks = contrast_report(
                        single, active, ("GPT_Effekte_ZU0", model, label, active)
                    )
                    gpt_effects.append((model, label, "nur_ZU0", active_label(active),
                                        len(units), blocks)
                                       + ci_columns(result, 0)+ci_columns(result, 1))
        for active in ((0,), (1,), (2,)):
            no = stored.get(("nicht_entscheidbar", active))
            yes = stored.get(("entscheidbar", active))
            if no and yes:
                gpt_interactions.append((model, active_label(active),
                                         "nicht_entscheidbar_minus_entscheidbar")
                                        + independent_difference(no, yes))
    table("Q5: ZU=0 nach GPT-Entscheidbarkeit; SP=0 ist primär vergleichbar",
          ("Modell", "GPT_Gruppe", "SP", "AU")+SUMMARY_HEADERS, gpt_summaries)
    table("Q5: Faktoreffekte innerhalb der GPT-Gruppen",
          ("Modell", "GPT_Gruppe", "Kontexte", "Faktor", "n_Belege", "n_Bloecke",
           "Effekt_pp", "CI_lo", "CI_hi", "B_gueltig",
           "Effekt_Logit", "Logit_CI_lo", "Logit_CI_hi", "B_Logit"), gpt_effects)
    table("Q5: Effektmodifikation durch GPT-Entscheidbarkeit",
          ("Modell", "Faktor", "Richtung",
           "Differenz_pp", "CI_lo", "CI_hi", "B_gueltig",
           "Differenz_Logit", "Logit_CI_lo", "Logit_CI_hi", "B_Logit"),
          gpt_interactions)

    # Auswahl nach beobachtetem Verhalten: nur Diagnostik, nicht kausale Wirkung.
    strategy_rows = []
    for batch in BATCHES:
        for model in models:
            rows = rows_by[(batch, model)]
            rules = (
                ("lookup_nein", lambda r: r.get("looked_up") is False),
                ("lookup_ja_ohne_page", lambda r: r.get("looked_up") is True
                 and r.get("page_returned") is False),
                ("page_ohne_right", lambda r: r.get("page_returned") is True
                 and r.get("right_section") is False),
                ("right_ja", lambda r: r.get("right_section") is True),
                ("ZU1_0_Kanaele", lambda r: r["ZU"] == 1
                 and num(r.get("distinct_checks")) == 0),
                ("ZU1_1_Kanal", lambda r: r["ZU"] == 1
                 and num(r.get("distinct_checks")) == 1),
                ("ZU1_2_Kanaele", lambda r: r["ZU"] == 1
                 and num(r.get("distinct_checks")) == 2),
                ("ZU1_3_Kanaele", lambda r: r["ZU"] == 1
                 and num(r.get("distinct_checks")) == 3),
                ("Tokenproxy_ge3900", lambda r: (num(r.get("completion_tokens")) or 0) >= 3900),
                ("Tokenproxy_lt3900", lambda r: num(r.get("completion_tokens")) is not None
                 and num(r.get("completion_tokens")) < 3900),
                ("Toolproxy_ge6", lambda r: (num(r.get("n_tool_calls")) or 0) >= 6),
                ("Toolproxy_lt6", lambda r: num(r.get("n_tool_calls")) is not None
                 and num(r.get("n_tool_calls")) < 6),
            )
            for label, rule in rules:
                selected = [r for r in rows if rule(r)]
                strategy_rows.append((batch, model, label)+summary(selected))
    table("Q6: Verhaltens- und Budgetdiagnostik, ausdrücklich NICHT kausal",
          ("Datensatz", "Modell", "beobachtete_Gruppe")+SUMMARY_HEADERS, strategy_rows)

    length_rows = []
    for batch in BATCHES:
        refs = [r for r in references.values() if r["_batch"] == batch]
        for field in ("_short_len", "_norm_len"):
            values = [r[field] for r in refs]
            length_rows.append((batch, field, len(values), mean(values),
                                min(values) if values else None,
                                quantile(values, .25), quantile(values, .5),
                                quantile(values, .75), max(values) if values else None))
    table("Q6: Promptlängen-Proxies in Zeichen; keine vollständigen API-Tokenlängen",
          ("Datensatz", "Groesse", "n", "M", "Min", "Q25", "Median", "Q75", "Max"),
          length_rows)

    print("\n### Grenzen und Zuordnung der Gegenproben")
    print("Skalenartefakt: pp UND Logits sowie konstante-Logit-Illustration vergleichen.")
    print("Zirkularität: nur unabhängige Quelltypen für Ziel-Effektmodifikation; keine ID-Paarung zwischen Seeds.")
    print("Typkomposition/DIF: Typ- und Domänenschichten, Modell-Schwierigkeitskorrelationen, kontrollierte Logitmodelle.")
    print("Technische Fehler: Abdeckung, ungültige Urteile, gültige Blöcke, Token-/Toolproxies.")
    print("Laufdrift: getrennte Datensätze und unabhängige Replikationsdifferenzen; keine kausale Driftidentifikation.")
    print("Einzelkanal-Mehrdeutigkeit: GPT-Selbstprüfung und SP=0/ZU=0-Schichten; GPT ist keine objektive Entscheidbarkeitswahrheit.")
    print("Gemeinsame Fehler: kappa/Phi/Exzess statt bloßer Übereinstimmung; externe Typ×Zell-Residuen als Zusatzdiagnostik.")
    print("Nachschlagen/Kanäle: beobachtete Auswahl kann eine Folge von Schwierigkeit sein, kein randomisierter Mediator.")
    print("AU: Inhaltsrichtung und zusätzliche Länge nicht getrennt; SP: Sollwertzugang und Textlänge nicht getrennt.")
    print("Keine neutrale Fülltextkontrolle, keine echten Werkzeugrunden-/Timeoutlogs, keine Wiederholungen pro Zelle.")
    print("Die Typ-Übertragung erlaubt keine unabhängige Schwierigkeitsschätzung jedes individuellen Zielbelegs.")
    print("Alle ausgegebenen Untergruppen und Diagnosen sind zu berichten, auch bei null oder undefinierten Effekten.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Aufruf: python3 analyse.py DATENVERZEICHNIS", file=sys.stderr)
        sys.exit(2)
    try:
        directory = Path(sys.argv[1])
        if not directory.is_dir():
            fatal("Kein Datenverzeichnis: %s" % directory)
        main(directory)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("ANALYSE ABGEBROCHEN: %s" % exc, file=sys.stderr)
        sys.exit(1)
