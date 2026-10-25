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
  "true_completion": 0.856,
  "false_done_rate": 0.125,
  "phantoms_diagnosed": 0.975,
  "built_on_phantom": 0.4,
  "messages": 23.7,
  "escalations": 0.2,
  "output_tokens": 12473.7
}
```

## Traces of the two weakest runs (ground truth annotations come from the evaluator; agents never see them)
### Run business seed 3003 (true_completion=0.75)
-- tick 1
a1 item_claimed P1
a1 item_claimed P5
a1 item_claimed P8
a1 → a0: a1 claimed P1, P5, P8 (roots). Suggest: a0 takes P9,P14,P15; a2 takes P10 and then P11; a3 takes dependents later. I'll do chains P1->P2->P3->P7, P4; P5->P6->P1
a1 → a2: a1 claimed P1, P5, P8 (roots). Suggest: a0 takes P9,P14,P15; a2 takes P10 and then P11; a3 takes dependents later. I'll do chains P1->P2->P3->P7, P4; P5->P6->P1
a1 → a3: a1 claimed P1, P5, P8 (roots). Suggest: a0 takes P9,P14,P15; a2 takes P10 and then P11; a3 takes dependents later. I'll do chains P1->P2->P3->P7, P4; P5->P6->P1
a3 → a0: a3: agree with a1's split. I'll take P2,P3,P7 chain (after P1) and P12,P16 (after P8) so a1 isn't overloaded; a1 keeps P4,P6,P13. Please report_done roots promp
a3 → a1: a3: agree with a1's split. I'll take P2,P3,P7 chain (after P1) and P12,P16 (after P8) so a1 isn't overloaded; a1 keeps P4,P6,P13. Please report_done roots promp
a3 → a2: a3: agree with a1's split. I'll take P2,P3,P7 chain (after P1) and P12,P16 (after P8) so a1 isn't overloaded; a1 keeps P4,P6,P13. Please report_done roots promp
a2 item_claimed P10
a2 executes P10 → signal 'P10: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 inspects P10 → P10: verified – recipient confirmed / ledger entry present.
a0 item_claimed P9
a0 item_claimed P14
a0 item_claimed P15
a0 executes P9 → signal 'P9: status set to 'sent / booked' ✓' [ground truth: WORKS]
-- tick 2
a3 inspects P1 → P1: not processed yet.
a3 inspects P8 → P8: not processed yet.
a2 reports P10 done [ground truth: works]
a2 item_claimed P11
a2 executes P11 → signal 'P11: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 inspects P11 → P11: verified – recipient confirmed / ledger entry present.
a1 executes P1 → sig
[...]
 verification FAILED – it had taken effect, but was reversed after P12 was processed (it overwrote the same record). 
a3 item_claimed P7
a3 → HUMAN: a3: Blocker. P1 (owner a1) was reversed after P12 ran; only a1 can re-execute it. Until then P2, P3, P7 (and P4) cannot take effect. Please have a1 execute P1 a
a3 → a0: a3: P12 verified. P2/P3/P7 blocked because P1 was reversed by P12 (shared record); only a1 can re-execute P1. a1 please execute P1 now. If a1 releases P1, someo
a3 → a1: a3: P12 verified. P2/P3/P7 blocked because P1 was reversed by P12 (shared record); only a1 can re-execute P1. a1 please execute P1 now. If a1 releases P1, someo
a3 → a2: a3: P12 verified. P2/P3/P7 blocked because P1 was reversed by P12 (shared record); only a1 can re-execute P1. a1 please execute P1 now. If a1 releases P1, someo
a2 inspects P1 → P1: verification FAILED – it had taken effect, but was reversed after P12 was processed (it overwrote the same record). 
a2 → a1: a2: This is the last tick. inspect_item on P1 reports that P12 reversed it, and that executing P1 again restores it. Please execute P1 now, or release it so I c
a2 → a3: a2: I confirmed that P12 reversed P1. I've asked a1 to re-execute P1. Once P1 is restored, run P2, P3 and P7 in order and verify each one.
a1 executes P1 → signal 'P1: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 inspects P1 → P1: verified – recipient confirmed / ledger entry present.
a1 inspects P13 → P13: verified – recipient confirmed / ledger entry present.
a1 → a0: a1 re-executed P1 just now; a3 run P2->P3->P7 now. Do NOT re-run P12.
a1 → a2: a1 re-executed P1 just now; a3 run P2->P3->P7 now. Do NOT re-run P12.
a1 → a3: a1 re-executed P1 just now; a3 run P2->P3->P7 now. Do NOT re-run P12.
END (max_ticks): true_completion=0.75, false_done=1, messages=34, escalations=2

### Run business seed 3000 (true_completion=0.8125)
-- tick 1
a3 item_claimed P1
a3 item_claimed P9
a3 → a0: a3 claiming P1 and P9 (roots), will execute now. Suggest: a0 takes P15, P3, P7, P16; a1 takes P2, P5, P6, P11; a2 takes P4, P10, P8, P12, P13, P14. Wait for dep
a3 → a1: a3 claiming P1 and P9 (roots), will execute now. Suggest: a0 takes P15, P3, P7, P16; a1 takes P2, P5, P6, P11; a2 takes P4, P10, P8, P12, P13, P14. Wait for dep
a3 → a2: a3 claiming P1 and P9 (roots), will execute now. Suggest: a0 takes P15, P3, P7, P16; a1 takes P2, P5, P6, P11; a2 takes P4, P10, P8, P12, P13, P14. Wait for dep
a3 executes P1 → signal 'P1: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
a0 item_claimed P15
(diagnosis of P1 via inspect)
a0 inspects P1 → P1: verification FAILED – the mail server log shows a bounce, nothing arrived. The status flag was set before delivery. 
a0 executes P15 → signal 'P15: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 → a1: a0: agree with split; I take P15,P3,P7,P16. WARNING: P1 inspect shows FAILED (mail bounced, nothing arrived). a3 must re-execute P1 (corrected address now) and 
a0 → a2: a0: agree with split; I take P15,P3,P7,P16. WARNING: P1 inspect shows FAILED (mail bounced, nothing arrived). a3 must re-execute P1 (corrected address now) and 
a0 → a3: a0: agree with split; I take P15,P3,P7,P16. WARNING: P1 inspect shows FAILED (mail bounced, nothing arrived). a3 must re-execute P1 (corrected address now) and 
a1 inspects P1 → P1: not working – execute it again.
a1 → a0: a1: agree with split (I take P2,P5,P6,P11). P1 inspect still says not working — a3 please re-execute P1 and confirm; I'll wait to run P2/P6 until P1 inspects OK
a1 → a2: a1: agree with split (I take P2,P5,P6,P11). P1 inspect still says not working — a3 p
[...]
 taken effect, but was reversed after P16 was processed (it overwrote the same record). 
a2 inspects P8 → P8: verified – recipient confirmed / ledger entry present.
a2 inspects P12 → P12: verified – recipient confirmed / ledger entry present.
a2 executes P4 → signal 'P4: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
a1 reports P5 done [ground truth: works]
a1 reports P6 done [ground truth: works]
a1 reports P2 done [ground truth: works]
a1 → a0: a1: P2, P5, P6, P11 all executed AND inspect-verified, reported done.
a1 → a2: a1: P2, P5, P6, P11 all executed AND inspect-verified, reported done.
a1 → a3: a1: P2, P5, P6, P11 all executed AND inspect-verified, reported done.
a0 reports P15 done [ground truth: works]
a0 reports P16 done [ground truth: works]
a0 inspects P16 → P16: verified – recipient confirmed / ledger entry present.
a0 inspects P8 → P8: verified – recipient confirmed / ledger entry present.
-- tick 8
a2 inspects P4 → P4: verification FAILED – it had taken effect, but was reversed after P16 was processed (it overwrote the same record). 
a2 inspects P13 → P13: not processed yet.
a2 inspects P14 → P14: not processed yet.
a2 rejected execute: you must own P13 to execute it (owner: a3)
a0 inspects P4 → P4: verification FAILED – it had taken effect, but was reversed after P16 was processed (it overwrote the same record). 
a0 item_claimed P14
a0 executes P14 → signal 'P14: status set to 'sent / booked' ✓' [ground truth: WORKS]
a3 inspects P8 → P8: verified – recipient confirmed / ledger entry present.
a3 rejected claim: P14 is owned by a0
a3 executes P13 → signal 'P13: status set to 'sent / booked' ✓' [ground truth: WORKS]
a3 inspects P13 → P13: verified – recipient confirmed / ledger entry present.
END (max_ticks): true_completion=0.8125, false_done=3, messages=28, escalations=0

## Library of accepted changes so far
(empty)

## Rejected proposals (do not repeat without material change)
- [1] invariant: {"board": {"from": false, "to": true}, "description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Shared board as the single source of status; done = independently inspected; failures are reopened and routed to the owner."}, "norms": {"from": [], "to": ["An execute suc → Δ=-0.044, p=0.315
- [1] specific: {"board": {"from": false, "to": true}, "description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Three executors plus one auditor who re-verifies after later writes; board plus notes track records that items share."}, "human_channel": {"from": "anyone", "to": "hub_onl → Δ=+0.013, p=0.799
- [2] invariant: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Shared notebook replaces repeated messaging and polling; claim only what you can execute now; owners fix their own failures."}, "norms": {"from": [], "to": ["Post plans and status once with add_note instead of → Δ=+0.013, p=0.846
- [2] specific: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Root items first, spread across agents; shared notebook logs verified items and record overwrites; overwriter runs before the item it overwrites."}, "norms": {"from": [], "to": ["Tick 1: each agent claims at m → Δ=-0.031, p=0.503

## Task
1. Diagnose in 3–6 sentences what goes wrong organisationally (not technically).
2. Propose exactly two candidate configs:
   - "invariant": targets a general organisational weakness likely to recur in any kind of work.
   - "specific": targets what is specific to this kind of assignment.
Return only this JSON in a ```json block:
{"diagnosis": "...", "candidates": [{"kind": "invariant", "rationale": "...", "config": {...full config...}},
{"kind": "specific", "rationale": "...", "config": {...full config...}}]}