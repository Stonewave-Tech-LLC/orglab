# Auswertung k2

Runs: 20

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_minimal | business | 5 | 0.843 (0.81–0.86) | 0.082 (0.04–0.12) | 1.000 (1.00–1.00) | 33.800 (30.40–37.40) | 12193.800 (11627.80–12838.40) |
| B_minimal | coding | 5 | 0.829 (0.76–0.93) | 0.165 (0.07–0.26) | 1.000 (1.00–1.00) | 35.200 (30.60–39.20) | 12745.000 (11564.60–13753.40) |
| B_verify_bureaucracy | business | 5 | 0.857 (0.74–0.97) | 0.092 (0.00–0.22) | 0.933 (0.80–1.00) | 33.600 (30.60–35.80) | 11617.800 (11121.80–12335.20) |
| B_verify_bureaucracy | coding | 5 | 0.843 (0.79–0.90) | 0.107 (0.05–0.15) | 1.000 (1.00–1.00) | 35.600 (31.00–39.20) | 12965.200 (12237.80–13674.00) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_minimal | 10 | 0.836 (0.79–0.89) | 0.124 (0.06–0.19) | 1.000 (1.00–1.00) | 34.500 (31.70–37.30) | 12469.400 (11825.50–13109.80) |
| B_verify_bureaucracy | 10 | 0.850 (0.79–0.91) | 0.099 (0.05–0.16) | 0.967 (0.90–1.00) | 34.600 (32.00–37.10) | 12291.500 (11674.70–12965.30) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; q = BH-FDR über diese Familie; Cohen's d)

| A | B | Δ (A−B) | p | q | d |
|---|---|---|---|---|---|
| B_minimal | B_verify_bureaucracy | -0.014 | 0.8692 | 0.8692 | -0.15 |