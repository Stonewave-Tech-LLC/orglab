# Auswertung probes

Runs: 10

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_minimal | business | 5 | 0.988 (0.96–1.00) | 0.013 (0.00–0.04) | 1.000 (1.00–1.00) | 26.200 (20.20–32.80) | 14726.600 (12640.40–17003.80) |
| B_minimal | coding | 5 | 1.000 (1.00–1.00) | 0.000 (0.00–0.00) | 1.000 (1.00–1.00) | 15.800 (13.40–18.20) | 12007.800 (10286.80–13698.00) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_minimal | 10 | 0.994 (0.98–1.00) | 0.006 (0.00–0.02) | 1.000 (1.00–1.00) | 21.000 (16.50–25.80) | 13367.200 (11751.60–15047.10) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; Cohen's d)

| A | B | Δ (A−B) | p | d |
|---|---|---|---|---|