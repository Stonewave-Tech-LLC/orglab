```json
{
  "diagnosis": "The team's main bottleneck is exclusive ownership combined with slow owners. Agents claim long future chains in tick 1. Once an item fails or is reversed, only the owner can re-execute it. Everyone else then spends scarce actions inspecting the same item and broadcasting the same pleas, while dependents wait (P1 in seed 3003 blocked P2, P3, P7 and P4 until the last tick). Broadcasting to all three peers costs three of the four tool calls per tick, so coordination crowds out execution and repair. 'Done' is reported once and never revisited, so items reversed by later work (P4 by P16, P1 by P12) stay reported done. No one owns the final state of the whole set, so these false-done items and some unprocessed items (P13, P14) survive to the end of the run.",
  "candidates": [
    {
      "kind": "invariant",
      "rationale": "This targets three general failures: (1) owner lock-in and hoarding, (2) coordination that consumes the action budget, and (3) 'done' treated as permanent. It changes structure rather than adding status tooling, which differs from the rejected attempts (board, notes, auditor role). The norms set a duty to respond: a failed item comes before new work, and if the owner cannot fix it this tick they hand it over. Messages go only to the single agent who must act, which frees tool calls for execution. Both final ticks are reserved for re-checking your own done items, which addresses late reversals. These rules apply to any work where pieces interact.",
      "config": {
        "name": "C_handoff_and_final_sweep",
        "description": "Full mesh, no roles. Owners repair or hand off immediately; messages are targeted, not broadcast; done is re-checked at the end.",
        "n_agents": 4,
        "topology": "mesh",
        "board": false,
        "shared_notes": false,
        "human_channel": "anyone",
        "role_mode": "none",
        "roles": [],
        "norms": [
          "Claim only items you will execute within the next tick. Leave later items in a chain unclaimed until their predecessor is verified.",
          "If you learn that an item you own failed or was reversed, fixing it comes before any new work. If you cannot re-execute it this tick, release it at once so someone else can.",
          "Do not broadcast. Send a message only to the one agent who must act on it, and only if they cannot learn it themselves by inspecting. Spend your tool calls on executing and inspecting.",
          "Done is provisional. In the last two ticks, re-inspect every item you reported done. Re-execute anything that was reversed, and take unclaimed items before re-checking anyone else's."
        ],
        "max_ticks": 8,
        "max_tool_calls": 4
      }
    },
    {
      "kind": "specific",
      "rationale": "In business runs the losses come from items that share a record: a later item (P12, P16) overwrites an earlier one (P1, P4). These pairs are owned by different agents, so the repair needs a cross-agent handoff that arrives too late. The rejected specific proposal tried to fix this by ordering execution. This proposal instead puts both items of an overwrite pair under one owner, so the agent who caused the overwrite can repair it within the same tick without negotiation. It also notes that bounced or failed sends are fixed by simply re-executing, and asks for a final verification pass.",
      "config": {
        "name": "C_record_coownership",
        "description": "Full mesh. Items that overwrite each other's records are consolidated under one owner, who repairs reversals immediately; final-tick verification of done items.",
        "n_agents": 4,
        "topology": "mesh",
        "board": false,
        "shared_notes": false,
        "human_channel": "anyone",
        "role_mode": "none",
        "roles": [],
        "norms": [
          "A green status signal after execute is not proof. Inspect before report_done. If inspect says FAILED or not working, simply execute it again, since a bounce or a stale flag is fixed by re-running.",
          "If inspect shows item X was reversed by item Y (they share a record), the owner of X releases X immediately. The owner of Y claims X, re-executes it right after Y, and inspects both. One agent should own both items of a shared record.",
          "Claim only items you can execute this tick or next. Message only the specific agent who must act, never all peers at once.",
          "In the last two ticks, re-inspect every item you reported done. Re-execute any that were reversed, then take any unclaimed or unprocessed items."
        ],
        "max_ticks": 8,
        "max_tool_calls": 4
      }
    }
  ]
}
```