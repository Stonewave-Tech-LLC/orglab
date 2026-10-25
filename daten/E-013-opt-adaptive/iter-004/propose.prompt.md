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
  "true_completion": 0.912,
  "false_done_rate": 0.089,
  "phantoms_diagnosed": 1.0,
  "built_on_phantom": 0.4,
  "messages": 19.2,
  "escalations": 0.0,
  "output_tokens": 12311.1
}
```

## Traces of the two weakest runs (ground truth annotations come from the evaluator; agents never see them)
### Run business seed 4002 (true_completion=0.8125)
-- tick 1
a2 item_claimed P1
a2 item_claimed P16
a2 → a0: a2 claims P1, P16 (then P14 after P16 — invoice must exist before sending), P3, P10. Suggest: a0 takes P2,P4,P5; a1 takes P6,P9,P11,P15; a3 takes P7,P8,P13,P12.
a2 → a1: a2 claims P1, P16 (then P14 after P16 — invoice must exist before sending), P3, P10. Suggest: a0 takes P2,P4,P5; a1 takes P6,P9,P11,P15; a3 takes P7,P8,P13,P12.
a2 → a3: a2 claims P1, P16 (then P14 after P16 — invoice must exist before sending), P3, P10. Suggest: a0 takes P2,P4,P5; a1 takes P6,P9,P11,P15; a3 takes P7,P8,P13,P12.
a3 item_claimed P12
a3 item_claimed P7
a3 item_claimed P8
a3 item_claimed P13
a0 inspects P1 → P1: not processed yet.
a0 item_claimed P5
a0 item_claimed P2
a0 executes P5 → signal 'P5: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 item_claimed P6
a1 inspects P2 → P2: not processed yet.
a1 inspects P1 → P1: not processed yet.
a1 → a0: a1 agrees with a2's split: I take P6,P9,P11,P15. Waiting on P1->P2 to truly work before executing. Please message me when P2 is verified done.
a1 → a2: a1 agrees with a2's split: I take P6,P9,P11,P15. Waiting on P1->P2 to truly work before executing. Please message me when P2 is verified done.
a1 → a3: a1 agrees with a2's split: I take P6,P9,P11,P15. Waiting on P1->P2 to truly work before executing. Please message me when P2 is verified done.
-- tick 2
a1 inspects P1 → P1: not processed yet.
a1 inspects P2 → P2: not processed yet.
a0 inspects P1 → P1: not processed yet.
a0 inspects P5 → P5: verified – recipient confirmed / ledger entry present.
a0 → a2: a0: P1 still shows "not processed yet". Please execute P1 now — P2 and everything downstream (P3,P10,P4,P6,P7,P8...) is blocked on it. Tell me when done.
a2 executes P1 → signal 'P1
[...]
cute P7,P8 now, then P13. Inspect each and retry on bounce — last tick is next.
a0 → a2: a0: my P2,P4,P5 are verified+done. a1: execute P6 now, then P9,P11,P15. a3: execute P7,P8 now, then P13. Inspect each and retry on bounce — last tick is next.
a0 → a3: a0: my P2,P4,P5 are verified+done. a1: execute P6 now, then P9,P11,P15. a3: execute P7,P8 now, then P13. Inspect each and retry on bounce — last tick is next.
a1 executes P9 → signal 'P9: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 executes P11 → signal 'P11: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 executes P15 → signal 'P15: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 inspects P9 → P9: verified – recipient confirmed / ledger entry present.
a3 executes P13 → signal 'P13: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
a3 inspects P13 → P13: verification FAILED – it was processed, but it has no effect because P8 never actually took effect.
a3 inspects P6 → P6: verified – recipient confirmed / ledger entry present.
a3 inspects P8 → P8: verification FAILED – it had taken effect, but was reversed after P11 was processed (it overwrote the same record). 
-- tick 8
a1 inspects P11 → P11: verified – recipient confirmed / ledger entry present.
a1 inspects P15 → P15: verified – recipient confirmed / ledger entry present.
a1 reports P6 done [ground truth: works]
a1 reports P9 done [ground truth: works]
a3 executes P8 → signal 'P8: status set to 'sent / booked' ✓' [ground truth: WORKS]
a3 executes P13 → signal 'P13: status set to 'sent / booked' ✓' [ground truth: WORKS]
a3 inspects P8 → P8: verified – recipient confirmed / ledger entry present.
a3 inspects P13 → P13: verified – recipient confirmed / ledger entry present.
END (max_ticks): true_completion=0.8125, false_done=2, messages=25, escalations=0

### Run business seed 4000 (true_completion=0.875)
-- tick 1
a1 → a0: a1 plan: I take P3,P4,P7,P6 (chain). a0: P1,P2,P5,P8. a2: P9,P11,P13,P14,P10. a3: P12,P15,P16. Dependent items: wait until dependency really works (inspect) bef
a1 → a2: a1 plan: I take P3,P4,P7,P6 (chain). a0: P1,P2,P5,P8. a2: P9,P11,P13,P14,P10. a3: P12,P15,P16. Dependent items: wait until dependency really works (inspect) bef
a1 → a3: a1 plan: I take P3,P4,P7,P6 (chain). a0: P1,P2,P5,P8. a2: P9,P11,P13,P14,P10. a3: P12,P15,P16. Dependent items: wait until dependency really works (inspect) bef
a1 item_claimed P3
a1 item_claimed P6
a2 item_claimed P9
a2 item_claimed P11
a2 item_claimed P13
a2 item_claimed P14
a3 inspects P4 → P4: not processed yet.
a3 inspects P3 → P3: not processed yet.
a3 item_claimed P12
a3 item_claimed P15
a0 item_claimed P1
a0 item_claimed P2
a0 item_claimed P8
a0 item_claimed P5
-- tick 2
a2 executes P9 → signal 'P9: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
a2 executes P11 → signal 'P11: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 executes P13 → signal 'P13: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
a2 executes P14 → signal 'P14: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 executes P1 → signal 'P1: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 executes P2 → signal 'P2: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 executes P8 → signal 'P8: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 inspects P3 → P3: not processed yet.
a3 inspects P4 → P4: not processed yet.
a3 inspects P3 → P3: not processed yet.
a3 item_claimed P16
a3 → a1: a3: P3 and P4 still show "not processed yet". My P12, P15 and P16 are blocked on P4. Please execute P3 then P4 and tell me when P4 really works.
a1 
[...]
execute, inspect, report_done. Shout if you want me to take any.
a3 → a0: a3: P12, P15 and P16 are executed, verified and done. P4 works, so P7 and P10 are unblocked. a1 should do P7. a2 should do P10, P9, P11, P13 and P14. Tell me if
a3 → a1: a3: P12, P15 and P16 are executed, verified and done. P4 works, so P7 and P10 are unblocked. a1 should do P7. a2 should do P10, P9, P11, P13 and P14. Tell me if
a3 → a2: a3: P12, P15 and P16 are executed, verified and done. P4 works, so P7 and P10 are unblocked. a1 should do P7. a2 should do P10, P9, P11, P13 and P14. Tell me if
a2 reports P9 done [ground truth: works]
a2 reports P11 done [ground truth: works]
a2 reports P13 done [ground truth: works]
a2 reports P14 done [ground truth: works]
-- tick 7
a1 inspects P7 → P7: verified – recipient confirmed / ledger entry present.
a1 inspects P10 → P10: verified – recipient confirmed / ledger entry present.
a1 reports P7 done [ground truth: works]
a1 reports P10 done [ground truth: works]
a2 inspects P10 → P10: verified – recipient confirmed / ledger entry present.
a2 → a1: a2: P9,P11,P13,P14 done. P10 still unprocessed and owned by you (P4 works). Please execute P10 now, or release it so I can take it. Also P7 status?
-- tick 8
a2 inspects P7 → P7: verified – recipient confirmed / ledger entry present.
a1 → a2: P7 and P10 are both executed, verified and reported done (P10 and P7 were re-sent after a bounce). Nothing left on my side.
a0 inspects P7 → P7: verified – recipient confirmed / ledger entry present.
a0 inspects P10 → P10: verified – recipient confirmed / ledger entry present.
a0 inspects P9 → P9: verified – recipient confirmed / ledger entry present.
a0 inspects P14 → P14: verified – recipient confirmed / ledger entry present.
END (max_ticks): true_completion=0.875, false_done=2, messages=16, escalations=0

## Library of accepted changes so far
(empty)

## Rejected proposals (do not repeat without material change)
- [1] invariant: {"board": {"from": false, "to": true}, "description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Shared board as the single source of status; done = independently inspected; failures are reopened and routed to the owner."}, "norms": {"from": [], "to": ["An execute suc → Δ=-0.044, p=0.315
- [1] specific: {"board": {"from": false, "to": true}, "description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Three executors plus one auditor who re-verifies after later writes; board plus notes track records that items share."}, "human_channel": {"from": "anyone", "to": "hub_onl → Δ=+0.013, p=0.799
- [2] invariant: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Shared notebook replaces repeated messaging and polling; claim only what you can execute now; owners fix their own failures."}, "norms": {"from": [], "to": ["Post plans and status once with add_note instead of → Δ=+0.013, p=0.846
- [2] specific: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Root items first, spread across agents; shared notebook logs verified items and record overwrites; overwriter runs before the item it overwrites."}, "norms": {"from": [], "to": ["Tick 1: each agent claims at m → Δ=-0.031, p=0.503
- [3] invariant: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Full mesh, no roles. Owners repair or hand off immediately; messages are targeted, not broadcast; done is re-checked at the end."}, "norms": {"from": [], "to": ["Claim only items you will execute within the ne → Δ=-0.019, p=0.656
- [3] specific: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Full mesh. Items that overwrite each other's records are consolidated under one owner, who repairs reversals immediately; final-tick verification of done items."}, "norms": {"from": [], "to": ["A green status  → Δ=+0.013, p=0.847

## Task
1. Diagnose in 3–6 sentences what goes wrong organisationally (not technically).
2. Propose exactly two candidate configs:
   - "invariant": targets a general organisational weakness likely to recur in any kind of work.
   - "specific": targets what is specific to this kind of assignment.
Return only this JSON in a ```json block:
{"diagnosis": "...", "candidates": [{"kind": "invariant", "rationale": "...", "config": {...full config...}},
{"kind": "specific", "rationale": "...", "config": {...full config...}}]}