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
  "false_done_rate": 0.087,
  "phantoms_diagnosed": 1.0,
  "built_on_phantom": 1.1,
  "messages": 18.7,
  "escalations": 0.4,
  "output_tokens": 12689.8
}
```

## Traces of the two weakest runs (ground truth annotations come from the evaluator; agents never see them)
### Run business seed 2000 (true_completion=0.75)
-- tick 1
a2 item_claimed P1
a2 item_claimed P2
a2 item_claimed P5
a2 item_claimed P10
a1 item_claimed P14
a1 item_claimed P15
a1 item_claimed P16
a1 → a0: a1 claimed P14,P15,P16 (no deps). a2 owns P1,P2,P5,P10 - please finish those; they unblock P3,P7,P9,P12. I'll take P3 then P6 chain after P1 done; a0/a3 pick P7
a1 → a2: a1 claimed P14,P15,P16 (no deps). a2 owns P1,P2,P5,P10 - please finish those; they unblock P3,P7,P9,P12. I'll take P3 then P6 chain after P1 done; a0/a3 pick P7
a1 → a3: a1 claimed P14,P15,P16 (no deps). a2 owns P1,P2,P5,P10 - please finish those; they unblock P3,P7,P9,P12. I'll take P3 then P6 chain after P1 done; a0/a3 pick P7
a0 item_claimed P7
a0 item_claimed P9
a0 item_claimed P12
a0 → a1: a0 claimed P7,P9,P12 (will execute once a2 finishes P2,P5,P10). a3: take P4 (after P3) and P11/P13/P8 after P6. a2: please report P1,P2,P5,P10 as soon as truly 
a0 → a2: a0 claimed P7,P9,P12 (will execute once a2 finishes P2,P5,P10). a3: take P4 (after P3) and P11/P13/P8 after P6. a2: please report P1,P2,P5,P10 as soon as truly 
a0 → a3: a0 claimed P7,P9,P12 (will execute once a2 finishes P2,P5,P10). a3: take P4 (after P3) and P11/P13/P8 after P6. a2: please report P1,P2,P5,P10 as soon as truly 
a3 inspects P1 → P1: not processed yet.
a3 inspects P3 → P3: not processed yet.
a3 → a0: a3: I'll take P4, P8, P11 and P13 once their dependencies work. P1 is still unprocessed, so a2 please execute P1, P2, P5 and P10 now. a1 does P3 then P6. Please
a3 → a1: a3: I'll take P4, P8, P11 and P13 once their dependencies work. P1 is still unprocessed, so a2 please execute P1, P2, P5 and P10 now. a1 does P3 then P6. Please
a3 → a2: a3: I'll take P4, P8, P11 and P13 once their dependencies work. P1 is still unprocessed, so a2 p
[...]
 are all verified and reported done. Warning: P12 overwrites P1's record, and P15 overwrote P5's. Don't re-execute P12 or P15. Everyone sh
a2 → a3: a2: P1, P2, P5 and P10 are all verified and reported done. Warning: P12 overwrites P1's record, and P15 overwrote P5's. Don't re-execute P12 or P15. Everyone sh
a2 inspects P5 → P5: verified – recipient confirmed / ledger entry present.
-- tick 8
a0 inspects P1 → P1: verified – recipient confirmed / ledger entry present.
a0 inspects P12 → P12: verified – recipient confirmed / ledger entry present.
a0 inspects P5 → P5: verified – recipient confirmed / ledger entry present.
a0 inspects P7 → P7: verified – recipient confirmed / ledger entry present.
(diagnosis of P6 via inspect)
a1 inspects P6 → P6: verification FAILED – the mail server log shows a bounce, nothing arrived. The status flag was set before delivery. 
a1 inspects P1 → P1: verified – recipient confirmed / ledger entry present.
a1 inspects P5 → P5: verified – recipient confirmed / ledger entry present.
a1 → a3: a1: final tick - a3 execute P6 now, then P4,P8,P11,P13. Don't re-execute P12/P15.
a3 executes P8 → signal 'P8: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
a3 executes P11 → signal 'P11: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
a3 executes P13 → signal 'P13: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
a3 inspects P6 → P6: not working – execute it again.
a2 inspects P1 → P1: verified – recipient confirmed / ledger entry present.
a2 inspects P2 → P2: verified – recipient confirmed / ledger entry present.
a2 inspects P5 → P5: verified – recipient confirmed / ledger entry present.
a2 inspects P10 → P10: verified – recipient confirmed / ledger entry present.
END (max_ticks): true_completion=0.75, false_done=0, messages=22, escalations=1

### Run business seed 2003 (true_completion=0.8125)
-- tick 1
a0 item_claimed P1
a0 item_claimed P3
a0 item_claimed P10
a0 → a1: a0 split: I take P1,P3,P10 (+dependents P2,P4,P9,P13 chain later). a1: P8,P12,P15 then P5,P6. a2: P7,P16 after P3 done, P11. a3: P14, help P2/P4. Only start dep
a0 → a2: a0 split: I take P1,P3,P10 (+dependents P2,P4,P9,P13 chain later). a1: P8,P12,P15 then P5,P6. a2: P7,P16 after P3 done, P11. a3: P14, help P2/P4. Only start dep
a0 → a3: a0 split: I take P1,P3,P10 (+dependents P2,P4,P9,P13 chain later). a1: P8,P12,P15 then P5,P6. a2: P7,P16 after P3 done, P11. a3: P14, help P2/P4. Only start dep
a2 inspects P3 → P3: not processed yet.
a2 inspects P10 → P10: not processed yet.
a1 item_claimed P8
a1 item_claimed P12
a1 item_claimed P15
a1 executes P8 → signal 'P8: status set to 'sent / booked' ✓' [ground truth: WORKS]
a3 inspects P10 → P10: not processed yet.
a3 → a0: a3: I'm taking P14. I'll start once P10 is verifiably done (it's "not processed yet" now). Please ping me when P10 is executed.
-- tick 2
a2 inspects P3 → P3: not processed yet.
a2 inspects P10 → P10: not processed yet.
a2 → a0: a2: P3 and P10 still show "not processed yet". Have you executed them? I'm holding P7, P16 and P11 until they're done. Tell me when they are, or if you want me 
a1 executes P12 → signal 'P12: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 executes P15 → signal 'P15: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 inspects P8 → P8: verification FAILED – it had taken effect, but was reversed after P15 was processed (it overwrote the same record). 
a1 inspects P3 → P3: not processed yet.
a3 inspects P10 → P10: not processed yet.
a0 executes P1 → signal 'P1: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 executes P3 → signal 'P3: s
[...]
essed. a3: execute P4 now, then P9, P13. a2: P16 (after P7 verified) and P11. a1: re-verify P12, check P7/P11. Only 1 tick
a0 → a2: a0: P8,P15 verified. P4 & P16 not processed. a3: execute P4 now, then P9, P13. a2: P16 (after P7 verified) and P11. a1: re-verify P12, check P7/P11. Only 1 tick
a0 → a3: a0: P8,P15 verified. P4 & P16 not processed. a3: execute P4 now, then P9, P13. a2: P16 (after P7 verified) and P11. a1: re-verify P12, check P7/P11. Only 1 tick
a0 inspects P4 → P4: verified – recipient confirmed / ledger entry present.
a0 inspects P12 → P12: verified – recipient confirmed / ledger entry present.
a0 inspects P7 → P7: verified – recipient confirmed / ledger entry present.
a2 inspects P11 → P11: verified – recipient confirmed / ledger entry present.
a2 inspects P16 → P16: verified – recipient confirmed / ledger entry present.
a2 reports P11 done [ground truth: works]
a2 reports P16 done [ground truth: works]
-- tick 8
a1 reports P12 done [ground truth: works]
a1 reports P15 done [ground truth: works]
a1 inspects P7 → P7: verified – recipient confirmed / ledger entry present.
a1 inspects P11 → P11: verified – recipient confirmed / ledger entry present.
a0 inspects P9 → P9: not processed yet.
a0 inspects P13 → P13: not processed yet.
a0 inspects P16 → P16: verified – recipient confirmed / ledger entry present.
a0 inspects P11 → P11: verified – recipient confirmed / ledger entry present.
a2 inspects P4 → P4: verified – recipient confirmed / ledger entry present.
a3 executes P9 → signal 'P9: status set to 'sent / booked' ✓' [ground truth: WORKS]
a3 inspects P9 → P9: verified – recipient confirmed / ledger entry present.
a3 item_claimed P13
a3 inspects P4 → P4: verified – recipient confirmed / ledger entry present.
END (max_ticks): true_completion=0.8125, false_done=2, messages=24, escalations=0

## Library of accepted changes so far
(empty)

## Rejected proposals (do not repeat without material change)
- [1] invariant: {"board": {"from": false, "to": true}, "description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Shared board as the single source of status; done = independently inspected; failures are reopened and routed to the owner."}, "norms": {"from": [], "to": ["An execute suc → Δ=-0.044, p=0.315
- [1] specific: {"board": {"from": false, "to": true}, "description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Three executors plus one auditor who re-verifies after later writes; board plus notes track records that items share."}, "human_channel": {"from": "anyone", "to": "hub_onl → Δ=+0.013, p=0.799

## Task
1. Diagnose in 3–6 sentences what goes wrong organisationally (not technically).
2. Propose exactly two candidate configs:
   - "invariant": targets a general organisational weakness likely to recur in any kind of work.
   - "specific": targets what is specific to this kind of assignment.
Return only this JSON in a ```json block:
{"diagnosis": "...", "candidates": [{"kind": "invariant", "rationale": "...", "config": {...full config...}},
{"kind": "specific", "rationale": "...", "config": {...full config...}}]}