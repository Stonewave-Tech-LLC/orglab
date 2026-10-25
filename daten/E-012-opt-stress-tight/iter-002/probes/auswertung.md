# Auswertung probes

Runs: 30

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_minimal_tight | business | 5 | 0.912 (0.89–0.94) | 0.061 (0.01–0.11) | 1.000 (1.00–1.00) | 19.800 (13.40–25.60) | 12466.200 (11526.40–13698.20) |
| B_minimal_tight | coding | 5 | 0.963 (0.94–0.99) | 0.041 (0.01–0.07) | 1.000 (1.00–1.00) | 13.600 (9.80–17.20) | 12575.400 (12050.20–13326.60) |
| B_minimal_tight~i2i | business | 5 | 0.850 (0.79–0.90) | 0.111 (0.09–0.13) | 1.000 (1.00–1.00) | 11.400 (8.20–14.60) | 10780.600 (10133.60–11475.00) |
| B_minimal_tight~i2i | coding | 5 | 0.875 (0.81–0.93) | 0.108 (0.07–0.16) | 1.000 (1.00–1.00) | 10.800 (8.40–13.80) | 11201.800 (10474.80–11975.00) |
| B_minimal_tight~i2s | business | 5 | 0.912 (0.89–0.94) | 0.106 (0.05–0.16) | 1.000 (1.00–1.00) | 23.000 (19.80–25.60) | 12234.600 (11574.40–12882.60) |
| B_minimal_tight~i2s | coding | 5 | 0.887 (0.85–0.93) | 0.120 (0.08–0.16) | 1.000 (1.00–1.00) | 14.600 (9.80–19.20) | 11282.200 (10646.80–11923.60) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_minimal_tight | 10 | 0.938 (0.91–0.96) | 0.051 (0.02–0.08) | 1.000 (1.00–1.00) | 16.700 (12.80–21.00) | 12520.800 (11946.60–13181.20) |
| B_minimal_tight~i2i | 10 | 0.863 (0.82–0.90) | 0.109 (0.09–0.13) | 1.000 (1.00–1.00) | 11.100 (9.00–13.30) | 10991.200 (10473.90–11517.80) |
| B_minimal_tight~i2s | 10 | 0.900 (0.88–0.93) | 0.113 (0.07–0.15) | 1.000 (1.00–1.00) | 18.800 (14.80–22.30) | 11758.400 (11202.50–12306.00) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; Cohen's d)

| A | B | Δ (A−B) | p | d |
|---|---|---|---|---|
| B_minimal_tight | B_minimal_tight~i2i | +0.075 | 0.0176 | 1.29 |
| B_minimal_tight | B_minimal_tight~i2s | +0.037 | 0.1298 | 0.88 |
| B_minimal_tight~i2i | B_minimal_tight~i2s | -0.037 | 0.2517 | -0.64 |