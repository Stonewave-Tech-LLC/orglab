#!/usr/bin/env python3
import sys
import os
import json
import random
import math

def load_data(data_dir):
    filepath = os.path.join(data_dir, "judgments.jsonl")
    records_by_pair = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            # Preregistration: "Bei mehreren Datensätzen für dasselbe Paar Beleg/Zelle gilt der letzte"
            key = (obj["id"], obj["cell"])
            records_by_pair[key] = obj
    return list(records_by_pair.values())

def filter_complete_seeds(records):
    # Group by seed
    by_seed = {}
    for r in records:
        s = r["seed"]
        if 6000 <= s <= 6023:
            by_seed.setdefault(s, []).append(r)
    
    # Expected: 24 seeds (6000-6023) = 288 items -> 12 items per seed, 8 cells per item = 96 records per seed.
    # Also determine the standard item count per seed from the data if uniform, else 12.
    all_cells = {f"SP{sp}-ZU{zu}-AU{au}" for sp in (0, 1) for zu in (0, 1) for au in (0, 1)}
    
    complete_seeds = set()
    valid_records = []
    
    for s, recs in sorted(by_seed.items()):
        items = set(r["id"] for r in recs)
        if len(items) != 12:
            continue
        complete = True
        for item_id in items:
            item_recs = [r for r in recs if r["id"] == item_id]
            cells_present = set(r["cell"] for r in item_recs)
            if cells_present != all_cells:
                complete = False
                break
            for r in item_recs:
                if r.get("verdict") not in (True, False):
                    complete = False
                    break
        if complete:
            complete_seeds.add(s)
            valid_records.extend(recs)
            
    return complete_seeds, valid_records

def bootstrap_ci_and_p(values, n_draws=5000, seed=201):
    rng = random.Random(seed)
    n = len(values)
    if n == 0:
        return 0.0, [0.0, 0.0], 1.0
    
    estimate = sum(values) / n
    means = []
    for _ in range(n_draws):
        sample = [values[rng.randrange(n)] for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    
    # 2.5th and 97.5th percentile after sorting
    # Standard index mapping for 5000 draws: index 125 (0-based) is 126th element (2.5%), 4874 or 4875 is 97.5%
    idx_low = int(0.025 * n_draws)
    idx_high = int(0.975 * n_draws)
    ci = [means[idx_low], means[idx_high]]
    
    # Two-sided bootstrap p-value for H0: theta = 0
    le_zero = sum(1 for m in means if m <= 0.0) / n_draws
    ge_zero = sum(1 for m in means if m >= 0.0) / n_draws
    p_val = min(1.0, 2.0 * min(le_zero, ge_zero))
    
    return estimate, ci, p_val

def decide_label(ci, q_val, pred_val, n_complete_seeds):
    if n_complete_seeds < 16:
        return "nur deskriptiv (unter 16 vollständige Seeds)"
    low, high = ci[0], ci[1]
    effekt_nachgewiesen = (low > 0.0) and (q_val <= 0.05)
    
    # Order of checks per Deviation 2:
    # - "Effekt nachgewiesen" = untere Grenze > 0 und BH-q <= 0,05
    # - "Vorhersage gestützt" = Effekt nachgewiesen und Vorhersagewert (V1 +0,10, V2 +0,05) nicht ausgeschlossen (obere Grenze >= Wert)
    # - "Vorhersage widerlegt" = obere Grenze < Vorhersagewert
    # - "praktisch null" = obere Grenze < +0,02
    # - sonst "nicht entschieden"
    if effekt_nachgewiesen and high >= pred_val:
        return "Vorhersage gestützt"
    if effekt_nachgewiesen and high < pred_val:
        # Both "Effekt nachgewiesen" and "Vorhersage widerlegt" apply; if we report the primary status:
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
    
    records = load_data(data_dir)
    complete_seeds, valid_records = filter_complete_seeds(records)
    n_complete_seeds = len(complete_seeds)
    
    # Organize valid records by item_id and cell
    items = {}
    for r in valid_records:
        item_id = r["id"]
        if item_id not in items:
            items[item_id] = {
                "truth": r["truth"],
                "primary": r["primary"],
                "seed": r["seed"],
                "cells": {}
            }
        items[item_id]["cells"][(r["SP"], r["ZU"], r["AU"])] = r
        
    sorted_item_ids = sorted(items.keys())
    
    # Per-cell miss_rate (broken judged as works: truth==False, verdict==True)
    # and false_alarm_rate (working judged as broken: truth==True, verdict==False)
    cell_names = [f"SP{sp}-ZU{zu}-AU{au}" for sp in (0, 1) for zu in (0, 1) for au in (0, 1)]
    miss_rate = {}
    false_alarm_rate = {}
    
    for sp in (0, 1):
        for zu in (0, 1):
            for au in (0, 1):
                c_name = f"SP{sp}-ZU{zu}-AU{au}"
                broken_recs = [items[iid]["cells"][(sp, zu, au)] for iid in sorted_item_ids if not items[iid]["truth"]]
                working_recs = [items[iid]["cells"][(sp, zu, au)] for iid in sorted_item_ids if items[iid]["truth"]]
                
                if broken_recs:
                    misses = sum(1 for r in broken_recs if r["verdict"] is True)
                    miss_rate[c_name] = misses / len(broken_recs)
                else:
                    miss_rate[c_name] = None
                    
                if working_recs:
                    fas = sum(1 for r in working_recs if r["verdict"] is False)
                    false_alarm_rate[c_name] = fas / len(working_recs)
                else:
                    false_alarm_rate[c_name] = None

    # V1: SPEC 1 - 0, only spec-pure broken items (truth == False and primary == True)
    # Miss = verdict is True (when truth is False)
    v1_diffs = []
    for iid in sorted_item_ids:
        it = items[iid]
        if (not it["truth"]) and it["primary"]:
            c = it["cells"]
            # SPEC=1 average miss rate over ZU in {0,1}, AU in {0,1}
            m_sp1 = sum(1.0 if c[(1, zu, au)]["verdict"] is True else 0.0 for zu in (0, 1) for au in (0, 1)) / 4.0
            m_sp0 = sum(1.0 if c[(0, zu, au)]["verdict"] is True else 0.0 for zu in (0, 1) for au in (0, 1)) / 4.0
            v1_diffs.append(m_sp1 - m_sp0)
            
    # V2: AUSKUNFT 1 - 0, all broken items (truth == False)
    v2_diffs = []
    for iid in sorted_item_ids:
        it = items[iid]
        if not it["truth"]:
            c = it["cells"]
            m_au1 = sum(1.0 if c[(sp, zu, 1)]["verdict"] is True else 0.0 for sp in (0, 1) for zu in (0, 1)) / 4.0
            m_au0 = sum(1.0 if c[(sp, zu, 0)]["verdict"] is True else 0.0 for sp in (0, 1) for zu in (0, 1)) / 4.0
            v2_diffs.append(m_au1 - m_au0)
            
    # V3: run_check calls (n_checks) AUSKUNFT 1 - 0, only ZUGANG=1 (all items)
    v3_diffs = []
    for iid in sorted_item_ids:
        it = items[iid]
        c = it["cells"]
        chk_au1 = sum(float(c[(sp, 1, 1)]["n_checks"]) for sp in (0, 1)) / 2.0
        chk_au0 = sum(float(c[(sp, 1, 0)]["n_checks"]) for sp in (0, 1)) / 2.0
        v3_diffs.append(chk_au1 - chk_au0)

    # Bootstrap CIs using preregistered seeds (201 for V1, 202 for V2, 203 for V3; 211/212 for BH p-values)
    v1_est, v1_ci, _ = bootstrap_ci_and_p(v1_diffs, n_draws=5000, seed=201)
    v2_est, v2_ci, _ = bootstrap_ci_and_p(v2_diffs, n_draws=5000, seed=202)
    v3_est, v3_ci, _ = bootstrap_ci_and_p(v3_diffs, n_draws=5000, seed=203)
    
    _, _, p1 = bootstrap_ci_and_p(v1_diffs, n_draws=5000, seed=211)
    _, _, p2 = bootstrap_ci_and_p(v2_diffs, n_draws=5000, seed=212)
    
    # Benjamini-Hochberg FDR over V1 and V2
    if p1 <= p2:
        q1 = min(1.0, min(2.0 * p1, p2))
        q2 = min(1.0, p2)
    else:
        q2 = min(1.0, min(2.0 * p2, p1))
        q1 = min(1.0, p1)
        
    v1_label = decide_label(v1_ci, q1, 0.10, n_complete_seeds)
    v2_label = decide_label(v2_ci, q2, 0.05, n_complete_seeds)
    
    choices = [
        "Seed filtering: restricted to main-run seeds 6000-6023 with all 12 items and all 8 cells per item having non-null boolean verdicts.",
        "Bootstrap percentile indexing: used sorted[int(0.025 * 5000)] (index 125) and sorted[int(0.975 * 5000)] (index 4875) on 5000 draws sorted ascending.",
        "Random seeds: used Python standard library random.Random with seed 201 for V1 CI, 202 for V2 CI, 203 for V3 CI, and 211/212 for V1/V2 BH-FDR p-values as listed in E-023 ('Startwerte 201/202 (V1/V2), 211/212 (BH)').",
        "Item order for bootstrap: sorted items alphabetically by 'id' before resampling.",
        "V3 item subset: included all items (both working and broken) in ZUGANG=1 when computing the AU1 - AU0 difference in n_checks, as V3 does not restrict to broken items.",
        "Decision label precedence (Abweichung 2): since 'praktisch null' (upper CI < +0.02) is a subset of 'Vorhersage widerlegt' (upper CI < +0.10 for V1 or < +0.05 for V2), assigned 'praktisch null' when upper CI < +0.02 and 'Vorhersage widerlegt' when +0.02 <= upper CI < prediction threshold.",
        "Primary dataset scope: included all complete seeds without excluding item 'coding-fail_moderate-6021' or the 8 'UNENTSCHEIDBAR' items, as the preregistration specifies the full dataset as primary and exclusions as secondary sensitivity analyses."
    ]
    
    out = {
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
    
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
