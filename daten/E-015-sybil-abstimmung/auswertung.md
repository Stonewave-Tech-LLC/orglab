# Auswertung E-015-sybil-abstimmung

Runs: 20

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_no_human_vote | business | 5 | 0.843 (0.73–0.94) | 0.167 (0.06–0.29) | 0.933 (0.80–1.00) | 53.200 (47.80–57.40) | 11861.800 (10795.00–12744.80) |
| B_no_human_vote | coding | 5 | 0.929 (0.89–0.97) | 0.070 (0.01–0.13) | 1.000 (1.00–1.00) | 55.200 (42.00–67.20) | 13666.600 (13088.80–14244.40) |
| B_no_human_vote3 | business | 5 | 0.514 (0.39–0.64) | 0.427 (0.33–0.53) | 0.600 (0.27–0.87) | 27.200 (23.20–31.40) | 9934.800 (8334.60–11103.00) |
| B_no_human_vote3 | coding | 5 | 0.500 (0.41–0.61) | 0.466 (0.37–0.53) | 0.800 (0.67–0.93) | 29.600 (26.40–33.00) | 10058.400 (9379.60–10737.20) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_no_human_vote | 10 | 0.886 (0.81–0.94) | 0.118 (0.05–0.19) | 0.967 (0.90–1.00) | 54.200 (47.50–60.60) | 12764.200 (11906.00–13540.60) |
| B_no_human_vote3 | 10 | 0.507 (0.42–0.59) | 0.446 (0.38–0.52) | 0.700 (0.50–0.87) | 28.400 (25.60–31.10) | 9996.600 (9136.20–10671.60) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; q = BH-FDR über diese Familie; Cohen's d)

| A | B | Δ (A−B) | p | q | d |
|---|---|---|---|---|---|
| B_no_human_vote | B_no_human_vote3 | +0.379 | 0.0004 | 0.0004 | 3.08 |