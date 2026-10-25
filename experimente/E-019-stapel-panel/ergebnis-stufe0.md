# E-019 Stufe 0 (Kalibrierungsleiter): nicht erfüllt, kein Hauptlauf

> **Korrektur 23.10. (E-021, Manipulationscheck):** Was hier "Reasoning aus" heißt, war in Wahrheit die **Standardeinstellung mit adaptivem, verborgenem Reasoning** (OpenRouter: Reasoning ist bei Sonnet 5.5 nicht abschaltbar). "Reasoning low" war **gedrosseltes** Reasoning. Alle Aussagen "Reasoning erhöht Fehlalarme" sind deshalb umzudrehen: **Gedrosseltes Reasoning erhöht Fehlalarme** (H-037). Details: `experimente/E-021-reasoning-fehlalarme/ergebnis.md`.

- **Datum:** 2026-10-22
- **Rohdaten:** `daten/E-019-stapel-panel/calls-kalibrierung-L*.jsonl`, `judgments-kalibrierung-L*.jsonl`, Berichte `kalibrierung-L*-bericht.md`. Lauf 1 von L1 enthielt Generatorfehler und ist markiert (`UNGUELTIG-L1-lauf1.txt`).
- **Material:** 144 Belege (Seeds 1100–1111). Jeder Beleg wurde einmal pro Kanal beurteilt, also 432 Urteile pro Stufe. Modell: Sonnet 5.5.
- **Kosten:** 3,27 $ (inkl. ungültigem L1-Lauf 1)

## Ergebnis je Leiterstufe

| Stufe | B | Reasoning | Fehlerrate | Fehlalarm | Übersehen | vordere / hintere Stapelhälfte | Kriterium 4 |
|---|---|---|---|---|---|---|---|
| L1 (Lauf 2) | 8 | low | 0,109 | 0,157 | 0,060 | 0,120 / 0,097 | ✘ |
| L2 | 12 | low | 0,102 | 0,157 | 0,046 | 0,097 / 0,106 | ✘ |
| L3 | 12 | aus | 0,046 | 0,037 | 0,056 | 0,023 / 0,069 | ✘ (dazu ✘ Kriterium 1) |

- **Übersehensrate je Fehlerart, über alle Stufen:**
  - `db_down` 0,27–0,33
  - alle anderen 0–0,06: `row_loss` 0,056 nur in L1, `weights_broken` 0,037 nur in L3, `stale_process` ~0,03, `bounced` und `wrong_recipient` 0
- **Kriterium 4** verlangt Fehler in ≥ 4 der 6 Fehlerarten. In keiner Stufe lagen mehr als 2 Fehlerarten bei ≥ 0,05.

## Stichprobe (Kriterium 5)
- **L1 Lauf 1:** 3 Generatorfehler in den neuen Routinezeilen. Behoben, getestet (`test_padding_is_internally_consistent`), L1 einmal wiederholt.
  1. Node-Listener ohne ps-Eintrag
  2. SMTP-Fremdnachrichten wurden vor dem Einreihen gesendet
  3. Wiederholte Endpunkt-Aufrufe lieferten verschiedene Werte
- **L2:** keine neuen Generatorfehler. Die Fehlalarme sind übervorsichtige Urteile zu Kanälen, die keine Fehlerspur enthalten ("nicht nachweisbar, dass nur Duplikate entfernt wurden", "Buchung zeigt keine Zustellung"). Die Ground Truth ist dort korrekt, denn die Abwesenheit einer Spur heißt ok.

## Was trotzdem interpretierbar ist (explorativ, nicht präregistriert)
1. **Stapelprüfung macht Sonnet 5.5 nicht unaufmerksam für Fehlerspuren.** Die Übersehensrate bleibt bei 5–6 %, wie bei Einzelbelegen in E-017. Bei B ≤ 12 erzeugt Aufmerksamkeitsknappheit kaum übersehene Fehler.
2. **Reasoning macht übervorsichtig.** Mit Reasoning "low" liegen die Fehlalarme bei 0,157, ohne Reasoning bei 0,037, bei gleicher Übersehensrate. Für Wave/Ace heißt das: Nachdenkende Prüfer erzeugen deutlich mehr unnötige Eskalationen, und die kosten Menschen-Minuten (`notizen/14`).
3. **Ein Positionseffekt zeigt sich nur ohne Reasoning** (vordere Hälfte 0,023, hintere 0,069). Ein Hinweis, aber bei n = 432 nicht belastbar.
4. **Wissens- bzw. Lesbarkeitsfehler bündeln sich in allen Settings auf denselben Spurtyp:** ein Healthcheck meldet ok, ein quantitatives Detail widerspricht (Pool 0/20). Das stützt HK-A4 und Chen 2606.27288: β wird von wenigen, bestimmten Items getragen.

## Konsequenz
- Mit diesem Material und starken Modellen lässt sich φ̄ zwischen Prüfern nicht sinnvoll über alle Fehlerarten messen. Die Fehler entstehen fast nur an einer Stelle.
- **Vorschlag zur Neuplanung (Neo entscheidet):** Das Material um mehrere Fehlerarten nach dem einzigen Muster erweitern, das starke Modelle tatsächlich übersehen: grüner Gesamtstatus, widersprechendes quantitatives Detail. Etwa 2 pro Domäne. Dann neu kalibrieren.

---

# Nachtrag: Material v3 (D-016), Leiter L1–L3 erneut, nicht erfüllt

- **Material:** 6 zusätzliche Fehlerarten "Status grün, quantitatives Detail widerspricht"; Kalibrierungsseeds 1200–1211
- **Kosten:** 3,64 $, inklusive des ungültigen Laufs 1 von L1

| Stufe | Fehlerrate | Fehlalarm | Übersehen | Fehlerarten mit Übersehen ≥ 0,05 | größter Beleganteil |
|---|---|---|---|---|---|
| L1 (Lauf 2) | 0,081 | 0,097 | 0,065 | 5/12 | 0,086 |
| L2 | 0,081 | 0,093 | 0,069 | 5/12 | 0,057 |
| L3 | 0,028 | 0,019 | 0,037 | 2/12 | 0,167 |

## Übersehensraten je Fehlerart (L2)

| Gruppe | Fehlerart | Übersehensrate |
|---|---|---|
| neu (D-016) | `empty_attachment` | 0,21 |
| neu (D-016) | `zero_traffic` | 0,17 |
| neu (D-016) | `amount_mismatch` | 0,07 |
| neu (D-016) | `cache_down` | 0,05 |
| neu (D-016) | `duplicates_kept` | 0 |
| neu (D-016) | `column_loss` | 0 |
| alt, Muster "grün" | `weights_broken` | 0,17 |
| alt, Muster "grün" | `db_down` | 0,13 |
| alt | `bounced`, `wrong_recipient`, `row_loss`, `stale_process` | 0 |

## Stichprobe (Kriterium 5)
- **L1 Lauf 1:** Die Ground Truth von `zero_traffic` war mehrdeutig. "0 Requests" ist kein eindeutiger Fehler, wenn der Auftrag die übliche Last nicht nennt.
  - Behoben: Der Auftrag nennt jetzt "normally handles ~N requests/min".
  - Lauf 1 ist als ungültig markiert, L1 wurde einmal wiederholt.
  - Die Übersehensrate von `zero_traffic` sank von 0,54 auf 0,17. Ein Drittel der damaligen "Fehler" lag also am Auftrag, nicht am Modell.

## Was explorativ jetzt zweimal gesehen wurde
- **Reasoning erhöht die Fehlalarme:**
  - Material v2: 0,157 (L1/L2) gegen 0,037 (L3)
  - Material v3: 0,093–0,097 gegen 0,019
  - Die Übersehensrate ändert sich nicht systematisch (v2: 0,046 → 0,056 ohne Reasoning; v3: 0,069 → 0,037). Reasoning kauft also keine erkennbar bessere Fehlerfindung mit den zusätzlichen Fehlalarmen.
- **Kein Positionseffekt im Stapel bei Reasoning low.** Er ist uneinheitlich: v2 L3 hinten höher, v3 L3 hinten niedriger.
- **Das Muster "grün plus widersprechendes Detail" erzeugt die Übersehen.** Doch selbst dort liegen die Raten bei 5–21 %, und Spuren, bei denen etwas fehlt (Spalten, Duplikate), werden fast immer erkannt.

## Konstruktionsfehler im eigenen Kriterium 4
Bei ~35–45 Fehlern pro Kalibrierung bedeutet "kein Beleg > 5 % der Fehler": Kein Beleg darf in mehr als 2 Kanälen falsch beurteilt werden. Das hängt vor allem an der Gesamtzahl der Fehler und kaum an deren Verteilung. **Das Kriterium wurde nicht mitten im Lauf geändert, gilt aber als fehlerhaft formuliert.** Ein Vorschlag steht im Laborbuch.
