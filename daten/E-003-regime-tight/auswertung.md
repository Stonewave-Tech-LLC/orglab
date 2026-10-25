# Auswertung E-003-regime-tight

Runs: 40

## Je Config und Domäne

| config_name | domain | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|---|
| A_contracts_tight | business | 5 | 0.775 (0.72–0.84) | 0.147 (0.06–0.24) | 1.000 (1.00–1.00) | 14.000 (12.60–15.40) | 11807.800 (11328.40–12234.00) |
| A_contracts_tight | coding | 5 | 0.812 (0.74–0.89) | 0.120 (0.08–0.20) | 1.000 (1.00–1.00) | 16.400 (15.20–17.80) | 11739.000 (11328.00–12344.20) |
| B_minimal_tight | business | 5 | 0.838 (0.79–0.90) | 0.152 (0.07–0.22) | 1.000 (1.00–1.00) | 26.200 (21.60–30.20) | 13261.000 (12838.60–13659.20) |
| B_minimal_tight | coding | 5 | 0.912 (0.89–0.94) | 0.100 (0.07–0.13) | 1.000 (1.00–1.00) | 24.000 (21.60–26.60) | 13047.000 (11830.00–14264.00) |
| C_stigmergy_tight | business | 5 | 0.863 (0.80–0.93) | 0.118 (0.05–0.18) | 1.000 (1.00–1.00) | 7.600 (4.20–11.40) | 13262.000 (12539.80–14095.00) |
| C_stigmergy_tight | coding | 5 | 0.900 (0.88–0.93) | 0.079 (0.06–0.10) | 1.000 (1.00–1.00) | 5.600 (3.20–8.60) | 13234.000 (11915.80–14693.00) |
| D_constitution_tight | business | 5 | 0.863 (0.80–0.93) | 0.121 (0.09–0.15) | 1.000 (1.00–1.00) | 22.800 (15.40–31.60) | 12572.600 (11820.60–13491.00) |
| D_constitution_tight | coding | 5 | 0.900 (0.85–0.95) | 0.094 (0.04–0.14) | 1.000 (1.00–1.00) | 19.000 (15.20–22.20) | 12444.600 (11488.00–13509.60) |

## Je Config (über Domänen)

| config_name | n | true_completion (95%-CI) | false_done_rate (95%-CI) | phantoms_diagnosed (95%-CI) | messages (95%-CI) | output_tokens (95%-CI) |
|---|---|---|---|---|---|---|
| A_contracts_tight | 10 | 0.794 (0.74–0.84) | 0.134 (0.08–0.20) | 1.000 (1.00–1.00) | 15.200 (14.00–16.50) | 11773.400 (11450.90–12141.90) |
| B_minimal_tight | 10 | 0.875 (0.83–0.91) | 0.126 (0.08–0.17) | 1.000 (1.00–1.00) | 25.100 (22.40–27.80) | 13154.000 (12497.60–13755.90) |
| C_stigmergy_tight | 10 | 0.881 (0.84–0.91) | 0.098 (0.06–0.14) | 1.000 (1.00–1.00) | 6.600 (4.40–8.90) | 13248.000 (12472.50–14068.10) |
| D_constitution_tight | 10 | 0.881 (0.84–0.93) | 0.107 (0.08–0.14) | 1.000 (1.00–1.00) | 20.900 (16.90–25.70) | 12508.600 (11886.40–13175.10) |

## true_completion

Paarvergleiche für `true_completion` (Permutationstest, zweiseitig; Cohen's d)

| A | B | Δ (A−B) | p | d |
|---|---|---|---|---|
| A_contracts_tight | B_minimal_tight | -0.081 | 0.0450 | -1.08 |
| A_contracts_tight | C_stigmergy_tight | -0.088 | 0.0274 | -1.19 |
| A_contracts_tight | D_constitution_tight | -0.088 | 0.0386 | -1.10 |
| B_minimal_tight | C_stigmergy_tight | -0.006 | 1.0000 | -0.10 |
| B_minimal_tight | D_constitution_tight | -0.006 | 1.0000 | -0.09 |
| C_stigmergy_tight | D_constitution_tight | +0.000 | 1.0000 | 0.00 |