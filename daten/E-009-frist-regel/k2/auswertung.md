# Auswertung k2

Runs: 10

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_no_human_deadline | business | 5 | 0.886 (0.79–0.99) | 0.114 (0.01–0.21) | 0.933 (0.80–1.00) | 31.600 (21.80–39.60) | 10967.000 (10286.00–11648.00) |
| B_no_human_deadline | coding | 5 | 0.871 (0.77–0.96) | 0.129 (0.04–0.23) | 1.000 (1.00–1.00) | 31.000 (25.60–36.40) | 12688.000 (11809.40–13566.60) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_no_human_deadline | 10 | 0.879 (0.81–0.94) | 0.121 (0.06–0.19) | 0.967 (0.90–1.00) | 31.300 (26.40–36.20) | 11827.500 (11064.80–12687.90) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; q = BH-FDR über diese Familie; Cohen's d)

| A | B | Δ (A−B) | p | q | d |
|---|---|---|---|---|---|