# Auswertung probes

Runs: 38

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_minimal_tight | business | 5 | 0.825 (0.79–0.86) | 0.147 (0.09–0.20) | 0.950 (0.85–1.00) | 21.800 (14.40–29.20) | 13122.000 (12432.80–13717.60) |
| B_minimal_tight | coding | 5 | 0.887 (0.88–0.91) | 0.102 (0.08–0.12) | 1.000 (1.00–1.00) | 25.600 (20.40–30.80) | 11825.400 (10964.60–12686.20) |
| B_minimal_tight~i3i | business | 8 | 0.852 (0.79–0.91) | 0.123 (0.06–0.21) | 0.938 (0.81–1.00) | 1.875 (0.75–3.12) | 11278.000 (11031.25–11510.88) |
| B_minimal_tight~i3i | coding | 10 | 0.856 (0.80–0.91) | 0.058 (0.03–0.09) | 0.950 (0.88–1.00) | 2.200 (1.60–2.70) | 11349.200 (11066.60–11655.20) |
| B_minimal_tight~i3s | business | 5 | 0.900 (0.82–0.97) | 0.055 (0.00–0.14) | 1.000 (1.00–1.00) | 5.200 (4.20–6.20) | 12068.800 (11721.40–12435.00) |
| B_minimal_tight~i3s | coding | 5 | 0.838 (0.78–0.90) | 0.068 (0.01–0.12) | 1.000 (1.00–1.00) | 6.200 (2.20–10.80) | 12525.000 (11772.40–13399.20) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_minimal_tight | 10 | 0.856 (0.82–0.89) | 0.125 (0.09–0.16) | 0.975 (0.93–1.00) | 23.700 (19.20–28.50) | 12473.700 (11748.20–13121.20) |
| B_minimal_tight~i3i | 18 | 0.854 (0.81–0.90) | 0.087 (0.05–0.13) | 0.944 (0.88–1.00) | 2.056 (1.44–2.61) | 11317.556 (11123.89–11519.67) |
| B_minimal_tight~i3s | 10 | 0.869 (0.81–0.93) | 0.062 (0.02–0.11) | 1.000 (1.00–1.00) | 5.700 (3.60–8.20) | 12296.900 (11873.90–12785.40) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; q = BH-FDR über diese Familie; Cohen's d)

| A | B | Δ (A−B) | p | q | d |
|---|---|---|---|---|---|
| B_minimal_tight | B_minimal_tight~i3i | +0.002 | 1.0000 | 1.0000 | 0.03 |
| B_minimal_tight | B_minimal_tight~i3s | -0.013 | 0.8514 | 1.0000 | -0.17 |
| B_minimal_tight~i3i | B_minimal_tight~i3s | -0.015 | 0.7912 | 1.0000 | -0.16 |