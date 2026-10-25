# Auswertung probes

Runs: 30

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_minimal_tight | business | 5 | 0.900 (0.85–0.94) | 0.102 (0.06–0.16) | 1.000 (1.00–1.00) | 19.600 (14.20–25.60) | 11730.200 (11344.00–12116.40) |
| B_minimal_tight | coding | 5 | 0.925 (0.89–0.97) | 0.075 (0.03–0.11) | 1.000 (1.00–1.00) | 18.800 (15.80–21.40) | 12892.000 (12176.00–13560.40) |
| B_minimal_tight~i4i | business | 5 | 0.875 (0.80–0.94) | 0.087 (0.02–0.17) | 1.000 (1.00–1.00) | 10.400 (9.20–11.80) | 10736.000 (10020.20–11566.40) |
| B_minimal_tight~i4i | coding | 5 | 0.900 (0.82–0.96) | 0.093 (0.04–0.14) | 1.000 (1.00–1.00) | 9.800 (8.20–11.20) | 10410.400 (9252.80–11181.40) |
| B_minimal_tight~i4s | business | 5 | 0.863 (0.82–0.90) | 0.134 (0.11–0.16) | 1.000 (1.00–1.00) | 12.400 (10.20–15.20) | 10890.600 (9911.40–11850.00) |
| B_minimal_tight~i4s | coding | 5 | 0.938 (0.88–0.99) | 0.079 (0.01–0.16) | 1.000 (1.00–1.00) | 9.400 (8.00–11.40) | 10579.800 (9784.80–11374.80) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_minimal_tight | 10 | 0.912 (0.88–0.94) | 0.089 (0.06–0.12) | 1.000 (1.00–1.00) | 19.200 (16.00–22.50) | 12311.100 (11815.90–12878.20) |
| B_minimal_tight~i4i | 10 | 0.887 (0.84–0.93) | 0.090 (0.04–0.14) | 1.000 (1.00–1.00) | 10.100 (9.10–11.10) | 10573.200 (9866.80–11191.90) |
| B_minimal_tight~i4s | 10 | 0.900 (0.86–0.94) | 0.106 (0.06–0.15) | 1.000 (1.00–1.00) | 10.900 (9.20–12.70) | 10735.200 (10093.00–11419.60) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; q = BH-FDR über diese Familie; Cohen's d)

| A | B | Δ (A−B) | p | q | d |
|---|---|---|---|---|---|
| B_minimal_tight | B_minimal_tight~i4i | +0.025 | 0.5653 | 0.8652 | 0.35 |
| B_minimal_tight | B_minimal_tight~i4s | +0.012 | 0.8344 | 0.8652 | 0.20 |
| B_minimal_tight~i4i | B_minimal_tight~i4s | -0.013 | 0.8652 | 0.8652 | -0.15 |