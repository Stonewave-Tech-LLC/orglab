# Auswertung probes

Runs: 10

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_minimal | business | 5 | 0.971 (0.91–1.00) | 0.029 (0.00–0.09) | 1.000 (1.00–1.00) | 17.200 (12.20–22.60) | 9611.000 (7813.20–11012.00) |
| B_minimal | coding | 5 | 1.000 (1.00–1.00) | 0.000 (0.00–0.00) | 1.000 (1.00–1.00) | 12.400 (10.20–15.00) | 8961.800 (7564.20–10390.80) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_minimal | 10 | 0.986 (0.96–1.00) | 0.014 (0.00–0.04) | 1.000 (1.00–1.00) | 14.800 (11.90–18.40) | 9286.400 (8147.50–10382.10) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; Cohen's d)

| A | B | Δ (A−B) | p | d |
|---|---|---|---|---|