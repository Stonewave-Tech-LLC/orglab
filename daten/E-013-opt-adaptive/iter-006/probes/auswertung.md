# Auswertung probes

Runs: 30

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_minimal_tight | business | 5 | 0.938 (0.90–0.97) | 0.054 (0.01–0.10) | 1.000 (1.00–1.00) | 16.800 (10.00–25.00) | 11759.000 (10297.60–12785.40) |
| B_minimal_tight | coding | 5 | 0.887 (0.81–0.96) | 0.059 (0.01–0.10) | 0.950 (0.85–1.00) | 20.400 (13.40–27.00) | 12384.600 (11261.00–13277.80) |
| B_minimal_tight~i6i | business | 5 | 0.875 (0.82–0.93) | 0.128 (0.07–0.18) | 1.000 (1.00–1.00) | 2.600 (0.00–5.80) | 7877.600 (7331.80–8424.40) |
| B_minimal_tight~i6i | coding | 5 | 0.875 (0.84–0.91) | 0.125 (0.09–0.16) | 1.000 (1.00–1.00) | 1.600 (0.60–2.40) | 8567.600 (7471.60–9694.20) |
| B_minimal_tight~i6s | business | 5 | 0.900 (0.85–0.96) | 0.100 (0.04–0.15) | 1.000 (1.00–1.00) | 2.200 (0.60–4.00) | 9964.000 (9189.00–10759.40) |
| B_minimal_tight~i6s | coding | 5 | 0.912 (0.88–0.96) | 0.089 (0.04–0.13) | 1.000 (1.00–1.00) | 7.200 (3.80–10.20) | 11956.000 (11461.80–12392.00) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_minimal_tight | 10 | 0.912 (0.87–0.95) | 0.056 (0.03–0.09) | 0.975 (0.93–1.00) | 18.600 (13.70–24.00) | 12071.800 (11170.90–12850.00) |
| B_minimal_tight~i6i | 10 | 0.875 (0.84–0.91) | 0.126 (0.10–0.16) | 1.000 (1.00–1.00) | 2.100 (0.70–3.70) | 8222.600 (7610.40–8954.90) |
| B_minimal_tight~i6s | 10 | 0.906 (0.88–0.94) | 0.095 (0.06–0.13) | 1.000 (1.00–1.00) | 4.700 (2.50–7.30) | 10960.000 (10169.70–11717.60) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; q = BH-FDR über diese Familie; Cohen's d)

| A | B | Δ (A−B) | p | q | d |
|---|---|---|---|---|---|
| B_minimal_tight | B_minimal_tight~i6i | +0.037 | 0.2953 | 0.4994 | 0.59 |
| B_minimal_tight | B_minimal_tight~i6s | +0.006 | 1.0000 | 1.0000 | 0.09 |
| B_minimal_tight~i6i | B_minimal_tight~i6s | -0.031 | 0.3329 | 0.4994 | -0.56 |