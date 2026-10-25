# Auswertung probes

Runs: 30

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_minimal_tight | business | 5 | 0.863 (0.82–0.90) | 0.156 (0.10–0.23) | 1.000 (1.00–1.00) | 17.400 (11.60–23.60) | 12296.000 (11654.00–12877.40) |
| B_minimal_tight | coding | 5 | 0.875 (0.82–0.93) | 0.128 (0.07–0.18) | 1.000 (1.00–1.00) | 19.400 (15.80–24.40) | 13176.000 (12227.20–13835.20) |
| B_minimal_tight~i1i | business | 5 | 0.775 (0.66–0.86) | 0.112 (0.06–0.14) | 0.950 (0.85–1.00) | 8.400 (5.00–12.60) | 13169.800 (12305.60–14180.80) |
| B_minimal_tight~i1i | coding | 5 | 0.875 (0.82–0.94) | 0.082 (0.01–0.16) | 0.950 (0.85–1.00) | 4.200 (2.40–5.80) | 12908.800 (12371.80–13434.60) |
| B_minimal_tight~i1s | business | 5 | 0.838 (0.76–0.93) | 0.122 (0.06–0.17) | 1.000 (1.00–1.00) | 12.000 (7.00–16.00) | 13411.800 (12859.40–13967.40) |
| B_minimal_tight~i1s | coding | 5 | 0.925 (0.89–0.96) | 0.067 (0.02–0.12) | 1.000 (1.00–1.00) | 10.600 (7.80–14.80) | 13504.800 (13008.00–14088.00) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_minimal_tight | 10 | 0.869 (0.84–0.90) | 0.142 (0.10–0.18) | 1.000 (1.00–1.00) | 18.400 (14.60–22.30) | 12736.000 (12170.40–13311.40) |
| B_minimal_tight~i1i | 10 | 0.825 (0.76–0.89) | 0.097 (0.05–0.14) | 0.950 (0.88–1.00) | 6.300 (4.10–9.00) | 13039.300 (12530.30–13628.30) |
| B_minimal_tight~i1s | 10 | 0.881 (0.82–0.93) | 0.094 (0.05–0.14) | 1.000 (1.00–1.00) | 11.300 (8.40–14.30) | 13458.300 (13081.30–13874.10) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; q = BH-FDR über diese Familie; Cohen's d)

| A | B | Δ (A−B) | p | q | d |
|---|---|---|---|---|---|
| B_minimal_tight | B_minimal_tight~i1i | +0.044 | 0.3889 | 0.5834 | 0.49 |
| B_minimal_tight | B_minimal_tight~i1s | -0.012 | 0.8516 | 0.8516 | -0.17 |
| B_minimal_tight~i1i | B_minimal_tight~i1s | -0.056 | 0.3019 | 0.5834 | -0.55 |