# Auswertung probes

Runs: 10

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_minimal_tight | business | 5 | 0.938 (0.88–0.99) | 0.070 (0.01–0.14) | 1.000 (1.00–1.00) | 15.200 (8.80–22.00) | 11174.400 (10508.20–11773.80) |
| B_minimal_tight | coding | 5 | 0.912 (0.89–0.94) | 0.098 (0.06–0.14) | 1.000 (1.00–1.00) | 20.600 (15.80–26.00) | 11971.000 (11680.40–12254.80) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_minimal_tight | 10 | 0.925 (0.89–0.96) | 0.084 (0.05–0.12) | 1.000 (1.00–1.00) | 17.900 (13.50–22.60) | 11572.700 (11127.20–11963.50) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; q = BH-FDR über diese Familie; Cohen's d)

| A | B | Δ (A−B) | p | q | d |
|---|---|---|---|---|---|