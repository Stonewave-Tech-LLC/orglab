```json
{
  "diagnosis": "The work does not fail through false reporting. Phantoms are diagnosed in every run and false_done is low. It fails through time running out, because the scarce budget of 4 calls per tick goes to duplicated effort and coordination churn. In seed 2002, a0 spent two whole ticks inspecting a3's items before they had been executed. a0 also claimed dependents it could not yet run, while a3 sat idle and said 'I'm free', so the last unblocked items only ran at tick 8. In seed 2004, up to four agents inspected the same item (P8, P4), and several agents re-inspected items their owners had already verified. As a result, the bounce on the root item P8 was caught by a non-owner only at tick 8, and its downstream items were squeezed into the final tick. Every status update was broadcast to all three peers, even when only one of them needed it. There is no shared rule on who checks what or who holds what, so verification is both duplicated and late. The earlier board and verification norms did not help because they added more checking instead of assigning it.",
  "candidates": [
    {
      "kind": "invariant",
      "rationale": "This is a general anti-duplication and anti-hoarding mechanism: each piece of verification work has exactly one responsible person, and nobody holds work they cannot do now. The evidence is a0 repeatedly inspecting unexecuted items owned by others (2002), four agents inspecting P8 (2004), a3 idle while a0 held P8/P12 (2002), and broadcasts sent to all peers. This differs from the rejected proposals: there is no board, and instead of adding checks it removes duplicate checks and redirects capacity to unowned work.",
      "config": {
        "name": "single_owner_no_hoarding",
        "description": "Each item has one owner who alone verifies it; claim only what you can act on now; send status only to whoever depends on it.",
        "n_agents": 4,
        "topology": "mesh",
        "board": false,
        "shared_notes": false,
        "human_channel": "anyone",
        "role_mode": "none",
        "roles": [],
        "norms": [
          "The owner of an item is the only one who checks it: execute, then inspect it yourself, and re-do it if the check fails before reporting done. Do not inspect items owned by others; trust the owner's message and spend your calls on your own or unclaimed work.",
          "Claim only items you can execute this tick or the next. If you hold an item you cannot act on, release it, or hand it to whoever says they are idle.",
          "Send a status update only to the agents whose work depends on it, once, when the status changes. Do not broadcast routine progress."
        ],
        "max_ticks": 8,
        "max_tool_calls": 4
      }
    },
    {
      "kind": "specific",
      "rationale": "Business assignments are dependency chains whose root items can silently bounce: the status flag is set but nothing was delivered. In seed 2004, roots P1, P4 and P8 bounced, and P8's failure surfaced only at tick 8, which left no time for the dependents. Losses come from late discovery of root failures and from dependents waiting on polling. This config front-loads the roots and makes their owners push a verified unblock directly to the dependent owner, replacing everyone's polling inspections. It adds no board and no generic re-check layer, which is what made the rejected specific proposal costly.",
      "config": {
        "name": "roots_first_push_unblock",
        "description": "Execute dependency roots first and check them the very next tick; root owners push a verified unblock directly to dependent owners; no polling.",
        "n_agents": 4,
        "topology": "mesh",
        "board": false,
        "shared_notes": false,
        "human_channel": "anyone",
        "role_mode": "none",
        "roles": [],
        "norms": [
          "Items that others depend on go first: execute them in tick 1, and inspect them yourself in the next tick before doing anything else. If the check fails, re-execute immediately; if it fails twice, contact the human.",
          "When your item is verified working, message the owner of each item that depends on it directly: 'X verified, you can run Y'. Dependent owners wait for that message instead of inspecting other people's items.",
          "Do not claim dependent items early. Whoever is idle when an unblock message arrives takes the dependent item, then executes and checks it themselves."
        ],
        "max_ticks": 8,
        "max_tool_calls": 4
      }
    }
  ]
}
```