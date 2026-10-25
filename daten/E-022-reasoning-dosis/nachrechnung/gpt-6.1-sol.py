#!/usr/bin/env python3
import json
import math
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ARMS = ("low", "medium", "high", "ohne")
POSITIONS = (0, 1, 2)
MODEL = "anthropic/claude-sonnet-5.5"
CELL = "I1-S0-E0"
SEED = 22022
N_BOOTSTRAP = 10000

CHOICES = [
    "Use random.Random(22022) and 10000 paired batch-bootstrap draws.",
    "Represent null effort as the output arm name 'ohne'.",
    "Treat the supplied files as this experiment's data; reject unexpected "
    "models, cells, arms, positions, or call attempts rather than silently filtering.",
    "For retries, use the highest recorded attempt (0, 1, or 2) for each "
    "batch/arm/position; do not pool attempts or select the most favorable attempt.",
    "Judgments without an attempt field are treated as the final retained "
    "judgments. If judgments have attempt fields, use only the selected call's "
    "attempt. Reject mixtures of these formats within a batch/arm/position.",
    "Collapse identical duplicate records; reject conflicting duplicates because "
    "the files do not otherwise identify which duplicate to use.",
    "Require each complete batch to contain the same 12 item IDs in all four "
    "arms and all three positions, with consistent truth and slot assignments. "
    "Require both the selected call's parsed count and its observed nonmissing "
    "judgments to meet 95%. With 12 items, this requires all 12 judgments; "
    "missing judgments are not imputed or counted as errors.",
    "Compute completion-token medians over selected final calls from complete "
    "batches only, giving every call equal weight and using the arithmetic "
    "midpoint for an even number of observations. Require valid token counts.",
    "Average the three binary channel errors within each item, then average "
    "equally over eligible items, not equally over batch-specific rates.",
    "Resample complete batches uniformly with replacement, drawing the original "
    "number of batches and keeping all arms, items, and positions together. "
    "Recompute item-weighted contrasts using the sampled batch multiplicities.",
    "Use percentile bootstrap bounds: the 5th percentile for P1 and the 95th "
    "percentile for P2, with linear interpolation at index (n-1)*p.",
    "Make exactly 10000 bootstrap draws when at least one batch is complete. "
    "For each contrast, omit bootstrap replicates with no items of its truth "
    "class from that contrast's quantile calculation; return null if undefined.",
    "Return null for rates, estimates, medians, or bounds that cannot be "
    "calculated. Undefined conditions cannot confirm the hypothesis.",
    "Below 16 complete batches, report bootstrap bounds only as descriptive "
    "uncertainty and force h_confirmed to false.",
    "Use P1 estimate > 0 and lower bound > 0 for confirmation; +0.05 is a "
    "relevance benchmark, not an additional confirmation threshold. "
    "Use P2 upper bound <= 0.03.",
    "Do not infer generator errors from unanimous alarms or automatically "
    "exclude them. These two files contain no documented manual adjudication, "
    "so report the analysis without generator-error exclusions; an adjudicated "
    "with-exclusion analysis cannot be reconstructed from these inputs."
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_jsonl(path):
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            require(isinstance(row, dict),
                    "{}:{}: expected an object".format(path.name, line_number))
            yield row


def arm_of(row):
    require("effort" in row, "Missing effort field")
    arm = "ohne" if row["effort"] is None else row["effort"]
    require(arm in ARMS, "Unexpected effort")
    return arm


def group_key(row):
    require(row.get("model") == MODEL, "Unexpected model")
    require(row.get("cell") == CELL, "Unexpected cell")
    require(isinstance(row.get("batch"), str), "Invalid batch identifier")
    position = row.get("position")
    require(type(position) is int and position in POSITIONS,
            "Unexpected position")
    return row["batch"], arm_of(row), position


def valid_attempt(value):
    return type(value) is int and value in (0, 1, 2)


def insert_unique(mapping, key, row, description):
    if key in mapping:
        require(mapping[key] == row, "Conflicting duplicate " + description)
    else:
        mapping[key] = row


def quantile(values, probability):
    if not values:
        return None
    values = sorted(values)
    index = (len(values) - 1) * probability
    lower = math.floor(index)
    upper = math.ceil(index)
    fraction = index - lower
    return values[lower] * (1.0 - fraction) + values[upper] * fraction


def main():
    require(len(sys.argv) == 2, "Expected exactly one data-directory argument")
    directory = Path(sys.argv[1])

    calls = defaultdict(dict)
    judgment_groups = defaultdict(list)
    batches = set()

    for row in read_jsonl(directory / "calls.jsonl"):
        key = group_key(row)
        attempt = row.get("attempt")
        require(valid_attempt(attempt), "Invalid call attempt")
        require(type(row.get("size")) is int and row["size"] == 12,
                "Expected calls containing 12 items")
        require(type(row.get("parsed")) is int
                and 0 <= row["parsed"] <= 12, "Invalid parsed count")
        insert_unique(calls[key], attempt, row, "call")
        batches.add(key[0])

    truth_by_item = {}
    batch_by_item = {}
    slot_by_batch_item = {}
    item_by_batch_slot = {}

    for row in read_jsonl(directory / "judgments.jsonl"):
        key = group_key(row)
        item = row.get("id")
        slot = row.get("slot")
        require(isinstance(item, str), "Invalid item ID")
        require(type(slot) is int and 1 <= slot <= 12, "Invalid item slot")
        require(type(row.get("truth")) is bool, "Invalid truth value")
        verdict = row.get("verdict")
        require("verdict" in row
                and (verdict is None or type(verdict) is bool),
                "Invalid verdict")
        if "attempt" in row:
            require(valid_attempt(row["attempt"]), "Invalid judgment attempt")

        if item in truth_by_item:
            require(truth_by_item[item] == row["truth"],
                    "Inconsistent ground truth")
            require(batch_by_item[item] == key[0],
                    "Item appears in multiple batches")
        truth_by_item[item] = row["truth"]
        batch_by_item[item] = key[0]

        bi = (key[0], item)
        bs = (key[0], slot)
        require(bi not in slot_by_batch_item
                or slot_by_batch_item[bi] == slot,
                "Inconsistent item slot")
        require(bs not in item_by_batch_slot
                or item_by_batch_slot[bs] == item,
                "Multiple items assigned to the same slot")
        slot_by_batch_item[bi] = slot
        item_by_batch_slot[bs] = item

        judgment_groups[key].append(row)
        batches.add(key[0])

    selected_calls = {
        key: attempts[max(attempts)] for key, attempts in calls.items()
    }
    selected_judgments = {}

    for key, rows in judgment_groups.items():
        tagged = ["attempt" in row for row in rows]
        require(all(tagged) or not any(tagged),
                "Mixed attempted and untagged judgments")
        selected = {}
        if key in selected_calls:
            attempt = selected_calls[key]["attempt"]
            for row in rows:
                if all(tagged) and row["attempt"] != attempt:
                    continue
                insert_unique(selected, row["id"], row, "judgment")
        selected_judgments[key] = selected

    complete = []
    for batch in sorted(batches):
        reference_items = None
        eligible = True
        for arm in ARMS:
            for position in POSITIONS:
                key = (batch, arm, position)
                call = selected_calls.get(key)
                rows = selected_judgments.get(key, {})
                if call is None or call["parsed"] * 100 < 95 * call["size"]:
                    eligible = False
                    continue
                observed = sum(row["verdict"] is not None
                               for row in rows.values())
                if len(rows) != 12 or observed * 100 < 95 * call["size"]:
                    eligible = False
                items = set(rows)
                if reference_items is None:
                    reference_items = items
                elif items != reference_items:
                    eligible = False
        if eligible:
            complete.append(batch)

    tokens = {arm: [] for arm in ARMS}
    # Each cluster stores class counts and sums of item-level error rates.
    clusters = []
    total_counts = [0, 0]  # working, broken
    total_errors = {arm: [0.0, 0.0] for arm in ARMS}

    for batch in complete:
        counts = [0, 0]
        errors = {arm: [0.0, 0.0] for arm in ARMS}
        items = sorted(selected_judgments[(batch, "low", 0)])
        for arm in ARMS:
            for position in POSITIONS:
                value = selected_calls[(batch, arm, position)].get(
                    "completion_tokens")
                require(type(value) in (int, float)
                        and math.isfinite(value) and value >= 0,
                        "Missing or invalid completion-token count")
                tokens[arm].append(value)

        for item in items:
            truth = truth_by_item[item]
            category = 0 if truth else 1
            counts[category] += 1
            for arm in ARMS:
                item_error = sum(
                    selected_judgments[(batch, arm, position)][item]["verdict"]
                    != truth
                    for position in POSITIONS
                ) / 3.0
                errors[arm][category] += item_error

        clusters.append((counts, errors))
        for category in (0, 1):
            total_counts[category] += counts[category]
            for arm in ARMS:
                total_errors[arm][category] += errors[arm][category]

    def rate(arm, category):
        denominator = total_counts[category]
        return (total_errors[arm][category] / denominator
                if denominator else None)

    false_alarm = {arm: rate(arm, 0) for arm in ARMS}
    miss = {arm: rate(arm, 1) for arm in ARMS}
    medians = {
        arm: statistics.median(tokens[arm]) if tokens[arm] else None
        for arm in ARMS
    }

    p1 = (false_alarm["low"] - false_alarm["high"]
          if total_counts[0] else None)
    p2 = (miss["high"] - miss["low"] if total_counts[1] else None)

    bootstrap_p1 = []
    bootstrap_p2 = []
    rng = random.Random(SEED)
    n = len(clusters)

    if n:
        # Preaggregate within clusters; multiplicity in a draw still weights
        # every original item equally rather than weighting batches equally.
        summaries = [
            (
                counts[0],
                counts[1],
                errors["low"][0] - errors["high"][0],
                errors["high"][1] - errors["low"][1]
            )
            for counts, errors in clusters
        ]
        for _ in range(N_BOOTSTRAP):
            count_ok = count_broken = 0
            delta_fa = delta_miss = 0.0
            for _ in range(n):
                ok, broken, fa_difference, miss_difference = summaries[
                    rng.randrange(n)
                ]
                count_ok += ok
                count_broken += broken
                delta_fa += fa_difference
                delta_miss += miss_difference
            if count_ok:
                bootstrap_p1.append(delta_fa / count_ok)
            if count_broken:
                bootstrap_p2.append(delta_miss / count_broken)

    lower = quantile(bootstrap_p1, 0.05)
    upper = quantile(bootstrap_p2, 0.95)

    manipulation = (
        all(medians[arm] is not None for arm in ("low", "medium", "high"))
        and medians["low"] < medians["medium"] < medians["high"]
        and medians["high"] >= 1.5 * medians["low"]
    )
    confirmed = (
        n >= 16
        and manipulation
        and p1 is not None and p1 > 0
        and lower is not None and lower > 0
        and p2 is not None
        and upper is not None and upper <= 0.03
    )

    result = {
        "n_complete_batches": n,
        "median_completion_tokens": medians,
        "manipulation_check_passed": bool(manipulation),
        "p1_estimate": p1,
        "p1_lower_bound_one_sided_95": lower,
        "p2_estimate": p2,
        "p2_upper_bound_one_sided_95": upper,
        "false_alarm_rate": false_alarm,
        "miss_rate": miss,
        "h_confirmed": bool(confirmed),
        "choices": CHOICES
    }
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()
