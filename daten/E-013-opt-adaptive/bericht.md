# Optimierungslauf E-013-opt-adaptive

Gestartet 2026-10-21T08:46:13, Iterationen 6, übernommene Änderungen 0.
Einstellungen: `{"scenario": "phantom_stress", "train": ["coding", "business"], "holdout": ["research"], "seeds_per_probe": 5, "max_seeds_per_probe": 20, "backend": {"kind": "agent_sdk", "model": "claude-sonnet-5-5", "effort": "medium"}, "alpha": 0.1, "min_effect": 0.02, "token_guard": 3.0, "editor_model": "claude-opus-5-5"}`

## Verlauf

| Iter | Kandidat | Δ | p | Tokens× | übernommen |
|---|---|---|---|---|---|
| 1 | invariant | -0.044 | 0.315 | 1.02 |  |
| 1 | specific | +0.013 | 0.799 | 1.06 |  |
| 2 | invariant | +0.013 | 0.846 | 1.02 |  |
| 2 | specific | -0.031 | 0.503 | 0.91 |  |
| 3 | invariant | -0.019 | 0.656 | 0.91 |  |
| 3 | specific | +0.013 | 0.847 | 0.99 |  |
| 4 | invariant | -0.025 | 0.498 | 0.86 |  |
| 4 | specific | -0.013 | 0.686 | 0.87 |  |
| 5 | invariant | -0.006 | 1.000 | 0.95 |  |
| 5 | specific | -0.044 | 0.246 | 1.03 |  |
| 6 | invariant | -0.037 | 0.153 | 0.68 |  |
| 6 | specific | -0.006 | 1.000 | 0.91 |  |

## Bibliothek


## Transfer (Holdout)


## Aktuelle Config

```yaml
name: B_minimal_tight
description: No roles, no rules, full mesh, scarce attention budget.
n_agents: 4
topology: mesh
board: false
shared_notes: false
human_channel: anyone
role_mode: none
roles: []
norms: []
max_ticks: 8
max_tool_calls: 4

```