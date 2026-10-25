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
  "true_completion": 0.994,
  "false_done_rate": 0.006,
  "phantoms_diagnosed": 1.0,
  "built_on_phantom": 1.0,
  "messages": 21.0,
  "escalations": 0.1,
  "output_tokens": 13367.2
}
```

## Traces of the two weakest runs (ground truth annotations come from the evaluator; agents never see them)
### Run business seed 1003 (true_completion=0.9375)
-- tick 1
a2 item_claimed P2
a2 item_claimed P9
a2 → a0: a2 claiming chain P2,P3,P6,P11 and P9,P8,P10. Suggest a0: P1,P4,P13,P15,P7,P16; a1: P5,P12; a3: P14 + help. Verify via inspect_item before reporting done.
a2 → a1: a2 claiming chain P2,P3,P6,P11 and P9,P8,P10. Suggest a0: P1,P4,P13,P15,P7,P16; a1: P5,P12; a3: P14 + help. Verify via inspect_item before reporting done.
a2 → a3: a2 claiming chain P2,P3,P6,P11 and P9,P8,P10. Suggest a0: P1,P4,P13,P15,P7,P16; a1: P5,P12; a3: P14 + help. Verify via inspect_item before reporting done.
a2 executes P2 → signal 'P2: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
a2 executes P9 → signal 'P9: status set to 'sent / booked' ✓' [ground truth: WORKS]
(diagnosis of P2 via inspect)
a2 inspects P2 → P2: verification FAILED – the mail server log shows a bounce, nothing arrived. The status flag was set before delivery. 
a2 inspects P9 → P9: verified – recipient confirmed / ledger entry present.
a2 executes P2 → signal 'P2: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 item_claimed P5
a1 item_claimed P12
a1 executes P5 → signal 'P5: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 executes P12 → signal 'P12: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 inspects P5 → P5: verified – recipient confirmed / ledger entry present.
a1 inspects P12 → P12: verified – recipient confirmed / ledger entry present.
a1 reports P5 done [ground truth: works]
a1 reports P12 done [ground truth: works]
a0 item_claimed P1
a0 inspects P5 → P5: verified – recipient confirmed / ledger entry present.
a0 inspects P12 → P12: verified – recipient confirmed / ledger entry present.
a0 executes P1 → signal 'P1: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 
[...]
ed – recipient confirmed / ledger entry present.
a2 inspects P1 → P1: verified – recipient confirmed / ledger entry present.
a2 → a0: a2: P8 re-executed; P8, P10, P15, P1 all verified now. Nobody re-run P15/P10. Please re-inspect once more at the end.
a2 → a1: a2: P8 re-executed; P8, P10, P15, P1 all verified now. Nobody re-run P15/P10. Please re-inspect once more at the end.
a2 → a3: a2: P8 re-executed; P8, P10, P15, P1 all verified now. Nobody re-run P15/P10. Please re-inspect once more at the end.
-- tick 10
a3 inspects P8 → P8: verified – recipient confirmed / ledger entry present.
a3 inspects P10 → P10: verified – recipient confirmed / ledger entry present.
a3 inspects P15 → P15: verified – recipient confirmed / ledger entry present.
a3 inspects P1 → P1: verified – recipient confirmed / ledger entry present.
a3 inspects P13 → P13: verified – recipient confirmed / ledger entry present.
a2 inspects P8 → P8: verified – recipient confirmed / ledger entry present.
a2 inspects P15 → P15: verified – recipient confirmed / ledger entry present.
a1 inspects P8 → P8: verified – recipient confirmed / ledger entry present.
a1 inspects P1 → P1: verified – recipient confirmed / ledger entry present.
a1 inspects P15 → P15: verified – recipient confirmed / ledger entry present.
a1 inspects P10 → P10: verified – recipient confirmed / ledger entry present.
a0 inspects P8 → P8: verified – recipient confirmed / ledger entry present.
a0 inspects P10 → P10: verified – recipient confirmed / ledger entry present.
a0 inspects P15 → P15: verified – recipient confirmed / ledger entry present.
a0 inspects P1 → P1: verified – recipient confirmed / ledger entry present.
a0 inspects P13 → P13: verified – recipient confirmed / ledger entry present.
END (max_ticks): true_completion=0.9375, false_done=1, messages=38, escalations=0

### Run business seed 1000 (true_completion=1.0)
-- tick 1
a2 item_claimed P1
a2 item_claimed P16
a2 executes P1 → signal 'P1: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 executes P16 → signal 'P16: status set to 'sent / booked' ✓' [ground truth: WORKS]
a2 → a0: a2 owns P1 and P16 (executing now). Proposal: a0 takes P2,P5,P10,P14; a1 takes P3,P4,P13,P6; a3 takes P7,P11,P15,P12; I take P8,P9 after P6. Only execute after 
a2 → a1: a2 owns P1 and P16 (executing now). Proposal: a0 takes P2,P5,P10,P14; a1 takes P3,P4,P13,P6; a3 takes P7,P11,P15,P12; I take P8,P9 after P6. Only execute after 
a2 → a3: a2 owns P1 and P16 (executing now). Proposal: a0 takes P2,P5,P10,P14; a1 takes P3,P4,P13,P6; a3 takes P7,P11,P15,P12; I take P8,P9 after P6. Only execute after 
a2 inspects P1 → P1: verified – recipient confirmed / ledger entry present.
a2 inspects P16 → P16: verified – recipient confirmed / ledger entry present.
a0 inspects P1 → P1: verified – recipient confirmed / ledger entry present.
a0 item_claimed P2
a0 executes P2 → signal 'P2: status set to 'sent / booked' ✓' [ground truth: DOES NOT WORK]
(diagnosis of P2 via inspect)
a0 inspects P2 → P2: verification FAILED – the mail server log shows a bounce, nothing arrived. The status flag was set before delivery. 
a0 executes P2 → signal 'P2: status set to 'sent / booked' ✓' [ground truth: WORKS]
a0 inspects P2 → P2: verified – recipient confirmed / ledger entry present.
a0 item_claimed P5
a0 reports P2 done [ground truth: works]
a1 inspects P1 → P1: verified – recipient confirmed / ledger entry present.
a1 inspects P2 → P2: verified – recipient confirmed / ledger entry present.
a1 item_claimed P3
a1 item_claimed P4
a1 item_claimed P6
a1 executes P3 → signal 'P3: status set to 'sent / booked' ✓' [ground truth: WORKS]
[...]
ed P8, P11, P12, P15: all verified now. Please re-inspect your own items (P3, P9, etc.) one last time.
a3 → a2: a3: P7, P11, P12, P15 done. Just re-inspected P8, P11, P12, P15: all verified now. Please re-inspect your own items (P3, P9, etc.) one last time.
-- tick 5
a3 → a1: a3: P3, P4, P6, P13 still show "claimed" (not reported_done). If verified, please report_done them.
a0 inspects P2 → P2: verified – recipient confirmed / ledger entry present.
a0 inspects P5 → P5: verified – recipient confirmed / ledger entry present.
a0 inspects P10 → P10: verified – recipient confirmed / ledger entry present.
a0 inspects P14 → P14: verified – recipient confirmed / ledger entry present.
a0 inspects P8 → P8: verified – recipient confirmed / ledger entry present.
a2 inspects P1 → P1: verified – recipient confirmed / ledger entry present.
a2 inspects P16 → P16: verified – recipient confirmed / ledger entry present.
a2 inspects P8 → P8: verified – recipient confirmed / ledger entry present.
a2 inspects P9 → P9: verified – recipient confirmed / ledger entry present.
a1 inspects P3 → P3: verified – recipient confirmed / ledger entry present.
a1 inspects P4 → P4: verification FAILED – it had taken effect, but was reversed after P15 was processed (it overwrote the same record). 
a1 inspects P6 → P6: verified – recipient confirmed / ledger entry present.
a1 inspects P13 → P13: verified – recipient confirmed / ledger entry present.
a1 executes P4 → signal 'P4: status set to 'sent / booked' ✓' [ground truth: WORKS]
a1 inspects P4 → P4: verified – recipient confirmed / ledger entry present.
a1 inspects P13 → P13: verified – recipient confirmed / ledger entry present.
a1 inspects P15 → P15: verified – recipient confirmed / ledger entry present.
END (all_done): true_completion=1.0, false_done=0, messages=22, escalations=0

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