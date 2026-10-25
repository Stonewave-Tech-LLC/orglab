#!/usr/bin/env python3
"""Recompute the preregistered primary V1–V3 analyses using only the standard library."""

import itertools
import json
import math
import random
import sys
from pathlib import Path

DRAWS = 5000
MAIN_SEEDS = range(6000, 6024)
FACTORS = tuple(itertools.product((0, 1), repeat=3))
CELL_NAMES = {
    factors: "SP{}-ZU{}-AU{}".format(*factors) for factors in FACTORS
}

CHOICES = [
    "Only main-run seeds 6000–6023 are eligible; pilot and other seeds are ignored.",
    "The last physical JSONL record for each (seed, id, cell) replaces all earlier "
    "records for that pair, including when its verdict is missing.",
    "A complete seed must contain exactly 12 distinct items, each in all eight "
    "cells, with strictly Boolean verdicts. Twelve follows from 288 items over "
    "24 seeds. An absent cell or a missing/non-Boolean verdict excludes the "
    "entire seed. Seeds with no records are also incomplete.",
    "Cell labels are authoritative; supplied SP, ZU and AU fields must agree. "
    "Retained records for an item must agree on Boolean truth and primary. "
    "Malformed records or inconsistent metadata are treated as input errors, "
    "not silently repaired.",
    "All estimates and per-cell rates use only complete seeds. miss_rate means "
    "P(verdict=true | truth=false), not the rate of missing judgments; "
    "false_alarm_rate means P(verdict=false | truth=true). Empty denominators "
    "are represented by null.",
    "V1 uses truth=false and primary=true; V2 uses all truth=false items. "
    "The spec-pure V2 analysis is secondary and does not replace primary V2.",
    "V3 uses all items, working and broken, but only ZU=1 cells, averaging "
    "the AU1-minus-AU0 contrast over SPEC within each item.",
    "Each item's contrast is an equally weighted mean over the other factors; "
    "the final estimate equally weights items, not seeds or individual calls.",
    "Bootstrap sampling independently resamples whole item contrasts with "
    "replacement, preserving the original item count; there is no seed-cluster "
    "or stratified bootstrap.",
    "The preregistration lists fixed seeds without assigning them to analyses. "
    "Independent random.Random instances use 201 for V1, 202 for V2 and 203 "
    "for V3, with 5000 draws each. Items are ordered by (seed, id).",
    "Percentile endpoints use linear interpolation at (B-1)*p in the sorted "
    "bootstrap means, for p=0.025 and p=0.975.",
    "The preregistration does not define p-values for BH. Here each two-sided "
    "p-value is a centered-bootstrap test: "
    "(1 + count(abs(bootstrap_mean-estimate) >= abs(estimate))) / (B+1). "
    "This is an explicit implementation choice, not a reconstruction of the "
    "unavailable original code.",
    "Benjamini–Hochberg adjustment is applied jointly to the two primary "
    "V1/V2 p-values only, with monotone adjusted q-values capped at one.",
    "The amended decision rule supersedes the original rule. Because its "
    "categories overlap, the single label uses this precedence: praktisch null "
    "(upper<0.02), Vorhersage widerlegt (upper<prediction), Vorhersage gestützt "
    "(lower>0 and BH q<=0.05 and upper>=prediction), otherwise nicht entschieden. "
    "Thus a detectable but smaller-than-predicted effect can be labeled "
    "widerlegt. The prediction thresholds are 0.10 and 0.05.",
    "With fewer than 16 complete seeds both labels are nur deskriptiv; estimates "
    "and bootstrap intervals are still reported when defined. An empty "
    "contrast sample produces null estimate and null interval, and its label "
    "is nicht auswertbar unless the under-16 rule applies.",
    "No n_checks values are imputed. Retained complete-seed records must have "
    "nonnegative integer n_checks wherever ZU=1, or the input is rejected.",
    "No discretionary generator-error exclusions are inferred from judgments. "
    "The flagged coding-fail_moderate-6021 item remains in the primary analysis. "
    "Sensitivity, secondary, failure-rate and prevalence analyses are outside "
    "the requested primary-output schema.",
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_data(path):
    retained = {}
    name_to_factors = {name: factors for factors, name in CELL_NAMES.items()}

    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            record = json.loads(line)
            require(isinstance(record, dict),
                    "Line {} is not an object".format(line_number))
            seed = record.get("seed")
            require(type(seed) is int,
                    "Invalid seed on line {}".format(line_number))
            if seed not in MAIN_SEEDS:
                continue

            item_id = record.get("id")
            require(isinstance(item_id, str) and bool(item_id),
                    "Invalid id on line {}".format(line_number))
            cell = record.get("cell")
            require(isinstance(cell, str) and cell in name_to_factors,
                    "Invalid cell on line {}".format(line_number))
            retained[(seed, item_id, cell)] = record

    # Validate the deduplicated records, not superseded attempts.
    items_by_seed = {seed: {} for seed in MAIN_SEEDS}
    for (seed, item_id, cell), record in retained.items():
        factors = name_to_factors[cell]
        for field, expected in zip(("SP", "ZU", "AU"), factors):
            if field in record:
                require(type(record[field]) is int and record[field] == expected,
                        "Cell/factor disagreement: {}".format((seed, item_id, cell)))
        require(type(record.get("truth")) is bool,
                "Non-Boolean truth: {}".format((seed, item_id, cell)))
        require(type(record.get("primary")) is bool,
                "Non-Boolean primary: {}".format((seed, item_id, cell)))
        items_by_seed[seed].setdefault(item_id, {})[factors] = record

    complete_seeds = []
    complete_items = []
    for seed in MAIN_SEEDS:
        items = items_by_seed[seed]
        for item_id, cells in items.items():
            metadata = {(r["truth"], r["primary"]) for r in cells.values()}
            require(len(metadata) == 1,
                    "Inconsistent item metadata: {}".format((seed, item_id)))

        complete = (
            len(items) == 12
            and all(
                len(cells) == 8
                and all(
                    factors in cells
                    and type(cells[factors].get("verdict")) is bool
                    for factors in FACTORS
                )
                for cells in items.values()
            )
        )
        if not complete:
            continue

        complete_seeds.append(seed)
        for item_id in sorted(items):
            cells = items[item_id]
            for factors, record in cells.items():
                if factors[1] == 1:
                    checks = record.get("n_checks")
                    require(type(checks) is int and checks >= 0,
                            "Invalid n_checks: {}".format(
                                (seed, item_id, CELL_NAMES[factors])))
            complete_items.append((seed, item_id, cells))

    return complete_seeds, complete_items


def percentile(sorted_values, probability):
    position = (len(sorted_values) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    fraction = position - lower
    return (
        sorted_values[lower] * (1.0 - fraction)
        + sorted_values[upper] * fraction
    )


def bootstrap(values, seed):
    if not values:
        return None, None, None

    n = len(values)
    estimate = sum(values) / n
    rng = random.Random(seed)
    means = []
    for _ in range(DRAWS):
        means.append(sum(values[rng.randrange(n)] for _ in range(n)) / n)

    p_value = (
        1 + sum(abs(mean - estimate) >= abs(estimate) for mean in means)
    ) / (DRAWS + 1)
    means.sort()
    interval = [percentile(means, 0.025), percentile(means, 0.975)]
    return estimate, interval, p_value


def bh_adjust(p_values):
    # Undefined tests are conservatively assigned p=1 within the fixed family.
    ordered = sorted(
        enumerate(1.0 if p is None else p for p in p_values),
        key=lambda pair: (pair[1], pair[0]),
    )
    adjusted = [None] * len(p_values)
    running = 1.0
    for rank_index in range(len(ordered) - 1, -1, -1):
        original_index, p_value = ordered[rank_index]
        rank = rank_index + 1
        running = min(running, p_value * len(ordered) / rank)
        adjusted[original_index] = running
    return adjusted


def label(interval, q_value, prediction, n_complete):
    if n_complete < 16:
        return "nur deskriptiv"
    if interval is None:
        return "nicht auswertbar"
    lower, upper = interval
    if upper < 0.02:
        return "praktisch null"
    if upper < prediction:
        return "Vorhersage widerlegt"
    if lower > 0 and q_value <= 0.05 and upper >= prediction:
        return "Vorhersage gestützt"
    return "nicht entschieden"


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: script.py DATA_DIRECTORY")

    complete_seeds, items = read_data(Path(sys.argv[1]) / "judgments.jsonl")
    v1 = []
    v2 = []
    v3 = []

    miss_counts = {cell: [0, 0] for cell in CELL_NAMES.values()}
    false_alarm_counts = {cell: [0, 0] for cell in CELL_NAMES.values()}

    for _, _, cells in items:
        first = cells[(0, 0, 0)]
        broken = first["truth"] is False

        if broken:
            spec_difference = sum(
                int(cells[(1, zu, au)]["verdict"])
                - int(cells[(0, zu, au)]["verdict"])
                for zu, au in itertools.product((0, 1), repeat=2)
            ) / 4.0
            if first["primary"]:
                v1.append(spec_difference)

            v2.append(sum(
                int(cells[(sp, zu, 1)]["verdict"])
                - int(cells[(sp, zu, 0)]["verdict"])
                for sp, zu in itertools.product((0, 1), repeat=2)
            ) / 4.0)

        v3.append(sum(
            cells[(sp, 1, 1)]["n_checks"]
            - cells[(sp, 1, 0)]["n_checks"]
            for sp in (0, 1)
        ) / 2.0)

        for factors, record in cells.items():
            cell = CELL_NAMES[factors]
            if broken:
                miss_counts[cell][0] += int(record["verdict"])
                miss_counts[cell][1] += 1
            else:
                false_alarm_counts[cell][0] += int(not record["verdict"])
                false_alarm_counts[cell][1] += 1

    estimate1, ci1, p1 = bootstrap(v1, 201)
    estimate2, ci2, p2 = bootstrap(v2, 202)
    estimate3, ci3, _ = bootstrap(v3, 203)
    q1, q2 = bh_adjust([p1, p2])

    def rates(counts):
        return {
            cell: numerator / denominator if denominator else None
            for cell, (numerator, denominator) in sorted(counts.items())
        }

    result = {
        "n_complete_seeds": len(complete_seeds),
        "v1_estimate": estimate1,
        "v1_ci95": ci1,
        "v1_label": label(ci1, q1, 0.10, len(complete_seeds)),
        "v2_estimate": estimate2,
        "v2_ci95": ci2,
        "v2_label": label(ci2, q2, 0.05, len(complete_seeds)),
        "v3_estimate": estimate3,
        "v3_ci95": ci3,
        "miss_rate": rates(miss_counts),
        "false_alarm_rate": rates(false_alarm_counts),
        "choices": CHOICES,
    }
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()
