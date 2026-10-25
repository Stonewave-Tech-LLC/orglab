#!/usr/bin/env python3
import sys
import os
import json
import random
import math
from collections import defaultdict

def bootstrap_mean_ci(values, seed, n_draws=5000):
    if not values:
        return None, [None, None], []
    n = len(values)
    est = sum(values) / n
    rng = random.Random(seed)
    boot_means = []
    for _ in range(n_draws):
        sample_sum = 0.0
        for _ in range(n):
            sample_sum += values[rng.randrange(n)]
        boot_means.append(sample_sum / n)
    boot_means.sort()
    # 2.5th and 97.5th percentile after sorting (5000 * 0.025 = 125, 5000 * 0.975 = 4875)
    idx_low = int(0.025 * n_draws)
    idx_high = int(0.975 * n_draws)
    if idx_high >= n_draws:
        idx_high = n_draws - 1
    return est, [boot_means[idx_low], boot_means[idx_high]], boot_means

def compute_two_sided_p(values, boot_means):
    if not values or not boot_means:
        return 1.0
    n_draws = len(boot_means)
    # Empirical bootstrap p-value from centered or uncentered distribution / normal approx
    # Using standard empirical percentile p-value: 2 * min(P(theta* <= 0), P(theta* >= 0))
    le_zero = sum(1 for x in boot_means if x <= 0.0) / n_draws
    ge_zero = sum(1 for x in boot_means if x >= 0.0) / n_draws
    p_emp = min(1.0, 2.0 * min(le_zero, ge_zero))
    return p_emp

def classify_v(ci, q_val, pred_val, n_complete_seeds):
    if n_complete_seeds < 16 or ci[0] is None or ci[1] is None:
        return "nur deskriptiv"
    low, high = ci[0], ci[1]
    effekt_nachgewiesen = (low > 0.0) and (q_val <= 0.05)
    if effekt_nachgewiesen and (high >= pred_val):
        return "Vorhersage gestützt"
    if effekt_nachgewiesen:
        return "Effekt nachgewiesen"
    if high < 0.02:
        return "praktisch null"
    if high < pred_val:
        return "Vorhersage widerlegt"
    return "nicht entschieden"

def main():
    if len(sys.argv) != 2:
        sys.exit(1)
    
    data_dir = sys.argv[1]
    file_path = os.path.join(data_dir, "judgments.jsonl")
    
    # Deduplicate keeping the last record for each (id, cell)
    records_by_key = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            key = (obj["id"], obj["cell"])
            records_by_key[key] = obj

    # Expected cells
    all_cells = [
        f"SP{sp}-ZU{zu}-AU{au}"
        for sp in (0, 1)
        for zu in (0, 1)
        for au in (0, 1)
    ]

    # Group by seed and item
    seed_items = defaultdict(lambda: defaultdict(dict))
    for (item_id, cell), obj in records_by_key.items():
        seed = obj["seed"]
        seed_items[seed][item_id][cell] = obj

    # Determine complete seeds:
    # A seed where every item has all 8 cells with a valid verdict (verdict is True or False)
    # Also check if seed has all expected items (12 items per seed: 288 items / 24 seeds = 12)
    # Wait: what if a seed was aborted mid-way and has fewer than 12 items?
    # Let's check the maximum number of items per seed across the dataset (or 12 as per prereg: 24 seeds = 288 items -> 12 per seed).
    item_counts = [len(items) for items in seed_items.values()]
    expected_items_per_seed = max(item_counts) if item_counts else 12

    complete_seeds = set()
    for seed, items in seed_items.items():
        if len(items) < expected_items_per_seed:
            continue
        seed_ok = True
        for item_id, cell_map in items.items():
            if len(cell_map) < 8:
                seed_ok = False
                break
            for c in all_cells:
                if c not in cell_map:
                    seed_ok = False
                    break
                v = cell_map[c].get("verdict")
                if v is not True and v is not False:
                    seed_ok = False
                    break
            if not seed_ok:
                break
        if seed_ok:
            complete_seeds.add(seed)

    n_complete_seeds = len(complete_seeds)

    # Collect items from complete seeds, sorted by item_id for deterministic bootstrap ordering
    valid_items = {}
    for seed in sorted(complete_seeds):
        for item_id, cell_map in seed_items[seed].items():
            valid_items[item_id] = cell_map
    sorted_item_ids = sorted(valid_items.keys())

    # Calculate per-cell miss_rate and false_alarm_rate
    miss_rate = {}
    false_alarm_rate = {}
    for c in all_cells:
        broken_count = 0
        miss_count = 0
        working_count = 0
        fa_count = 0
        for item_id in sorted_item_ids:
            rec = valid_items[item_id][c]
            truth = rec["truth"]
            verdict = rec["verdict"]
            if truth is False:
                broken_count += 1
                if verdict is True:
                    miss_count += 1
            elif truth is True:
                working_count += 1
                if verdict is False:
                    fa_count += 1
        miss_rate[c] = (miss_count / broken_count) if broken_count > 0 else None
        false_alarm_rate[c] = (fa_count / working_count) if working_count > 0 else None

    # V1: SPEC 1 - 0, only spec-pure broken items (truth == False and primary == True)
    # Unit of analysis: item (Beleg). Difference of miss rate between SPEC=1 and SPEC=0 averaged over ZU and AU (4 cells each).
    v1_diffs = []
    for item_id in sorted_item_ids:
        cell_map = valid_items[item_id]
        first_rec = cell_map[all_cells[0]]
        if first_rec["truth"] is False and first_rec.get("primary") is True:
            sp1_misses = [1.0 if cell_map[f"SP1-ZU{zu}-AU{au}"]["verdict"] is True else 0.0 for zu in (0, 1) for au in (0, 1)]
            sp0_misses = [1.0 if cell_map[f"SP0-ZU{zu}-AU{au}"]["verdict"] is True else 0.0 for zu in (0, 1) for au in (0, 1)]
            diff = (sum(sp1_misses) / 4.0) - (sum(sp0_misses) / 4.0)
            v1_diffs.append(diff)

    # V2: AUSKUNFT 1 - 0, all broken items (truth == False)
    # Difference of miss rate between AU=1 and AU=0 averaged over SP and ZU (4 cells each).
    v2_diffs = []
    for item_id in sorted_item_ids:
        cell_map = valid_items[item_id]
        first_rec = cell_map[all_cells[0]]
        if first_rec["truth"] is False:
            au1_misses = [1.0 if cell_map[f"SP{sp}-ZU{zu}-AU1"]["verdict"] is True else 0.0 for sp in (0, 1) for zu in (0, 1)]
            au0_misses = [1.0 if cell_map[f"SP{sp}-ZU{zu}-AU0"]["verdict"] is True else 0.0 for sp in (0, 1) for zu in (0, 1)]
            diff = (sum(au1_misses) / 4.0) - (sum(au0_misses) / 4.0)
            v2_diffs.append(diff)

    # V3: run_check calls AUSKUNFT 1 - 0, only ZUGANG=1, all items
    # Difference of n_checks between AU=1 and AU=0 within ZU=1, averaged over SP=0 and SP=1 (2 cells each).
    v3_diffs = []
    for item_id in sorted_item_ids:
        cell_map = valid_items[item_id]
        au1_checks = [float(cell_map[f"SP{sp}-ZU1-AU1"]["n_checks"]) for sp in (0, 1)]
        au0_checks = [float(cell_map[f"SP{sp}-ZU1-AU0"]["n_checks"]) for sp in (0, 1)]
        diff = (sum(au1_checks) / 2.0) - (sum(au0_checks) / 2.0)
        v3_diffs.append(diff)

    # Bootstrap with fixed seeds 201, 202, 203 (from stated range 201-205, 211-212) and 5000 draws
    v1_est, v1_ci, v1_boot = bootstrap_mean_ci(v1_diffs, seed=201, n_draws=5000)
    v2_est, v2_ci, v2_boot = bootstrap_mean_ci(v2_diffs, seed=202, n_draws=5000)
    v3_est, v3_ci, v3_boot = bootstrap_mean_ci(v3_diffs, seed=203, n_draws=5000)

    # BH-FDR across V1 and V2
    p1 = compute_two_sided_p(v1_diffs, v1_boot)
    p2 = compute_two_sided_p(v2_diffs, v2_boot)
    if p1 <= p2:
        q2 = p2
        q1 = min(p1 * 2.0, q2)
    else:
        q1 = p1
        q2 = min(p2 * 2.0, q1)

    v1_label = classify_v(v1_ci, q1, 0.10, n_complete_seeds)
    v2_label = classify_v(v2_ci, q2, 0.05, n_complete_seeds)

    choices = [
        "Bootstrap seeds assigned as 201 for V1, 202 for V2, and 203 for V3 from the preregistered list of seeds (201-205, 211-212).",
        "Percentile bootstrap 95% CI computed using sorted array indices 125 (0.025 * 5000) and 4875 (0.975 * 5000), with items sorted by id before resampling.",
        "Complete seeds defined as seeds having the full set of items and all 8 cells per item with non-null boolean verdicts.",
        "V3 computed across all items (both broken and working) in complete seeds, averaging n_checks over SP=0 and SP=1 within ZU=1 for AU=1 minus AU=0.",
        "Decision rule hierarchy when both 'Vorhersage widerlegt' (upper CI < prediction threshold) and 'praktisch null' (upper CI < +0.02) hold: assigned the more specific 'praktisch null' (both imply the prediction is refuted).",
        "Two-sided p-values for BH-FDR (over V1 and V2) derived from the empirical bootstrap distribution as 2 * min(P(boot <= 0), P(boot >= 0)), which aligns directly with the 95% percentile CI."
    ]

    output = {
        "n_complete_seeds": n_complete_seeds,
        "v1_estimate": v1_est,
        "v1_ci95": v1_ci,
        "v1_label": v1_label,
        "v2_estimate": v2_est,
        "v2_ci95": v2_ci,
        "v2_label": v2_label,
        "v3_estimate": v3_est,
        "v3_ci95": v3_ci,
        "miss_rate": miss_rate,
        "false_alarm_rate": false_alarm_rate,
        "choices": choices
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
