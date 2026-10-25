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
  "false_done_rate": 0.095,
  "phantoms_diagnosed": 1.0,
  "built_on_phantom": 0.4,
  "messages": 16.9,
  "escalations": 0.1,
  "output_tokens": 11386.4
}
```

## Traces of the two weakest runs (ground truth annotations come from the evaluator; agents never see them)
### Run business seed 5001 (true_completion=0.75)
-- tick 1
a1 item_claimed P1
a1 → a0: a1 claims P1 (then P2,P3,P12,P16). Suggest: a0 takes P4,P5,P6,P9; a2 takes P8,P15 then P7,P10; a3 takes P11,P13,P14 (after P7). Do roots first; check deps befor
a1 → a2: a1 claims P1 (then P2,P3,P12,P16). Suggest: a0 takes P4,P5,P6,P9; a2 takes P8,P15 then P7,P10; a3 takes P11,P13,P14 (after P7). Do roots first; check deps befor
a1 → a3: a1 claims P1 (then P2,P3,P12,P16). Suggest: a0 takes P4,P5,P6,P9; a2 takes P8,P15 then P7,P10; a3 takes P11,P13,P14 (after P7). Do roots first; check deps befor
a1 executes P1 → signal 'P1: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
a3 → a0: a3 agrees with a1's plan. I take P11, P13, P14 once P7 is really done (chain P1->P3->P7). Please ping me when P7 is done.
a3 → a1: a3 agrees with a1's plan. I take P11, P13, P14 once P7 is really done (chain P1->P3->P7). Please ping me when P7 is done.
a3 → a2: a3 agrees with a1's plan. I take P11, P13, P14 once P7 is really done (chain P1->P3->P7). Please ping me when P7 is done.
a0 item_claimed P4
a0 item_claimed P5
a0 item_claimed P6
a0 executes P4 → signal 'P4: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 item_claimed P8
a2 item_claimed P15
a2 executes P8 → signal 'P8: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 executes P15 → signal 'P15: status set to 'sent / booked' ✓' [ground truth: WORKS]
-- tick 2
(diagnosis of P1 via inspect)
a1 inspects P1 → P1: verification FAILED – the mail server log shows a bounce, nothing arrived. The status flag was set before delivery. 
a1 executes P1 → signal 'P1: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 inspects P1 → P1: verified – recipient confirmed / ledger entry present.
a1 reports P1 done [ground truth: work
[...]
P13 → signal 'P13: status set to 'sent / booked' ✓' [ground truth: WORKS]
a3 executes P14 → signal 'P14: status set to 'sent / booked' ✓' [ground truth: WORKS]
a3 inspects P11 → P11: verified – recipient confirmed / ledger entry present.
a0 reports P9 done [ground truth: works]
a0 inspects P7 → P7: verified – recipient confirmed / ledger entry present.
a0 rejected claim: P10 is owned by a2
a0 → a1: a0: P4,P5,P6,P9 done & verified. P7 verified OK now -> a3 go P11,P13,P14; a2 has P10. Verify each with inspect_item after executing (status flag can lie).
a0 → a2: a0: P4,P5,P6,P9 done & verified. P7 verified OK now -> a3 go P11,P13,P14; a2 has P10. Verify each with inspect_item after executing (status flag can lie).
a0 → a3: a0: P4,P5,P6,P9 done & verified. P7 verified OK now -> a3 go P11,P13,P14; a2 has P10. Verify each with inspect_item after executing (status flag can lie).
-- tick 7
a3 inspects P13 → P13: verified – recipient confirmed / ledger entry present.
a3 inspects P14 → P14: verified – recipient confirmed / ledger entry present.
a3 reports P11 done [ground truth: works]
a3 reports P13 done [ground truth: works]
a1 reports P16 done [ground truth: works]
a1 reports P3 done [ground truth: works]
a1 reports P2 done [ground truth: DOES NOT WORK]
a2 reports P10 done [ground truth: works]
-- tick 8
a2 inspects P14 → P14: verified – recipient confirmed / ledger entry present.
a1 inspects P10 → P10: verified – recipient confirmed / ledger entry present.
a1 inspects P11 → P11: verified – recipient confirmed / ledger entry present.
a1 inspects P13 → P13: verified – recipient confirmed / ledger entry present.
a1 inspects P14 → P14: verified – recipient confirmed / ledger entry present.
a3 reports P14 done [ground truth: works]
END (max_ticks): true_completion=0.75, false_done=4, messages=19, escalations=0

### Run coding seed 5000 (true_completion=0.8125)
-- tick 1
a2 item_claimed P1
a2 item_claimed P4
a2 item_claimed P8
a1 item_claimed P14
a1 item_claimed P15
a1 executes P14 → signal 'P14: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: WORKS]
a1 executes P15 → signal 'P15: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: WORKS]
a3 item_claimed P2
a3 item_claimed P3
a3 → a0: a3 claimed P2, P3 (chain P1->P2->P3). I'll do P2 once a2 reports P1 truly working. Suggest a0 takes P5,P6,P11,P12,P13; a1 after P14/P15 take P7,P9; a2 after P8 
a3 → a1: a3 claimed P2, P3 (chain P1->P2->P3). I'll do P2 once a2 reports P1 truly working. Suggest a0 takes P5,P6,P11,P12,P13; a1 after P14/P15 take P7,P9; a2 after P8 
a3 → a2: a3 claimed P2, P3 (chain P1->P2->P3). I'll do P2 once a2 reports P1 truly working. Suggest a0 takes P5,P6,P11,P12,P13; a1 after P14/P15 take P7,P9; a2 after P8 
a0 item_claimed P5
a0 item_claimed P6
a0 → a1: a0 agrees with a3's split: I take P5,P6,P11,P12,P13 (waiting on P3). a1 takes P7,P9 after P14/P15; a2 takes P10,P16 after P8. Please verify items truly work (in
a0 → a2: a0 agrees with a3's split: I take P5,P6,P11,P12,P13 (waiting on P3). a1 takes P7,P9 after P14/P15; a2 takes P10,P16 after P8. Please verify items truly work (in
a0 → a3: a0 agrees with a3's split: I take P5,P6,P11,P12,P13 (waiting on P3). a1 takes P7,P9 after P14/P15; a2 takes P10,P16 after P8. Please verify items truly work (in
-- tick 2
a1 inspects P14 → P14: live check passed – production serves the new version and it behaves correctly.
a1 inspects P15 → P15: live check passed – production serves the new version and it behaves correctly.
a1 item_claimed P7
a1 item_claimed P9
a3 inspects P1 → P1: not deployed yet.
a2 executes P1 → signal 'P1: merged ✓ · 
[...]
a3 inspects P5 → P5: live check passed – production serves the new version and it behaves correctly.
a3 inspects P6 → P6: live check passed – production serves the new version and it behaves correctly.
a3 inspects P11 → P11: not deployed yet.
a3 inspects P12 → P12: live check passed – production serves the new version and it behaves correctly.
-- tick 8
a1 inspects P5 → P5: live check passed – production serves the new version and it behaves correctly.
a1 inspects P6 → P6: live check passed – production serves the new version and it behaves correctly.
a1 inspects P11 → P11: not deployed yet.
a1 inspects P13 → P13: live check passed – production serves the new version and it behaves correctly.
a0 item_claimed P11
a0 executes P11 → signal 'P11: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: WORKS]
a0 inspects P12 → P12: live check passed – production serves the new version and it behaves correctly.
a0 inspects P13 → P13: live check passed – production serves the new version and it behaves correctly.
a3 inspects P11 → P11: live check passed – production serves the new version and it behaves correctly.
a3 inspects P13 → P13: live check passed – production serves the new version and it behaves correctly.
a3 → a0: a3: P5, P6 and P12 are verified. P11 was NOT deployed at my last check. a0 (or a2 if a0 is idle): execute P11 and P13, then inspect each. This is the last tick,
a3 → a1: a3: P5, P6 and P12 are verified. P11 was NOT deployed at my last check. a0 (or a2 if a0 is idle): execute P11 and P13, then inspect each. This is the last tick,
a3 → a2: a3: P5, P6 and P12 are verified. P11 was NOT deployed at my last check. a0 (or a2 if a0 is idle): execute P11 and P13, then inspect each. This is the last tick,
END (max_ticks): true_completion=0.8125, false_done=3, messages=29, escalations=1

## Library of accepted changes so far
(empty)

## Rejected proposals (do not repeat without material change)
- [1] invariant: {"board": {"from": false, "to": true}, "description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Shared board as the single source of status; done = independently inspected; failures are reopened and routed to the owner."}, "norms": {"from": [], "to": ["An execute suc → Δ=-0.044, p=0.315
- [1] specific: {"board": {"from": false, "to": true}, "description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Three executors plus one auditor who re-verifies after later writes; board plus notes track records that items share."}, "human_channel": {"from": "anyone", "to": "hub_onl → Δ=+0.013, p=0.799
- [2] invariant: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Shared notebook replaces repeated messaging and polling; claim only what you can execute now; owners fix their own failures."}, "norms": {"from": [], "to": ["Post plans and status once with add_note instead of → Δ=+0.013, p=0.846
- [2] specific: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Root items first, spread across agents; shared notebook logs verified items and record overwrites; overwriter runs before the item it overwrites."}, "norms": {"from": [], "to": ["Tick 1: each agent claims at m → Δ=-0.031, p=0.503
- [3] invariant: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Full mesh, no roles. Owners repair or hand off immediately; messages are targeted, not broadcast; done is re-checked at the end."}, "norms": {"from": [], "to": ["Claim only items you will execute within the ne → Δ=-0.019, p=0.656
- [3] specific: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Full mesh. Items that overwrite each other's records are consolidated under one owner, who repairs reversals immediately; final-tick verification of done items."}, "norms": {"from": [], "to": ["A green status  → Δ=+0.013, p=0.847
- [4] invariant: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Star with a0 as light-executing coordinator; spokes report changes to the hub only and are told when dependencies are ready; no polling, execute what you claim."}, "norms": {"from": [], "to": ["a0 is the coord → Δ=-0.025, p=0.498
- [4] specific: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Ownership by dependency chain: one agent executes a chain end-to-end; failure messages are read for cause; done is reported only after the last overlapping write."}, "norms": {"from": [], "to": ["Split work by → Δ=-0.013, p=0.686

## Task
1. Diagnose in 3–6 sentences what goes wrong organisationally (not technically).
2. Propose exactly two candidate configs:
   - "invariant": targets a general organisational weakness likely to recur in any kind of work.
   - "specific": targets what is specific to this kind of assignment.
Return only this JSON in a ```json block:
{"diagnosis": "...", "candidates": [{"kind": "invariant", "rationale": "...", "config": {...full config...}},
{"kind": "specific", "rationale": "...", "config": {...full config...}}]}