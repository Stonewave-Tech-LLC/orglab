# Auswertung probes

Runs: 30

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_minimal_tight | business | 5 | 0.838 (0.79–0.88) | 0.139 (0.12–0.17) | 1.000 (1.00–1.00) | 21.200 (18.00–24.60) | 11403.000 (10825.60–11980.40) |
| B_minimal_tight | coding | 5 | 0.925 (0.86–0.99) | 0.067 (0.01–0.13) | 1.000 (1.00–1.00) | 19.200 (14.80–23.60) | 12711.800 (11708.80–13714.80) |
| B_minimal_tight~i1i | business | 5 | 0.863 (0.80–0.93) | 0.119 (0.07–0.20) | 1.000 (1.00–1.00) | 19.800 (14.80–24.80) | 13625.400 (13010.40–14102.20) |
| B_minimal_tight~i1i | coding | 5 | 0.887 (0.84–0.93) | 0.102 (0.06–0.15) | 1.000 (1.00–1.00) | 11.600 (6.20–18.00) | 12835.600 (11537.80–13501.60) |
| B_minimal_tight~i1s | business | 5 | 0.850 (0.81–0.90) | 0.152 (0.10–0.19) | 1.000 (1.00–1.00) | 12.800 (9.60–16.60) | 11905.400 (11065.60–12813.60) |
| B_minimal_tight~i1s | coding | 5 | 0.838 (0.81–0.86) | 0.117 (0.05–0.18) | 1.000 (1.00–1.00) | 17.800 (11.80–23.60) | 12954.600 (12685.00–13239.40) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_minimal_tight | 10 | 0.881 (0.84–0.93) | 0.103 (0.06–0.14) | 1.000 (1.00–1.00) | 20.200 (17.10–23.00) | 12057.400 (11397.20–12821.40) |
| B_minimal_tight~i1i | 10 | 0.875 (0.84–0.91) | 0.111 (0.07–0.15) | 1.000 (1.00–1.00) | 15.700 (10.90–20.30) | 13230.500 (12481.40–13775.60) |
| B_minimal_tight~i1s | 10 | 0.844 (0.82–0.87) | 0.135 (0.09–0.17) | 1.000 (1.00–1.00) | 15.300 (11.70–19.20) | 12430.000 (11821.40–12971.20) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; Cohen's d)

| A | B | Δ (A−B) | p | d |
|---|---|---|---|---|
| B_minimal_tight | B_minimal_tight~i1i | +0.006 | 1.0000 | 0.09 |
| B_minimal_tight | B_minimal_tight~i1s | +0.037 | 0.2975 | 0.58 |
| B_minimal_tight~i1i | B_minimal_tight~i1s | +0.031 | 0.3369 | 0.56 |