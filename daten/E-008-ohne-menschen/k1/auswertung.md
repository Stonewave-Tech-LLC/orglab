# Auswertung k1

Runs: 20

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_no_human | business | 5 | 0.657 (0.50–0.84) | 0.296 (0.13–0.43) | 0.733 (0.47–0.93) | 26.800 (24.60–29.20) | 11492.200 (9817.60–12893.60) |
| B_no_human | coding | 5 | 0.829 (0.77–0.89) | 0.134 (0.09–0.18) | 0.933 (0.80–1.00) | 30.800 (27.80–33.80) | 13559.000 (12824.60–14326.40) |
| B_no_human_vote | business | 5 | 0.986 (0.96–1.00) | 0.014 (0.00–0.04) | 1.000 (1.00–1.00) | 28.400 (25.60–31.00) | 11446.200 (10423.40–12488.60) |
| B_no_human_vote | coding | 5 | 1.000 (1.00–1.00) | 0.000 (0.00–0.00) | 1.000 (1.00–1.00) | 21.800 (14.00–29.60) | 11429.800 (10828.80–12030.80) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_no_human | 10 | 0.743 (0.63–0.85) | 0.215 (0.13–0.31) | 0.833 (0.67–0.97) | 28.800 (26.60–31.30) | 12525.600 (11376.80–13570.50) |
| B_no_human_vote | 10 | 0.993 (0.98–1.00) | 0.007 (0.00–0.02) | 1.000 (1.00–1.00) | 25.100 (19.70–29.60) | 11438.000 (10815.00–12076.70) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; q = BH-FDR über diese Familie; Cohen's d)

| A | B | Δ (A−B) | p | q | d |
|---|---|---|---|---|---|
| B_no_human | B_no_human_vote | -0.250 | 0.0004 | 0.0004 | -1.93 |