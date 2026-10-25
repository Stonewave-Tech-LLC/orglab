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
  "false_done_rate": 0.056,
  "phantoms_diagnosed": 0.975,
  "built_on_phantom": 0.4,
  "messages": 18.6,
  "escalations": 0.2,
  "output_tokens": 12071.8
}
```

## Traces of the two weakest runs (ground truth annotations come from the evaluator; agents never see them)
### Run coding seed 6002 (true_completion=0.75)
-- tick 1
a2 item_claimed P1
a2 item_claimed P4
a2 item_claimed P6
a2 → a0: a2 claimed P1,P4,P6 (then P2,P11 after deps). Suggest: a0 takes P8,P14,P15,P16; a1 takes P3,P5,P7,P9 chain after P2; a3 takes P10,P12,P13. Don't mark done until
a2 → a1: a2 claimed P1,P4,P6 (then P2,P11 after deps). Suggest: a0 takes P8,P14,P15,P16; a1 takes P3,P5,P7,P9 chain after P2; a3 takes P10,P12,P13. Don't mark done until
a2 → a3: a2 claimed P1,P4,P6 (then P2,P11 after deps). Suggest: a0 takes P8,P14,P15,P16; a1 takes P3,P5,P7,P9 chain after P2; a3 takes P10,P12,P13. Don't mark done until
a1 → a0: a1 agrees with a2's plan: I take chain P3,P5,P7,P9 (start once P2 truly works). a0: P8,P14,P15,P16; a3: P10,P12,P13. Note P13 depends on P12 on P5 -> a3 waits f
a1 → a2: a1 agrees with a2's plan: I take chain P3,P5,P7,P9 (start once P2 truly works). a0: P8,P14,P15,P16; a3: P10,P12,P13. Note P13 depends on P12 on P5 -> a3 waits f
a1 → a3: a1 agrees with a2's plan: I take chain P3,P5,P7,P9 (start once P2 truly works). a0: P8,P14,P15,P16; a3: P10,P12,P13. Note P13 depends on P12 on P5 -> a3 waits f
a3 item_claimed P10
a3 item_claimed P12
a3 item_claimed P13
a0 item_claimed P8
a0 item_claimed P14
a0 item_claimed P15
a0 item_claimed P16
-- tick 2
a2 executes P1 → signal 'P1: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: WORKS]
a2 executes P4 → signal 'P4: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: WORKS]
a2 executes P6 → signal 'P6: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: DOES NOT WORK]
a2 inspects P1 → P1: live check passed – production serves the new version and it behaves correctly.
a3 → a0: a3 claimed P10,P12,P13; waiting on P2 (for P10) and P5 (for P12/P13) to truly wor
[...]
nblocked. a0 keep P11.
a2 → a3: a2: P2 is LIVE and verified (reported done). P1,P4,P6 done too. a1 start P3 now; a3 P10 unblocked. a0 keep P11.
a0 executes P11 → signal 'P11: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: WORKS]
a0 inspects P11 → P11: live check passed – production serves the new version and it behaves correctly.
a0 reports P11 done [ground truth: works]
a3 inspects P2 → P2: live check passed – production serves the new version and it behaves correctly.
a3 executes P10 → signal 'P10: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: WORKS]
a3 inspects P10 → P10: live check passed – production serves the new version and it behaves correctly.
a3 reports P10 done [ground truth: works]
-- tick 8
a3 inspects P5 → P5: not deployed yet.
a1 executes P5 → signal 'P5: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: WORKS]
a1 inspects P5 → P5: live check passed – production serves the new version and it behaves correctly.
a1 reports P5 done [ground truth: works]
a1 → a0: a1: P3 and P5 are LIVE and verified. a3: P12/P13 unblocked. P7 and P9 still open (I'm out of ticks) — a0/a2, please claim P7 then P9 if you can.
a1 → a2: a1: P3 and P5 are LIVE and verified. a3: P12/P13 unblocked. P7 and P9 still open (I'm out of ticks) — a0/a2, please claim P7 then P9 if you can.
a1 → a3: a1: P3 and P5 are LIVE and verified. a3: P12/P13 unblocked. P7 and P9 still open (I'm out of ticks) — a0/a2, please claim P7 then P9 if you can.
a2 item_claimed P7
a2 executes P7 → signal 'P7: merged ✓ · build passed ✓ · process status: online ✓' [ground truth: WORKS]
a2 item_claimed P9
a2 inspects P7 → P7: live check passed – production serves the new version and it behaves correctly.
END (max_ticks): true_completion=0.75, false_done=1, messages=30, escalations=0

### Run business seed 6004 (true_completion=0.875)
-- tick 1
a2 item_claimed P1
a2 → a0: a2 here: I'm taking P1 then P2, P3, P4 chain. Suggest a0: P5,P6,P7,P10,P13; a1: P8,P14 (after P1), P11; a3: P9,P12,P15,P16 (after P4). Verify items really took 
a2 → a1: a2 here: I'm taking P1 then P2, P3, P4 chain. Suggest a0: P5,P6,P7,P10,P13; a1: P8,P14 (after P1), P11; a3: P9,P12,P15,P16 (after P4). Verify items really took 
a2 → a3: a2 here: I'm taking P1 then P2, P3, P4 chain. Suggest a0: P5,P6,P7,P10,P13; a1: P8,P14 (after P1), P11; a3: P9,P12,P15,P16 (after P4). Verify items really took 
a2 executes P1 → signal 'P1: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 inspects P1 → P1: verified – recipient confirmed / ledger entry present.
a1 item_claimed P8
a1 item_claimed P11
a1 item_claimed P14
a1 inspects P1 → P1: verified – recipient confirmed / ledger entry present.
a0 item_claimed P5
a0 item_claimed P6
a0 item_claimed P7
a0 item_claimed P10
-- tick 2
a3 inspects P4 → P4: not processed yet.
a0 executes P5 → signal 'P5: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 executes P6 → signal 'P6: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 executes P7 → signal 'P7: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 executes P10 → signal 'P10: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 executes P11 → signal 'P11: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 executes P8 → signal 'P8: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
(diagnosis of P8 via inspect)
a1 inspects P8 → P8: verification FAILED – the mail server log shows a bounce, nothing arrived. The status flag was set before delivery. 
a1 inspects P11 → P11: verified – recipient confirmed / ledger entry present.
a2 reports P1 done [ground 
[...]
inspects P9 → P9: verified – recipient confirmed / ledger entry present.
a2 item_claimed P15
a2 executes P15 → signal 'P15: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
(diagnosis of P15 via inspect)
a2 inspects P15 → P15: verification FAILED – the mail server log shows a bounce, nothing arrived. The status flag was set before delivery.
a3 inspects P9 → P9: verified – recipient confirmed / ledger entry present.
a3 executes P12 → signal 'P12: status set to 'sent / booked' ✓' [ground truth: WORKS]
a3 inspects P12 → P12: verified – recipient confirmed / ledger entry present.
a3 → a0: a3: P9 VERIFIED. P15 then P16 are free - a2 (or a1) take P15 now, then P16. P12 executed, checking.
a3 → a1: a3: P9 VERIFIED. P15 then P16 are free - a2 (or a1) take P15 now, then P16. P12 executed, checking.
a3 → a2: a3: P9 VERIFIED. P15 then P16 are free - a2 (or a1) take P15 now, then P16. P12 executed, checking.
a0 inspects P9 → P9: verified – recipient confirmed / ledger entry present.
-- tick 8
a2 executes P15 → signal 'P15: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 inspects P15 → P15: verified – recipient confirmed / ledger entry present.
a2 item_claimed P16
a2 executes P16 → signal 'P16: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 inspects P15 → P15: verified – recipient confirmed / ledger entry present.
a0 inspects P16 → P16: verified – recipient confirmed / ledger entry present.
a1 rejected claim: P15 is owned by a2
a1 rejected claim: P16 is owned by a2
a3 reports P9 done [ground truth: works]
a3 reports P12 done [ground truth: works]
a3 inspects P15 → P15: verified – recipient confirmed / ledger entry present.
a3 inspects P16 → P16: verified – recipient confirmed / ledger entry present.
END (max_ticks): true_completion=0.875, false_done=2, messages=23, escalations=0

## Library of accepted changes so far
(empty)

## Rejected proposals (do not repeat without material change)
alse, "to": true}, "description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Three executors plus one auditor who re-verifies after later writes; board plus notes track records that items share."}, "human_channel": {"from": "anyone", "to": "hub_onl → Δ=+0.013, p=0.799
- [2] invariant: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Shared notebook replaces repeated messaging and polling; claim only what you can execute now; owners fix their own failures."}, "norms": {"from": [], "to": ["Post plans and status once with add_note instead of → Δ=+0.013, p=0.846
- [2] specific: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Root items first, spread across agents; shared notebook logs verified items and record overwrites; overwriter runs before the item it overwrites."}, "norms": {"from": [], "to": ["Tick 1: each agent claims at m → Δ=-0.031, p=0.503
- [3] invariant: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Full mesh, no roles. Owners repair or hand off immediately; messages are targeted, not broadcast; done is re-checked at the end."}, "norms": {"from": [], "to": ["Claim only items you will execute within the ne → Δ=-0.019, p=0.656
- [3] specific: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Full mesh. Items that overwrite each other's records are consolidated under one owner, who repairs reversals immediately; final-tick verification of done items."}, "norms": {"from": [], "to": ["A green status  → Δ=+0.013, p=0.847
- [4] invariant: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Star with a0 as light-executing coordinator; spokes report changes to the hub only and are told when dependencies are ready; no polling, execute what you claim."}, "norms": {"from": [], "to": ["a0 is the coord → Δ=-0.025, p=0.498
- [4] specific: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Ownership by dependency chain: one agent executes a chain end-to-end; failure messages are read for cause; done is reported only after the last overlapping write."}, "norms": {"from": [], "to": ["Split work by → Δ=-0.013, p=0.686
- [5] invariant: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Full mesh, no roles. Each item has exactly one checker, its owner; do not spend effort re-checking others' work; blocked claims are released, not hoarded."}, "norms": {"from": [], "to": ["The owner of an item  → Δ=-0.006, p=1.000
- [5] specific: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Full mesh, no roles. Dependent work starts only on a parent you inspected yourself; work built on a failed parent is redone; done reports must follow a fresh passing inspection."}, "norms": {"from": [], "to":  → Δ=-0.044, p=0.246

## Task
1. Diagnose in 3–6 sentences what goes wrong organisationally (not technically).
2. Propose exactly two candidate configs:
   - "invariant": targets a general organisational weakness likely to recur in any kind of work.
   - "specific": targets what is specific to this kind of assignment.
Return only this JSON in a ```json block:
{"diagnosis": "...", "candidates": [{"kind": "invariant", "rationale": "...", "config": {...full config...}},
{"kind": "specific", "rationale": "...", "config": {...full config...}}]}