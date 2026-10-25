# Auswertung E-004-owner-only-replikation

Runs: 60

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_minimal_tight | business | 10 | 0.931 (0.91–0.96) | 0.068 (0.04–0.10) | 1.000 (1.00–1.00) | 16.700 (13.50–19.80) | 11888.900 (11422.80–12315.00) |
| B_minimal_tight | coding | 10 | 0.881 (0.82–0.93) | 0.120 (0.07–0.17) | 1.000 (1.00–1.00) | 20.600 (17.20–23.40) | 12865.300 (12299.40–13444.90) |
| B_minimal_tight | research | 10 | 0.887 (0.82–0.94) | 0.089 (0.03–0.16) | 0.975 (0.93–1.00) | 18.100 (15.20–20.80) | 12283.700 (11527.20–13257.10) |
| B_tight_owner_only | business | 10 | 0.863 (0.79–0.93) | 0.091 (0.05–0.15) | 0.950 (0.88–1.00) | 11.000 (8.80–13.00) | 10488.900 (9950.80–11078.30) |
| B_tight_owner_only | coding | 10 | 0.856 (0.78–0.92) | 0.129 (0.07–0.20) | 1.000 (1.00–1.00) | 11.400 (9.60–13.50) | 11051.600 (10645.00–11574.10) |
| B_tight_owner_only | research | 10 | 0.875 (0.84–0.91) | 0.069 (0.03–0.11) | 0.975 (0.93–1.00) | 9.800 (8.10–11.70) | 11316.900 (10868.20–11799.20) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_minimal_tight | 30 | 0.900 (0.87–0.93) | 0.092 (0.06–0.12) | 0.992 (0.97–1.00) | 18.467 (16.63–20.23) | 12345.967 (11953.73–12750.20) |
| B_tight_owner_only | 30 | 0.865 (0.83–0.90) | 0.096 (0.07–0.13) | 0.975 (0.94–1.00) | 10.733 (9.63–11.87) | 10952.467 (10649.90–11272.93) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; q = BH-FDR über diese Familie; Cohen's d)

| A | B | Δ (A−B) | p | q | d |
|---|---|---|---|---|---|
| B_minimal_tight | B_tight_owner_only | +0.035 | 0.1658 | 0.1658 | 0.38 |