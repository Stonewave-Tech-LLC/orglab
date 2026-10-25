# Auswertung probes

Runs: 30

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_minimal_tight | business | 5 | 0.900 (0.85–0.94) | 0.132 (0.07–0.22) | 1.000 (1.00–1.00) | 20.400 (16.80–24.00) | 12261.800 (10982.60–13359.20) |
| B_minimal_tight | coding | 5 | 0.900 (0.88–0.95) | 0.093 (0.04–0.13) | 1.000 (1.00–1.00) | 18.200 (14.00–23.20) | 11213.000 (10978.40–11477.40) |
| B_minimal_tight~i3i | business | 5 | 0.875 (0.82–0.94) | 0.126 (0.06–0.19) | 1.000 (1.00–1.00) | 19.200 (13.80–24.00) | 12919.400 (12113.60–13814.80) |
| B_minimal_tight~i3i | coding | 5 | 0.925 (0.89–0.96) | 0.081 (0.04–0.12) | 1.000 (1.00–1.00) | 20.600 (14.80–25.40) | 13016.400 (12301.20–13696.40) |
| B_minimal_tight~i3s | business | 5 | 0.863 (0.80–0.95) | 0.126 (0.05–0.19) | 1.000 (1.00–1.00) | 6.000 (2.60–9.80) | 12820.800 (12066.80–13543.40) |
| B_minimal_tight~i3s | coding | 5 | 0.900 (0.88–0.93) | 0.078 (0.03–0.13) | 1.000 (1.00–1.00) | 7.400 (5.00–9.20) | 12449.200 (11552.60–13072.60) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_minimal_tight | 10 | 0.900 (0.87–0.93) | 0.112 (0.07–0.17) | 1.000 (1.00–1.00) | 19.300 (16.40–22.50) | 11737.400 (11106.70–12491.60) |
| B_minimal_tight~i3i | 10 | 0.900 (0.86–0.94) | 0.104 (0.06–0.14) | 1.000 (1.00–1.00) | 19.900 (15.90–23.40) | 12967.900 (12432.90–13519.40) |
| B_minimal_tight~i3s | 10 | 0.881 (0.84–0.92) | 0.102 (0.05–0.15) | 1.000 (1.00–1.00) | 6.700 (4.60–8.70) | 12635.000 (12038.50–13149.20) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; Cohen's d)

| A | B | Δ (A−B) | p | d |
|---|---|---|---|---|
| B_minimal_tight | B_minimal_tight~i3i | +0.000 | 1.0000 | 0.00 |
| B_minimal_tight | B_minimal_tight~i3s | +0.019 | 0.6591 | 0.31 |
| B_minimal_tight~i3i | B_minimal_tight~i3s | +0.019 | 0.6911 | 0.28 |