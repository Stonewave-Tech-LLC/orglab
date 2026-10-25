# Auswertung k0

Runs: 20

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_minimal | business | 5 | 0.986 (0.96–1.00) | 0.014 (0.00–0.04) | 1.000 (1.00–1.00) | 14.200 (10.60–19.40) | 10557.000 (9674.00–11511.20) |
| B_minimal | coding | 5 | 1.000 (1.00–1.00) | 0.000 (0.00–0.00) | 1.000 (1.00–1.00) | 15.600 (12.00–19.80) | 9521.400 (8215.80–10786.40) |
| B_verify_bureaucracy | business | 5 | 0.986 (0.96–1.00) | 0.014 (0.00–0.04) | 1.000 (1.00–1.00) | 17.000 (9.40–23.20) | 10547.000 (9159.00–11779.60) |
| B_verify_bureaucracy | coding | 5 | 1.000 (1.00–1.00) | 0.000 (0.00–0.00) | 1.000 (1.00–1.00) | 17.400 (11.80–21.80) | 10851.200 (9604.20–12426.00) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_minimal | 10 | 0.993 (0.98–1.00) | 0.007 (0.00–0.02) | 1.000 (1.00–1.00) | 14.900 (12.30–18.10) | 10039.200 (9165.40–10814.40) |
| B_verify_bureaucracy | 10 | 0.993 (0.98–1.00) | 0.007 (0.00–0.02) | 1.000 (1.00–1.00) | 17.200 (12.80–21.30) | 10699.100 (9766.50–11690.80) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; q = BH-FDR über diese Familie; Cohen's d)

| A | B | Δ (A−B) | p | q | d |
|---|---|---|---|---|---|
| B_minimal | B_verify_bureaucracy | +0.000 | 1.0000 | 1.0000 | 0.00 |