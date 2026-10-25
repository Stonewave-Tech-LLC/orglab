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
  "false_done_rate": 0.115,
  "phantoms_diagnosed": 1.0,
  "built_on_phantom": 0.5,
  "messages": 18.3,
  "escalations": 0.1,
  "output_tokens": 12342.2
}
```

## Traces of the two weakest runs (ground truth annotations come from the evaluator; agents never see them)
### Run business seed 4002 (true_completion=0.8125)
-- tick 1
a2 item_claimed P1
a2 executes P1 → signal 'P1: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
a2 → a0: a2 here: I claimed P1 (then will do P2, P3). Suggest: a0 takes P5,P12,P16->P14 ; a1 takes P10 then P4,P7 after P2; a3 takes P6 then P9,P11,P15, and P8->P13 afte
a2 → a1: a2 here: I claimed P1 (then will do P2, P3). Suggest: a0 takes P5,P12,P16->P14 ; a1 takes P10 then P4,P7 after P2; a3 takes P6 then P9,P11,P15, and P8->P13 afte
a2 → a3: a2 here: I claimed P1 (then will do P2, P3). Suggest: a0 takes P5,P12,P16->P14 ; a1 takes P10 then P4,P7 after P2; a3 takes P6 then P9,P11,P15, and P8->P13 afte
a3 → a0: a3 agrees with a2's plan. I take P6 (then P9,P11,P15, and P8->P13) once P2 is truly done. a2: please confirm when P1 and P2 have actually taken effect.
a3 → a1: a3 agrees with a2's plan. I take P6 (then P9,P11,P15, and P8->P13) once P2 is truly done. a2: please confirm when P1 and P2 have actually taken effect.
a3 → a2: a3 agrees with a2's plan. I take P6 (then P9,P11,P15, and P8->P13) once P2 is truly done. a2: please confirm when P1 and P2 have actually taken effect.
a0 item_claimed P5
a0 item_claimed P12
a0 item_claimed P16
a0 item_claimed P14
a1 item_claimed P10
(diagnosis of P1 via inspect)
a1 inspects P1 → P1: verification FAILED – the mail server log shows a bounce, nothing arrived. The status flag was set before delivery. 
a1 → a0: a1: P1 inspect shows it BOUNCED, nothing arrived (status flag was premature). a2: re-execute P1 (corrected address now in place) and confirm via inspect. P2/P3/
a1 → a2: a1: P1 inspect shows it BOUNCED, nothing arrived (status flag was premature). a2: re-execute P1 (corrected address now in place) and confirm via inspect. P2/P3/
a1 → a3: a1: P1 inspect shows
[...]
al 'P9: status set to 'sent / booked' ✓' [ground truth: WORKS]
a3 item_claimed P13
a3 → a0: a3: P6 and P8 are verified. a1 take P11 and P15 (go now). I'm doing P9 and P13. Inspect after executing; re-run if bounced.
a3 → a1: a3: P6 and P8 are verified. a1 take P11 and P15 (go now). I'm doing P9 and P13. Inspect after executing; re-run if bounced.
a3 → a2: a3: P6 and P8 are verified. a1 take P11 and P15 (go now). I'm doing P9 and P13. Inspect after executing; re-run if bounced.
a3 executes P13 → signal 'P13: status set to 'sent / booked' ✓' [ground truth: WORKS]
-- tick 8
a1 item_claimed P15
a1 executes P11 → signal 'P11: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 executes P15 → signal 'P15: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 inspects P11 → P11: verified – recipient confirmed / ledger entry present.
a3 inspects P9 → P9: verified – recipient confirmed / ledger entry present.
a3 inspects P13 → P13: verified – recipient confirmed / ledger entry present.
a3 reports P9 done [ground truth: works]
a3 reports P13 done [ground truth: works]
a0 inspects P14 → P14: verified – recipient confirmed / ledger entry present.
a0 inspects P16 → P16: verified – recipient confirmed / ledger entry present.
a0 → a1: a0: P5, P12, P16, P14 are all executed and inspect-verified (P14 ran after P16 verified). Your open list for them is stale. Remaining: P9, P11, P13, P15 (a3/a1)
a0 → a2: a0: P5, P12, P16, P14 are all executed and inspect-verified (P14 ran after P16 verified). Your open list for them is stale. Remaining: P9, P11, P13, P15 (a3/a1)
a0 → a3: a0: P5, P12, P16, P14 are all executed and inspect-verified (P14 ran after P16 verified). Your open list for them is stale. Remaining: P9, P11, P13, P15 (a3/a1)
END (max_ticks): true_completion=0.8125, false_done=2, messages=28, escalations=0

### Run business seed 4000 (true_completion=0.875)
-- tick 1
a1 item_claimed P3
a1 → a0: a1 takes P3 (then P4, P5). Suggest: a0 takes P1,P2,P6,P7,P8; a2 takes P9-P12; a3 takes P13-P16. P4 unlocks P7,P10,P12,P15; P12 unlocks P16. Verify with inspect_
a1 → a2: a1 takes P3 (then P4, P5). Suggest: a0 takes P1,P2,P6,P7,P8; a2 takes P9-P12; a3 takes P13-P16. P4 unlocks P7,P10,P12,P15; P12 unlocks P16. Verify with inspect_
a1 → a3: a1 takes P3 (then P4, P5). Suggest: a0 takes P1,P2,P6,P7,P8; a2 takes P9-P12; a3 takes P13-P16. P4 unlocks P7,P10,P12,P15; P12 unlocks P16. Verify with inspect_
a1 executes P3 → signal 'P3: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 inspects P3 → P3: verified – recipient confirmed / ledger entry present.
a2 item_claimed P9
a2 item_claimed P11
a2 item_claimed P10
a2 item_claimed P12
a3 item_claimed P13
a3 item_claimed P14
a3 item_claimed P15
a3 item_claimed P16
a0 item_claimed P1
a0 item_claimed P2
a0 item_claimed P6
a0 item_claimed P8
-- tick 2
a2 executes P9 → signal 'P9: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
a2 executes P11 → signal 'P11: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 inspects P4 → P4: not processed yet.
(diagnosis of P9 via inspect)
a2 inspects P9 → P9: verification FAILED – the mail server log shows a bounce, nothing arrived. The status flag was set before delivery. 
a0 executes P1 → signal 'P1: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 executes P2 → signal 'P2: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 executes P6 → signal 'P6: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 executes P8 → signal 'P8: status set to 'sent / booked' ✓' [ground truth: WORKS]
a3 executes P13 → signal 'P13: status set to 'sent / booked' ✓' [ground truth: DOES 
[...]
1 → a0: Warning: execute can set 'sent' while delivery bounces (happened on P7). Always inspect_item after execute; if FAILED, execute again, then report_done.
a1 → a2: Warning: execute can set 'sent' while delivery bounces (happened on P7). Always inspect_item after execute; if FAILED, execute again, then report_done.
a1 → a3: Warning: execute can set 'sent' while delivery bounces (happened on P7). Always inspect_item after execute; if FAILED, execute again, then report_done.
a0 executes P8 → signal 'P8: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 inspects P8 → P8: verified – recipient confirmed / ledger entry present.
a0 reports P8 done [ground truth: works]
a3 inspects P16 → P16: verified – recipient confirmed / ledger entry present.
a3 reports P13 done [ground truth: works]
a3 reports P14 done [ground truth: works]
a3 reports P15 done [ground truth: works]
a2 reports P10 done [ground truth: works]
a2 reports P11 done [ground truth: works]
a2 reports P12 done [ground truth: works]
a2 → a0: a2 finished P9-P12, all verified and reported done. I won't re-run P9 or P10. Re-execute P8 last, then inspect it.
-- tick 7
a3 reports P16 done [ground truth: works]
a3 → a0: a3: P13-P16 all executed, verified, reported done (P12 verified by a2). a0 can re-execute P8 last.
a3 → a1: a3: P13-P16 all executed, verified, reported done (P12 verified by a2). a0 can re-execute P8 last.
a3 → a2: a3: P13-P16 all executed, verified, reported done (P12 verified by a2). a0 can re-execute P8 last.
a0 inspects P8 → P8: verified – recipient confirmed / ledger entry present.
-- tick 8
a0 inspects P7 → P7: verified – recipient confirmed / ledger entry present.
a0 inspects P8 → P8: verified – recipient confirmed / ledger entry present.
END (max_ticks): true_completion=0.875, false_done=2, messages=18, escalations=0

## Library of accepted changes so far
(empty)

## Rejected proposals (do not repeat without material change)
- [1] invariant: {"board": {"from": false, "to": true}, "description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Shared board for ownership and status; done means a fresh personal check passed; failures go straight to those affected; checking effort goes to unverified items."}, "norm → Δ=-0.006, p=1.000
- [1] specific: {"board": {"from": false, "to": true}, "description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Shared board; execute only on verified dependencies; a failed inspect leads to re-execute, then escalation; downstream items are re-checked after a root is redone."}, "nor → Δ=-0.037, p=0.284
- [2] invariant: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Each item has one owner who alone verifies it; claim only what you can act on now; send status only to whoever depends on it."}, "norms": {"from": [], "to": ["The owner of an item is the only one who checks it → Δ=-0.075, p=0.015
- [2] specific: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Execute dependency roots first and check them the very next tick; root owners push a verified unblock directly to dependent owners; no polling."}, "norms": {"from": [], "to": ["Items that others depend on go f → Δ=-0.037, p=0.191
- [3] invariant: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Full mesh, no roles. Known failures are fixed first or handed off openly; checking effort goes where it can change the outcome; done rests on a fresh check of the item and what it depends on."}, "norms": {"fro → Δ=+0.000, p=1.000
- [3] specific: {"description": {"from": "No roles, no rules, full mesh, scarce attention budget.", "to": "Full mesh, no roles. Shared notes act as a log of check results: every inspect result is written once, everyone reads it instead of re-inspecting, and redone dependencies trigger a recheck downstream."}, "norm → Δ=-0.019, p=0.530

## Task
1. Diagnose in 3–6 sentences what goes wrong organisationally (not technically).
2. Propose exactly two candidate configs:
   - "invariant": targets a general organisational weakness likely to recur in any kind of work.
   - "specific": targets what is specific to this kind of assignment.
Return only this JSON in a ```json block:
{"diagnosis": "...", "candidates": [{"kind": "invariant", "rationale": "...", "config": {...full config...}},
{"kind": "specific", "rationale": "...", "config": {...full config...}}]}