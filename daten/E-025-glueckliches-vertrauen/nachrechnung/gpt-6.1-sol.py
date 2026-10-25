import json
import sys
import random
import itertools
from pathlib import Path


ARMS = ("A", "B")
SEEDS = tuple(range(8000, 8016))
CELLS = tuple(itertools.product((0, 1), repeat=3))
PLANNED_ITEMS = 192
ITEMS_PER_SEED = 12
DRAWS = 5000
CI_SEEDS = {"K0": 341, "R1": 342, "R2": 343, "K3": 344}
P_SEEDS = {"R1": 352, "R2": 353}


def percentile(sorted_values, probability):
    """Linearly interpolated empirical percentile (index (B - 1) * p)."""
    position = (len(sorted_values) - 1) * probability
    lower = int(position)
    upper = min(lower + 1, len(sorted_values) - 1)
    fraction = position - lower
    return (
        sorted_values[lower] * (1.0 - fraction)
        + sorted_values[upper] * fraction
    )


def bootstrap_means(values, seed):
    """Ordinary item bootstrap: n independent item draws, with replacement."""
    rng = random.Random(seed)
    n = len(values)
    means = []
    for _ in range(DRAWS):
        total = 0.0
        for _ in range(n):
            total += values[rng.randrange(n)]
        means.append(total / n)
    return means


def summarize(values, ci_seed):
    if not values:
        return {
            "estimate": None,
            "ci95": [None, None],
            "q": None,
            "n": 0,
            "label": "deskriptiv",
            "confirmed": False,
            "comparison": None,
        }
    means = sorted(bootstrap_means(values, ci_seed))
    return {
        "estimate": float(sum(values) / len(values)),
        "ci95": [
            percentile(means, 0.025),
            percentile(means, 0.975),
        ],
        "q": None,
        "n": len(values),
        "label": "deskriptiv",
        "confirmed": False,
        "comparison": None,
    }


def bootstrap_p(values, seed):
    if not values:
        return None
    means = bootstrap_means(values, seed)
    # Explicitly chosen convention for the otherwise unspecified bootstrap p:
    # opposite-direction tail of the ordinary, uncentered bootstrap.
    nonpositive = sum(value <= 0.0 for value in means)
    return (nonpositive + 1.0) / (DRAWS + 1.0)


def bh_four(pvalues):
    """BH adjustment over all four planned tests, including unestimable ones."""
    ordered = sorted(
        pvalues,
        key=lambda key: (
            1.0 if pvalues[key] is None else pvalues[key],
            key,
        ),
    )
    adjusted = {}
    running = 1.0
    for index in range(len(ordered) - 1, -1, -1):
        key = ordered[index]
        p = 1.0 if pvalues[key] is None else pvalues[key]
        running = min(running, p * 4.0 / (index + 1))
        adjusted[key] = None if pvalues[key] is None else min(1.0, running)
    return adjusted


def counted(row):
    verdict = row.get("verdict")
    readable_verdict = (
        verdict is True
        or verdict is False
        or (isinstance(verdict, str) and verdict == "not established")
    )
    return (
        row.get("parse_ok") is True
        and row.get("finish_reason") in ("stop", "end_turn")
        and readable_verdict
    )


def primary_label(result, eligible):
    if not eligible or result["estimate"] is None or result["q"] is None:
        return
    lower, upper = result["ci95"]
    if lower > 0.0 and result["q"] <= 0.05:
        result["confirmed"] = True
        if upper >= 0.15:
            result["label"] = "gestützt, Vorhersagewert nicht ausgeschlossen"
        else:
            result["label"] = "gestützt, aber kleiner als vorhergesagt"
    elif upper < 0.02:
        result["label"] = "praktisch null"
    elif upper < 0.15:
        result["label"] = "Vorhersagewert ausgeschlossen"
    else:
        result["label"] = "nicht entschieden"


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python analysis.py DATA_DIRECTORY")

    choices = [
        "Only the preregistered material seeds 8000–8015 are analyzed; "
        "other seeds, including pilot seeds, are ignored.",
        "An item is identified by (seed, id). Within each (arm, item, cell), "
        "'last record' means the last JSONL occurrence, even if it is invalid; "
        "there is no fallback to an earlier valid record.",
        "The cell string and integer D/N/T fields must agree. Inconsistent "
        "item truth, malformed identifiers, unexpected arms, or more than "
        "12 observed items in a planned seed cause an error rather than "
        "an inferred repair.",
        "A counted judgment requires parse_ok literally true, finish_reason "
        "stop or end_turn, and verdict literally true, false, or "
        "'not established'. Missing/null or unrecognized verdicts are failures. "
        "'not established' counts as non-confirmation, including at T0.",
        "answer_chars is deliberately absent from the blinded export and is "
        "not required for judgment inclusion. The source audit of this field "
        "cannot be reconstructed from judgments.jsonl.",
        "Completeness is joint across both arms and all eight cells at item "
        "level. All estimates, including manipulation checks 2 and 3 and "
        "the additional descriptive rates, use this same complete-item set.",
        "Failure rates use the fixed planned denominator of 192 judgments "
        "per arm and cell, before complete-item exclusion. Missing planned "
        "records, including entirely unobserved items, count as failures. "
        "The failure threshold is inclusive: at most 5%.",
        "Manipulation check 2 treats only a boolean verdict equal to truth "
        "as correct; 'not established' is incorrect. Manipulation check 3 "
        "uses the absolute difference between truth-group confirmation rates "
        "pooled across all four D1 cells. An undefined check does not pass.",
        "The N/T code-test results in tests/test_e025.py are not present in "
        "judgments.jsonl and cannot be inferred from factor labels or model "
        "responses. No pass is assumed. A fail-closed convention treats this "
        "unverified fourth manipulation check as not passed, so the reported "
        "overall manipulation flags are false and inferential labels remain "
        "deskriptiv. This is not evidence that the external code tests failed.",
        "No material-ledger exclusions, preflight audits, or external-control "
        "results are inferred from missing records. They cannot be independently "
        "verified using this input alone.",
        "Bootstrap resampling is over individual complete items, not seeds "
        "or individual judgments. Each item's paired contrast is calculated "
        "first. K3 resamples only complete truth-true items. Item ordering is "
        "ascending (seed, id). Each arm and quantity gets a fresh RNG using "
        "the preregistered seed, with 5000 draws.",
        "The E-024 percentile implementation is unavailable. Percentile bounds "
        "use linear interpolation at indices (5000 - 1) * 0.025 and "
        "(5000 - 1) * 0.975.",
        "The preregistration does not define its one-sided bootstrap-p "
        "algorithm. Here p = (1 + number of ordinary, uncentered bootstrap "
        "means <= 0) / 5001, with separate RNGs seeded 352 for R1 and "
        "353 for R2. Ties at zero enter the nonpositive tail. This explicitly "
        "chooses a bootstrap sign-tail convention, not a null-centered test.",
        "BH includes the four planned arm-by-primary tests regardless of "
        "manipulation status or sample-size eligibility. An unestimable test "
        "occupies the family with p=1 for adjustment but reports q=null.",
        "Decision rules are evaluated in listed order: supporting label, "
        "praktisch null, Vorhersagewert ausgeschlossen, nicht entschieden. "
        "Failed/unverified manipulation checks or fewer than 144 complete "
        "items override primary labels to deskriptiv, but not estimates, "
        "intervals, or computable q-values.",
        "Empty estimands have estimate=null, ci95=[null,null], n=0; an empty "
        "primary test has q=null. n counts items, not judgments or seeds.",
        "The requested output schema has no separate fields for the "
        "preregistered NE rate, broken-item excerpt confirmations, check "
        "diagnostics, or premise warning. These are reported below as "
        "per-arm descriptive JSON strings in choices. NE pools the two "
        "D1-T1 cells; broken-item confirmations count judgments across "
        "all four D1 cells, not distinct items.",
    ]

    latest = {}
    ignored_rows = 0
    source = Path(sys.argv[1]) / "judgments.jsonl"
    with source.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError("Line %d is not a JSON object" % line_number)
            seed = row.get("seed")
            if type(seed) is not int:
                raise ValueError("Invalid seed on line %d" % line_number)
            if seed not in SEEDS:
                ignored_rows += 1
                continue
            arm = row.get("model")
            item_id = row.get("id")
            if arm not in ARMS or not isinstance(item_id, str) or not item_id:
                raise ValueError("Invalid arm/id on line %d" % line_number)
            cell = (row.get("D"), row.get("N"), row.get("T"))
            if (
                any(type(x) is not int or x not in (0, 1) for x in cell)
                or row.get("cell") != "D%d-N%d-T%d" % cell
            ):
                raise ValueError("Inconsistent cell on line %d" % line_number)
            latest[(arm, (seed, item_id), cell)] = row

    items = sorted({key[1] for key in latest})
    by_seed = {seed: [] for seed in SEEDS}
    truth = {}
    for item in items:
        by_seed[item[0]].append(item)
    if any(len(group) > ITEMS_PER_SEED for group in by_seed.values()):
        raise ValueError("More than 12 distinct items in a planned seed")

    for (arm, item, cell), row in latest.items():
        value = row.get("truth")
        if type(value) is not bool:
            raise ValueError("Missing or non-boolean truth for %r" % (item,))
        if item in truth and truth[item] is not value:
            raise ValueError("Inconsistent truth for %r" % (item,))
        truth[item] = value

    valid = {key: row for key, row in latest.items() if counted(row)}
    complete = [
        item for item in items
        if all((arm, item, cell) in valid for arm in ARMS for cell in CELLS)
    ]
    complete_set = set(complete)
    n_complete_seeds = sum(
        len(by_seed[seed]) == ITEMS_PER_SEED
        and all(item in complete_set for item in by_seed[seed])
        for seed in SEEDS
    )

    def confirmation(arm, item, cell):
        return float(valid[(arm, item, cell)]["verdict"] is True)

    assignments = {}
    pvalues = {}
    checks = {}

    for arm in ARMS:
        k0 = []
        r1 = []
        r2 = []
        k3 = []
        for item in complete:
            a = confirmation(arm, item, (1, 0, 0))
            b = confirmation(arm, item, (1, 0, 1))
            c = confirmation(arm, item, (1, 1, 0))
            d = confirmation(arm, item, (1, 1, 1))
            k0.append(a)
            r1.append((a + b - c - d) / 2.0)
            r2.append((a + c - b - d) / 2.0)
            if truth[item]:
                k3.append(
                    confirmation(arm, item, (0, 1, 1))
                    - confirmation(arm, item, (0, 0, 0))
                )

        values = {"K0": k0, "R1": r1, "R2": r2, "K3": k3}
        assignments[arm] = {
            name: summarize(values[name], CI_SEEDS[name])
            for name in ("K0", "R1", "R2", "K3")
        }
        for name in ("R1", "R2"):
            pvalues[(arm, name)] = bootstrap_p(values[name], P_SEEDS[name])

        failures = {}
        for cell in CELLS:
            n_valid = sum(
                (arm, item, cell) in valid for item in items
            )
            failures["D%d-N%d-T%d" % cell] = (
                PLANNED_ITEMS - n_valid
            ) / PLANNED_ITEMS

        accuracy = None
        if complete:
            accuracy = sum(
                valid[(arm, item, (0, 0, 0))]["verdict"] is truth[item]
                for item in complete
            ) / len(complete)

        group_rates = {}
        for status in (False, True):
            group = [item for item in complete if truth[item] is status]
            group_rates[status] = (
                sum(
                    confirmation(arm, item, (1, n, t))
                    for item in group
                    for n, t in itertools.product((0, 1), repeat=2)
                ) / (4 * len(group))
                if group else None
            )
        difference = (
            abs(group_rates[True] - group_rates[False])
            if all(rate is not None for rate in group_rates.values())
            else None
        )
        check1 = all(rate <= 0.05 for rate in failures.values())
        check2 = accuracy is not None and accuracy >= 0.80
        check3 = difference is not None and difference <= 0.15
        check4 = False  # Unverifiable external code-test prerequisite.
        checks[arm] = check1 and check2 and check3 and check4

        ne_denominator = 2 * len(complete)
        ne_count = sum(
            valid[(arm, item, (1, n, 1))]["verdict"] == "not established"
            for item in complete for n in (0, 1)
        )
        broken = [item for item in complete if not truth[item]]
        broken_confirmations = int(sum(
            confirmation(arm, item, (1, n, t))
            for item in broken
            for n, t in itertools.product((0, 1), repeat=2)
        ))
        upper_k0 = assignments[arm]["K0"]["ci95"][1]
        diagnostics = {
            "arm": arm,
            "n_complete_items": len(complete),
            "failure_rates_by_cell": failures,
            "check1_passed": check1,
            "D0_N0_T0_accuracy": accuracy,
            "check2_passed": check2,
            "D1_confirmation_rate_truth_true": group_rates[True],
            "D1_confirmation_rate_truth_false": group_rates[False],
            "D1_absolute_truth_group_difference": difference,
            "check3_passed": check3,
            "check4_status": "not verifiable from supplied input",
            "minimum_complete_items_met": len(complete) >= 144,
            "NE_D1_T1_count": ne_count,
            "NE_D1_T1_denominator": ne_denominator,
            "NE_D1_T1_rate": (
                ne_count / ne_denominator if ne_denominator else None
            ),
            "D1_confirmations_on_broken_items": broken_confirmations,
            "D1_broken_item_judgments": 4 * len(broken),
            "premise_note": (
                "Prämisse nicht gegeben"
                if upper_k0 is not None and upper_k0 < 0.30
                else None
            ),
        }
        choices.append(
            "Additional preregistered descriptive output and diagnostics: "
            + json.dumps(diagnostics, ensure_ascii=False, allow_nan=False)
        )

    qvalues = bh_four(pvalues)
    for arm in ARMS:
        for name in ("R1", "R2"):
            result = assignments[arm][name]
            result["q"] = qvalues[(arm, name)]
            primary_label(
                result,
                eligible=checks[arm] and len(complete) >= 144,
            )

    choices.append(
        "Rows outside the preregistered seed range ignored: %d." % ignored_rows
    )
    output = {
        "n_complete_seeds": n_complete_seeds,
        "manipulation_check_passed": checks,
        "assignments": assignments,
        "choices": choices,
    }
    print(json.dumps(output, ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()
