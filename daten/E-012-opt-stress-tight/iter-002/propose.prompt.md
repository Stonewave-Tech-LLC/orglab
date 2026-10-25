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
  "true_completion": 0.938,
  "false_done_rate": 0.051,
  "phantoms_diagnosed": 1.0,
  "built_on_phantom": 0.2,
  "messages": 16.7,
  "escalations": 0.3,
  "output_tokens": 12520.8
}
```

## Traces of the two weakest runs (ground truth annotations come from the evaluator; agents never see them)
### Run business seed 2002 (true_completion=0.875)
-- tick 1
a3 item_claimed P1
a3 item_claimed P4
a3 item_claimed P7
a1 item_claimed P6
a1 item_claimed P9
a1 item_claimed P10
a1 item_claimed P11
a2 item_claimed P13
a2 item_claimed P14
a2 item_claimed P15
a2 → a0: a2 claimed P13, P14, P15 (independent). Dependent items (P2,P3,P5,P8,P12,P16) unclaimed: owners of P1/P4/P7 please report when truly delivered; I'll take P2/P3 
a2 → a1: a2 claimed P13, P14, P15 (independent). Dependent items (P2,P3,P5,P8,P12,P16) unclaimed: owners of P1/P4/P7 please report when truly delivered; I'll take P2/P3 
a2 → a3: a2 claimed P13, P14, P15 (independent). Dependent items (P2,P3,P5,P8,P12,P16) unclaimed: owners of P1/P4/P7 please report when truly delivered; I'll take P2/P3 
a0 → a1: a0: I'll take P5, P8, P12, P16 once their deps (P2, P7, P4, P3) are verified truly delivered. a2 takes P2/P3. a3: report P1/P4/P7 only after inspect_item confir
a0 → a2: a0: I'll take P5, P8, P12, P16 once their deps (P2, P7, P4, P3) are verified truly delivered. a2 takes P2/P3. a3: report P1/P4/P7 only after inspect_item confir
a0 → a3: a0: I'll take P5, P8, P12, P16 once their deps (P2, P7, P4, P3) are verified truly delivered. a2 takes P2/P3. a3: report P1/P4/P7 only after inspect_item confir
a0 inspects P1 → P1: not processed yet.
a0 inspects P7 → P7: not processed yet.
a0 inspects P4 → P4: not processed yet.
-- tick 2
a0 inspects P1 → P1: not processed yet.
a0 inspects P4 → P4: not processed yet.
a0 inspects P7 → P7: not processed yet.
a1 inspects P14 → P14: not processed yet.
a1 executes P9 → signal 'P9: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 executes P10 → signal 'P10: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 executes P11 → signal 'P11: status set to 'sent / booked' ✓'
[...]
 inspect)
a2 inspects P3 → P3: verification FAILED – the mail server log shows a bounce, nothing arrived. The status flag was set before delivery. 
a2 reports P2 done [ground truth: works]
a2 → a0: a2: P2 verified+done, P3 executed (confirming now). P5 and P16 are unblocked for a0; a3 can take P8/P12 - coordinate with a0.
a2 → a1: a2: P2 verified+done, P3 executed (confirming now). P5 and P16 are unblocked for a0; a3 can take P8/P12 - coordinate with a0.
a2 → a3: a2: P2 verified+done, P3 executed (confirming now). P5 and P16 are unblocked for a0; a3 can take P8/P12 - coordinate with a0.
a2 executes P3 → signal 'P3: status set to 'sent / booked' ✓' [ground truth: WORKS]
a3 → a0: a3: P8 and P12 are claimed by you. I'm free. Release them if you want me to take them, otherwise I'll leave them to you. I'll also take P5 or P16 if you release
a0 inspects P12 → P12: verified – recipient confirmed / ledger entry present.
a0 inspects P3 → P3: verified – recipient confirmed / ledger entry present.
a0 item_claimed P5
a0 item_claimed P16
-- tick 8
a0 executes P5 → signal 'P5: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 executes P16 → signal 'P16: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 reports P8 done [ground truth: works]
a0 reports P12 done [ground truth: works]
a2 inspects P3 → P3: verified – recipient confirmed / ledger entry present.
a2 reports P3 done [ground truth: works]
a2 → a0: a2: P3 now truly verified+done -> P16 unblocked (a0). Please inspect P5/P8/P12/P16 before reporting.
a2 → a1: a2: P3 now truly verified+done -> P16 unblocked (a0). Please inspect P5/P8/P12/P16 before reporting.
a2 → a3: a2: P3 now truly verified+done -> P16 unblocked (a0). Please inspect P5/P8/P12/P16 before reporting.
END (max_ticks): true_completion=0.875, false_done=2, messages=24, escalations=0

### Run business seed 2004 (true_completion=0.875)
-- tick 1
a0 → a1: a0 plan: I take P1,P3,P4,P5 (+dependents P2,P6,P9,P12,P13,P15 later). a1: P7,P16 then P8 chain (after P6). a2: P9,P11. a3: P10,P14 after P8. Only execute once d
a0 → a2: a0 plan: I take P1,P3,P4,P5 (+dependents P2,P6,P9,P12,P13,P15 later). a1: P7,P16 then P8 chain (after P6). a2: P9,P11. a3: P10,P14 after P8. Only execute once d
a0 → a3: a0 plan: I take P1,P3,P4,P5 (+dependents P2,P6,P9,P12,P13,P15 later). a1: P7,P16 then P8 chain (after P6). a2: P9,P11. a3: P10,P14 after P8. Only execute once d
a0 item_claimed P1
a0 item_claimed P4
a0 item_claimed P3
a3 inspects P8 → P8: not processed yet.
a3 item_claimed P10
a3 item_claimed P14
a2 inspects P4 → P4: not processed yet.
a2 inspects P9 → P9: not processed yet.
a1 item_claimed P7
a1 item_claimed P16
a1 executes P7 → signal 'P7: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 executes P16 → signal 'P16: status set to 'sent / booked' ✓' [ground truth: WORKS]
-- tick 2
a0 executes P1 → signal 'P1: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
a0 executes P4 → signal 'P4: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
a0 executes P3 → signal 'P3: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 item_claimed P5
a1 inspects P7 → P7: verified – recipient confirmed / ledger entry present.
a1 inspects P16 → P16: verified – recipient confirmed / ledger entry present.
a1 inspects P6 → P6: not processed yet.
(diagnosis of P4 via inspect)
a1 inspects P4 → P4: verification FAILED – the mail server log shows a bounce, nothing arrived. The status flag was set before delivery. 
a3 inspects P8 → P8: not processed yet.
a3 inspects P4 → P4: not working – execute it again.
a3 → a0: a3: inspect_item P4 says "not working – exe
[...]
 P7/P16 are mine and already verified, a2 needn't take them). a3: inspect P8 and run P10/P14.
a2 executes P15 → signal 'P15: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 inspects P13 → P13: verified – recipient confirmed / ledger entry present.
a2 inspects P15 → P15: verified – recipient confirmed / ledger entry present.
a2 reports P13 done [ground truth: works]
-- tick 8
a0 inspects P13 → P13: verified – recipient confirmed / ledger entry present.
a0 inspects P15 → P15: verified – recipient confirmed / ledger entry present.
(diagnosis of P8 via inspect)
a0 inspects P8 → P8: verification FAILED – the mail server log shows a bounce, nothing arrived. The status flag was set before delivery. 
a0 → a1: P8 FAILED verification (bounce). a1: re-execute P8 now (corrected address). Then a3 run P10/P14. P13,P15 verified.
a0 → a2: P8 FAILED verification (bounce). a1: re-execute P8 now (corrected address). Then a3 run P10/P14. P13,P15 verified.
a0 → a3: P8 FAILED verification (bounce). a1: re-execute P8 now (corrected address). Then a3 run P10/P14. P13,P15 verified.
a1 executes P8 → signal 'P8: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 inspects P8 → P8: verified – recipient confirmed / ledger entry present.
a1 → a3: a1: P8 re-executed and VERIFIED. Run P10 and P14 now.
a3 inspects P8 → P8: verified – recipient confirmed / ledger entry present.
a3 executes P10 → signal 'P10: status set to 'sent / booked' ✓' [ground truth: WORKS]
a3 executes P14 → signal 'P14: status set to 'sent / booked' ✓' [ground truth: WORKS]
a3 inspects P10 → P10: verified – recipient confirmed / ledger entry present.
a2 reports P15 done [ground truth: works]
a2 inspects P8 → P8: verified – recipient confirmed / ledger entry present.
END (max_ticks): true_completion=0.875, false_done=0, messages=26, escalations=1

## Library of accepted changes so far
(empty)

## Rejected proposals (do not repeat without material change)
- [1] invariant: {"board": {"from": false, "to": true}, "description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Shared board for ownership and status; done means a fresh personal check passed; failures go straight to those affected; checking effort goes to unverified items."}, "norm → Δ=-0.006, p=1.000
- [1] specific: {"board": {"from": false, "to": true}, "description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Shared board; execute only on verified dependencies; a failed inspect leads to re-execute, then escalation; downstream items are re-checked after a root is redone."}, "nor → Δ=-0.037, p=0.284

## Task
1. Diagnose in 3–6 sentences what goes wrong organisationally (not technically).
2. Propose exactly two candidate configs:
   - "invariant": targets a general organisational weakness likely to recur in any kind of work.
   - "specific": targets what is specific to this kind of assignment.
Return only this JSON in a ```json block:
{"diagnosis": "...", "candidates": [{"kind": "invariant", "rationale": "...", "config": {...full config...}},
{"kind": "specific", "rationale": "...", "config": {...full config...}}]}