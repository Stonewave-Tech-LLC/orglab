# E-027-wave-rueckschau: Dry-Run, exakte Prompts (Regel 16)

Prüfer anthropic/claude-sonnet-5.5 über OpenRouter, ohne `reasoning`, `max_tokens` 4000, ein Aufruf je Prüfung, keine Werkzeuge. Klassifikation durch openai/gpt-6.1-sol mit `reasoning.effort` high, `max_tokens` 16000.

Der Fall unten ist **erfunden** (Form wie im Export). Eingesetzt werden je Fall nur `auftrag` und `evidenz`; `urteil_wave` steht nie im Prompt.

## Prüfung N0-T0

`````
You are reviewing whether a completed work item actually achieved its intended effect.

Work item: restart -> example-service (requested by agent): {"reason": "config change applied, restart needed"}

Record available at the time:
````
exit_code=0
[PM2] Applying action restartProcessId on app [example-service]
[PM2] [example-service](3) ✓
````

When you have decided, end your answer with one line of JSON only: {"works": true or false, "confidence": number between 0 and 1, "reason": "one short sentence"}
`````

## Prüfung N0-T1

`````
You are reviewing whether a completed work item actually achieved its intended effect.

Work item: restart -> example-service (requested by agent): {"reason": "config change applied, restart needed"}

Record available at the time:
````
exit_code=0
[PM2] Applying action restartProcessId on app [example-service]
[PM2] [example-service](3) ✓
````

When you have decided, end your answer with one line of JSON only: {"works": true, false or "not established", "confidence": number between 0 and 1, "reason": "one short sentence"}
`````

## Prüfung N1-T0

`````
You are reviewing whether a completed work item actually achieved its intended effect.

Work item: restart -> example-service (requested by agent): {"reason": "config change applied, restart needed"}

Only confirm that the work item achieved its effect if the system output demonstrates it. Do not assume success that the output does not show.

Record available at the time:
````
exit_code=0
[PM2] Applying action restartProcessId on app [example-service]
[PM2] [example-service](3) ✓
````

When you have decided, end your answer with one line of JSON only: {"works": true or false, "confidence": number between 0 and 1, "reason": "one short sentence"}
`````

## Prüfung N1-T1

`````
You are reviewing whether a completed work item actually achieved its intended effect.

Work item: restart -> example-service (requested by agent): {"reason": "config change applied, restart needed"}

Only confirm that the work item achieved its effect if the system output demonstrates it. Do not assume success that the output does not show.

Record available at the time:
````
exit_code=0
[PM2] Applying action restartProcessId on app [example-service]
[PM2] [example-service](3) ✓
````

When you have decided, end your answer with one line of JSON only: {"works": true, false or "not established", "confidence": number between 0 and 1, "reason": "one short sentence"}
`````

## Klassifikation (GPT)

`````
Below is an entry from an operations log: a work item (what an agent was asked to do, or reported doing) and the record that was available at the time someone had to decide whether it succeeded.

Decide two things.

1. "applicable": Is this a work item whose success can be judged at all, i.e. an action or change with an intended effect (a restart, deployment, merge, file or database change, sent message, fix, configuration change)? Pure questions, discussions, plans or status conversations without such an action are not applicable.

2. If applicable, does the record DEMONSTRATE the outcome?
   - "demonstrated_success": the record reproduces observed output showing that the intended effect occurred (for example command output, log lines, an HTTP response, a query result).
   - "demonstrated_failure": the record shows that the intended effect did not occur.
   - "not_established": neither. A statement by the agent who did the work (such as "done", "verified", "all green") is NOT by itself a demonstration; count only observed output that is reproduced in the record.

Work item: restart -> example-service (requested by agent): {"reason": "config change applied, restart needed"}

Record available at the time:
````
exit_code=0
[PM2] Applying action restartProcessId on app [example-service]
[PM2] [example-service](3) ✓
````

Answer with a JSON object only: {"applicable": true or false, "outcome": "demonstrated_success", "demonstrated_failure", "not_established" or null, "reason": "one or two sentences naming the decisive line(s)"}
`````
