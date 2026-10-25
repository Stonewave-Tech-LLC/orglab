#!/usr/bin/env python3
import json
import sys
import random
from pathlib import Path

ARMS = ("A", "B")
CELLS = tuple(
    "D%d-N%d-T%d" % (d, n, t)
    for d in (0, 1)
    for n in (0, 1)
    for t in (0, 1)
)
FACTORS = {
    "D%d-N%d-T%d" % (d, n, t): (d, n, t)
    for d in (0, 1)
    for n in (0, 1)
    for t in (0, 1)
}
DRAWS = 5000
PREDICTIONS = (0.08, 0.05, 0.05, 0.08)

CHOICES = [
    "Only material seeds 9000–9015 are analyzed; other seeds, if present, "
    "are treated as outside the preregistered main run.",
    "Items are keyed by id, as specified for deduplication and bootstrap ordering. "
    "A given id must have consistent seed and truth across its records.",
    "For each arm, the failure-rate denominator is the number of distinct item "
    "ids observed for that arm before complete-item exclusion. Missing cells for "
    "these ids count as failures. Entirely unobserved items cannot be recovered "
    "from this file; no unobserved ids or material exclusions are invented.",
    "Last record means last occurrence in JSONL file order for each "
    "(model, id, cell), including when that last record is a failure.",
    "The prompt-presence check applies literally to every in-scope input row, "
    "including superseded rows; cell names determine the expected prompt flags.",
    "Apart from failure rates and the every-row prompt check, manipulation-check "
    "rates use the same jointly complete items as the contrasts. An empty "
    "denominator, including an absent truth group, fails the applicable check.",
    "A failed manipulation check in either arm makes both assignments descriptive, "
    "because each assignment involves both arms. Fewer than 144 complete items "
    "also makes both assignments descriptive. Such primary results retain their "
    "estimates and intervals but have q=null, label=deskriptiv, confirmed=false.",
    "Decision rules are applied in their listed order: supporting evidence first, "
    "then practically null, then prediction excluded, then undecided.",
    "Descriptive bootstrap seeds 445–449 are assigned in output order to "
    "K0Z, K0V, R1V, R2V, B4Z. Each assignment and each quantity starts a fresh "
    "random.Random with its specified seed.",
    "n_complete_seeds counts distinct material seeds represented by at least one "
    "jointly complete item. It is not the complete-item count used for the "
    "144-item gate, and does not impose a seed-level exclusion rule.",
    "The fixed output schema reports the nine requested item-level quantities "
    "per assignment. Additional preregistered descriptive cell/domain rates and "
    "the 5%-broken prevalence illustration are computed internally but have no "
    "dedicated output fields.",
    "The prevalence illustration assumes the confirmation rate on actually broken "
    "items transports to a population with 5% broken items; expected overlooked "
    "errors per 1000 are 1000*0.05 times that rate, separately for each N,T cell.",
    "The two attested harness checks are accepted as passed and are not "
    "recomputed."
]


def counted(row):
    return (
        row is not None
        and row.get("verdict") is not None
        and row.get("parse_ok") is True
        and row.get("finish_reason") in ("stop", "end_turn")
    )


def confirmation(row):
    return float(row["verdict"] is True)


def correct(row):
    verdict = row["verdict"]
    return float(
        isinstance(verdict, bool) and verdict == row["truth"]
    )


def mean(values):
    return sum(values) / len(values) if values else None


def bootstrap_means(values, seed):
    if not values:
        return []
    rng = random.Random(seed)
    n = len(values)
    return [
        sum(rng.choices(values, k=n)) / n
        for _ in range(DRAWS)
    ]


def interval(values, seed):
    draws = bootstrap_means(values, seed)
    if not draws:
        return [None, None]
    draws.sort()
    # Exact preregistered percentile indices for B = 5000.
    return [draws[125], draws[4874]]


def bootstrap_p(values, seed):
    draws = bootstrap_means(values, seed)
    if not draws:
        return None
    return sum(x <= 0.0 for x in draws) / DRAWS


def bh(p_values):
    if any(p is None for p in p_values):
        return [None] * len(p_values)
    m = len(p_values)
    order = sorted(range(m), key=lambda i: (p_values[i], i))
    adjusted = [None] * m
    running = 1.0
    for position in range(m - 1, -1, -1):
        i = order[position]
        running = min(running, p_values[i] * m / (position + 1))
        adjusted[i] = running
    return adjusted


def primary_label(ci, q, prediction):
    lower, upper = ci
    if lower is None or q is None:
        return "nicht entschieden"
    if lower > 0.0 and q <= 0.05:
        if upper >= prediction:
            return "BESTÄTIGT (Vorhersagewert nicht ausgeschlossen)"
        return "BESTÄTIGT, aber kleiner als vorhergesagt"
    if upper < 0.02:
        return "praktisch null (widerlegt)"
    if upper < prediction:
        return "Vorhersagewert ausgeschlossen (widerlegt)"
    return "nicht entschieden"


def make_result(values, ci_seed, q=None, prediction=None, inferential=False):
    ci = interval(values, ci_seed)
    label = (
        primary_label(ci, q, prediction)
        if inferential
        else "deskriptiv"
    )
    return {
        "estimate": mean(values),
        "ci95": ci,
        "q": q if inferential else None,
        "n": len(values),
        "label": label,
        "confirmed": inferential and label.startswith("BESTÄTIGT"),
        "comparison": None,
    }


def read_data(path):
    latest = {arm: {} for arm in ARMS}
    observed = {arm: set() for arm in ARMS}
    prompt_ok = {arm: True for arm in ARMS}
    metadata = {}

    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError("Line %d is not a JSON object" % line_number)
            seed = row.get("seed")
            if type(seed) is not int:
                raise ValueError("Invalid material seed on line %d" % line_number)
            if not 9000 <= seed <= 9015:
                continue

            arm = row.get("model")
            item = row.get("id")
            cell = row.get("cell")
            if arm not in ARMS or not isinstance(item, str) or cell not in FACTORS:
                raise ValueError("Invalid model, id, or cell on line %d" % line_number)
            if type(row.get("truth")) is not bool:
                raise ValueError("Invalid truth on line %d" % line_number)

            d, n, t = FACTORS[cell]
            if any(
                type(row.get(field)) is not int or row[field] != expected
                for field, expected in (("D", d), ("N", n), ("T", t))
            ):
                raise ValueError("Inconsistent factor coding on line %d" % line_number)

            item_metadata = (seed, row["truth"])
            if item in metadata and metadata[item] != item_metadata:
                raise ValueError("Inconsistent seed/truth for id %s" % item)
            metadata[item] = item_metadata

            prompt_ok[arm] = prompt_ok[arm] and (
                row.get("norm_im_prompt") is bool(n)
                and row.get("dritte_antwort_im_prompt") is bool(t)
            )
            observed[arm].add(item)
            latest[arm][(item, cell)] = row

    return latest, observed, prompt_ok, metadata


def manipulation_checks(latest, observed, prompt_ok, complete, metadata):
    passed = {}
    for arm in ARMS:
        rows = latest[arm]
        denominator = len(observed[arm])
        failures_ok = denominator > 0 and all(
            20 * (
                denominator
                - sum(counted(rows.get((item, cell))) for item in observed[arm])
            ) <= denominator
            for cell in CELLS
        )

        full_accuracy = mean([
            correct(rows[(item, "D0-N0-T0")])
            for item in complete
        ])
        full_ok = full_accuracy is not None and full_accuracy >= 0.80

        grouped_confirmations = {True: [], False: []}
        for item in complete:
            truth = metadata[item][1]
            for n in (0, 1):
                for t in (0, 1):
                    grouped_confirmations[truth].append(
                        confirmation(rows[(item, "D1-N%d-T%d" % (n, t))])
                    )
        ok_rate = mean(grouped_confirmations[True])
        broken_rate = mean(grouped_confirmations[False])
        excerpt_ok = (
            ok_rate is not None
            and broken_rate is not None
            and abs(ok_rate - broken_rate) <= 0.15
        )
        passed[arm] = bool(
            failures_ok and full_ok and excerpt_ok and prompt_ok[arm]
        )
    return passed


def item_vectors(latest, complete):
    vectors = {}
    for arm in ARMS:
        rows = latest[arm]
        vectors[arm] = {"K0": [], "R1": [], "R2": [], "KV": []}
        for item in complete:
            c00 = confirmation(rows[(item, "D1-N0-T0")])
            c01 = confirmation(rows[(item, "D1-N0-T1")])
            c10 = confirmation(rows[(item, "D1-N1-T0")])
            c11 = confirmation(rows[(item, "D1-N1-T1")])
            vectors[arm]["K0"].append(c00)
            vectors[arm]["R1"].append((c00 + c01 - c10 - c11) / 2.0)
            vectors[arm]["R2"].append((c00 + c10 - c01 - c11) / 2.0)
            vectors[arm]["KV"].append(
                correct(rows[(item, "D0-N0-T0")])
                - correct(rows[(item, "D0-N0-T1")])
            )
    return vectors


def additional_descriptives(latest, complete, metadata):
    """Compute preregistered descriptives not accommodated by the output schema."""
    summaries = {}
    for arm in ARMS:
        groups = {}
        for item in complete:
            for cell in CELLS:
                row = latest[arm][(item, cell)]
                domain = row.get("domain")
                for key in (("cell", cell), ("domain_cell", domain, cell)):
                    group = groups.setdefault(key, [])
                    group.append(row)
        rates = {}
        for key, rows in groups.items():
            rates[key] = {
                "n": len(rows),
                "confirmation_rate": mean([confirmation(r) for r in rows]),
                "accuracy": mean([correct(r) for r in rows]),
                "not_established_rate": mean([
                    float(r["verdict"] == "not established") for r in rows
                ]),
            }
        all_rows = [
            latest[arm][(item, cell)]
            for item in complete
            for cell in CELLS
        ]
        overall_not_established = mean([
            float(row["verdict"] == "not established") for row in all_rows
        ])
        missed_errors = {}
        for n in (0, 1):
            for t in (0, 1):
                cell = "D1-N%d-T%d" % (n, t)
                broken_confirmation = mean([
                    confirmation(latest[arm][(item, cell)])
                    for item in complete
                    if metadata[item][1] is False
                ])
                missed_errors[cell] = (
                    None if broken_confirmation is None
                    else 50.0 * broken_confirmation
                )
        summaries[arm] = {
            "rates": rates,
            "not_established_rate": overall_not_established,
            "missed_errors_per_1000_at_5_percent_broken": missed_errors,
        }
    return summaries


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 analysis.py DATA_DIRECTORY")

    latest, observed, prompt_ok, metadata = read_data(
        Path(sys.argv[1]) / "judgments.jsonl"
    )
    complete = sorted(
        item
        for item in observed["A"] & observed["B"]
        if all(
            counted(latest[arm].get((item, cell)))
            for arm in ARMS
            for cell in CELLS
        )
    )
    checks = manipulation_checks(
        latest, observed, prompt_ok, complete, metadata
    )
    inferential = len(complete) >= 144 and all(checks.values())
    vectors = item_vectors(latest, complete)
    additional_descriptives(latest, complete, metadata)

    assignments = {}
    for target in ARMS:
        comparison = "B" if target == "A" else "A"
        z = vectors[target]
        v = vectors[comparison]
        primary = [
            [a - b for a, b in zip(z["K0"], v["K0"])],
            z["R1"],
            z["R2"],
            v["KV"],
        ]
        p_values = [
            bootstrap_p(values, 451 + i)
            for i, values in enumerate(primary)
        ]
        q_values = bh(p_values)
        results = {}
        for i, values in enumerate(primary):
            results["B%d" % (i + 1)] = make_result(
                values,
                441 + i,
                q=q_values[i],
                prediction=PREDICTIONS[i],
                inferential=inferential,
            )
        descriptive = [
            ("K0Z", z["K0"]),
            ("K0V", v["K0"]),
            ("R1V", v["R1"]),
            ("R2V", v["R2"]),
            ("B4Z", z["KV"]),
        ]
        for i, (name, values) in enumerate(descriptive):
            results[name] = make_result(values, 445 + i)
        assignments[target] = results

    output = {
        "n_complete_seeds": len({metadata[item][0] for item in complete}),
        "manipulation_check_passed": checks,
        "assignments": assignments,
        "choices": CHOICES,
    }
    print(json.dumps(output, ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()
