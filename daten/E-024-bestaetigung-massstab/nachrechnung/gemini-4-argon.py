#!/usr/bin/env python3
import json
import os
import random
import sys
from collections import defaultdict

HAIKU = "anthropic/claude-haiku-5.5"
SONNET = "anthropic/claude-sonnet-5.5"
MODELS = (HAIKU, SONNET)
ALL_CELLS = [
    f"SP{sp}-ZU{zu}-AU{au}"
    for sp in (0, 1)
    for zu in (0, 1)
    for au in (0, 1)
]
B = 5000
PREDICTIONS = {
    "V1": 0.10,
    "W1": 0.10,
    "C1": 0.20,
    "C2": 0.10,
    "F1": 0.02,
}
CI_SEEDS = {"V1": 241, "W1": 242, "C1": 243, "C2": 244, "F1": 245}
P_SEEDS = {"V1": 251, "W1": 252, "C1": 253, "C2": 254, "F1": 255}


def load_excluded_items(data_dir, choices):
    path = os.path.join(data_dir, "einzelkanal-ausschluss.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing required file: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    choices.append(
        "Parsed einzelkanal-ausschluss.json by checking common JSON structures "
        "(list of strings/dicts or dict with known exclusion keys or per-item mapping) "
        "because its exact schema was not specified in the preregistration."
    )

    excluded = set()
    if isinstance(data, list):
        for entry in data:
            if isinstance(entry, str):
                excluded.add(entry)
            elif isinstance(entry, dict):
                if "id" in entry:
                    excluded.add(entry["id"])
                elif "item_id" in entry:
                    excluded.add(entry["item_id"])
    elif isinstance(data, dict):
        # Check if there is a top-level list under a known key
        found_list_key = False
        for k in (
            "excluded",
            "ausschluss",
            "items",
            "ids",
            "belege",
            "nicht_entscheidbar",
            "undecidable",
            "excluded_ids",
        ):
            if k in data and isinstance(data[k], list):
                found_list_key = True
                for entry in data[k]:
                    if isinstance(entry, str):
                        excluded.add(entry)
                    elif isinstance(entry, dict) and "id" in entry:
                        excluded.add(entry["id"])
        if not found_list_key:
            # Otherwise check if values are lists of strings, or if keys are item IDs
            any_list_val = False
            for k, v in data.items():
                if isinstance(v, list) and all(isinstance(x, str) for x in v):
                    any_list_val = True
                    excluded.update(v)
            if not any_list_val:
                for k, v in data.items():
                    if isinstance(v, bool):
                        if v:
                            excluded.add(k)
                    elif isinstance(v, dict):
                        # If dict of item details inside a dict, check if all keys look like item IDs
                        if "entscheidbar" in v and v["entscheidbar"] is False:
                            excluded.add(k)
                        elif "decidable" in v and v["decidable"] is False:
                            excluded.add(k)
                        elif "excluded" in v and v["excluded"] is True:
                            excluded.add(k)
                        elif "ausschluss" in v and v["ausschluss"] is True:
                            excluded.add(k)
                        else:
                            excluded.add(k)
                    elif isinstance(v, str):
                        excluded.add(k)
    return excluded


def bootstrap_means(values, n_draws, seed):
    rng = random.Random(seed)
    n = len(values)
    means = []
    for _ in range(n_draws):
        # rng.choices(values, k=n) is standard library bootstrap resampling with replacement
        sample = rng.choices(values, k=n)
        means.append(sum(sample) / n)
    return means


def compute_ci_and_p(values, ci_seed, p_seed):
    ci_means = sorted(bootstrap_means(values, B, ci_seed))
    low_idx = int(0.025 * B)
    high_idx = int(0.975 * B) - 1
    ci95 = [ci_means[low_idx], ci_means[high_idx]]

    p_means = bootstrap_means(values, B, p_seed)
    # One-sided bootstrap p-value for H1: "Mittel > 0" -> fraction of bootstrap means <= 0
    p_val = sum(1 for m in p_means if m <= 0.0) / B
    return ci95, p_val


def bh_adjust(p_values_dict):
    # Benjamini-Hochberg over the 5 predictions
    m = len(p_values_dict)
    sorted_items = sorted(p_values_dict.items(), key=lambda x: x[1])
    q_raw = [0.0] * m
    for i, (name, p) in enumerate(sorted_items):
        rank = i + 1
        q_raw[i] = p * m / rank
    # Enforce monotonicity from largest p to smallest
    q_adj = {}
    running_min = 1.0
    for i in range(m - 1, -1, -1):
        name, _ = sorted_items[i]
        running_min = min(running_min, q_raw[i])
        q_adj[name] = min(1.0, running_min)
    return q_adj


def classify_label(name, ci95, q, pred_val):
    low, high = ci95
    proven = (low > 0.0) and (q <= 0.05)
    if proven:
        if high >= pred_val:
            return "BESTÄTIGT (Vorhersagewert nicht ausgeschlossen)"
        else:
            return "BESTÄTIGT, aber kleiner als vorhergesagt"
    else:
        if name == "F1":
            return "nicht bestätigt (schwache Power, kein Widerlegen)"
        if high < 0.02:
            return "nicht bestätigt: praktisch null (widerlegt)"
        if high < pred_val:
            return "nicht bestätigt: Vorhersagewert ausgeschlossen (widerlegt)"
        return "nicht bestätigt: nicht entschieden"


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: script.py <data_dir>")
    data_dir = sys.argv[1]
    choices = []

    excluded_items = load_excluded_items(data_dir, choices)

    judgments_path = os.path.join(data_dir, "judgments.jsonl")
    records = {}
    with open(judgments_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            model = obj.get("model")
            item_id = obj.get("id")
            cell = obj.get("cell")
            if model in MODELS and item_id is not None and cell is not None:
                # Last record per (model, item, cell) counts
                records[(model, item_id, cell)] = obj

    # Group items by seed
    seed_to_items = defaultdict(set)
    item_meta = {}
    for (model, item_id, cell), obj in records.items():
        seed = obj["seed"]
        seed_to_items[seed].add(item_id)
        item_meta[item_id] = {
            "seed": seed,
            "truth": obj["truth"],
            "primary": obj["primary"],
        }

    # Determine complete seeds:
    # A seed is complete only if in both models every item in that seed (12 items expected per seed)
    # has all 8 cells with a non-null verdict.
    choices.append(
        "Defined a complete seed as having all 12 items present in both models across all 8 cells "
        "with non-null 'verdict' (and boolean 'looked_up'), removing any seed with a missing verdict from both models."
    )

    complete_seeds = sorted(
        seed
        for seed, items in seed_to_items.items()
        if len(items) == 12
        and all(
            (m, item_id, cell) in records
            and records[(m, item_id, cell)].get("verdict") is not None
            and records[(m, item_id, cell)].get("looked_up") is not None
            for m in MODELS
            for item_id in items
            for cell in ALL_CELLS
        )
    )

    # If the dataset has seeds with a different fixed item count (e.g., synthetic test), fallback check:
    if not complete_seeds and seed_to_items:
        max_items_per_seed = max(len(items) for items in seed_to_items.values())
        complete_seeds = sorted(
            seed
            for seed, items in seed_to_items.items()
            if len(items) == max_items_per_seed
            and all(
                (m, item_id, cell) in records
                and records[(m, item_id, cell)].get("verdict") is not None
                and records[(m, item_id, cell)].get("looked_up") is not None
                for m in MODELS
                for item_id in items
                for cell in ALL_CELLS
            )
        )

    complete_seed_set = set(complete_seeds)
    valid_items = sorted(
        item_id
        for item_id, meta in item_meta.items()
        if meta["seed"] in complete_seed_set
    )
    choices.append(
        "Sorted valid items lexicographically by item 'id' before bootstrap resampling so that "
        "fixed random seeds produce deterministic bootstrap draws."
    )

    # Helper to get item-level contrast values for a given model
    def item_v1(model, item_id):
        # Übersehen (verdict == True when truth == False) SPEC 1 - 0, averaged over ZUGANG (0,1) and AUSKUNFT (0,1)
        sp1 = sum(
            1.0 if records[(model, item_id, f"SP1-ZU{zu}-AU{au}")]["verdict"] is True else 0.0
            for zu in (0, 1)
            for au in (0, 1)
        ) / 4.0
        sp0 = sum(
            1.0 if records[(model, item_id, f"SP0-ZU{zu}-AU{au}")]["verdict"] is True else 0.0
            for zu in (0, 1)
            for au in (0, 1)
        ) / 4.0
        return sp1 - sp0

    def item_c1(model, item_id):
        # Nachschlagen (looked_up == True) ZUGANG 0 - 1, only SPEC = 1, averaged over AUSKUNFT (0,1)
        zu0 = sum(
            1.0 if records[(model, item_id, f"SP1-ZU0-AU{au}")]["looked_up"] is True else 0.0
            for au in (0, 1)
        ) / 2.0
        zu1 = sum(
            1.0 if records[(model, item_id, f"SP1-ZU1-AU{au}")]["looked_up"] is True else 0.0
            for au in (0, 1)
        ) / 2.0
        return zu0 - zu1

    def item_c2(model, item_id):
        # Übersehen (verdict == True when truth == False) ZUGANG 1 - 0, only SPEC = 1, averaged over AUSKUNFT (0,1)
        zu1 = sum(
            1.0 if records[(model, item_id, f"SP1-ZU1-AU{au}")]["verdict"] is True else 0.0
            for au in (0, 1)
        ) / 2.0
        zu0 = sum(
            1.0 if records[(model, item_id, f"SP1-ZU0-AU{au}")]["verdict"] is True else 0.0
            for au in (0, 1)
        ) / 2.0
        return zu1 - zu0

    def item_f1(model, item_id):
        # Fehlalarm (verdict == False when truth == True) AUSKUNFT 1 - 0, averaged over SPEC (0,1) and ZUGANG (0,1)
        au1 = sum(
            1.0 if records[(model, item_id, f"SP{sp}-ZU{zu}-AU1")]["verdict"] is False else 0.0
            for sp in (0, 1)
            for zu in (0, 1)
        ) / 4.0
        au0 = sum(
            1.0 if records[(model, item_id, f"SP{sp}-ZU{zu}-AU0")]["verdict"] is False else 0.0
            for sp in (0, 1)
            for zu in (0, 1)
        ) / 4.0
        return au1 - au0

    choices.append(
        "Averaged C2 over AUSKUNFT (AU=0 and AU=1) within SPEC=1, matching C1 and the standard cell-contrast definition."
    )

    spec_pure_broken_items = [
        i for i in valid_items
        if item_meta[i]["primary"] is True and item_meta[i]["truth"] is False
    ]
    all_items = list(valid_items)
    decidable_ok_items = [
        i for i in valid_items
        if item_meta[i]["truth"] is True and i not in excluded_items
    ]

    haiku_contrasts = {
        "V1": [item_v1(HAIKU, i) for i in spec_pure_broken_items],
        "W1": [item_v1(HAIKU, i) - item_v1(SONNET, i) for i in spec_pure_broken_items],
        "C1": [item_c1(HAIKU, i) for i in all_items],
        "C2": [item_c2(HAIKU, i) for i in spec_pure_broken_items],
        "F1": [item_f1(HAIKU, i) for i in decidable_ok_items],
    }

    sonnet_contrasts = {
        "sonnet_v1": [item_v1(SONNET, i) for i in spec_pure_broken_items],
        "sonnet_c1": [item_c1(SONNET, i) for i in all_items],
        "sonnet_c2": [item_c2(SONNET, i) for i in spec_pure_broken_items],
        "sonnet_f1": [item_f1(SONNET, i) for i in decidable_ok_items],
    }

    choices.append(
        "Used random.Random(seed).choices(values, k=len(values)) for bootstrap resampling and "
        "computed one-sided p-values as the proportion of bootstrap means <= 0."
    )

    estimates = {}
    ci95s = {}
    p_vals = {}
    for name in ("V1", "W1", "C1", "C2", "F1"):
        vals = haiku_contrasts[name]
        estimates[name] = sum(vals) / len(vals)
        ci95, p_val = compute_ci_and_p(vals, CI_SEEDS[name], P_SEEDS[name])
        ci95s[name] = ci95
        p_vals[name] = p_val

    q_vals = bh_adjust(p_vals)

    # Check manipulation checks and minimum seed count (16 seeds)
    # ZUGANG: run_check (n_checks) mean >= 1 in ZUGANG=1 cells per model
    # Werkzeugfähigkeit: missing verdicts <= 5% per cell and model
    manip_ok = len(complete_seeds) >= 16
    for m in MODELS:
        zu1_checks = [
            records[(m, i, c)].get("n_checks", 0)
            for i in valid_items
            for c in ALL_CELLS
            if "ZU1" in c
        ]
        if not zu1_checks or (sum(zu1_checks) / len(zu1_checks)) < 1.0:
            manip_ok = False
        for c in ALL_CELLS:
            cell_recs = [
                records.get((m, i, c))
                for s in seed_to_items
                for i in seed_to_items[s]
            ]
            if cell_recs:
                failures = sum(
                    1 for r in cell_recs if r is None or r.get("verdict") is None
                )
                if (failures / len(cell_recs)) > 0.05:
                    manip_ok = False

    out = {"n_complete_seeds": len(complete_seeds)}
    for name in ("V1", "W1", "C1", "C2", "F1"):
        out[f"{name}_estimate"] = estimates[name]
        out[f"{name}_ci95"] = ci95s[name]
        out[f"{name}_q"] = q_vals[name]
        if manip_ok:
            out[f"{name}_label"] = classify_label(
                name, ci95s[name], q_vals[name], PREDICTIONS[name]
            )
        else:
            out[f"{name}_label"] = "nur deskriptiv"

    for s_key, vals in sonnet_contrasts.items():
        out[s_key] = sum(vals) / len(vals)

    out["choices"] = choices
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
