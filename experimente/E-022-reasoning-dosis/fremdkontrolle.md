# E-022: Fremdkontrolle der Ground Truth (Regel 12)

Prüfer: `openai/gpt-6.1-sol` über OpenRouter, `reasoning.effort = high`, je Beleg einzeln, sieht Auftrag und alle drei Kanäle, keine Fehlerart und keinen Befundtext.

- Belege: 36, Übereinstimmung mit der Generator-Wahrheit: 33, **Abweichungen oder 'nicht entscheidbar': 3**
- Kosten: 0.20 $

Jede Abweichung klärt Neo von Hand (Spalte 'Klärung'): Generatorfehler, Prüferfehler oder echte Mehrdeutigkeit. Der Hauptlauf startet erst, wenn alle geklärt sind.

## business-fail_moderate-5020

- Generator: kaputt (`bounced`)
- Prüfer: False (entscheidbar: False)
- Begründung: The mail log shows 'status=deferred (452 4.2.2 over quota)' and 'still pending,' while tracking's last update is 71 hours old. Neither delivery nor final failure is confirmed, and the accounting/CRM 'SENT' entries do not establish delivery.
- Spur laut Generator: {'smtp': 'queue: 0990D6811C still pending, next retry in 4h (attempt 9 of 12)', 'delivery': 'tracking 0990D6811C: last update 71h ago (deferred)', 'ledger': "crm: contact s.berger@lindner-logistik.at email status 'soft-bounce' (reported by mail gateway)"}
- **Klärung (Neo):** 

<details><summary>Beleg</summary>

```
A colleague finished the work item below. Afterwards, three independent observations of the system were collected. Decide whether the work item actually achieved its intended effect.

Work item: Send invoice INV-2026-1084 (€ 1,781.57, PDF attached) to customer K-72, billing contact s.berger@lindner-logistik.at

Observation (outgoing mail server log):
```
10:25:25 0990D6811C: from=<billing@nordwerk-gmbh.at> to=<s.berger@lindner-logistik.at> size=87341 subject='Invoice INV-2026-1084 (€ 1,781.57)'
10:25:25 0990D6811C: 250 2.0.0 OK queued
10:43:58 0990D6811C: relay=mx1.lindner-logistik.at:25, status=deferred (452 4.2.2 over quota)
queue: 0990D6811C still pending, next retry in 4h (attempt 9 of 12)
```

Observation (delivery tracking report):
```
tracking 0990D6811C: queued for retry at 10:43:58
tracking 0990D6811C: last update 71h ago (deferred)
tracking 0990D6811C: 1 attachment (invoice_INV-2026-1084.pdf, 85 kB)
tracking 0990D6811C: payment link pay.nordwerk-gmbh.at/INV-2026-1084 (€ 1,781.57)
read receipt: not requested
```

Observation (accounting and CRM entries):
```
receivables: INV-2026-1084 posted, customer K-72, € 1,781.57, status SENT
crm: activity 'invoice sent' on K-72 (contact s.berger@lindner-logistik.at)
crm: contact s.berger@lindner-logistik.at email status 'soft-bounce' (reported by mail gateway)
archive: invoice_INV-2026-1084.pdf stored (2 pages)
dunning: reminder for INV-2026-1084 scheduled 2026-11-21
```

Answer with a JSON object only: {"works": true or false, "reason": "one or two sentences naming the decisive line(s)", "decidable": true or false}. Set "decidable" to false if the observations do not allow a confident decision either way.
```

</details>

## research-ok_clear-5013

- Generator: ok (`none`)
- Prüfer: False (entscheidbar: False)
- Begründung: “Dropped 74 duplicates” and “13,697 unique of 13,697” confirm deduplication, but no observation verifies that retained values, including weights, were unchanged. The requirement to remove duplicates only therefore cannot be confidently confirmed or ruled out.
- Spur laut Generator: —
- **Klärung (Neo):** 

<details><summary>Beleg</summary>

```
A colleague finished the work item below. Afterwards, three independent observations of the system were collected. Decide whether the work item actually achieved its intended effect.

Work item: Clean survey dataset D5: remove duplicate respondents only and write clean/d5.parquet (raw file: 13,771 rows, 47 columns, 74 duplicate respondents; survey weights are normalised to mean 1)

Observation (job log):
```
job clean_d5 started
read raw/d5.csv: 13,771 rows, 47 columns
dedupe on respondent_id: dropped 74 duplicates
dtypes: weight float64, income float64, age int64
wrote clean/d5.parquet (47 columns)
job clean_d5 finished ✓ exit 0 (16.5s)
```

Observation (output file statistics):
```
clean/d5.parquet: 13,697 rows x 47 columns (2.9 MB)
weight: min 0.31  max 4.87  mean 1.00  nulls 0
respondent_id: 13,697 unique of 13,697
```

Observation (downstream validation report):
```
schema: 47/47 columns present ✓
row count: 13,697 (raw 13,771, duplicates removed 74) ✓
weighted share female: 0.51 (census 0.51) ✓
sum of weights / n: 1.00 ✓
```

Answer with a JSON object only: {"works": true or false, "reason": "one or two sentences naming the decisive line(s)", "decidable": true or false}. Set "decidable" to false if the observations do not allow a confident decision either way.
```

</details>

## research-ok_clear-5023

- Generator: ok (`none`)
- Prüfer: False (entscheidbar: False)
- Begründung: The reported 190 removals and 39,388 unique IDs support successful deduplication, but no observation verifies that retained values were unchanged. The weight mean of 1.00 and schema checks cannot establish the 'remove duplicate respondents only' requirement.
- Spur laut Generator: —
- **Klärung (Neo):** 

<details><summary>Beleg</summary>

```
A colleague finished the work item below. Afterwards, three independent observations of the system were collected. Decide whether the work item actually achieved its intended effect.

Work item: Clean survey dataset D9: remove duplicate respondents only and write clean/d9.parquet (raw file: 39,578 rows, 47 columns, 190 duplicate respondents; survey weights are normalised to mean 1)

Observation (job log):
```
job clean_d9 started
read raw/d9.csv: 39,578 rows, 47 columns
dedupe on respondent_id: dropped 190 duplicates
dtypes: weight float64, income float64, age int64
wrote clean/d9.parquet (47 columns)
job clean_d9 finished ✓ exit 0 (27.2s)
```

Observation (output file statistics):
```
clean/d9.parquet: 39,388 rows x 47 columns (8.3 MB)
weight: min 0.31  max 4.87  mean 1.00  nulls 0
respondent_id: 39,388 unique of 39,388
```

Observation (downstream validation report):
```
schema: 47/47 columns present
row count: 39,388 (raw 39,578, duplicates removed 190)
weighted share female: 0.51 (census 0.51)
sum of weights / n: 1.00
```

Answer with a JSON object only: {"works": true or false, "reason": "one or two sentences naming the decisive line(s)", "decidable": true or false}. Set "decidable" to false if the observations do not allow a confident decision either way.
```

</details>

## Alle Urteile

| Beleg | Fehlerart | Wahrheit | Prüfer | entscheidbar |
|---|---|---|---|---|
| business-fail_moderate-5009 | empty_attachment | False | False | True |
| business-fail_moderate-5017 | empty_attachment | False | False | True |
| business-fail_moderate-5020 | bounced | False | False | False |
| business-fail_moderate-5021 | wrong_recipient | False | False | True |
| business-fail_subtle-5002 | bounced | False | False | True |
| business-fail_subtle-5006 | amount_mismatch | False | False | True |
| business-fail_subtle-5007 | amount_mismatch | False | False | True |
| business-fail_subtle-5018 | wrong_recipient | False | False | True |
| business-ok_clear-5002 | none | True | True | True |
| business-ok_clear-5012 | none | True | True | True |
| business-ok_noisy-5003 | none | True | True | True |
| business-ok_noisy-5023 | none | True | True | True |
| coding-fail_moderate-5005 | zero_traffic | False | False | True |
| coding-fail_subtle-5005 | zero_traffic | False | False | True |
| coding-fail_subtle-5008 | cache_down | False | False | True |
| coding-fail_subtle-5009 | stale_process | False | False | True |
| coding-fail_subtle-5010 | db_down | False | False | True |
| coding-fail_subtle-5015 | stale_process | False | False | True |
| coding-fail_subtle-5017 | db_down | False | False | True |
| coding-fail_subtle-5022 | cache_down | False | False | True |
| coding-ok_clear-5002 | none | True | True | True |
| coding-ok_clear-5014 | none | True | True | True |
| coding-ok_noisy-5003 | none | True | True | True |
| coding-ok_noisy-5013 | none | True | True | True |
| research-fail_moderate-5002 | duplicates_kept | False | False | True |
| research-fail_moderate-5008 | duplicates_kept | False | False | True |
| research-fail_moderate-5014 | row_loss | False | False | True |
| research-fail_subtle-5001 | column_loss | False | False | True |
| research-fail_subtle-5003 | weights_broken | False | False | True |
| research-fail_subtle-5008 | row_loss | False | False | True |
| research-fail_subtle-5016 | weights_broken | False | False | True |
| research-fail_subtle-5020 | column_loss | False | False | True |
| research-ok_clear-5013 | none | True | False | False |
| research-ok_clear-5023 | none | True | False | False |
| research-ok_noisy-5011 | none | True | True | True |
| research-ok_noisy-5014 | none | True | True | True |