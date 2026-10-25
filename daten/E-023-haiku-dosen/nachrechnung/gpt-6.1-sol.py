#!/usr/bin/env python3
import itertools
import json
import math
import os
import random
import re
import sys

DRAWS = 5000
SEEDS = tuple(range(6000, 6024))
ITEMS_PER_SEED = 12
CELLS = tuple(itertools.product((0, 1), repeat=3))
CELL_RE = re.compile(r"SP([01])-ZU([01])-AU([01])")

CHOICES = [
    "Analyze the primary, all-items E-023 run only; retain all items, including "
    "coding-fail_moderate-6021. Secondary analyses, sensitivities, and model "
    "interactions are outside the requested output.",
    "Restrict material seeds to 6000–6023 and ignore other seeds. Expect 12 "
    "distinct item IDs per seed, as implied by 288 items over 24 seeds. A seed "
    "is complete only if all 12 items have all eight cells with Boolean verdicts.",
    "Use the final physical line for each (seed, item ID, cell), even if its "
    "verdict is missing or invalid. Only JSON true and false are valid verdicts.",
    "Use cell names as the factor encoding and reject contradictory redundant "
    "SP/ZU/AU fields. Reject inconsistent truth or primary metadata across "
    "retained cells of an item; do not infer or repair metadata.",
    "Do not pool different models. Reject multiple model names in the retained "
    "main-run records; a single model name is treated as the supplied run.",
    "Sort items by (seed, item ID) before resampling. Resample items independently "
    "with replacement, not seeds or individual judgments.",
    "For V1 use broken items with primary=true; for V2 use all broken items; "
    "for V3 use all items, including working items. Average each factor level "
    "equally over its other eligible cells before taking level 1 minus level 0.",
    "Use 5000 ordinary bootstrap draws and independent Python random.Random "
    "streams: 201 for V1 CI, 202 for V2 CI, 203 for V3 CI, and 211/212 for "
    "V1/V2 bootstrap tests. The preregistration does not explicitly map V3 "
    "to a start value; choose 203.",
    "Compute percentile endpoints by linear interpolation at (B-1)*p in the "
    "sorted bootstrap estimates, for p=0.025 and p=0.975.",
    "The preregistration does not define the p-values needed for BH. Use "
    "two-sided, null-centered nonparametric bootstrap tests: count draws with "
    "|bootstrap mean - observed mean| >= |observed mean|, with add-one "
    "correction (count+1)/(5000+1). Apply standard BH adjustment jointly to "
    "V1 and V2 only.",
    "The decision-rule labels overlap. Give priority to 'praktisch null', then "
    "'Vorhersage widerlegt', then 'Vorhersage gestützt', otherwise "
    "'nicht entschieden'. Practical null is the stated upper-bound criterion, "
    "not a two-sided equivalence claim; estimates and intervals retain direction.",
    "Use 'nur deskriptiv' for V1/V2 when fewer than 16 seeds are complete. "
    "For E-023 also use that label if mean run_check use at ZU=1 is below 1 "
    "or any cell has more than 5% missing verdicts. Continue reporting estimates "
    "and intervals in these cases.",
    "For the E-023 technical gates, use all planned main-run trials after "
    "deduplication: absent trials contribute zero run_check calls and count "
    "as missing verdicts. Each cell has 24*12 planned trials.",
    "No numerical threshold defines 'misses almost everything'; do not invent "
    "a floor-effect cutoff or automatically suppress inference for that reason.",
    "Compute miss and false-alarm rates from complete seeds only, on all broken "
    "and all working items respectively. Return null for an empty denominator "
    "or unavailable estimate/interval.",
    "Do not make discretionary ground-truth exclusions: raw judgments alone "
    "cannot establish the manual generator-error exclusion criterion.",
]


def cell_name(cell):
    return "SP%d-ZU%d-AU%d" % cell


def mean(values):
    return math.fsum(values) / len(values) if values else None


def percentile(sorted_values, p):
    position = (len(sorted_values) - 1) * p
    lo = int(math.floor(position))
    hi = int(math.ceil(position))
    fraction = position - lo
    return (
        sorted_values[lo] * (1.0 - fraction)
        + sorted_values[hi] * fraction
    )


def bootstrap_means(values, seed):
    rng = random.Random(seed)
    n = len(values)
    return [
        math.fsum(rng.choices(values, k=n)) / n
        for _ in range(DRAWS)
    ]


def estimate_and_ci(values, seed):
    if not values:
        return None, None
    draws = sorted(bootstrap_means(values, seed))
    return mean(values), [
        percentile(draws, 0.025),
        percentile(draws, 0.975),
    ]


def bootstrap_p(values, seed):
    if not values:
        return None
    observed = mean(values)
    # Centering each item at the observed mean is equivalent to subtracting
    # the observed mean from each ordinary bootstrap replicate.
    draws = bootstrap_means(values, seed)
    count = sum(
        abs(draw - observed) >= abs(observed)
        for draw in draws
    )
    return (count + 1) / (DRAWS + 1)


def bh_adjust(p_values):
    if any(p is None for p in p_values):
        # Both preregistered tests are required for this two-test family.
        return [None] * len(p_values)
    order = sorted(range(len(p_values)), key=lambda i: (p_values[i], i))
    adjusted = [None] * len(p_values)
    running = 1.0
    m = len(p_values)
    for rank_index in range(m - 1, -1, -1):
        i = order[rank_index]
        running = min(running, p_values[i] * m / (rank_index + 1))
        adjusted[i] = min(1.0, running)
    return adjusted


def label(ci, q_value, target, descriptive):
    if ci is None:
        return "nur deskriptiv"
    if descriptive:
        return "nur deskriptiv"
    lower, upper = ci
    if upper < 0.02:
        return "praktisch null"
    if upper < target:
        return "Vorhersage widerlegt"
    if lower > 0 and q_value is not None and q_value <= 0.05:
        return "Vorhersage gestützt"
    return "nicht entschieden"


def main():
    if len(sys.argv) != 2:
        raise ValueError("Expected exactly one argument: the data directory")

    latest = {}
    path = os.path.join(sys.argv[1], "judgments.jsonl")
    with open(path, "r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            # JSONL requires one object on every line; blank lines are errors.
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError("Non-object JSON on line %d" % line_number)
            seed = row.get("seed")
            if type(seed) is not int:
                raise ValueError("Seed must be an integer")
            if seed not in SEEDS:
                continue
            item_id = row.get("id")
            if not isinstance(item_id, str) or not item_id:
                raise ValueError("Item ID must be a nonempty string")
            match = CELL_RE.fullmatch(str(row.get("cell", "")))
            if match is None:
                raise ValueError("Invalid cell name")
            cell = tuple(map(int, match.groups()))
            latest[(seed, item_id, cell)] = row

    grouped = {seed: {} for seed in SEEDS}
    models = set()

    for (seed, item_id, cell), row in latest.items():
        for field, level in zip(("SP", "ZU", "AU"), cell):
            if field in row and (
                type(row[field]) is not int or row[field] != level
            ):
                raise ValueError("Contradictory factor field: " + field)
        if type(row.get("truth")) is not bool:
            raise ValueError("truth must be Boolean")
        if type(row.get("primary")) is not bool:
            raise ValueError("primary must be Boolean")
        checks = row.get("n_checks")
        if type(checks) is not int or checks < 0:
            raise ValueError("n_checks must be a nonnegative integer")
        if row.get("model") is not None:
            if not isinstance(row["model"], str):
                raise ValueError("model must be a string")
            models.add(row["model"])
        grouped[seed].setdefault(item_id, {})[cell] = row

    if len(models) > 1:
        raise ValueError("Multiple models cannot be pooled")

    complete_seeds = []
    for seed in SEEDS:
        items = grouped[seed]
        if len(items) > ITEMS_PER_SEED:
            raise ValueError("More than 12 item IDs in seed %d" % seed)
        for item_id, rows in items.items():
            metadata = {(r["truth"], r["primary"]) for r in rows.values()}
            if len(metadata) != 1:
                raise ValueError(
                    "Inconsistent item metadata: %d/%s" % (seed, item_id)
                )
        if len(items) == ITEMS_PER_SEED and all(
            len(rows) == len(CELLS)
            and all(type(rows[c].get("verdict")) is bool for c in CELLS)
            for rows in items.values()
        ):
            complete_seeds.append(seed)

    # Planned-trial technical checks include incomplete and wholly absent seeds.
    planned_per_cell = len(SEEDS) * ITEMS_PER_SEED
    valid_by_cell = {cell: 0 for cell in CELLS}
    access_checks = 0
    for (_, _, cell), row in latest.items():
        if type(row.get("verdict")) is bool:
            valid_by_cell[cell] += 1
        if cell[1] == 1:
            access_checks += row["n_checks"]
    failure_rates = {
        cell: 1.0 - valid_by_cell[cell] / planned_per_cell
        for cell in CELLS
    }
    access_mean = access_checks / (planned_per_cell * 4)
    technical_failure = (
        access_mean < 1.0
        or any(rate > 0.05 for rate in failure_rates.values())
    )
    descriptive = len(complete_seeds) < 16 or technical_failure

    v1, v2, v3 = [], [], []
    misses = {cell: [] for cell in CELLS}
    false_alarms = {cell: [] for cell in CELLS}

    def contrast(rows, factor_index, value, eligible=CELLS):
        level_one = [value(rows[c]) for c in eligible if c[factor_index] == 1]
        level_zero = [value(rows[c]) for c in eligible if c[factor_index] == 0]
        return mean(level_one) - mean(level_zero)

    access_cells = tuple(c for c in CELLS if c[1] == 1)
    for seed in complete_seeds:
        for item_id in sorted(grouped[seed]):
            rows = grouped[seed][item_id]
            metadata = rows[CELLS[0]]
            broken = not metadata["truth"]
            if broken:
                for cell in CELLS:
                    misses[cell].append(int(rows[cell]["verdict"]))
                item_v2 = contrast(rows, 2, lambda r: int(r["verdict"]))
                v2.append(item_v2)
                if metadata["primary"]:
                    v1.append(contrast(rows, 0, lambda r: int(r["verdict"])))
            else:
                for cell in CELLS:
                    false_alarms[cell].append(int(not rows[cell]["verdict"]))
            v3.append(
                contrast(rows, 2, lambda r: r["n_checks"], access_cells)
            )

    e1, ci1 = estimate_and_ci(v1, 201)
    e2, ci2 = estimate_and_ci(v2, 202)
    e3, ci3 = estimate_and_ci(v3, 203)
    q1, q2 = bh_adjust([bootstrap_p(v1, 211), bootstrap_p(v2, 212)])

    result = {
        "n_complete_seeds": len(complete_seeds),
        "v1_estimate": e1,
        "v1_ci95": ci1,
        "v1_label": label(ci1, q1, 0.10, descriptive),
        "v2_estimate": e2,
        "v2_ci95": ci2,
        "v2_label": label(ci2, q2, 0.05, descriptive),
        "v3_estimate": e3,
        "v3_ci95": ci3,
        "miss_rate": {cell_name(c): mean(misses[c]) for c in CELLS},
        "false_alarm_rate": {
            cell_name(c): mean(false_alarms[c]) for c in CELLS
        },
        "choices": CHOICES,
    }
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()
