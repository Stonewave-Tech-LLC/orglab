# E-020v4: Fremdkontrolle der Ground Truth (Regel 12)

Prüfer: `openai/gpt-6.1-sol` über OpenRouter, `reasoning.effort = high`, je Beleg einzeln, sieht Auftrag und alle drei Kanäle, keine Fehlerart und keinen Befundtext.

- Belege: 48, Übereinstimmung mit der Generator-Wahrheit: 48, **Abweichungen oder 'nicht entscheidbar': 0**
- Kosten: 0.17 $

Jede Abweichung klärt Neo von Hand (Spalte 'Klärung'): Generatorfehler, Prüferfehler oder echte Mehrdeutigkeit. Der Hauptlauf startet erst, wenn alle geklärt sind.

## Alle Urteile

| Beleg | Fehlerart | Wahrheit | Prüfer | entscheidbar |
|---|---|---|---|---|
| business-fail_moderate-6006 | amount_mismatch | False | False | True |
| business-fail_moderate-6009 | wrong_contact | False | False | True |
| business-fail_moderate-6011 | wrong_terms | False | False | True |
| business-fail_moderate-6015 | wrong_terms | False | False | True |
| business-fail_moderate-6018 | amount_mismatch | False | False | True |
| business-fail_moderate-6021 | wrong_contact | False | False | True |
| business-fail_subtle-6001 | wrong_terms | False | False | True |
| business-fail_subtle-6002 | bounced | False | False | True |
| business-fail_subtle-6003 | wrong_contact | False | False | True |
| business-fail_subtle-6006 | bounced | False | False | True |
| business-fail_subtle-6008 | amount_mismatch | False | False | True |
| business-fail_subtle-6010 | bounced | False | False | True |
| business-ok_clear-6001 | none | True | True | True |
| business-ok_clear-6008 | none | True | True | True |
| business-ok_noisy-6003 | none | True | True | True |
| business-ok_noisy-6008 | none | True | True | True |
| coding-fail_moderate-6001 | low_traffic | False | False | True |
| coding-fail_moderate-6003 | cache_partial | False | False | True |
| coding-fail_moderate-6013 | low_traffic | False | False | True |
| coding-fail_moderate-6015 | cache_partial | False | False | True |
| coding-fail_moderate-6021 | low_traffic | False | False | True |
| coding-fail_subtle-6002 | stale_process | False | False | True |
| coding-fail_subtle-6004 | db_down | False | False | True |
| coding-fail_subtle-6008 | db_down | False | False | True |
| coding-fail_subtle-6010 | stale_process | False | False | True |
| coding-fail_subtle-6012 | db_down | False | False | True |
| coding-fail_subtle-6014 | stale_process | False | False | True |
| coding-fail_subtle-6017 | cache_partial | False | False | True |
| coding-ok_clear-6004 | none | True | True | True |
| coding-ok_clear-6021 | none | True | True | True |
| coding-ok_noisy-6004 | none | True | True | True |
| coding-ok_noisy-6023 | none | True | True | True |
| research-fail_moderate-6002 | duplicates_partial | False | False | True |
| research-fail_moderate-6004 | row_loss | False | False | True |
| research-fail_moderate-6007 | column_loss | False | False | True |
| research-fail_moderate-6012 | row_loss | False | False | True |
| research-fail_moderate-6019 | column_loss | False | False | True |
| research-fail_moderate-6020 | row_loss | False | False | True |
| research-fail_subtle-6000 | duplicates_partial | False | False | True |
| research-fail_subtle-6005 | column_loss | False | False | True |
| research-fail_subtle-6007 | weights_misscaled | False | False | True |
| research-fail_subtle-6008 | duplicates_partial | False | False | True |
| research-fail_subtle-6015 | weights_misscaled | False | False | True |
| research-fail_subtle-6023 | weights_misscaled | False | False | True |
| research-ok_clear-6004 | none | True | True | True |
| research-ok_clear-6010 | none | True | True | True |
| research-ok_noisy-6002 | none | True | True | True |
| research-ok_noisy-6016 | none | True | True | True |