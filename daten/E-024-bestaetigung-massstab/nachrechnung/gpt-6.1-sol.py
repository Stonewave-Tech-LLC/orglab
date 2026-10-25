#!/usr/bin/env python3
"""Recompute the five preregistered E-024 primary contrasts (stdlib only)."""

import itertools
import json
import math
import random
import sys
from pathlib import Path

TARGET = "anthropic/claude-haiku-5.5"
COMPARISON = "anthropic/claude-sonnet-5.5"
MODELS = (TARGET, COMPARISON)
SEEDS = set(range(7000, 7024))
CELLS = tuple(itertools.product((0, 1), repeat=3))
NAMES = ("V1", "W1", "C1", "C2", "F1")
PREDICTIONS = dict(zip(NAMES, (0.10, 0.10, 0.20, 0.10, 0.02)))
B = 5000

CHOICES = [
    "The latest pre-start amendments control: F1 uses only non-excluded "
    "true items; F1 without statistical evidence receives the weak-power "
    "label, never a refutation label.",
    "Primary V1/W1/C1/C2 retain all eligible items, including single-channel "
    "exclusions and coding-ok_clear-7009. No manual generator-error exclusions "
    "or secondary/sensitivity analyses are applied.",
    "Only the two specified models and material seeds 7000–7023 are analysed. "
    "Duplicate model/item/cell records are resolved by physical JSONL order, "
    "keeping the last record.",
    "The item roster for each seed is the union of item IDs observed in either "
    "model. Completeness requires every roster item in all eight cells of "
    "both models, with Boolean verdicts. Entirely absent items in both models "
    "cannot be detected without a material manifest; 288/24 is not assumed "
    "to imply exactly 12 items in every seed.",
    "A verdict of true on a false, primary item is an oversight; a verdict "
    "of false on a true item is a false alarm. Missing verdicts are not "
    "recoded as judgments.",
    "Cell differences are first averaged within item over the unspecified "
    "factors. Items receive equal weight. W1 is formed by subtracting the "
    "two model-specific V1 differences for each identical item.",
    "Bootstrap sampling resamples item-level differences independently with "
    "replacement, not seeds or individual cells. Item order is (seed, ID). "
    "Python random.Random.randrange is used; each CI and each p-value gets "
    "its own freshly initialized generator with the preregistered seed.",
    "The unspecified one-sided bootstrap-p convention is chosen as the "
    "uncentered bootstrap proportion of means <= 0, with a plus-one Monte "
    "Carlo correction: (count + 1)/(5000 + 1). Ties count against a positive "
    "effect. CI and p-value bootstrap draws are independent.",
    "CI endpoints use exactly sorted indices floor(0.025*5000) and "
    "floor(0.975*5000)-1, without interpolation. BH uses all five Haiku "
    "predictions, including the paired W1; Sonnet entries are point estimates.",
    "For overlapping labels, statistically evidenced effects are classified "
    "first; otherwise F1 gets its weak-power exception, then practically null "
    "takes precedence over prediction excluded.",
    "Manipulation checks use n_checks as the recorded run_check count. "
    "For each model its mean is over recorded ZU=1 judgments, including "
    "null verdicts. Missing judgment rows are not assigned invented tool "
    "counts; a recorded missing/invalid n_checks makes the check unverifiable.",
    "Failure rates use the last records before complete-seed deletion. "
    "For each model/cell the denominator is the observed union item roster "
    "across started study seeds; absent rows and null verdicts are failures. "
    "Wholly unobserved seeds are not treated as attempted trials.",
    "If either model fails a manipulation check, or a required check cannot "
    "be verified, all five labels are descriptive only, following the final "
    "amendment. Fewer than 16 complete seeds also makes all labels descriptive. "
    "Numerical bootstrap summaries remain reported when computable.",
    "SPEC/AUSKUNFT code tests and transcript-based tool-round diagnostics "
    "cannot be reconstructed from these judgments; the supplied design "
    "coding is checked for internal consistency, not treated as an independent "
    "prompt-manipulation test.",
    "The exclusion-file schema was not specified. Accepted explicit formats "
    "are a list of IDs or objects with an id field, an object containing "
    "exactly one of excluded_ids/excluded/ids/ausschluss with such a list, "
    "or an ID-keyed object whose values are metadata objects or null. "
    "No exclusions are inferred from judgments, item names, or truth.",
    "An empty contrast has null estimate, [null,null] CI and null q. If any "
    "of the five contrasts is empty, the five-test BH family is unavailable "
    "and all q values are null."
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def exclusion_ids(path):
    with path.open("r", encoding="utf-8") as handle:
        obj = json.load(handle)

    if isinstance(obj, dict):
        wrappers = [
            key for key in ("excluded_ids", "excluded", "ids", "ausschluss")
            if key in obj
        ]
        if wrappers:
            require(len(wrappers) == 1,
                    "Ambiguous exclusion-file wrapper keys")
            obj = obj[wrappers[0]]
        else:
            # Only accept an unmistakable ID-keyed mapping.
            require(
                bool(obj)
                and all(
                    isinstance(key, str)
                    and key.rsplit("-", 1)[-1] in
                    {str(seed) for seed in SEEDS}
                    and (value is None or isinstance(value, dict))
                    for key, value in obj.items()
                ),
                "Unsupported exclusion-file schema; supply an explicit ID list"
            )
            obj = list(obj)

    require(isinstance(obj, list),
            "Exclusions must be an explicit list")
    result = set()
    for entry in obj:
        item_id = entry.get("id") if isinstance(entry, dict) else entry
        require(isinstance(item_id, str) and bool(item_id),
                "Every exclusion must contain a nonempty string ID")
        result.add(item_id)
    return result


def read_records(path):
    latest = {}
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            require(isinstance(row, dict),
                    "JSONL line %d is not an object" % line_number)
            if row.get("model") not in MODELS:
                continue
            seed = row.get("seed")
            require(type(seed) is int,
                    "Study records must have integer seed fields")
            if seed not in SEEDS:
                continue

            item_id = row.get("id")
            require(isinstance(item_id, str) and bool(item_id),
                    "Missing or invalid item ID")
            cell = tuple(row.get(key) for key in ("SP", "ZU", "AU"))
            require(all(type(x) is int and x in (0, 1) for x in cell),
                    "SP/ZU/AU must be binary integers")
            expected_cell = "SP%d-ZU%d-AU%d" % cell
            require(row.get("cell") == expected_cell,
                    "Cell name disagrees with SP/ZU/AU for " + item_id)
            latest[(row["model"], item_id, cell)] = row

    metadata = {}
    rosters = {}
    for (_, item_id, _), row in latest.items():
        require(type(row.get("truth")) is bool,
                "truth must be Boolean for " + item_id)
        require(type(row.get("primary")) is bool,
                "primary must be Boolean for " + item_id)
        require("verdict" in row and
                (row["verdict"] is None or type(row["verdict"]) is bool),
                "verdict must be Boolean or null for " + item_id)
        require(not (row["truth"] and row["primary"]),
                "A primary broken item cannot have truth=true: " + item_id)
        info = (row["seed"], row["truth"], row["primary"])
        if item_id in metadata:
            require(metadata[item_id] == info,
                    "Inconsistent item metadata for " + item_id)
        else:
            metadata[item_id] = info
        rosters.setdefault(row["seed"], set()).add(item_id)

    return latest, metadata, rosters


def check_manipulations(records, rosters):
    reasons = []
    total_items = sum(len(ids) for ids in rosters.values())
    if not total_items:
        return ["No study records: manipulation checks are unavailable."]

    for model in MODELS:
        for cell in CELLS:
            failures = sum(
                1
                for ids in rosters.values()
                for item_id in ids
                if (model, item_id, cell) not in records
                or records[(model, item_id, cell)]["verdict"] is None
            )
            if failures / total_items > 0.05:
                reasons.append(
                    "%s %s failure rate %d/%d exceeds 5%%."
                    % (model, "SP%d-ZU%d-AU%d" % cell,
                       failures, total_items)
                )

        rows = [
            row for (m, _, cell), row in records.items()
            if m == model and cell[1] == 1
        ]
        counts = [row.get("n_checks") for row in rows]
        valid = bool(counts) and all(
            type(value) in (int, float)
            and math.isfinite(value)
            and value >= 0
            for value in counts
        )
        if not valid:
            reasons.append(model + " run_check manipulation check unavailable.")
        else:
            average = math.fsum(counts) / len(counts)
            if average < 1.0:
                reasons.append(
                    "%s mean n_checks at ZU=1 is %.12g, below 1."
                    % (model, average)
                )
    return reasons


def complete_seeds(records, rosters):
    result = []
    for seed in sorted(rosters):
        if all(
            (model, item_id, cell) in records
            and type(records[(model, item_id, cell)]["verdict"]) is bool
            for item_id in rosters[seed]
            for model in MODELS
            for cell in CELLS
        ):
            result.append(seed)
    return result


def item_contrasts(records, model, item_id, truth, primary, excluded):
    def verdict(sp, zu, au):
        return records[(model, item_id, (sp, zu, au))]["verdict"]

    result = {}
    if not truth and primary:
        result["V1"] = math.fsum(
            int(verdict(1, zu, au)) - int(verdict(0, zu, au))
            for zu in (0, 1) for au in (0, 1)
        ) / 4.0
        result["C2"] = math.fsum(
            int(verdict(1, 1, au)) - int(verdict(1, 0, au))
            for au in (0, 1)
        ) / 2.0

    lookup = {}
    for zu in (0, 1):
        for au in (0, 1):
            value = records[(model, item_id, (1, zu, au))].get("looked_up")
            require(type(value) is bool,
                    "Missing/non-Boolean looked_up for retained item " + item_id)
            lookup[(zu, au)] = int(value)
    result["C1"] = math.fsum(
        lookup[(0, au)] - lookup[(1, au)] for au in (0, 1)
    ) / 2.0

    if truth and item_id not in excluded:
        result["F1"] = math.fsum(
            int(not verdict(sp, zu, 1)) - int(not verdict(sp, zu, 0))
            for sp in (0, 1) for zu in (0, 1)
        ) / 4.0
    return result


def mean(values):
    return math.fsum(values) / len(values) if values else None


def bootstrap_means(values, seed):
    rng = random.Random(seed)
    n = len(values)
    return [
        math.fsum(values[rng.randrange(n)] for _ in range(n)) / n
        for _ in range(B)
    ]


def bootstrap_summary(values, ci_seed, p_seed):
    if not values:
        return None, [None, None], None
    interval_draws = sorted(bootstrap_means(values, ci_seed))
    ci = [
        interval_draws[math.floor(0.025 * B)],
        interval_draws[math.floor(0.975 * B) - 1],
    ]
    p_draws = bootstrap_means(values, p_seed)
    p = (1 + sum(value <= 0.0 for value in p_draws)) / (B + 1)
    return mean(values), ci, p


def bh_adjust(p_values):
    if any(p is None for p in p_values):
        return [None] * len(p_values)
    m = len(p_values)
    order = sorted(range(m), key=lambda index: (p_values[index], index))
    result = [None] * m
    running = 1.0
    for position in range(m - 1, -1, -1):
        index = order[position]
        running = min(running, p_values[index] * m / (position + 1))
        result[index] = running
    return result


def label(name, ci, q, descriptive_reasons):
    if descriptive_reasons:
        return "nur deskriptiv (" + "; ".join(descriptive_reasons) + ")"
    if q is None or ci[0] is None:
        return "nur deskriptiv (Kontrast oder BH-Familie nicht auswertbar)"

    lower, upper = ci
    evidenced = lower > 0.0 and q <= 0.05
    if evidenced:
        if upper >= PREDICTIONS[name]:
            return "BESTÄTIGT (Vorhersagewert nicht ausgeschlossen)"
        return "BESTÄTIGT, aber kleiner als vorhergesagt"
    if name == "F1":
        return "nicht bestätigt (schwache Power, kein Widerlegen)"
    if upper < 0.02:
        return "nicht bestätigt: praktisch null (widerlegt)"
    if upper < PREDICTIONS[name]:
        return "nicht bestätigt: Vorhersagewert ausgeschlossen (widerlegt)"
    return "nicht bestätigt: nicht entschieden"


def main():
    require(len(sys.argv) == 2,
            "Usage: python3 analysis.py DATA_DIRECTORY")
    directory = Path(sys.argv[1])

    # Mandatory even if no retained items would use it.
    excluded = exclusion_ids(directory / "einzelkanal-ausschluss.json")
    records, metadata, rosters = read_records(directory / "judgments.jsonl")
    complete = complete_seeds(records, rosters)
    manipulation_reasons = check_manipulations(records, rosters)

    values = {name: [] for name in NAMES}
    sonnet = {name: [] for name in ("V1", "C1", "C2", "F1")}

    for seed in complete:
        for item_id in sorted(rosters[seed]):
            _, truth, primary = metadata[item_id]
            target = item_contrasts(
                records, TARGET, item_id, truth, primary, excluded
            )
            comparison = item_contrasts(
                records, COMPARISON, item_id, truth, primary, excluded
            )
            for name, value in target.items():
                values[name].append(value)
            for name, value in comparison.items():
                sonnet[name].append(value)
            if "V1" in target:
                values["W1"].append(target["V1"] - comparison["V1"])

    summaries = {}
    p_values = []
    for index, name in enumerate(NAMES):
        estimate, ci, p = bootstrap_summary(
            values[name], 241 + index, 251 + index
        )
        summaries[name] = (estimate, ci)
        p_values.append(p)
    q_values = bh_adjust(p_values)

    descriptive_reasons = []
    if len(complete) < 16:
        descriptive_reasons.append("weniger als 16 vollständige Seeds")
    if manipulation_reasons:
        descriptive_reasons.append(
            "Manipulationscheck gescheitert oder nicht verifizierbar"
        )

    choices = list(CHOICES)
    if manipulation_reasons:
        choices.append(
            "Observed manipulation-check problems: "
            + " ".join(manipulation_reasons)
        )
    if any(p is None for p in p_values):
        choices.append(
            "At least one primary contrast is empty; the five-test BH "
            "adjustment is therefore not computable."
        )

    result = {"n_complete_seeds": len(complete)}
    for index, name in enumerate(NAMES):
        estimate, ci = summaries[name]
        q = q_values[index]
        result[name + "_estimate"] = estimate
        result[name + "_ci95"] = ci
        result[name + "_q"] = q
        result[name + "_label"] = label(
            name, ci, q, descriptive_reasons
        )
    for name in ("V1", "C1", "C2", "F1"):
        result["sonnet_" + name.lower()] = mean(sonnet[name])
    result["choices"] = choices

    print(json.dumps(result, ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError) as exc:
        # Invalid/missing inputs abort rather than silently changing analysis.
        sys.stderr.write("Analysis aborted: %s\n" % exc)
        sys.exit(1)
