# Auswertung probes

Runs: 60

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| B_minimal_tight | business | 5 | 0.850 (0.80–0.90) | 0.114 (0.05–0.18) | 1.000 (1.00–1.00) | 23.200 (18.20–29.40) | 12915.200 (12249.60–13559.80) |
| B_minimal_tight | coding | 5 | 0.950 (0.94–0.97) | 0.061 (0.03–0.08) | 1.000 (1.00–1.00) | 14.200 (7.60–22.40) | 12464.400 (11517.20–13411.60) |
| B_minimal_tight~i2i | business | 15 | 0.896 (0.86–0.93) | 0.069 (0.04–0.10) | 1.000 (1.00–1.00) | 2.867 (1.87–3.93) | 11482.267 (10894.67–12060.33) |
| B_minimal_tight~i2i | coding | 15 | 0.904 (0.88–0.93) | 0.095 (0.07–0.12) | 1.000 (1.00–1.00) | 1.400 (0.73–2.13) | 11598.467 (10893.07–12298.13) |
| B_minimal_tight~i2s | business | 7 | 0.857 (0.81–0.89) | 0.089 (0.03–0.15) | 1.000 (1.00–1.00) | 6.000 (2.29–10.29) | 10885.286 (9941.86–11694.86) |
| B_minimal_tight~i2s | coding | 13 | 0.880 (0.84–0.92) | 0.096 (0.06–0.13) | 1.000 (1.00–1.00) | 6.615 (3.85–9.31) | 10625.077 (10063.08–11144.23) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| B_minimal_tight | 10 | 0.900 (0.85–0.94) | 0.087 (0.05–0.13) | 1.000 (1.00–1.00) | 18.700 (13.20–24.20) | 12689.800 (12042.40–13278.10) |
| B_minimal_tight~i2i | 30 | 0.900 (0.88–0.92) | 0.082 (0.06–0.10) | 1.000 (1.00–1.00) | 2.133 (1.50–2.83) | 11540.367 (11106.77–12008.83) |
| B_minimal_tight~i2s | 20 | 0.872 (0.84–0.90) | 0.094 (0.06–0.13) | 1.000 (1.00–1.00) | 6.400 (4.15–8.60) | 10716.150 (10233.95–11176.90) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; q = BH-FDR über diese Familie; Cohen's d)

| A | B | Δ (A−B) | p | q | d |
|---|---|---|---|---|---|
| B_minimal_tight | B_minimal_tight~i2i | +0.000 | 1.0000 | 1.0000 | 0.00 |
| B_minimal_tight | B_minimal_tight~i2s | +0.028 | 0.4135 | 0.6203 | 0.38 |
| B_minimal_tight~i2i | B_minimal_tight~i2s | +0.028 | 0.1852 | 0.5555 | 0.42 |