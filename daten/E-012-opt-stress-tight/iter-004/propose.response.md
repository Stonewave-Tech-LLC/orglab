```json
{
  "diagnosis": "The basic flow works: agents inspect their items and spot failed deliveries (phantoms_diagnosed = 1.0). Things go wrong after that, in coordination. 1) Plans are proposed by whoever speaks first and get overwritten repeatedly, so nobody holds the true picture of who owns what is still open. In seed 4002, a0 tells the others their lists are stale. In seed 4000, a2 tells a0 to re-execute P8, which had already been verified, and says it 'won't re-run P9' even though P9 had failed. 2) A failure is often found by someone who doesn't own the item, as when a1 found the P1 bounce. They broadcast it with a request, but no one confirms they are taking the fix, so the item drifts until the run ends. 3) On a mesh, every status update goes to all three teammates, using up to three of the four calls an agent gets per tick. That leaves less room for the execute → inspect → re-execute cycle, so both weak runs ran out of ticks with false dones and work built on failed items still in place. 4) Nothing protects the last ticks. Agents keep sending coordination messages at tick 8 instead of re-checking items that were executed but never verified.",
  "candidates": [
    {
      "kind": "invariant",
      "rationale": "This is a structural fix, not more rules, and it doesn't revisit any rejected idea. The board, owner-only checking, notes logs and 'fix known failures first' have all been tried; star topology and roles have not. Under a star with a0 as coordinator there is one source of truth for who owns what: workers send one message to the hub instead of copying three teammates, which saves their calls for execute and inspect. The hub's single job is to make sure every known failure has exactly one named fixer who has confirmed taking it. That gap appears in both traces (P1 in 4002, P9 in 4000). This weakness (competing plans, no one holding failures, broadcast overhead) shows up in any multi-agent work, not just this domain. Both norms are general: one defines done using fresh evidence, the other sets how failures are handed off.",
      "config": {
        "name": "star_coordinator",
        "description": "Star with a0 as coordinator who holds the single view of ownership and open failures; workers execute, check and report their own items and talk only to the hub.",
        "n_agents": 4,
        "topology": "star",
        "board": false,
        "shared_notes": false,
        "human_channel": "hub_only",
        "role_mode": "fixed",
        "roles": [
          {
            "name": "coordinator",
            "mandate": "Hand out items once at the start, with dependency roots first. Keep the only authoritative list of who owns what is still open. When a failure is reported, name exactly one fixer and get their confirmation. Use spare calls to do items yourself, not to repeat status. Escalate to the human only for something no one on the team can fix."
          },
          {
            "name": "worker",
            "mandate": "Do your assigned items yourself: execute, inspect, and report done. Send the coordinator one short message per tick, and only when something changed: an item verified, an item failed, or you are free for more work."
          }
        ],
        "norms": [
          "An item is done only if its most recent inspect, made after its most recent execute, says it works. A success message from execute is not evidence that it works.",
          "If you find a problem in someone else's item, tell the coordinator once, with the evidence. Only the fixer the coordinator names acts on it, and that fixer confirms when it is checked and working."
        ]
      },
      "max_ticks": 8,
      "max_tool_calls": 4
    },
    {
      "kind": "specific",
      "rationale": "This targets the specific setup in this domain. The execute signal ('status set to sent') says nothing about whether delivery actually happened, re-executing fixes a bounce, items depend on each other, and the budget is 4 calls per tick over 8 ticks. Unlike the rejected proposals (which used a board, notes, roots-first ordering or owner-only checking), this is about how a tick is spent. Each item gets an execute → inspect → report cycle inside one tick, so no false done slips through between ticks. Messages are limited to one per tick, sent to the one agent whose next action changes, which cuts the broadcast cost seen in the traces. Dependent items wait for a 'verified' message from the root's owner, which targets built_on_phantom = 0.5. The last two ticks are reserved for a sweep, because both weak runs ended with failed items still sitting unverified at max_ticks.",
      "config": {
        "name": "tight_cycle_endgame",
        "description": "Full mesh, no roles. Each item's execute, inspect and report happen in one tick; messaging is kept to a minimum; dependents wait for a verified root; the last two ticks are a verification sweep.",
        "n_agents": 4,
        "topology": "mesh",
        "board": false,
        "shared_notes": false,
        "human_channel": "anyone",
        "role_mode": "none",
        "roles": [],
        "norms": [
          "Handle an item in one tick: execute, then inspect it right away, then report done if it is verified. If the inspect fails, re-execute and inspect again before touching anything else.",
          "Send at most one message per tick, to the one agent whose next action it changes (an unblock, a failure in their item, a handover). Never copy everyone on status updates.",
          "Execute an item that depends on another only after that item's owner has told you its inspect says verified.",
          "From tick 7 on, don't claim new items. Spend your calls inspecting items you executed that aren't verified yet, and re-executing the ones that failed."
        ]
      },
      "max_ticks": 8,
      "max_tool_calls": 4
    }
  ]
}
```