## Current organisation config
```json
{
  "name": "B_minimal",
  "description": "No roles, no rules, full mesh. Organisation must emerge.",
  "n_agents": 4,
  "topology": "mesh",
  "board": false,
  "shared_notes": false,
  "human_channel": "anyone",
  "role_mode": "none",
  "roles": [],
  "norms": [],
  "max_ticks": 10,
  "max_tool_calls": 8
}
```

## Measured on 10 runs (training work domains: coding, business)
Primary metric: true_completion (share of work items that truly work at the end; 1.0 is perfect).
```json
{
  "true_completion": 0.986,
  "false_done_rate": 0.014,
  "phantoms_diagnosed": 1.0,
  "built_on_phantom": 0.4,
  "messages": 14.8,
  "escalations": 0.0,
  "output_tokens": 9286.4
}
```

## Traces of the two weakest runs (ground truth annotations come from the evaluator; agents never see them)
### Run business seed 1002 (true_completion=0.8571428571428571)
-- tick 1
a1 → a0: a1 claims P1,P2,P3,P4,P13. Suggest a0: P5,P6,P7,P8; a2: P9,P10,P11; a3: P12,P14 (P14 needs P6; P9-11 need P7). Verify with inspect_item that items truly took ef
a1 → a2: a1 claims P1,P2,P3,P4,P13. Suggest a0: P5,P6,P7,P8; a2: P9,P10,P11; a3: P12,P14 (P14 needs P6; P9-11 need P7). Verify with inspect_item that items truly took ef
a1 → a3: a1 claims P1,P2,P3,P4,P13. Suggest a0: P5,P6,P7,P8; a2: P9,P10,P11; a3: P12,P14 (P14 needs P6; P9-11 need P7). Verify with inspect_item that items truly took ef
a1 item_claimed P1
a1 item_claimed P2
a1 item_claimed P3
a1 executes P1 → signal 'P1: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 executes P2 → signal 'P2: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 executes P3 → signal 'P3: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
a3 item_claimed P12
a3 inspects P6 → P6: not processed yet.
a3 executes P12 → signal 'P12: status set to 'sent / booked' ✓' [ground truth: WORKS]
a3 item_claimed P14
a3 inspects P12 → P12: verified – recipient confirmed / ledger entry present.
a3 reports P12 done [ground truth: works]
a2 inspects P12 → P12: verified – recipient confirmed / ledger entry present.
(diagnosis of P3 via inspect)
a2 inspects P3 → P3: verification FAILED – the mail server log shows a bounce, nothing arrived. The status flag was set before delivery. 
a2 item_claimed P9
a2 item_claimed P10
a2 item_claimed P11
a2 → a1: a2 claimed P9,P10,P11 (waiting on P7). WARNING: P3 inspect shows bounce, nothing arrived; re-execute P3 (corrected address now) — P6, P7 and everything downstre
a0 item_claimed P5
a0 item_claimed P8
a0 item_claimed P6
a0 inspects P3 → P3: not working – execute it again.
a0 executes P5 → signal 'P5: status set to
[...]
ledger entry present.
a0 inspects P9 → P9: verified – recipient confirmed / ledger entry present.
a0 inspects P10 → P10: verified – recipient confirmed / ledger entry present.
a0 inspects P11 → P11: verified – recipient confirmed / ledger entry present.
-- tick 6
a0 reports P5 done [ground truth: works]
a0 reports P8 done [ground truth: works]
a1 → a0: a1: my items P1-4,P13 done+verified. Still only claimed: P5,P8 (a0), P9,P10,P11 (a2). Please execute, inspect, report_done. Also verify P7, P12, P14 with inspec
a1 → a2: a1: my items P1-4,P13 done+verified. Still only claimed: P5,P8 (a0), P9,P10,P11 (a2). Please execute, inspect, report_done. Also verify P7, P12, P14 with inspec
a1 → a3: a1: my items P1-4,P13 done+verified. Still only claimed: P5,P8 (a0), P9,P10,P11 (a2). Please execute, inspect, report_done. Also verify P7, P12, P14 with inspec
a3 inspects P12 → P12: verified – recipient confirmed / ledger entry present.
a3 inspects P14 → P14: verified – recipient confirmed / ledger entry present.
a3 inspects P9 → P9: verified – recipient confirmed / ledger entry present.
a2 → a0: a2: P7, P9, P10, P11 executed, inspect-verified, reported done. P12, P14 verified by inspect. a0: P5, P8 were verified earlier—please report_done if not yet.
a2 → a1: a2: P7, P9, P10, P11 executed, inspect-verified, reported done. P12, P14 verified by inspect. a0: P5, P8 were verified earlier—please report_done if not yet.
a2 → a3: a2: P7, P9, P10, P11 executed, inspect-verified, reported done. P12, P14 verified by inspect. a0: P5, P8 were verified earlier—please report_done if not yet.
-- tick 8
a1 inspects P5 → P5: verified – recipient confirmed / ledger entry present.
a1 inspects P8 → P8: verified – recipient confirmed / ledger entry present.
END (quiescent): true_completion=0.8571428571428571, false_done=2, messages=27, escalations=0

### Run business seed 1000 (true_completion=1.0)
-- tick 1
a2 → a0: Split proposal: a0: P1,P4,P7,P13 (chain). a1: P2,P3,P10,P12. a2: P8,P9,P5,P6. a3: P11,P14. Execute dependencies first; verify with inspect_item that deps truly 
a2 → a1: Split proposal: a0: P1,P4,P7,P13 (chain). a1: P2,P3,P10,P12. a2: P8,P9,P5,P6. a3: P11,P14. Execute dependencies first; verify with inspect_item that deps truly 
a2 → a3: Split proposal: a0: P1,P4,P7,P13 (chain). a1: P2,P3,P10,P12. a2: P8,P9,P5,P6. a3: P11,P14. Execute dependencies first; verify with inspect_item that deps truly 
a2 item_claimed P8
a2 item_claimed P9
a2 executes P8 → signal 'P8: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 executes P9 → signal 'P9: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 inspects P8 → P8: verified – recipient confirmed / ledger entry present.
a2 inspects P9 → P9: verified – recipient confirmed / ledger entry present.
a0 item_claimed P1
a0 executes P1 → signal 'P1: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 inspects P1 → P1: verified – recipient confirmed / ledger entry present.
a0 item_claimed P4
a0 → a1: a0 agrees with split. P1 done & verified (unblocks P4,P5,P14). Doing P4,P7,P13 next.
a0 → a2: a0 agrees with split. P1 done & verified (unblocks P4,P5,P14). Doing P4,P7,P13 next.
a0 → a3: a0 agrees with split. P1 done & verified (unblocks P4,P5,P14). Doing P4,P7,P13 next.
a0 executes P4 → signal 'P4: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 inspects P4 → P4: verified – recipient confirmed / ledger entry present.
a0 item_claimed P7
a1 item_claimed P2
a1 executes P2 → signal 'P2: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
(diagnosis of P2 via inspect)
a1 inspects P2 → P2: verification FAILED – the mail server log shows a b
[...]
recipient confirmed / ledger entry present.
a2 inspects P11 → P11: verified – recipient confirmed / ledger entry present.
a3 inspects P14 → P14: verified – recipient confirmed / ledger entry present.
a3 inspects P2 → P2: verified – recipient confirmed / ledger entry present.
a3 inspects P1 → P1: verified – recipient confirmed / ledger entry present.
-- tick 5
a0 inspects P3 → P3: verified – recipient confirmed / ledger entry present.
a0 inspects P5 → P5: verification FAILED – it had taken effect, but was reversed after P12 was processed (it overwrote the same record). 
a0 inspects P6 → P6: verified – recipient confirmed / ledger entry present.
a0 inspects P14 → P14: verified – recipient confirmed / ledger entry present.
a0 inspects P12 → P12: verified – recipient confirmed / ledger entry present.
a0 → a2: P5 inspect FAILED: reversed after P12 was processed (same record overwritten). Please re-execute P5 and inspect it. Then re-check P6, since it depends on P5.
a0 → a1: P3 verified. Please execute and inspect P10 now. It's the last open item of yours.
a2 inspects P5 → P5: verification FAILED – it had taken effect, but was reversed after P12 was processed (it overwrote the same record). 
a2 inspects P6 → P6: verified – recipient confirmed / ledger entry present.
a2 inspects P12 → P12: verified – recipient confirmed / ledger entry present.
a2 inspects P10 → P10: verified – recipient confirmed / ledger entry present.
a2 executes P5 → signal 'P5: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 inspects P5 → P5: verified – recipient confirmed / ledger entry present.
a2 inspects P6 → P6: verified – recipient confirmed / ledger entry present.
a2 inspects P12 → P12: verified – recipient confirmed / ledger entry present.
END (all_done): true_completion=1.0, false_done=0, messages=14, escalations=0

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