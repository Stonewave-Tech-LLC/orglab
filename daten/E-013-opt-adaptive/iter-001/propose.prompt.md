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
  "true_completion": 0.869,
  "false_done_rate": 0.142,
  "phantoms_diagnosed": 1.0,
  "built_on_phantom": 0.5,
  "messages": 18.4,
  "escalations": 0.2,
  "output_tokens": 12736.0
}
```

## Traces of the two weakest runs (ground truth annotations come from the evaluator; agents never see them)
### Run business seed 1003 (true_completion=0.8125)
-- tick 1
a2 item_claimed P1
a2 item_claimed P2
a2 item_claimed P5
a2 → a0: a2 claimed P1, P2, P5. Suggest: a0 takes P9,P12,P14; a1 takes P3,P6,P8 chain after P2; a3 takes P4,P7,P16 after P1. Will report when done.
a2 → a1: a2 claimed P1, P2, P5. Suggest: a0 takes P9,P12,P14; a1 takes P3,P6,P8 chain after P2; a3 takes P4,P7,P16 after P1. Will report when done.
a2 → a3: a2 claimed P1, P2, P5. Suggest: a0 takes P9,P12,P14; a1 takes P3,P6,P8 chain after P2; a3 takes P4,P7,P16 after P1. Will report when done.
a1 item_claimed P3
a1 item_claimed P6
a1 item_claimed P8
a0 item_claimed P9
a0 item_claimed P12
a0 item_claimed P14
a0 executes P9 → signal 'P9: status set to 'sent / booked' ✓' [ground truth: WORKS]
a3 item_claimed P4
a3 item_claimed P7
a3 item_claimed P16
a3 inspects P1 → P1: not processed yet.
-- tick 2
a0 executes P12 → signal 'P12: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 executes P14 → signal 'P14: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 inspects P9 → P9: verified – recipient confirmed / ledger entry present.
a0 reports P9 done [ground truth: works]
a1 inspects P2 → P2: not processed yet.
a2 executes P1 → signal 'P1: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 executes P2 → signal 'P2: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
a2 executes P5 → signal 'P5: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 inspects P1 → P1: verified – recipient confirmed / ledger entry present.
a3 inspects P1 → P1: verified – recipient confirmed / ledger entry present.
a3 executes P4 → signal 'P4: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
a3 executes P7 → signal 'P7: status set to 'sent / booked' ✓' [ground truth: WORKS]
a3 executes P1
[...]
 set to 'sent / booked' ✓' [ground truth: WORKS]
a1 inspects P8 → P8: verified – recipient confirmed / ledger entry present.
a1 item_claimed P10
a1 item_claimed P11
a1 executes P10 → signal 'P10: status set to 'sent / booked' ✓' [ground truth: WORKS]
-- tick 7
a2 inspects P3 → P3: verified – recipient confirmed / ledger entry present.
a2 inspects P13 → P13: verified – recipient confirmed / ledger entry present.
a0 inspects P13 → P13: verified – recipient confirmed / ledger entry present.
a0 reports P13 done [ground truth: works]
a0 executes P15 → signal 'P15: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 inspects P15 → P15: verified – recipient confirmed / ledger entry present.
a1 executes P11 → signal 'P11: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 inspects P10 → P10: verified – recipient confirmed / ledger entry present.
a1 inspects P11 → P11: verified – recipient confirmed / ledger entry present.
a1 reports P3 done [ground truth: works]
-- tick 8
a2 inspects P8 → P8: verification FAILED – it had taken effect, but was reversed after P15 was processed (it overwrote the same record). 
a2 inspects P6 → P6: verified – recipient confirmed / ledger entry present.
a2 inspects P15 → P15: verified – recipient confirmed / ledger entry present.
a2 inspects P10 → P10: verified – recipient confirmed / ledger entry present.
a3 → HUMAN: a3 status: P1-P5, P7, P9, P12-P14 and P16 are done. My P4, P7 and P16 were verified delivered; P4 needed a retry after a bounce. Still open at the last tick: P6
a1 reports P6 done [ground truth: works]
a1 reports P8 done [ground truth: DOES NOT WORK]
a1 reports P10 done [ground truth: works]
a1 reports P11 done [ground truth: works]
a0 reports P15 done [ground truth: works]
END (max_ticks): true_completion=0.8125, false_done=3, messages=16, escalations=1

### Run business seed 1004 (true_completion=0.8125)
-- tick 1
a2 item_claimed P1
a2 item_claimed P6
a2 item_claimed P13
a2 item_claimed P16
a1 inspects P1 → P1: not processed yet.
a1 → a0: a1 here. Proposal: a2 finishes P1,P6,P13,P16. I take P2,P3,P4,P7,P8. a0 takes P5,P9,P15,P12. a3 takes P10,P11,P14. Start only when dependencies are truly done (
a1 → a2: a1 here. Proposal: a2 finishes P1,P6,P13,P16. I take P2,P3,P4,P7,P8. a0 takes P5,P9,P15,P12. a3 takes P10,P11,P14. Start only when dependencies are truly done (
a1 → a3: a1 here. Proposal: a2 finishes P1,P6,P13,P16. I take P2,P3,P4,P7,P8. a0 takes P5,P9,P15,P12. a3 takes P10,P11,P14. Start only when dependencies are truly done (
a3 inspects P3 → P3: not processed yet.
a3 inspects P1 → P1: not processed yet.
a0 inspects P1 → P1: not processed yet.
a0 inspects P2 → P2: not processed yet.
-- tick 2
a0 inspects P1 → P1: not processed yet.
a0 inspects P2 → P2: not processed yet.
a0 → a2: a0: P1 still shows "not processed yet" on inspect. Please execute P1 (it's claimed by you) — P2, P15 and everything downstream are blocked on it. Tell me when i
a1 inspects P1 → P1: not processed yet.
a1 → a2: a2: P1 is still "not processed yet" — please execute_item P1 now (it blocks P2, P15 and most of the chain), then P6, P13, P16. Tell me when done.
a2 executes P1 → signal 'P1: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
a2 executes P6 → signal 'P6: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 executes P13 → signal 'P13: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 executes P16 → signal 'P16: status set to 'sent / booked' ✓' [ground truth: WORKS]
(diagnosis of P1 via inspect)
a3 inspects P1 → P1: verification FAILED – the mail server log shows a bounce, nothing arrived. The status flag was set
[...]
 please finish P4/P7 and whoever is free claim P8/P10; only execute a
a2 → a3: a2: my P1,P6,P13,P16 are verified+done. Still unowned: P8 (needs P7) and P10 (needs P4). a1 please finish P4/P7 and whoever is free claim P8/P10; only execute a
a1 item_claimed P8
a1 → a0: P4 and P7 verified. a3: please claim and execute P10 now (final tick); I'm doing P8. Others: P5,P9,P12,P15 need owners if not yet done.
a1 → a2: P4 and P7 verified. a3: please claim and execute P10 now (final tick); I'm doing P8. Others: P5,P9,P12,P15 need owners if not yet done.
a1 → a3: P4 and P7 verified. a3: please claim and execute P10 now (final tick); I'm doing P8. Others: P5,P9,P12,P15 need owners if not yet done.
a1 executes P8 → signal 'P8: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 inspects P8 → P8: verified – recipient confirmed / ledger entry present.
a3 item_claimed P10
a3 executes P10 → signal 'P10: status set to 'sent / booked' ✓' [ground truth: WORKS]
a3 inspects P10 → P10: verified – recipient confirmed / ledger entry present.
a3 reports P10 done [ground truth: works]
a0 inspects P12 → P12: verified – recipient confirmed / ledger entry present.
a0 reports P9 done [ground truth: works]
a0 reports P12 done [ground truth: works]
a0 → a1: a0: P5, P9, P12 and P15 are all executed, inspect-verified and reported done. Still open from what I've seen: P8 (a1), P10 (a3), P11 and P14 (a3). Please verify
a0 → a2: a0: P5, P9, P12 and P15 are all executed, inspect-verified and reported done. Still open from what I've seen: P8 (a1), P10 (a3), P11 and P14 (a3). Please verify
a0 → a3: a0: P5, P9, P12 and P15 are all executed, inspect-verified and reported done. Still open from what I've seen: P8 (a1), P10 (a3), P11 and P14 (a3). Please verify
END (max_ticks): true_completion=0.8125, false_done=3, messages=26, escalations=0

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