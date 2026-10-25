# Auswertung E-018-beleg-statt-stimme

Runs: 40

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_no_human_deadline | business | 10 | 0.914 (0.87–0.96) | 0.084 (0.05–0.13) | 1.000 (1.00–1.00) | 27.100 (20.90–33.60) | 11173.500 (10281.50–11908.70) |
| B_no_human_deadline | coding | 10 | 0.879 (0.79–0.96) | 0.106 (0.04–0.18) | 0.900 (0.70–1.00) | 35.100 (30.30–40.10) | 12029.400 (11548.10–12506.00) |
| B_no_human_vote | business | 10 | 0.836 (0.79–0.89) | 0.170 (0.11–0.23) | 1.000 (1.00–1.00) | 53.900 (48.90–59.00) | 13204.300 (12451.80–13900.80) |
| B_no_human_vote | coding | 10 | 0.893 (0.84–0.94) | 0.107 (0.07–0.15) | 1.000 (1.00–1.00) | 57.800 (52.80–63.10) | 13701.300 (12932.50–14510.50) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_no_human_deadline | 20 | 0.896 (0.85–0.94) | 0.095 (0.06–0.14) | 0.950 (0.85–1.00) | 31.100 (26.65–35.75) | 11601.450 (11089.65–12071.00) |
| B_no_human_vote | 20 | 0.864 (0.83–0.90) | 0.138 (0.10–0.18) | 1.000 (1.00–1.00) | 55.850 (52.30–59.70) | 13452.800 (12870.50–13986.95) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; q = BH-FDR über diese Familie; Cohen's d)

| A | B | Δ (A−B) | p | q | d |
|---|---|---|---|---|---|
| B_no_human_deadline | B_no_human_vote | +0.032 | 0.3807 | 0.3807 | 0.32 |