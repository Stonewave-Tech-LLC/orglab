# Auswertung k2

Runs: 20

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_no_human | business | 5 | 0.486 (0.39–0.56) | 0.455 (0.38–0.55) | 0.600 (0.27–0.87) | 28.400 (27.00–29.80) | 9443.600 (8756.40–10109.60) |
| B_no_human | coding | 5 | 0.529 (0.43–0.64) | 0.437 (0.35–0.51) | 0.800 (0.67–0.93) | 29.400 (26.80–33.40) | 10721.000 (9491.60–11950.40) |
| B_no_human_vote | business | 5 | 0.957 (0.90–1.00) | 0.043 (0.00–0.10) | 1.000 (1.00–1.00) | 30.600 (25.20–35.20) | 12380.800 (11172.20–13491.60) |
| B_no_human_vote | coding | 5 | 0.900 (0.80–0.99) | 0.118 (0.01–0.22) | 1.000 (1.00–1.00) | 27.800 (25.40–31.00) | 12619.400 (11693.00–13458.80) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_no_human | 10 | 0.507 (0.43–0.57) | 0.446 (0.39–0.51) | 0.700 (0.50–0.87) | 28.900 (27.30–31.00) | 10082.300 (9304.40–10928.30) |
| B_no_human_vote | 10 | 0.929 (0.87–0.98) | 0.080 (0.02–0.15) | 1.000 (1.00–1.00) | 29.200 (26.30–32.20) | 12500.100 (11752.70–13190.40) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; q = BH-FDR über diese Familie; Cohen's d)

| A | B | Δ (A−B) | p | q | d |
|---|---|---|---|---|---|
| B_no_human | B_no_human_vote | -0.421 | 0.0004 | 0.0004 | -3.91 |