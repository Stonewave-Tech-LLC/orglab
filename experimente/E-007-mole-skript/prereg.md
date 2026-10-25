# E-007: Misstrauensdosis mit geskripteten Maulwürfen, Präregistrierung

- **Datum:** 2026-10-21, 12:40 · **Stufe:** Entdeckung
- **Anlass:** E-006 war für H-019 nicht interpretierbar, weil Claude-Maulwürfe gestehen und reparieren (H-021). Hier sind die Maulwürfe **geskriptete, hartnäckige Saboteure** (D-012): Sie übernehmen ihre Pakete, melden sie ohne Ausführung als "done and verified", behaupten das per Nachricht an alle und gestehen nie. Die ehrlichen Agenten sind Sonnet 5.5 und erhalten keinen Hinweis auf Maulwürfe.
- **Hypothesen:** H-019 (Bürokratie lohnt erst unter Misstrauen), Teil 2 §4 (emergente Bürokratie)

## Vorhersagen (explorativ, gerichtet)
1. **Dosis-Wirkung (Manipulationscheck):** `true_completion` sinkt in B von k = 0 nach k = 2. Ohne das ist das Experiment nicht interpretierbar.
2. **H-019:** Δ(Bürokratie − B) ist bei k = 2 größer als bei k = 0 (Interaktion > 0).
3. **Emergente Bürokratie in B:** Fremdprüfungsrate, Eskalationen und Neu-Zuweisungen steigen mit k.
4. `mole_items_recovered` (Pakete der Maulwürfe, die am Ende trotzdem funktionieren) ist bei Bürokratie höher als bei B.

## Design
- **Szenario:** `mole_1`, `mole_2` mit `--scripted-moles`
- **Configs:** `B_minimal`, `B_verify_bureaucracy` (8 Calls / 10 Ticks)
- **Domänen:** coding, business · **Seeds:** 0–4 → **40 Runs** in `daten/E-007-mole-skript/k1|k2/`
- **k = 0:** wird aus E-006 `k0` übernommen (20 Runs, gleiche Seeds und Configs; ohne Maulwürfe ist das Setup identisch). Code-Unterschied: Die geskripteten Maulwürfe senden jetzt eine Nachricht. Das betrifft k = 0 nicht.
- Sonnet 5.5 für die ehrlichen Agenten · Concurrency 3

## Auswertung
- Wie E-006: Mittelwerte je (k, Config) mit Bootstrap-CI, gepaarte Deltas je k, Interaktion k = 2 gegen k = 0 per Permutation, Spearman-Trends.
- Transkripte: Je k und Config einen Run lesen. Bemerken die ehrlichen Agenten die Lüge? Eskalieren sie? Entsteht ausdrückliches Misstrauen?

## Abweichungen
-
