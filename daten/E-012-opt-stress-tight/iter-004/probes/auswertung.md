# Auswertung probes

Runs: 30

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_minimal_tight | business | 5 | 0.887 (0.85–0.93) | 0.126 (0.08–0.19) | 1.000 (1.00–1.00) | 20.000 (13.00–25.80) | 11906.600 (11210.40–12575.20) |
| B_minimal_tight | coding | 5 | 0.912 (0.89–0.94) | 0.104 (0.07–0.13) | 1.000 (1.00–1.00) | 16.600 (12.00–21.20) | 12777.800 (12321.80–13357.60) |
| B_minimal_tight~i4i | business | 5 | 0.887 (0.88–0.91) | 0.085 (0.04–0.13) | 1.000 (1.00–1.00) | 14.400 (12.40–16.40) | 11734.400 (11332.20–12260.80) |
| B_minimal_tight~i4i | coding | 5 | 0.900 (0.85–0.94) | 0.089 (0.04–0.15) | 1.000 (1.00–1.00) | 12.400 (11.00–13.80) | 12769.400 (12185.60–13353.20) |
| B_minimal_tight~i4s | business | 5 | 0.838 (0.76–0.93) | 0.093 (0.04–0.14) | 1.000 (1.00–1.00) | 5.200 (4.20–6.20) | 10190.000 (9822.60–10550.00) |
| B_minimal_tight~i4s | coding | 5 | 0.850 (0.78–0.93) | 0.054 (0.03–0.07) | 1.000 (1.00–1.00) | 5.000 (4.00–5.80) | 10909.200 (10426.40–11472.20) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_minimal_tight | 10 | 0.900 (0.88–0.93) | 0.115 (0.08–0.15) | 1.000 (1.00–1.00) | 18.300 (14.10–22.20) | 12342.200 (11810.20–12836.00) |
| B_minimal_tight~i4i | 10 | 0.894 (0.87–0.92) | 0.087 (0.05–0.12) | 1.000 (1.00–1.00) | 13.400 (12.10–14.80) | 12251.900 (11804.40–12768.40) |
| B_minimal_tight~i4s | 10 | 0.844 (0.79–0.90) | 0.073 (0.04–0.11) | 1.000 (1.00–1.00) | 5.100 (4.40–5.80) | 10549.600 (10169.50–10951.00) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; q = BH-FDR über diese Familie; Cohen's d)

| A | B | Δ (A−B) | p | q | d |
|---|---|---|---|---|---|
| B_minimal_tight | B_minimal_tight~i4i | +0.006 | 1.0000 | 1.0000 | 0.15 |
| B_minimal_tight | B_minimal_tight~i4s | +0.056 | 0.1434 | 0.2987 | 0.77 |
| B_minimal_tight~i4i | B_minimal_tight~i4s | +0.050 | 0.1992 | 0.2987 | 0.68 |