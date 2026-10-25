```json
{
  "diagnosis": "Responsibility for checking work is left unassigned, so it gets duplicated. In both runs several agents inspect the same items: in business tick 8, a1 inspects P10, P11, P13 and P14, all owned by others; in coding ticks 7–8, a1 and a3 both inspect P5, P6, P11 and P13. With only 4 tool calls per tick, this spends scarce attention on work that is already verified. Meanwhile some items owned by others go unexecuted or unverified. In coding, P11 was claimed early by a0, sat blocked, and was executed only in the last tick. In business, a1 reported P2 done in a late batch with no fresh inspect visible, and P2 did not work. A second problem is that 'done' is treated as permanent once said. Agents act on teammates' status messages, and items executed downstream of a failed parent (built_on_phantom = 0.4) are never re-checked after the parent is fixed. The real gaps are who owns verification, when a 'done' expires, and how stuck claims are handed on, rather than any lack of information sharing.",
  "candidates": [
    {
      "kind": "invariant",
      "rationale": "This targets a general failure: no single owner for checking, so effort duplicates while gaps remain. The traces show redundant cross-inspection (a1 inspecting four foreign items in business tick 8; a1 and a3 overlapping in coding) and a blocked claim (P11) that sat idle until the final tick. The change keeps everything else fixed and adds no board, notes or roles, unlike rejected proposals 1, 2 and 4. It only sets three rules: each agent verifies only what it owns, spends its budget on its own pipeline, and releases claims it cannot act on. This applies to any work where effort is scarce and ownership is implicit.",
      "config": {
        "name": "B_single_owner_verification",
        "description": "Full mesh, no roles. Each item has exactly one checker, its owner; do not spend effort re-checking others' work; blocked claims are released, not hoarded.",
        "n_agents": 4,
        "topology": "mesh",
        "board": false,
        "shared_notes": false,
        "human_channel": "anyone",
        "role_mode": "none",
        "roles": [],
        "norms": [
          "The owner of an item is its only verifier. Spend your tool calls in this order: execute your item, then inspect_item it yourself, then report_done in the same tick the inspection passes. Never report done on a success signal alone.",
          "Do not inspect items you do not own unless your own next item depends on them. If you have spare calls, use them to claim and execute unclaimed work, not to re-check teammates.",
          "If you hold a claim you cannot execute this tick because it is blocked or you lack calls, release_item it and tell the team in one message, so an idle agent can take it. Never sit on a blocked claim."
        ],
        "max_ticks": 8,
        "max_tool_calls": 4
      }
    },
    {
      "kind": "specific",
      "rationale": "These assignments have dependency chains and status flags that lie (P1 'sent/booked' bounced; 'process status: online' on items not yet deployed). Items built on a phantom parent remain broken (built_on_phantom = 0.4), and P2 was reported done without a fresh check. The change makes 'done' expire. A dependent item may run only after its owner personally inspects the parent; teammates' messages do not count. Any item executed before its parent was fixed must be re-run. A done report is valid only if a passing inspect happened after the last relevant write. Unlike rejected 4-specific, this does not restructure ownership by chain. Unlike 3-specific, it does not rely on a final-tick sweep. It is a local precondition-and-rerun rule.",
      "config": {
        "name": "B_fresh_done_dependencies",
        "description": "Full mesh, no roles. Dependent work starts only on a parent you inspected yourself; work built on a failed parent is redone; done reports must follow a fresh passing inspection.",
        "n_agents": 4,
        "topology": "mesh",
        "board": false,
        "shared_notes": false,
        "human_channel": "anyone",
        "role_mode": "none",
        "roles": [],
        "norms": [
          "Before executing an item that depends on another, inspect_item the parent yourself. A teammate's message or a success signal is not proof. If the parent is not verified, do other work and do not execute the dependent item.",
          "When you fix a failed item, tell the owners of its dependents in one message. Any dependent executed before the fix must be re-executed and re-inspected by its owner before being reported done.",
          "Report done only if your passing inspect_item came after the last execute of the item and of its parents. If either was re-run since your inspect, inspect again before reporting."
        ],
        "max_ticks": 8,
        "max_tool_calls": 4
      }
    }
  ]
}
```