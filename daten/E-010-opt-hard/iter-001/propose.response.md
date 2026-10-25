```json
{
  "diagnosis": "Each agent confirms an item once, right after executing it. Nobody owns the question of whether the whole set still works once all execution has stopped. In seed 1000 an item that had already passed inspection (P5) was later undone by another item (P12). That run only got away with it because someone happened to re-check. In seed 1002 the run ended with 2 false 'done' reports. The final inspections covered only a few items, and the agents simply stopped. Nobody ran a full re-check after the last execution. Without a shared view of status, agents broadcast long 'who has done what' messages (27 messages in the weak run vs 14). Dependent items were claimed and worked on before the item they relied on had been fixed (built_on_phantom 0.4). Failures were found, but news of them reached people unevenly and late.",
  "candidates": [
    {
      "kind": "invariant",
      "rationale": "This targets a general weakness: checks happen per item and only at the time the work is done, with no shared state and no final check of everything together. A board gives everyone the same status view, which should replace the broadcast messages. A single 'final sweep' rule stops the team from going quiet while items are stale, and that holds for any kind of work where later changes can break earlier ones. A second rule makes a discovered failure visible to everyone at once and blocks work that depends on it. The rule set is kept to two to protect agents' attention.",
      "config": {
        "name": "I_board_final_sweep",
        "description": "Full mesh with a shared board. Items count as done only once inspected, and the team finishes only after a full re-inspection following the last execution.",
        "n_agents": 4,
        "topology": "mesh",
        "board": true,
        "shared_notes": false,
        "human_channel": "anyone",
        "role_mode": "none",
        "roles": [],
        "norms": [
          "An execute signal is not evidence. Only report_done after inspect_item confirms the item works. If an inspection fails, tell the item's owner and everyone working on items that depend on it right away, and don't build on that item until it re-inspects as working.",
          "Later work can break earlier work. Before you stop, check the board. If any item was executed after another item was last verified, re-inspect every done item and fix and re-report any that fail. The team is finished only when one full inspection pass with no executions after it shows every item verified."
        ],
        "max_ticks": 10,
        "max_tool_calls": 8
      }
    },
    {
      "kind": "specific",
      "rationale": "This targets what is specific to these assignments. Status flags like 'sent / booked ✓' are set before delivery. Items depend on one another. Items that share a record can overwrite each other, as P12 did to P5. Making one agent a dedicated auditor gives a single clear owner for checking across items and for the end-of-run sweep. The executors run dependencies first, and the auditor keeps re-inspecting as new executions land, so overwrites are caught before the run goes quiet. The board lets the auditor see what changed without anyone broadcasting status.",
      "config": {
        "name": "S_executors_plus_auditor",
        "description": "Three executors plus one auditor who owns ongoing and final verification across items, using a shared board.",
        "n_agents": 4,
        "topology": "mesh",
        "board": true,
        "shared_notes": false,
        "human_channel": "anyone",
        "role_mode": "fixed",
        "roles": [
          {"name": "executor", "mandate": "Claim, execute and inspect your items. Do dependencies first, and start a dependent item only after its prerequisites inspect as verified. Report done only after a successful inspection. Re-execute any item of yours the auditor flags."},
          {"name": "executor", "mandate": "Claim, execute and inspect your items. Do dependencies first, and start a dependent item only after its prerequisites inspect as verified. Report done only after a successful inspection. Re-execute any item of yours the auditor flags."},
          {"name": "executor", "mandate": "Claim, execute and inspect your items. Do dependencies first, and start a dependent item only after its prerequisites inspect as verified. Report done only after a successful inspection. Re-execute any item of yours the auditor flags."},
          {"name": "auditor", "mandate": "Don't execute unless an item is left without an owner. Each tick, re-inspect items reported done, giving priority to items that share a record with, or depend on, anything executed since their last check. Tell the owner and the owners of dependent items about each failure. Before the team stops, run a full inspection pass after the last execution, and only declare the work finished if every item verifies."}
        ],
        "norms": [
          "Status flags such as 'sent / booked ✓' are set before delivery and prove nothing. Only inspect_item counts. An item that verified earlier can be undone by a later item that touches the same record, so a check is only valid if no execution came after it."
        ],
        "max_ticks": 10,
        "max_tool_calls": 8
      }
    }
  ]
}
```