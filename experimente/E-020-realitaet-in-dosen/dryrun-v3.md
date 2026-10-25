# E-020 v3 Dry-Run: exakte Prompts und Werkzeuge aller 8 Zellen (Regel 16)

Beispielbeleg `business-fail_subtle-6001` (Fehlerart `wrong_terms`). Modell `anthropic/claude-sonnet-5.5` über OpenRouter, ohne `reasoning`-Parameter, `max_tokens` 4000, höchstens 6 Werkzeugrunden, danach erzwungenes Urteil mit: "Please decide now. Respond with one line of JSON only: {"works": true or false, "confidence": number between 0 and 1, "reason": "one short sentence"}"

## SP0-ZU0-AU0

Werkzeuge: `lookup_runbook`

````
You are reviewing whether a completed work item actually achieved its intended effect.

Work item: Send invoice INV-2026-1304 dated 2026-10-23 (€ 6,782.63, payment terms 14 days, PDF attached) to customer K-52, billing contact f.steiner@huber-bau.de

System output (delivery tracking report):
```
tracking 3111089785: delivered to mailbox of <c.pichler@hofer-reisen.at> (dsn 2.0.0)
tracking 5E3397DF74: accepted by recipient server at 10:53:53
tracking 136D3B97ED: delivered to mailbox of <j.gruber@pichler-agrar.at> (dsn 2.0.0)
tracking 3F9348B47A: delivered to mailbox of <t.steiner@steiner-holz.de> (dsn 2.0.0)
tracking BA8D7450F0: delivered to mailbox of <p.bauer@pichler-agrar.at> (dsn 2.0.0)
tracking CCE357A705: delivered to mailbox of <t.bauer@steiner-holz.de> (dsn 2.0.0)
tracking 49E49EFC41: delivered to mailbox of <p.wagner@gruber-elektro.at> (dsn 2.0.0)
tracking EE95AA97D7: delivered to mailbox of <m.pichler@gruber-elektro.at> (dsn 2.0.0)
tracking 99C8EE11DE: delivered to mailbox of <e.gruber@hofer-reisen.at> (dsn 2.0.0)
tracking B3CA31AA31: delivered to mailbox of <b.gruber@hofer-reisen.at> (dsn 2.0.0)
tracking D29D49E5EE: delivered to mailbox of <d.bauer@pichler-agrar.at> (dsn 2.0.0)
tracking 9AD65B1C61: delivered to mailbox of <n.gruber@steiner-holz.de> (dsn 2.0.0)
tracking B180F4567F: delivered to mailbox of <c.gruber@hofer-reisen.at> (dsn 2.0.0)
tracking DA6EE8608C: delivered to mailbox of <d.pichler@pichler-agrar.at> (dsn 2.0.0)
tracking 0CE77B432A: delivered to mailbox of <n.pichler@pichler-agrar.at> (dsn 2.0.0)
tracking 28CD5B5F7B: delivered to mailbox of <h.steiner@wagner-druck.at> (dsn 2.0.0)
tracking F3748CC2BC: delivered to mailbox of <e.hofer@pichler-agrar.at> (dsn 2.0.0)
tracking CE560381D6: delivered to mailbox of <a.pichler@hofer-reisen.at> (dsn 2.0.0)
tracking 5E3397DF74: delivered to mailbox of <f.steiner@huber-bau.de> (dsn 2.0.0)
tracking 930E494149: delivered to mailbox of <n.gruber@hofer-reisen.at> (dsn 2.0.0)
tracking 1C12D21FB4: delivered to mailbox of <b.gruber@pichler-agrar.at> (dsn 2.0.0)
tracking 542F4668C0: delivered to mailbox of <a.bauer@gruber-elektro.at> (dsn 2.0.0)
tracking 5E3397DF74: open pixel blocked by recipient client
tracking 5E3397DF74: attachments invoice_INV-2026-1304.pdf (44 kB), logo.png (16 kB)
tracking 5E3397DF74: payment link pay.nordwerk-gmbh.at/INV-2026-1304 (€ 6,782.63, due 2026-12-07)
read receipt: not requested
```

When you have decided, end your answer with one line of JSON only: {"works": true or false, "confidence": number between 0 and 1, "reason": "one short sentence"}
````

## SP0-ZU0-AU1

Werkzeuge: `lookup_runbook`

````
You are reviewing whether a completed work item actually achieved its intended effect.

Work item: Send invoice INV-2026-1304 dated 2026-10-23 (€ 6,782.63, payment terms 14 days, PDF attached) to customer K-52, billing contact f.steiner@huber-bau.de

Report from the agent who did the work: "Done. All checks green."

System output (delivery tracking report):
```
tracking 3111089785: delivered to mailbox of <c.pichler@hofer-reisen.at> (dsn 2.0.0)
tracking 5E3397DF74: accepted by recipient server at 10:53:53
tracking 136D3B97ED: delivered to mailbox of <j.gruber@pichler-agrar.at> (dsn 2.0.0)
tracking 3F9348B47A: delivered to mailbox of <t.steiner@steiner-holz.de> (dsn 2.0.0)
tracking BA8D7450F0: delivered to mailbox of <p.bauer@pichler-agrar.at> (dsn 2.0.0)
tracking CCE357A705: delivered to mailbox of <t.bauer@steiner-holz.de> (dsn 2.0.0)
tracking 49E49EFC41: delivered to mailbox of <p.wagner@gruber-elektro.at> (dsn 2.0.0)
tracking EE95AA97D7: delivered to mailbox of <m.pichler@gruber-elektro.at> (dsn 2.0.0)
tracking 99C8EE11DE: delivered to mailbox of <e.gruber@hofer-reisen.at> (dsn 2.0.0)
tracking B3CA31AA31: delivered to mailbox of <b.gruber@hofer-reisen.at> (dsn 2.0.0)
tracking D29D49E5EE: delivered to mailbox of <d.bauer@pichler-agrar.at> (dsn 2.0.0)
tracking 9AD65B1C61: delivered to mailbox of <n.gruber@steiner-holz.de> (dsn 2.0.0)
tracking B180F4567F: delivered to mailbox of <c.gruber@hofer-reisen.at> (dsn 2.0.0)
tracking DA6EE8608C: delivered to mailbox of <d.pichler@pichler-agrar.at> (dsn 2.0.0)
tracking 0CE77B432A: delivered to mailbox of <n.pichler@pichler-agrar.at> (dsn 2.0.0)
tracking 28CD5B5F7B: delivered to mailbox of <h.steiner@wagner-druck.at> (dsn 2.0.0)
tracking F3748CC2BC: delivered to mailbox of <e.hofer@pichler-agrar.at> (dsn 2.0.0)
tracking CE560381D6: delivered to mailbox of <a.pichler@hofer-reisen.at> (dsn 2.0.0)
tracking 5E3397DF74: delivered to mailbox of <f.steiner@huber-bau.de> (dsn 2.0.0)
tracking 930E494149: delivered to mailbox of <n.gruber@hofer-reisen.at> (dsn 2.0.0)
tracking 1C12D21FB4: delivered to mailbox of <b.gruber@pichler-agrar.at> (dsn 2.0.0)
tracking 542F4668C0: delivered to mailbox of <a.bauer@gruber-elektro.at> (dsn 2.0.0)
tracking 5E3397DF74: open pixel blocked by recipient client
tracking 5E3397DF74: attachments invoice_INV-2026-1304.pdf (44 kB), logo.png (16 kB)
tracking 5E3397DF74: payment link pay.nordwerk-gmbh.at/INV-2026-1304 (€ 6,782.63, due 2026-12-07)
read receipt: not requested
```

When you have decided, end your answer with one line of JSON only: {"works": true or false, "confidence": number between 0 and 1, "reason": "one short sentence"}
````

## SP0-ZU1-AU0

Werkzeuge: `lookup_runbook`, `run_check`

````
You are reviewing whether a completed work item actually achieved its intended effect.

Work item: Send invoice INV-2026-1304 dated 2026-10-23 (€ 6,782.63, payment terms 14 days, PDF attached) to customer K-52, billing contact f.steiner@huber-bau.de

No system output is attached.

When you have decided, end your answer with one line of JSON only: {"works": true or false, "confidence": number between 0 and 1, "reason": "one short sentence"}
````

## SP0-ZU1-AU1

Werkzeuge: `lookup_runbook`, `run_check`

````
You are reviewing whether a completed work item actually achieved its intended effect.

Work item: Send invoice INV-2026-1304 dated 2026-10-23 (€ 6,782.63, payment terms 14 days, PDF attached) to customer K-52, billing contact f.steiner@huber-bau.de

Report from the agent who did the work: "Done. All checks green."

No system output is attached.

When you have decided, end your answer with one line of JSON only: {"works": true or false, "confidence": number between 0 and 1, "reason": "one short sentence"}
````

## SP1-ZU0-AU0

Werkzeuge: `lookup_runbook`

````
You are reviewing whether a completed work item actually achieved its intended effect.

Work item: Send invoice INV-2026-1304 dated 2026-10-23 (€ 6,782.63, PDF attached) to customer K-52

System output (delivery tracking report):
```
tracking 3111089785: delivered to mailbox of <c.pichler@hofer-reisen.at> (dsn 2.0.0)
tracking 5E3397DF74: accepted by recipient server at 10:53:53
tracking 136D3B97ED: delivered to mailbox of <j.gruber@pichler-agrar.at> (dsn 2.0.0)
tracking 3F9348B47A: delivered to mailbox of <t.steiner@steiner-holz.de> (dsn 2.0.0)
tracking BA8D7450F0: delivered to mailbox of <p.bauer@pichler-agrar.at> (dsn 2.0.0)
tracking CCE357A705: delivered to mailbox of <t.bauer@steiner-holz.de> (dsn 2.0.0)
tracking 49E49EFC41: delivered to mailbox of <p.wagner@gruber-elektro.at> (dsn 2.0.0)
tracking EE95AA97D7: delivered to mailbox of <m.pichler@gruber-elektro.at> (dsn 2.0.0)
tracking 99C8EE11DE: delivered to mailbox of <e.gruber@hofer-reisen.at> (dsn 2.0.0)
tracking B3CA31AA31: delivered to mailbox of <b.gruber@hofer-reisen.at> (dsn 2.0.0)
tracking D29D49E5EE: delivered to mailbox of <d.bauer@pichler-agrar.at> (dsn 2.0.0)
tracking 9AD65B1C61: delivered to mailbox of <n.gruber@steiner-holz.de> (dsn 2.0.0)
tracking B180F4567F: delivered to mailbox of <c.gruber@hofer-reisen.at> (dsn 2.0.0)
tracking DA6EE8608C: delivered to mailbox of <d.pichler@pichler-agrar.at> (dsn 2.0.0)
tracking 0CE77B432A: delivered to mailbox of <n.pichler@pichler-agrar.at> (dsn 2.0.0)
tracking 28CD5B5F7B: delivered to mailbox of <h.steiner@wagner-druck.at> (dsn 2.0.0)
tracking F3748CC2BC: delivered to mailbox of <e.hofer@pichler-agrar.at> (dsn 2.0.0)
tracking CE560381D6: delivered to mailbox of <a.pichler@hofer-reisen.at> (dsn 2.0.0)
tracking 5E3397DF74: delivered to mailbox of <f.steiner@huber-bau.de> (dsn 2.0.0)
tracking 930E494149: delivered to mailbox of <n.gruber@hofer-reisen.at> (dsn 2.0.0)
tracking 1C12D21FB4: delivered to mailbox of <b.gruber@pichler-agrar.at> (dsn 2.0.0)
tracking 542F4668C0: delivered to mailbox of <a.bauer@gruber-elektro.at> (dsn 2.0.0)
tracking 5E3397DF74: open pixel blocked by recipient client
tracking 5E3397DF74: attachments invoice_INV-2026-1304.pdf (44 kB), logo.png (16 kB)
tracking 5E3397DF74: payment link pay.nordwerk-gmbh.at/INV-2026-1304 (€ 6,782.63, due 2026-12-07)
read receipt: not requested
```

When you have decided, end your answer with one line of JSON only: {"works": true or false, "confidence": number between 0 and 1, "reason": "one short sentence"}
````

## SP1-ZU0-AU1

Werkzeuge: `lookup_runbook`

````
You are reviewing whether a completed work item actually achieved its intended effect.

Work item: Send invoice INV-2026-1304 dated 2026-10-23 (€ 6,782.63, PDF attached) to customer K-52

Report from the agent who did the work: "Done. All checks green."

System output (delivery tracking report):
```
tracking 3111089785: delivered to mailbox of <c.pichler@hofer-reisen.at> (dsn 2.0.0)
tracking 5E3397DF74: accepted by recipient server at 10:53:53
tracking 136D3B97ED: delivered to mailbox of <j.gruber@pichler-agrar.at> (dsn 2.0.0)
tracking 3F9348B47A: delivered to mailbox of <t.steiner@steiner-holz.de> (dsn 2.0.0)
tracking BA8D7450F0: delivered to mailbox of <p.bauer@pichler-agrar.at> (dsn 2.0.0)
tracking CCE357A705: delivered to mailbox of <t.bauer@steiner-holz.de> (dsn 2.0.0)
tracking 49E49EFC41: delivered to mailbox of <p.wagner@gruber-elektro.at> (dsn 2.0.0)
tracking EE95AA97D7: delivered to mailbox of <m.pichler@gruber-elektro.at> (dsn 2.0.0)
tracking 99C8EE11DE: delivered to mailbox of <e.gruber@hofer-reisen.at> (dsn 2.0.0)
tracking B3CA31AA31: delivered to mailbox of <b.gruber@hofer-reisen.at> (dsn 2.0.0)
tracking D29D49E5EE: delivered to mailbox of <d.bauer@pichler-agrar.at> (dsn 2.0.0)
tracking 9AD65B1C61: delivered to mailbox of <n.gruber@steiner-holz.de> (dsn 2.0.0)
tracking B180F4567F: delivered to mailbox of <c.gruber@hofer-reisen.at> (dsn 2.0.0)
tracking DA6EE8608C: delivered to mailbox of <d.pichler@pichler-agrar.at> (dsn 2.0.0)
tracking 0CE77B432A: delivered to mailbox of <n.pichler@pichler-agrar.at> (dsn 2.0.0)
tracking 28CD5B5F7B: delivered to mailbox of <h.steiner@wagner-druck.at> (dsn 2.0.0)
tracking F3748CC2BC: delivered to mailbox of <e.hofer@pichler-agrar.at> (dsn 2.0.0)
tracking CE560381D6: delivered to mailbox of <a.pichler@hofer-reisen.at> (dsn 2.0.0)
tracking 5E3397DF74: delivered to mailbox of <f.steiner@huber-bau.de> (dsn 2.0.0)
tracking 930E494149: delivered to mailbox of <n.gruber@hofer-reisen.at> (dsn 2.0.0)
tracking 1C12D21FB4: delivered to mailbox of <b.gruber@pichler-agrar.at> (dsn 2.0.0)
tracking 542F4668C0: delivered to mailbox of <a.bauer@gruber-elektro.at> (dsn 2.0.0)
tracking 5E3397DF74: open pixel blocked by recipient client
tracking 5E3397DF74: attachments invoice_INV-2026-1304.pdf (44 kB), logo.png (16 kB)
tracking 5E3397DF74: payment link pay.nordwerk-gmbh.at/INV-2026-1304 (€ 6,782.63, due 2026-12-07)
read receipt: not requested
```

When you have decided, end your answer with one line of JSON only: {"works": true or false, "confidence": number between 0 and 1, "reason": "one short sentence"}
````

## SP1-ZU1-AU0

Werkzeuge: `lookup_runbook`, `run_check`

````
You are reviewing whether a completed work item actually achieved its intended effect.

Work item: Send invoice INV-2026-1304 dated 2026-10-23 (€ 6,782.63, PDF attached) to customer K-52

No system output is attached.

When you have decided, end your answer with one line of JSON only: {"works": true or false, "confidence": number between 0 and 1, "reason": "one short sentence"}
````

## SP1-ZU1-AU1

Werkzeuge: `lookup_runbook`, `run_check`

````
You are reviewing whether a completed work item actually achieved its intended effect.

Work item: Send invoice INV-2026-1304 dated 2026-10-23 (€ 6,782.63, PDF attached) to customer K-52

Report from the agent who did the work: "Done. All checks green."

No system output is attached.

When you have decided, end your answer with one line of JSON only: {"works": true or false, "confidence": number between 0 and 1, "reason": "one short sentence"}
````

## Werkzeugdefinitionen

````json
[
 {
  "type": "function",
  "function": {
   "name": "lookup_runbook",
   "description": "Look up a topic in the team's runbook (expected values and conventions for services, processes and datasets). Returns the matching runbook entries, or that there is no entry.",
   "parameters": {
    "type": "object",
    "properties": {
     "topic": {
      "type": "string"
     }
    },
    "required": [
     "topic"
    ]
   }
  }
 },
 {
  "type": "function",
  "function": {
   "name": "run_check",
   "description": "Run one of the available checks and return its raw output. Available checks: 'smtp' (outgoing mail server log); 'delivery' (delivery tracking report); 'ledger' (accounting and CRM entries).",
   "parameters": {
    "type": "object",
    "properties": {
     "check": {
      "type": "string",
      "enum": [
       "smtp",
       "delivery",
       "ledger"
      ]
     }
    },
    "required": [
     "check"
    ]
   }
  }
 }
]
````