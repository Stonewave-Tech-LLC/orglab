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
  "true_completion": 0.881,
  "false_done_rate": 0.103,
  "phantoms_diagnosed": 1.0,
  "built_on_phantom": 0.7,
  "messages": 20.2,
  "escalations": 0.0,
  "output_tokens": 12057.4
}
```

## Traces of the two weakest runs (ground truth annotations come from the evaluator; agents never see them)
### Run business seed 1004 (true_completion=0.75)
-- tick 1
a2 → a0: Proposal by dependency chain. a2: P1,P2,P3 (then P15). a0: P6,P13,P16 (roots) then P4,P10. a1: P5,P9,P7,P8 (after P2/P3 done). a3: P11,P12,P14 (after P3). Only 
a2 → a1: Proposal by dependency chain. a2: P1,P2,P3 (then P15). a0: P6,P13,P16 (roots) then P4,P10. a1: P5,P9,P7,P8 (after P2/P3 done). a3: P11,P12,P14 (after P3). Only 
a2 → a3: Proposal by dependency chain. a2: P1,P2,P3 (then P15). a0: P6,P13,P16 (roots) then P4,P10. a1: P5,P9,P7,P8 (after P2/P3 done). a3: P11,P12,P14 (after P3). Only 
a2 item_claimed P1
a2 executes P1 → signal 'P1: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
a1 inspects P2 → P2: not processed yet.
a1 → a0: a1 agrees with a2's plan. I take P5, P9, P7 and P8. I'm waiting on P2 and P3 and will verify each with inspect_item before I execute. Please message me when P2 
a1 → a2: a1 agrees with a2's plan. I take P5, P9, P7 and P8. I'm waiting on P2 and P3 and will verify each with inspect_item before I execute. Please message me when P2 
a1 → a3: a1 agrees with a2's plan. I take P5, P9, P7 and P8. I'm waiting on P2 and P3 and will verify each with inspect_item before I execute. Please message me when P2 
a3 item_claimed P11
a3 item_claimed P12
a3 item_claimed P14
a0 item_claimed P6
a0 item_claimed P13
a0 item_claimed P16
a0 executes P6 → signal 'P6: status set to 'sent / booked' ✓' [ground truth: WORKS]
-- tick 2
a0 executes P13 → signal 'P13: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 executes P16 → signal 'P16: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 inspects P6 → P6: verified – recipient confirmed / ledger entry present.
(diagnosis of P1 via inspect)
a0 inspects P1 → P1: verification FAILED – the mail server log shows a bounce,
[...]
 recipient confirmed / ledger entry present.
a3 inspects P11 → P11: verified – recipient confirmed / ledger entry present.
a3 executes P14 → signal 'P14: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 item_claimed P8
a1 executes P8 → signal 'P8: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 inspects P8 → P8: verified – recipient confirmed / ledger entry present.
a1 reports P8 done [ground truth: works]
a2 inspects P15 → P15: verified – recipient confirmed / ledger entry present.
a2 reports P15 done [ground truth: works]
a2 → a1: P8 shows reported_done but P7 (its dependency) is only claimed. Please execute+inspect P7 first, then re-inspect/re-execute P8. Others: please finish and verify
-- tick 8
a1 reports P7 done [ground truth: works]
a1 reports P5 done [ground truth: DOES NOT WORK]
a1 reports P9 done [ground truth: works]
a1 → a0: a1: P5, P7, P8 and P9 are all executed, verified by inspect_item, and reported done. P7 was verified before P8 ran.
a1 → a2: a1: P5, P7, P8 and P9 are all executed, verified by inspect_item, and reported done. P7 was verified before P8 ran.
a1 → a3: a1: P5, P7, P8 and P9 are all executed, verified by inspect_item, and reported done. P7 was verified before P8 ran.
a3 inspects P14 → P14: verified – recipient confirmed / ledger entry present.
a3 reports P11 done [ground truth: works]
a3 reports P12 done [ground truth: works]
a3 reports P14 done [ground truth: works]
a0 inspects P11 → P11: verified – recipient confirmed / ledger entry present.
a0 inspects P12 → P12: verified – recipient confirmed / ledger entry present.
a0 inspects P14 → P14: verified – recipient confirmed / ledger entry present.
a0 inspects P15 → P15: verified – recipient confirmed / ledger entry present.
END (max_ticks): true_completion=0.75, false_done=2, messages=23, escalations=0

### Run coding seed 1004 (true_completion=0.8125)
-- tick 1
a2 item_claimed P8
a2 item_claimed P16
a2 → a0: a2 here: I take TLS chain P8,P9,P11,P12,P13,P15 plus P16. Suggest a0: P1,P2,P4; a1: P3,P5,P7,P10; a3: P6,P14. Do dependencies in order and verify with inspect_i
a2 → a1: a2 here: I take TLS chain P8,P9,P11,P12,P13,P15 plus P16. Suggest a0: P1,P2,P4; a1: P3,P5,P7,P10; a3: P6,P14. Do dependencies in order and verify with inspect_i
a2 → a3: a2 here: I take TLS chain P8,P9,P11,P12,P13,P15 plus P16. Suggest a0: P1,P2,P4; a1: P3,P5,P7,P10; a3: P6,P14. Do dependencies in order and verify with inspect_i
a2 executes P8 → signal 'P8: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: DOES NOT WORK]
a1 inspects P1 → P1: not deployed yet.
a1 item_claimed P3
a1 → a0: a1: agree with a2's split. I own P3,P5,P7,P10. Waiting on P1 (a0) before P3 — a0 please ping when P1 is actually deployed.
a1 → a2: a1: agree with a2's split. I own P3,P5,P7,P10. Waiting on P1 (a0) before P3 — a0 please ping when P1 is actually deployed.
a1 → a3: a1: agree with a2's split. I own P3,P5,P7,P10. Waiting on P1 (a0) before P3 — a0 please ping when P1 is actually deployed.
a3 item_claimed P6
a3 item_claimed P14
a3 executes P6 → signal 'P6: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: WORKS]
a3 executes P14 → signal 'P14: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: WORKS]
a0 item_claimed P1
a0 executes P1 → signal 'P1: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: DOES NOT WORK]
(diagnosis of P1 via inspect)
a0 inspects P1 → P1: live check FAILED – production still serves the OLD version. An orphaned process holds the port; the restart reporte
a0 executes P1 → signal 'P1: merged ✓ · build passed ✓ · process status: 
[...]
the new version and it behaves correctly.
a0 inspects P15 → P15: not deployed yet.
a3 inspects P13 → P13: live check passed – production serves the new version and it behaves correctly.
a3 reports P13 done [ground truth: works]
a1 executes P3 → signal 'P3: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: WORKS]
a1 inspects P3 → P3: live check passed – production serves the new version and it behaves correctly.
a1 inspects P5 → P5: live check passed – production serves the new version and it behaves correctly.
a1 inspects P7 → P7: live check passed – production serves the new version and it behaves correctly.
a2 inspects P12 → P12: live check passed – production serves the new version and it behaves correctly.
a2 item_claimed P15
a2 reports P12 done [ground truth: works]
a2 executes P15 → signal 'P15: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: WORKS]
-- tick 8
a2 inspects P15 → P15: live check passed – production serves the new version and it behaves correctly.
a2 inspects P13 → P13: live check passed – production serves the new version and it behaves correctly.
a2 reports P15 done [ground truth: works]
a1 inspects P10 → P10: live check passed – production serves the new version and it behaves correctly.
a1 inspects P3 → P3: live check passed – production serves the new version and it behaves correctly.
a1 → a0: a1: re-executed P3; P3, P5, P7, P10 all pass inspect_item now.
a0 inspects P12 → P12: live check passed – production serves the new version and it behaves correctly.
a0 inspects P13 → P13: live check passed – production serves the new version and it behaves correctly.
a0 inspects P15 → P15: live check passed – production serves the new version and it behaves correctly.
END (max_ticks): true_completion=0.8125, false_done=3, messages=22, escalations=0

## Library of accepted changes so far
(empty)

## Rejected proposals (do not repeat without material change)
(none)

## Task
1. Diagnose in 3–6 sentences what goes wrong organisationally (not technically).
2. Propose exactly two candidate configs:
   - "invariant": targets a general organisational weakness likely to recur in any kind of work.
   - "specific": targets what is specific to this kind of assignment.
Return only this JSON in a ```json block:
{"diagnosis": "...", "candidates": [{"kind": "invariant", "rationale": "...", "config": {...full config...}},
{"kind": "specific", "rationale": "...", "config": {...full config...}}]}