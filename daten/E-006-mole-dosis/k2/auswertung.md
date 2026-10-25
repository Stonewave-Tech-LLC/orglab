# Auswertung k2

Runs: 20

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_minimal | business | 5 | 1.000 (1.00–1.00) | 0.000 (0.00–0.00) | 1.000 (1.00–1.00) | 20.200 (15.40–25.60) | 10961.400 (9061.40–12834.20) |
| B_minimal | coding | 5 | 1.000 (1.00–1.00) | 0.000 (0.00–0.00) | 1.000 (1.00–1.00) | 23.600 (16.80–30.40) | 11800.400 (9923.00–13969.00) |
| B_verify_bureaucracy | business | 5 | 1.000 (1.00–1.00) | 0.000 (0.00–0.00) | 1.000 (1.00–1.00) | 31.800 (24.00–41.00) | 12146.800 (10045.80–14335.60) |
| B_verify_bureaucracy | coding | 5 | 1.000 (1.00–1.00) | 0.000 (0.00–0.00) | 1.000 (1.00–1.00) | 19.000 (15.00–24.20) | 10708.000 (8921.60–12962.60) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_minimal | 10 | 1.000 (1.00–1.00) | 0.000 (0.00–0.00) | 1.000 (1.00–1.00) | 21.900 (17.80–26.20) | 11380.900 (10039.10–12818.80) |
| B_verify_bureaucracy | 10 | 1.000 (1.00–1.00) | 0.000 (0.00–0.00) | 1.000 (1.00–1.00) | 25.400 (19.50–32.50) | 11427.400 (10012.20–12981.00) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; q = BH-FDR über diese Familie; Cohen's d)

| A | B | Δ (A−B) | p | q | d |
|---|---|---|---|---|---|
| B_minimal | B_verify_bureaucracy | +0.000 | 1.0000 | 1.0000 | inf |