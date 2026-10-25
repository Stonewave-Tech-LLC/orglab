# Auswertung E-005-aa-positivkontrolle

Runs: 60

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | inspections (95%-CI) | regressions_repaired (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|---|
| B_minimal_tight | business | 10 | 0.894 (0.86–0.93) | 0.064 (0.04–0.09) | 42.900 (37.40–48.00) | 0.543 (0.36–0.73) | 22.500 (19.70–25.80) | 12348.300 (11662.20–12917.90) |
| B_minimal_tight | coding | 10 | 0.912 (0.85–0.96) | 0.069 (0.04–0.10) | 44.800 (40.30–49.00) | 0.492 (0.25–0.73) | 16.500 (13.30–19.40) | 12253.500 (11755.80–12761.40) |
| B_minimal_tight_AA | business | 10 | 0.906 (0.84–0.96) | 0.066 (0.03–0.11) | 41.100 (35.70–46.30) | 0.583 (0.30–0.85) | 15.400 (11.60–19.30) | 12191.200 (11303.00–12984.30) |
| B_minimal_tight_AA | coding | 10 | 0.912 (0.86–0.96) | 0.039 (0.01–0.07) | 47.600 (44.60–50.60) | 0.733 (0.50–0.95) | 20.900 (15.00–27.40) | 12627.700 (11945.70–13431.70) |
| B_tight_trust_flags | business | 10 | 0.375 (0.27–0.49) | 0.625 (0.51–0.73) | 1.100 (0.00–2.90) | 0.700 (0.40–1.00) | 11.300 (7.10–16.00) | 7934.000 (6938.60–9009.70) |
| B_tight_trust_flags | coding | 10 | 0.381 (0.35–0.41) | 0.617 (0.59–0.65) | 0.600 (0.00–1.80) | 0.900 (0.70–1.00) | 11.600 (7.50–15.70) | 8204.400 (7523.30–8934.10) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | inspections (95%-CI) | regressions_repaired (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_minimal_tight | 20 | 0.903 (0.87–0.93) | 0.066 (0.04–0.09) | 43.850 (40.20–47.25) | 0.517 (0.36–0.68) | 19.500 (16.90–22.05) | 12300.900 (11888.20–12681.90) |
| B_minimal_tight_AA | 20 | 0.909 (0.87–0.95) | 0.053 (0.03–0.08) | 44.350 (41.05–47.60) | 0.658 (0.47–0.82) | 18.150 (14.45–22.00) | 12409.450 (11841.70–12973.15) |
| B_tight_trust_flags | 20 | 0.378 (0.32–0.44) | 0.621 (0.56–0.68) | 0.850 (0.00–2.00) | 0.800 (0.60–0.95) | 11.450 (8.45–14.60) | 8069.200 (7468.80–8700.65) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; q = BH-FDR über diese Familie; Cohen's d)

| A | B | Δ (A−B) | p | q | d |
|---|---|---|---|---|---|
| B_minimal_tight | B_minimal_tight_AA | -0.006 | 0.9028 | 0.9028 | -0.08 |
| B_minimal_tight | B_tight_trust_flags | +0.525 | 0.0002 | 0.0003 | 4.90 |
| B_minimal_tight_AA | B_tight_trust_flags | +0.531 | 0.0002 | 0.0003 | 4.75 |