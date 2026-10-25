## Current organisation config
```json
{
  "name": "B_minimal_tight",
  "description": "No roles, no rules, full mesh, scarce attention budget.",
  "n_agents": 4,
  "topology": "mesh",
  "board": false,
  "shared_notes": false,
  "human_channel": "anyone",
  "role_mode": "none",
  "roles": [],
  "norms": [],
  "max_ticks": 8,
  "max_tool_calls": 4
}
```

## Measured on 10 runs (training work domains: coding, business)
Primary metric: true_completion (share of work items that truly work at the end; 1.0 is perfect).
```json
{
  "true_completion": 0.9,
  "false_done_rate": 0.112,
  "phantoms_diagnosed": 1.0,
  "built_on_phantom": 0.3,
  "messages": 19.3,
  "escalations": 0.0,
  "output_tokens": 11737.4
}
```

## Traces of the two weakest runs (ground truth annotations come from the evaluator; agents never see them)
### Run business seed 3000 (true_completion=0.8125)
-- tick 1
a3 item_claimed P1
a3 item_claimed P9
a3 item_claimed P15
a3 → a0: a3 claimed P1, P9, P15 (no deps). Suggest: a0 takes P2,P5,P3; a1 takes P4,P6,P11,P10; a2 takes P7,P8,P12,P13,P14,P16. I'll report when P1 done.
a3 → a1: a3 claimed P1, P9, P15 (no deps). Suggest: a0 takes P2,P5,P3; a1 takes P4,P6,P11,P10; a2 takes P7,P8,P12,P13,P14,P16. I'll report when P1 done.
a3 → a2: a3 claimed P1, P9, P15 (no deps). Suggest: a0 takes P2,P5,P3; a1 takes P4,P6,P11,P10; a2 takes P7,P8,P12,P13,P14,P16. I'll report when P1 done.
a0 item_claimed P2
a0 item_claimed P3
a0 item_claimed P5
a1 item_claimed P4
a1 item_claimed P6
a1 item_claimed P10
a1 item_claimed P11
a2 item_claimed P7
a2 item_claimed P8
a2 item_claimed P12
a2 item_claimed P16
-- tick 2
a1 inspects P1 → P1: not processed yet.
a2 item_claimed P13
a2 item_claimed P14
a2 inspects P3 → P3: not processed yet.
a2 inspects P1 → P1: not processed yet.
a3 executes P1 → signal 'P1: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
a3 executes P9 → signal 'P9: status set to 'sent / booked' ✓' [ground truth: WORKS]
a3 executes P15 → signal 'P15: status set to 'sent / booked' ✓' [ground truth: WORKS]
(diagnosis of P1 via inspect)
a3 inspects P1 → P1: verification FAILED – the mail server log shows a bounce, nothing arrived. The status flag was set before delivery. 
a0 inspects P1 → P1: not working – execute it again.
a0 → a3: a0: inspect P1 says "not working – execute it again". Please re-execute P1 and verify with inspect before reporting done; P2,P3,P5 (mine) are waiting on it.
-- tick 3
a0 inspects P1 → P1: not working – execute it again.
a2 inspects P1 → P1: not working – execute it again.
a2 inspects P3 → P3: not processed yet.
a2 → a3: P1 inspects as "not workin
[...]
 P5 → P5: verified – recipient confirmed / ledger entry present.
a0 → a1: a0: P2 and P3 are VERIFIED (P3 bounced first, re-executed OK). P7/P16 can go ahead. Always inspect after execute.
a0 → a2: a0: P2 and P3 are VERIFIED (P3 bounced first, re-executed OK). P7/P16 can go ahead. Always inspect after execute.
a0 → a3: a0: P2 and P3 are VERIFIED (P3 bounced first, re-executed OK). P7/P16 can go ahead. Always inspect after execute.
a0 reports P2 done [ground truth: works]
a0 reports P3 done [ground truth: works]
a2 executes P7 → signal 'P7: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 inspects P16 → P16: verified – recipient confirmed / ledger entry present.
a2 inspects P7 → P7: verified – recipient confirmed / ledger entry present.
a2 executes P8 → signal 'P8: status set to 'sent / booked' ✓' [ground truth: WORKS]
-- tick 7
a2 inspects P8 → P8: verified – recipient confirmed / ledger entry present.
a2 executes P12 → signal 'P12: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 inspects P12 → P12: verified – recipient confirmed / ledger entry present.
a2 executes P13 → signal 'P13: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 reports P6 done [ground truth: works]
a1 reports P10 done [ground truth: works]
a1 reports P11 done [ground truth: works]
a1 → a2: a1: P4,P6,P10,P11 done+verified. P1,P2,P3 verified, so P7,P16 can go; then P8,P12,P13,P14. Inspect after each execute (first try can bounce).
a0 reports P5 done [ground truth: DOES NOT WORK]
-- tick 8
a2 executes P14 → signal 'P14: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 inspects P14 → P14: verified – recipient confirmed / ledger entry present.
a2 inspects P13 → P13: verified – recipient confirmed / ledger entry present.
END (max_ticks): true_completion=0.8125, false_done=3, messages=15, escalations=0

### Run business seed 3001 (true_completion=0.875)
-- tick 1
a1 → a0: a1 takes P1,P3,P4,P6,P10 (chain) and P2. a0: P7,P15,P9,P11. a2: P5,P8,P12,P13. a3: P14,P16. Only execute after deps truly work; verify with inspect_item.
a1 → a2: a1 takes P1,P3,P4,P6,P10 (chain) and P2. a0: P7,P15,P9,P11. a2: P5,P8,P12,P13. a3: P14,P16. Only execute after deps truly work; verify with inspect_item.
a1 → a3: a1 takes P1,P3,P4,P6,P10 (chain) and P2. a0: P7,P15,P9,P11. a2: P5,P8,P12,P13. a3: P14,P16. Only execute after deps truly work; verify with inspect_item.
a1 item_claimed P1
a1 item_claimed P2
a2 inspects P1 → P1: not processed yet.
a2 inspects P3 → P3: not processed yet.
a2 item_claimed P5
a2 item_claimed P8
a0 item_claimed P7
a0 item_claimed P9
a0 item_claimed P11
a0 executes P7 → signal 'P7: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
a3 item_claimed P14
a3 item_claimed P16
a3 executes P14 → signal 'P14: status set to 'sent / booked' ✓' [ground truth: WORKS]
a3 executes P16 → signal 'P16: status set to 'sent / booked' ✓' [ground truth: WORKS]
-- tick 2
a0 executes P9 → signal 'P9: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 executes P11 → signal 'P11: status set to 'sent / booked' ✓' [ground truth: WORKS]
(diagnosis of P7 via inspect)
a0 inspects P7 → P7: verification FAILED – the mail server log shows a bounce, nothing arrived. The status flag was set before delivery. 
a0 executes P7 → signal 'P7: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 inspects P1 → P1: not processed yet.
a2 inspects P3 → P3: not processed yet.
a3 inspects P14 → P14: verified – recipient confirmed / ledger entry present.
a3 inspects P16 → P16: verified – recipient confirmed / ledger entry present.
a3 reports P14 done [ground truth: works]
a3 reports P16 done [gr
[...]
 entry present.
a2 executes P12 → signal 'P12: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 inspects P12 → P12: verified – recipient confirmed / ledger entry present.
a2 executes P13 → signal 'P13: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 inspects P13 → P13: verified – recipient confirmed / ledger entry present.
a1 → a0: Remaining: P6 (a3), P12 then P13 (a2), P10 (unassigned, after P6). I'll take P10 once P6 verifies. Please execute then inspect, re-execute on bounce.
a1 → a2: Remaining: P6 (a3), P12 then P13 (a2), P10 (unassigned, after P6). I'll take P10 once P6 verifies. Please execute then inspect, re-execute on bounce.
a1 → a3: Remaining: P6 (a3), P12 then P13 (a2), P10 (unassigned, after P6). I'll take P10 once P6 verifies. Please execute then inspect, re-execute on bounce.
a1 item_claimed P10
-- tick 8
a3 reports P6 done [ground truth: works]
a3 rejected claim: P10 is owned by a1
a3 → a1: a3: P6 executed, verified and reported done. P10 is yours: execute, inspect, re-execute on bounce. This is the last tick.
a1 executes P10 → signal 'P10: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 inspects P10 → P10: verified – recipient confirmed / ledger entry present.
a1 reports P10 done [ground truth: works]
a1 inspects P13 → P13: verified – recipient confirmed / ledger entry present.
a2 reports P12 done [ground truth: works]
a2 reports P13 done [ground truth: works]
a2 → a0: a2: P5,P8,P12,P13 all verified and reported done. Only P6 -> P10 remain.
a2 → a1: a2: P5,P8,P12,P13 all verified and reported done. Only P6 -> P10 remain.
a2 → a3: a2: P5,P8,P12,P13 all verified and reported done. Only P6 -> P10 remain.
a0 inspects P6 → P6: verified – recipient confirmed / ledger entry present.
END (max_ticks): true_completion=0.875, false_done=2, messages=20, escalations=0

## Library of accepted changes so far
(empty)

## Rejected proposals (do not repeat without material change)
- [1] invariant: {"board": {"from": false, "to": true}, "description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Shared board for ownership and status; done means a fresh personal check passed; failures go straight to those affected; checking effort goes to unverified items."}, "norm → Δ=-0.006, p=1.000
- [1] specific: {"board": {"from": false, "to": true}, "description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Shared board; execute only on verified dependencies; a failed inspect leads to re-execute, then escalation; downstream items are re-checked after a root is redone."}, "nor → Δ=-0.037, p=0.284
- [2] invariant: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Each item has one owner who alone verifies it; claim only what you can act on now; send status only to whoever depends on it."}, "norms": {"from": [], "to": ["The owner of an item is the only one who checks it → Δ=-0.075, p=0.015
- [2] specific: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Execute dependency roots first and check them the very next tick; root owners push a verified unblock directly to dependent owners; no polling."}, "norms": {"from": [], "to": ["Items that others depend on go f → Δ=-0.037, p=0.191

## Task
1. Diagnose in 3–6 sentences what goes wrong organisationally (not technically).
2. Propose exactly two candidate configs:
   - "invariant": targets a general organisational weakness likely to recur in any kind of work.
   - "specific": targets what is specific to this kind of assignment.
Return only this JSON in a ```json block:
{"diagnosis": "...", "candidates": [{"kind": "invariant", "rationale": "...", "config": {...full config...}},
{"kind": "specific", "rationale": "...", "config": {...full config...}}]}