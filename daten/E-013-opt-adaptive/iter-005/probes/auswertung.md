# Auswertung probes

Runs: 30

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_minimal_tight | business | 5 | 0.925 (0.84–0.99) | 0.082 (0.01–0.17) | 1.000 (1.00–1.00) | 15.600 (7.40–22.40) | 10832.400 (9037.00–11833.40) |
| B_minimal_tight | coding | 5 | 0.900 (0.85–0.96) | 0.108 (0.04–0.19) | 1.000 (1.00–1.00) | 18.200 (8.40–28.60) | 11940.400 (11511.80–12412.00) |
| B_minimal_tight~i5i | business | 5 | 0.925 (0.86–0.99) | 0.062 (0.01–0.11) | 1.000 (1.00–1.00) | 16.000 (13.60–18.80) | 10804.200 (10066.00–11744.60) |
| B_minimal_tight~i5i | coding | 5 | 0.887 (0.85–0.93) | 0.089 (0.04–0.14) | 1.000 (1.00–1.00) | 12.000 (7.00–16.00) | 10867.800 (10083.20–11792.60) |
| B_minimal_tight~i5s | business | 5 | 0.900 (0.81–0.99) | 0.050 (0.00–0.12) | 1.000 (1.00–1.00) | 16.800 (13.20–20.00) | 11442.200 (11262.00–11605.80) |
| B_minimal_tight~i5s | coding | 5 | 0.838 (0.72–0.91) | 0.094 (0.08–0.11) | 1.000 (1.00–1.00) | 18.800 (12.20–27.00) | 12113.000 (11044.60–13448.60) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_minimal_tight | 10 | 0.912 (0.86–0.96) | 0.095 (0.04–0.16) | 1.000 (1.00–1.00) | 16.900 (10.60–23.30) | 11386.400 (10418.20–12041.70) |
| B_minimal_tight~i5i | 10 | 0.906 (0.86–0.94) | 0.076 (0.04–0.11) | 1.000 (1.00–1.00) | 14.000 (10.80–16.80) | 10836.000 (10286.50–11478.40) |
| B_minimal_tight~i5s | 10 | 0.869 (0.79–0.93) | 0.072 (0.04–0.11) | 1.000 (1.00–1.00) | 17.800 (13.90–22.50) | 11777.600 (11231.90–12488.30) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; q = BH-FDR über diese Familie; Cohen's d)

| A | B | Δ (A−B) | p | q | d |
|---|---|---|---|---|---|
| B_minimal_tight | B_minimal_tight~i5i | +0.006 | 1.0000 | 1.0000 | 0.08 |
| B_minimal_tight | B_minimal_tight~i5s | +0.044 | 0.4205 | 0.7142 | 0.43 |
| B_minimal_tight~i5i | B_minimal_tight~i5s | +0.037 | 0.4761 | 0.7142 | 0.40 |