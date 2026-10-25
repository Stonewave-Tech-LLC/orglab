# Auswertung k1

Runs: 20

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_minimal | business | 5 | 0.900 (0.83–0.96) | 0.059 (0.01–0.11) | 1.000 (1.00–1.00) | 36.200 (29.20–44.20) | 15003.400 (14160.80–15871.00) |
| B_minimal | coding | 5 | 0.986 (0.96–1.00) | 0.014 (0.00–0.04) | 1.000 (1.00–1.00) | 28.800 (21.80–35.80) | 13099.400 (12730.80–13468.00) |
| B_verify_bureaucracy | business | 5 | 0.914 (0.86–0.97) | 0.086 (0.03–0.14) | 1.000 (1.00–1.00) | 32.000 (25.60–38.40) | 14497.600 (12990.80–16063.00) |
| B_verify_bureaucracy | coding | 5 | 0.914 (0.81–0.99) | 0.062 (0.01–0.11) | 1.000 (1.00–1.00) | 30.800 (21.40–39.00) | 15503.400 (12897.20–18109.60) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_minimal | 10 | 0.943 (0.89–0.98) | 0.037 (0.01–0.07) | 1.000 (1.00–1.00) | 32.500 (27.30–38.40) | 14051.400 (13310.70–14820.40) |
| B_verify_bureaucracy | 10 | 0.914 (0.86–0.96) | 0.074 (0.04–0.12) | 1.000 (1.00–1.00) | 31.400 (25.50–36.40) | 15000.500 (13472.00–16565.70) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; q = BH-FDR über diese Familie; Cohen's d)

| A | B | Δ (A−B) | p | q | d |
|---|---|---|---|---|---|
| B_minimal | B_verify_bureaucracy | +0.029 | 0.5717 | 0.5717 | 0.34 |