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
  "true_completion": 0.925,
  "false_done_rate": 0.084,
  "phantoms_diagnosed": 1.0,
  "built_on_phantom": 0.2,
  "messages": 17.9,
  "escalations": 0.1,
  "output_tokens": 11572.7
}
```

## Traces of the two weakest runs (ground truth annotations come from the evaluator; agents never see them)
### Run business seed 5001 (true_completion=0.8125)
-- tick 1
a1 item_claimed P1
a1 item_claimed P4
a1 item_claimed P5
a1 → a0: a1 claimed P1,P4,P5. Suggest: a2 takes P6,P8,P15 then P9; a3 takes P3,P7 chain (after P1); a0 takes P2,P12,P16 (after P1). Dependents wait for deps to truly wor
a1 → a2: a1 claimed P1,P4,P5. Suggest: a2 takes P6,P8,P15 then P9; a3 takes P3,P7 chain (after P1); a0 takes P2,P12,P16 (after P1). Dependents wait for deps to truly wor
a1 → a3: a1 claimed P1,P4,P5. Suggest: a2 takes P6,P8,P15 then P9; a3 takes P3,P7 chain (after P1); a0 takes P2,P12,P16 (after P1). Dependents wait for deps to truly wor
a3 item_claimed P3
a3 item_claimed P7
a3 inspects P1 → P1: not processed yet.
a0 inspects P1 → P1: not processed yet.
a0 item_claimed P2
a0 item_claimed P12
a2 item_claimed P6
a2 item_claimed P8
a2 item_claimed P15
a2 executes P6 → signal 'P6: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
-- tick 2
a1 executes P1 → signal 'P1: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
a1 executes P4 → signal 'P4: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 executes P5 → signal 'P5: status set to 'sent / booked' ✓' [ground truth: WORKS]
(diagnosis of P1 via inspect)
a0 inspects P1 → P1: verification FAILED – the mail server log shows a bounce, nothing arrived. The status flag was set before delivery. 
a0 item_claimed P16
a0 → a1: a0 here. I've claimed P2, P12 and P16, and I'll run them once P1 truly works. Nobody owns P10, P11, P13 or P14 yet. They depend on P7, so please take them or te
a0 → a2: a0 here. I've claimed P2, P12 and P16, and I'll run them once P1 truly works. Nobody owns P10, P11, P13 or P14 yet. They depend on P7, so please take them or te
a0 → a3: a0 here. I've claimed P2, P12 and P16, and I'll run them on
[...]
 (a0), P10, P11 (a1), P13, P14 (a2). Please execute each one, then inspect it. A status flag alo
a3 → a2: a3: My P3 and P7 are verified and done. Still open: P2, P12, P16 (a0), P10, P11 (a1), P13, P14 (a2). Please execute each one, then inspect it. A status flag alo
a1 inspects P10 → P10: verified – recipient confirmed / ledger entry present.
a1 inspects P11 → P11: verified – recipient confirmed / ledger entry present.
a1 reports P10 done [ground truth: works]
a1 reports P11 done [ground truth: works]
a2 executes P13 → signal 'P13: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 executes P14 → signal 'P14: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 inspects P13 → P13: verified – recipient confirmed / ledger entry present.
a2 inspects P14 → P14: verified – recipient confirmed / ledger entry present.
-- tick 8
a2 reports P13 done [ground truth: works]
a2 reports P14 done [ground truth: works]
a0 → a1: a0: P2, P12 and P16 are verified and reported done. P2 needed a re-execute after P12 overwrote its record. Still open: P10 and P11 (a1), P13 and P14 (a2). P7 is
a0 → a2: a0: P2, P12 and P16 are verified and reported done. P2 needed a re-execute after P12 overwrote its record. Still open: P10 and P11 (a1), P13 and P14 (a2). P7 is
a0 → a3: a0: P2, P12 and P16 are verified and reported done. P2 needed a re-execute after P12 overwrote its record. Still open: P10 and P11 (a1), P13 and P14 (a2). P7 is
a3 inspects P10 → P10: verified – recipient confirmed / ledger entry present.
a3 inspects P11 → P11: verified – recipient confirmed / ledger entry present.
a3 inspects P13 → P13: verified – recipient confirmed / ledger entry present.
a3 inspects P14 → P14: verified – recipient confirmed / ledger entry present.
END (max_ticks): true_completion=0.8125, false_done=3, messages=22, escalations=0

### Run coding seed 5000 (true_completion=0.875)
-- tick 1
a2 item_claimed P1
a2 item_claimed P4
a2 → a0: a2 claiming P1 and P4. Suggest: a0 take P8,P10,P16; a1 take P14,P15; a3 wait for P1 then P2/P3 chain. Verify with inspect_item before report_done.
a2 → a1: a2 claiming P1 and P4. Suggest: a0 take P8,P10,P16; a1 take P14,P15; a3 wait for P1 then P2/P3 chain. Verify with inspect_item before report_done.
a2 → a3: a2 claiming P1 and P4. Suggest: a0 take P8,P10,P16; a1 take P14,P15; a3 wait for P1 then P2/P3 chain. Verify with inspect_item before report_done.
a1 item_claimed P14
a1 item_claimed P15
a1 executes P14 → signal 'P14: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: WORKS]
a1 executes P15 → signal 'P15: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: WORKS]
a3 item_claimed P8
a3 inspects P1 → P1: not deployed yet.
a3 executes P8 → signal 'P8: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: DOES NOT WORK]
a3 → a0: a3 took P8 (executing now), will wait on P1 for P2/P3 chain. a0: please take P10,P16 after P8 works (I'll confirm).
a3 → a1: a3 took P8 (executing now), will wait on P1 for P2/P3 chain. a0: please take P10,P16 after P8 works (I'll confirm).
a3 → a2: a3 took P8 (executing now), will wait on P1 for P2/P3 chain. a0: please take P10,P16 after P8 works (I'll confirm).
(diagnosis of P8 via inspect)
a0 inspects P8 → P8: live check FAILED – production still serves the OLD version. An orphaned process holds the port; the restart reporte
a0 → a3: a0: inspect P8 shows live check FAILED (orphaned process holds port, old version still served). Diagnosis says re-executing P8 will now replace it correctly. Pl
-- tick 2
a1 inspects P14 → P14: live check passed – production serves the new version and it be
[...]
claimed P9
a1 item_claimed P5
a1 item_claimed P12
a1 executes P5 → signal 'P5: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: WORKS]
a1 executes P12 → signal 'P12: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: WORKS]
a3 item_claimed P13
a3 executes P13 → signal 'P13: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: WORKS]
a3 inspects P13 → P13: live check passed – production serves the new version and it behaves correctly.
a3 reports P13 done [ground truth: works]
-- tick 8
a2 item_claimed P11
a2 executes P11 → signal 'P11: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: WORKS]
a2 inspects P11 → P11: live check passed – production serves the new version and it behaves correctly.
a2 reports P11 done [ground truth: works]
a1 inspects P5 → P5: live check passed – production serves the new version and it behaves correctly.
a1 inspects P12 → P12: live check passed – production serves the new version and it behaves correctly.
a1 inspects P3 → P3: live check passed – production serves the new version and it behaves correctly.
a1 reports P5 done [ground truth: works]
a0 executes P9 → signal 'P9: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: WORKS]
a0 inspects P9 → P9: live check passed – production serves the new version and it behaves correctly.
a0 reports P9 done [ground truth: works]
a3 inspects P12 → P12: live check passed – production serves the new version and it behaves correctly.
a3 inspects P4 → P4: live check FAILED – it worked before, but broke after P9 was rolled out (shared config overwritten). Executing P4 ag
a3 inspects P7 → P7: live check passed – production serves the new version and it behaves correctly.
END (max_ticks): true_completion=0.875, false_done=2, messages=24, escalations=0

## Library of accepted changes so far
(empty)

## Rejected proposals (do not repeat without material change)
- [1] invariant: {"board": {"from": false, "to": true}, "description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Shared board for ownership and status; done means a fresh personal check passed; failures go straight to those affected; checking effort goes to unverified items."}, "norm → Δ=-0.006, p=1.000
- [1] specific: {"board": {"from": false, "to": true}, "description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Shared board; execute only on verified dependencies; a failed inspect leads to re-execute, then escalation; downstream items are re-checked after a root is redone."}, "nor → Δ=-0.037, p=0.284
- [2] invariant: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Each item has one owner who alone verifies it; claim only what you can act on now; send status only to whoever depends on it."}, "norms": {"from": [], "to": ["The owner of an item is the only one who checks it → Δ=-0.075, p=0.015
- [2] specific: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Execute dependency roots first and check them the very next tick; root owners push a verified unblock directly to dependent owners; no polling."}, "norms": {"from": [], "to": ["Items that others depend on go f → Δ=-0.037, p=0.191
- [3] invariant: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Full mesh, no roles. Known failures are fixed first or handed off openly; checking effort goes where it can change the outcome; done rests on a fresh check of the item and what it depends on."}, "norms": {"fro → Δ=+0.000, p=1.000
- [3] specific: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Full mesh, no roles. Shared notes act as a log of check results: every inspect result is written once, everyone reads it instead of re-inspecting, and redone dependencies trigger a recheck downstream."}, "norm → Δ=-0.019, p=0.530
- [4] invariant: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Star with a0 as coordinator who holds the single view of ownership and open failures; workers execute, check and report their own items and talk only to the hub."}, "human_channel": {"from": "anyone", "to": "h → Δ=-0.006, p=1.000
- [4] specific: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Full mesh, no roles. Each item's execute, inspect and report happen in one tick; messaging is kept to a minimum; dependents wait for a verified root; the last two ticks are a verification sweep."}, "norms": {" → Δ=-0.056, p=0.176

## Task
1. Diagnose in 3–6 sentences what goes wrong organisationally (not technically).
2. Propose exactly two candidate configs:
   - "invariant": targets a general organisational weakness likely to recur in any kind of work.
   - "specific": targets what is specific to this kind of assignment.
Return only this JSON in a ```json block:
{"diagnosis": "...", "candidates": [{"kind": "invariant", "rationale": "...", "config": {...full config...}},
{"kind": "specific", "rationale": "...", "config": {...full config...}}]}