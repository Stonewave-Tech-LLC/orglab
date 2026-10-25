# Auswertung k1

Runs: 20

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_minimal | business | 5 | 0.986 (0.96–1.00) | 0.014 (0.00–0.04) | 1.000 (1.00–1.00) | 20.200 (15.20–24.40) | 10770.400 (9999.40–11802.80) |
| B_minimal | coding | 5 | 0.986 (0.96–1.00) | 0.014 (0.00–0.04) | 1.000 (1.00–1.00) | 12.000 (5.80–21.60) | 9533.200 (7773.60–11220.60) |
| B_verify_bureaucracy | business | 5 | 0.986 (0.96–1.00) | 0.014 (0.00–0.04) | 1.000 (1.00–1.00) | 27.600 (17.80–38.20) | 12873.400 (10803.80–14934.20) |
| B_verify_bureaucracy | coding | 5 | 1.000 (1.00–1.00) | 0.000 (0.00–0.00) | 1.000 (1.00–1.00) | 17.200 (11.60–25.80) | 11913.200 (10021.20–14218.60) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_minimal | 10 | 0.986 (0.96–1.00) | 0.014 (0.00–0.04) | 1.000 (1.00–1.00) | 16.100 (10.50–21.30) | 10151.800 (9150.90–11046.90) |
| B_verify_bureaucracy | 10 | 0.993 (0.98–1.00) | 0.007 (0.00–0.02) | 1.000 (1.00–1.00) | 22.400 (16.00–29.70) | 12393.300 (10942.60–13970.40) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; q = BH-FDR über diese Familie; Cohen's d)

| A | B | Δ (A−B) | p | q | d |
|---|---|---|---|---|---|
| B_minimal | B_verify_bureaucracy | -0.007 | 1.0000 | 1.0000 | -0.27 |