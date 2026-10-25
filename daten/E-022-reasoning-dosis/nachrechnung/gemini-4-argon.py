#!/usr/bin/env python3
import sys
import os
import json
import random
import statistics
from collections import defaultdict

def effort_to_arm(effort):
    return "ohne" if effort is None else str(effort)

def quantile(sorted_vals, q):
    if not sorted_vals:
        return None
    n = len(sorted_vals)
    pos = q * (n - 1)
    lo = int(pos)
    hi = min(lo + 1, n - 1)
    frac = pos - lo
    return sorted_vals[lo] * (1.0 - frac) + sorted_vals[hi] * frac

def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: script.py <data_dir>")
    data_dir = sys.argv[1]
    
    calls_path = os.path.join(data_dir, "calls.jsonl")
    judgments_path = os.path.join(data_dir, "judgments.jsonl")
    
    calls = []
    with open(calls_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                calls.append(json.loads(line))
                
    judgments = []
    with open(judgments_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                judgments.append(json.loads(line))

    arms = ["low", "medium", "high", "ohne"]
    positions = [0, 1, 2]
    
    # Deduplicate calls if retries happened: keep latest attempt per (batch, arm, position)
    latest_calls = {}
    for c in calls:
        b = c["batch"]
        arm = effort_to_arm(c.get("effort"))
        pos = c["position"]
        key = (b, arm, pos)
        if key not in latest_calls or c.get("attempt", 0) >= latest_calls[key].get("attempt", 0):
            latest_calls[key] = c

    # Deduplicate judgments: keep latest per (batch, arm, position, id)
    latest_judgments = {}
    for j in judgments:
        b = j["batch"]
        arm = effort_to_arm(j.get("effort"))
        pos = j["position"]
        item_id = j["id"]
        key = (b, arm, pos, item_id)
        latest_judgments[key] = j

    # Determine complete batches:
    # "jeder Arm an jeder Position mit >= 95 % geparsten Urteilen nach bis zu zwei Wiederholungen"
    batches_in_data = sorted(set( b for (b, _, _) in latest_calls.keys() ) | set( b for (b, _, _, _) in latest_judgments.keys() ))
    
    complete_batches = []
    for b in batches_in_data:
        is_complete = True
        for arm in arms:
            for pos in positions:
                ckey = (b, arm, pos)
                if ckey in latest_calls:
                    c = latest_calls[ckey]
                    size = c.get("size", 12)
                    parsed = c.get("parsed", 0)
                    if size <= 0 or (parsed / size) < 0.95:
                        is_complete = False
                        break
                else:
                    # Fallback to judgments if call entry is missing
                    j_list = [j for (jb, jarm, jpos, _), j in latest_judgments.items() if jb == b and jarm == arm and jpos == pos]
                    if len(j_list) == 0:
                        is_complete = False
                        break
                    valid_v = sum(1 for j in j_list if j.get("verdict") is not None)
                    if (valid_v / max(len(j_list), 12)) < 0.95:
                        is_complete = False
                        break
            if not is_complete:
                break
        if is_complete:
            complete_batches.append(b)

    complete_batches_set = set(complete_batches)

    # Manipulation check: Median of completion_tokens per call and arm (in complete batches)
    tokens_by_arm = {arm: [] for arm in arms}
    for (b, arm, pos), c in latest_calls.items():
        if b in complete_batches_set and arm in tokens_by_arm:
            ct = c.get("completion_tokens")
            if ct is not None:
                tokens_by_arm[arm].append(ct)

    median_completion_tokens = {}
    for arm in arms:
        if tokens_by_arm[arm]:
            median_completion_tokens[arm] = statistics.median(tokens_by_arm[arm])
        else:
            median_completion_tokens[arm] = None

    med_low = median_completion_tokens.get("low")
    med_med = median_completion_tokens.get("medium")
    med_high = median_completion_tokens.get("high")
    
    if med_low is not None and med_med is not None and med_high is not None:
        manipulation_check_passed = bool(
            (med_low < med_med < med_high) and (med_high >= 1.5 * med_low)
        )
    else:
        manipulation_check_passed = False

    # Group judgments by batch -> item_id -> arm -> list of verdicts
    # Only for complete batches
    item_truth = {}
    item_batch = {}
    verdicts_by_item_arm = defaultdict(lambda: defaultdict(list))

    for (b, arm, pos, item_id), j in latest_judgments.items():
        if b not in complete_batches_set:
            continue
        verdict = j.get("verdict")
        if verdict is None:
            continue
        item_truth[item_id] = j["truth"]
        item_batch[item_id] = b
        verdicts_by_item_arm[item_id][arm].append(verdict)

    # Compute item-level error rates per arm
    # For truth == True (Ok-Beleg): False alarm is verdict == False (1.0 if False else 0.0)
    # For truth == False (kaputter Beleg): Miss is verdict == True (1.0 if True else 0.0)
    ok_items_by_batch = defaultdict(list)
    broken_items_by_batch = defaultdict(list)
    
    fa_item_arm = defaultdict(dict)
    miss_item_arm = defaultdict(dict)

    for item_id, truth in item_truth.items():
        b = item_batch[item_id]
        if truth is True:
            ok_items_by_batch[b].append(item_id)
            for arm in arms:
                v_list = verdicts_by_item_arm[item_id].get(arm, [])
                if v_list:
                    fa_item_arm[item_id][arm] = sum(1.0 for v in v_list if v is False) / len(v_list)
        elif truth is False:
            broken_items_by_batch[b].append(item_id)
            for arm in arms:
                v_list = verdicts_by_item_arm[item_id].get(arm, [])
                if v_list:
                    miss_item_arm[item_id][arm] = sum(1.0 for v in v_list if v is True) / len(v_list)

    # Per-arm false_alarm_rate and miss_rate across all items in complete batches
    false_alarm_rate = {}
    miss_rate = {}
    for arm in arms:
        fa_vals = [fa_item_arm[i][arm] for b in complete_batches for i in ok_items_by_batch[b] if arm in fa_item_arm[i]]
        miss_vals = [miss_item_arm[i][arm] for b in complete_batches for i in broken_items_by_batch[b] if arm in miss_item_arm[i]]
        false_alarm_rate[arm] = sum(fa_vals) / len(fa_vals) if fa_vals else None
        miss_rate[arm] = sum(miss_vals) / len(miss_vals) if miss_vals else None

    # Paired diffs per item for P1 (low - high on Ok items) and P2 (high - low on Broken items)
    p1_diffs_by_batch = defaultdict(list)
    p2_diffs_by_batch = defaultdict(list)

    for b in complete_batches:
        for i in ok_items_by_batch[b]:
            if "low" in fa_item_arm[i] and "high" in fa_item_arm[i]:
                p1_diffs_by_batch[b].append(fa_item_arm[i]["low"] - fa_item_arm[i]["high"])
        for i in broken_items_by_batch[b]:
            if "high" in miss_item_arm[i] and "low" in miss_item_arm[i]:
                p2_diffs_by_batch[b].append(miss_item_arm[i]["high"] - miss_item_arm[i]["low"])

    all_p1_diffs = [d for b in complete_batches for d in p1_diffs_by_batch[b]]
    all_p2_diffs = [d for b in complete_batches for d in p2_diffs_by_batch[b]]

    p1_estimate = sum(all_p1_diffs) / len(all_p1_diffs) if all_p1_diffs else None
    p2_estimate = sum(all_p2_diffs) / len(all_p2_diffs) if all_p2_diffs else None

    # Cluster bootstrap over batches (10,000 draws)
    rng = random.Random(5000)
    n_boot = 10000
    n_batches = len(complete_batches)

    # Pre-aggregate sum and count per batch for fast exact item-weighted mean calculation
    p1_batch_stats = [(sum(p1_diffs_by_batch[b]), len(p1_diffs_by_batch[b])) for b in complete_batches]
    p2_batch_stats = [(sum(p2_diffs_by_batch[b]), len(p2_diffs_by_batch[b])) for b in complete_batches]

    boot_p1 = []
    boot_p2 = []

    if n_batches > 0:
        for _ in range(n_boot):
            indices = [rng.randrange(n_batches) for _ in range(n_batches)]
            s1 = sum(p1_batch_stats[idx][0] for idx in indices)
            c1 = sum(p1_batch_stats[idx][1] for idx in indices)
            if c1 > 0:
                boot_p1.append(s1 / c1)
                
            s2 = sum(p2_batch_stats[idx][0] for idx in indices)
            c2 = sum(p2_batch_stats[idx][1] for idx in indices)
            if c2 > 0:
                boot_p2.append(s2 / c2)

    boot_p1.sort()
    boot_p2.sort()

    # One-sided 95% intervals:
    # P1 lower bound: 5th percentile
    # P2 upper bound: 95th percentile
    p1_lower_bound = quantile(boot_p1, 0.05)
    p2_upper_bound = quantile(boot_p2, 0.95)

    # Hypothesis confirmation criteria:
    # P1: p1_lower_bound > 0 and p1_estimate > 0
    # P2: p2_upper_bound <= 0.03
    # Manipulation check passed
    # Also check >= 16 complete batches rule from Abbruchkriterien ("Unter 16 vollständigen Stapeln wird nur deskriptiv berichtet, nicht konfirmatorisch.")
    p1_passed = (p1_estimate is not None and p1_lower_bound is not None and p1_estimate > 0.0 and p1_lower_bound > 0.0)
    p2_passed = (p2_estimate is not None and p2_upper_bound is not None and p2_upper_bound <= 0.03)
    enough_batches = (len(complete_batches) >= 16)

    h_confirmed = bool(manipulation_check_passed and p1_passed and p2_passed and enough_batches)

    choices = [
        "Bootstrap random seed set to 5000 (first seed of the preregistered 5000-5023 range, as no specific bootstrap seed was specified).",
        "Percentile bootstrap method (5th percentile for P1 lower one-sided 95% bound, 95th percentile for P2 upper one-sided 95% bound) with linear interpolation between order statistics.",
        "In each cluster-bootstrap draw over complete batches, both P1 and P2 are evaluated on the same resampled set of batches, weighting each resampled item equally.",
        "If multiple call attempts exist in calls.jsonl for the same (batch, arm, position), only the latest attempt is used for completeness and token median calculations.",
        "Missing verdicts (verdict: null) within complete batches are ignored when averaging the remaining channel verdicts for an item.",
        "No Ok-items are excluded under the Generatorfehler-Regel because manual inspection of ground truth is not possible in an automated script (preregistration states exclusion only upon proven false ground truth and reporting with/without).",
        "Confirmed H-037 requires manipulation_check_passed, P1 (estimate > 0 and 95% one-sided LB > 0), P2 (95% one-sided UB <= 0.03), and at least 16 complete batches."
    ]

    result = {
        "n_complete_batches": len(complete_batches),
        "median_completion_tokens": median_completion_tokens,
        "manipulation_check_passed": manipulation_check_passed,
        "p1_estimate": p1_estimate,
        "p1_lower_bound_one_sided_95": p1_lower_bound,
        "p2_estimate": p2_estimate,
        "p2_upper_bound_one_sided_95": p2_upper_bound,
        "false_alarm_rate": false_alarm_rate,
        "miss_rate": miss_rate,
        "h_confirmed": h_confirmed,
        "choices": choices
    }

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
