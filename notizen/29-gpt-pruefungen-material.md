# GPT-Prüfungen des Materials (Regel 12 und 17), 23.10.2026

Prüfer: `openai/gpt-6.1-sol` über OpenRouter, `reasoning.effort = high`, je Beleg einzeln (`orglab/fremdkontrolle.py`). Kosten der ersten Runde zusammen ~0,7 $.

## 1. E-022 (Material v3.1): Fremdkontrolle der Ground Truth
- 36 geschichtete Belege, **33 übereinstimmend, 3 als "nicht entscheidbar" markiert**, kein Fall mit entgegengesetztem Urteil.
- Die 3 Fälle (Bericht: `experimente/E-022-reasoning-dosis/fremdkontrolle.md`):
  1. `business-fail_moderate-5020` (`bounced`): Die Mail steht seit 71 h in der Warteschlange ("over quota", Versuch 9 von 12). GPT sagt: weder zugestellt noch endgültig gescheitert. Die Generator-Wahrheit sagt "kaputt". **Claudes Einschätzung:** Die Wahrheit ist haltbar, denn der Auftrag "Rechnung an den Kunden schicken" ist nach drei Tagen nicht erfüllt. Ein Rest Mehrdeutigkeit bleibt ("noch nicht" gegen "gescheitert").
  2. und 3. `research-ok_clear-5013` und `-5023`: GPT kann "remove duplicates only" nicht positiv bestätigen, weil keine Zeile beweist, dass sonst nichts verändert wurde. **Claudes Einschätzung:** Das ist Prüferstrenge, kein Generatorfehler. Die Belege sind ok.
- **Folge:** Kein Generatorfehler gefunden. Neo bestätigt die Einschätzung, dann ist E-022 startklar.

## 2. Material v4.0: Lecktest und Fremdkontrolle zeigen drei Generatorfehler und ein Konventionsleck
Rohdaten archiviert als `daten/E-020-realitaet-in-dosen/lecktest-v4.0.jsonl` und `fremdkontrolle-v4.0.jsonl`, Berichte `experimente/E-020…/lecktest-v4.0.md` und `fremdkontrolle-v4.0.md`.

| Befund | Wo | Art | Behebung in v4.1 |
|---|---|---|---|
| "weights: rescaled to total …" widerspricht "remove duplicate respondents **only**". GPT erklärte deshalb **alle** Research-Belege für kaputt, auch die korrekten. Die 100 % "ohne Norm erkannt" bei den drei Research-Fehlerarten waren also kein Leck, sondern dieser Fehler. | research | **Generatorfehler (Claude)** | Auftrag nennt die Neukalibrierung: "remove duplicate respondents (nothing else may be dropped), recalibrate the survey weights to the target population". Kalibrierung trifft die Zielsumme exakt, Zielpopulation nicht rund. |
| Portal-Kunden: Auftrag "no attachment", aber ein Logo hing an | business | **Generatorfehler (Claude)** | Portal-Variante ganz entfernt |
| "Rechnung ohne PDF" ist auch ohne Sollwert verdächtig: GPT erklärte alle Belege ohne PDF für kaputt, auch die korrekten Portal-Belege | business | **Konventionsleck** (Regel 17) | `attachment_missing` ersetzt durch `wrong_terms`: falsches Zahlungsziel. Ohne Norm ist jedes Fälligkeitsdatum plausibel (14/30/45/60 Tage, gleiche Menge für Ok und Fehler). |
| `low_traffic`: Auch **mit** Norm sagt GPT "nicht entscheidbar", weil die Last gerade nur vorübergehend niedrig sein könnte | coding | **Mehrdeutige Ground Truth** | Norm ergänzt: "steady around the clock (±20 %)" |
| `low_traffic`, `cache_partial`: 0 von 6 ohne Norm erkannt, keine Fehlalarme auf Ok-Belegen | coding | **bestätigt spec-rein** | – |
| `wrong_contact`: Der Kontakt selbst wurde ohne Norm nie beanstandet. Die zwei "Treffer" kamen vom fehlenden PDF (Portal). | business | spec-rein, durch das PDF-Leck überdeckt | – |

## 3. Lehre
- Der Code-Lecktest (`tests/test_evidence_v4.py`) prüft Marker und Zahlenverteilungen. Er konnte nicht sehen, dass eine Zeile dem **Auftragstext** widerspricht oder dass **Weltwissen** ("Rechnungen haben ein PDF") die Norm ersetzt. Das kann nur ein Modell prüfen. **Beide Prüfungen sind nötig.**
- Wieder hat ein Modell aus einer anderen Familie Fehler in von Claude gebautem Material gefunden (vgl. `notizen/25`: rund zehn Generatorfehler, alle durch Modellwiderspruch entdeckt). Regel 12 hat sich gelohnt, bevor ein Euro in den Hauptlauf ging.
- Die Ergebnisse von v4.1 folgen unten, sobald die Wiederholung gelaufen ist.

## 4. v4.1: Wiederholung (Generator-Commit d66fe71)
- **Lecktest (nur Kurzauftrag, kein Runbook):** **0 von 42** spec-reinen kaputten Belegen ohne Sollwert sicher als kaputt erkannt, in allen 7 Fehlerarten 0 von 6. Kriterium (≤ 25 % je Art) erfüllt. Auf den Ok-Belegen gab es keinen sicheren Fehlalarm, nur zwei Research-Belege, die GPT ohne Norm "nicht entscheidbar" nennt. Das ist erwünscht.
- **Fremdkontrolle (voller Auftrag):** **47 von 48** übereinstimmend. Einzige Abweichung: `coding-fail_moderate-6021` (`low_traffic`). GPT urteilt richtig "kaputt", markiert den Fall aber als nicht entscheidbar, weil 2 Requests gegen üblich ~20/min auch nur die eigenen Sonden sein könnten. Grenzfall bei sehr kleinen Lasten, keine falsche Wahrheit. Mögliche Nachbesserung: übliche Last ab 50 statt ab 10 req/min (Neo entscheidet).
- Kosten der Wiederholung ~0,6 $.
- **Folge:** Die Primärmenge für E-020 umfasst 7 Fehlerarten mit je 12 kaputten Belegen bei 24 Seeds, also 84.

## 5. Nachtrag: Was "effort: high" bei GPT-6.1 Sol tatsächlich heißt (Regel 11)
- Neos Frage: "Wie kann das so günstig sein?"
- **Preis:** 2 $ je Mio. Eingabe-Tokens, 10 $ je Mio. Ausgabe-Tokens, gleich teuer wie Sonnet 5.5. Laut OpenRouter liegt das Modell in der GPT-6-Reihe unter dem Flaggschiff GPT-6 Astra, ist also kein Mini-Modell.
- **Pro Prüfung:** Median 873 Eingabe- und 176 Ausgabe-Tokens (242 Aufrufe, Spanne 66–1.000), also rund 0,4 Cent. Wiederholte Prompt-Teile kommen zusätzlich aus dem Cache.
- **Manipulationscheck nachgeholt (eine Probe, 0,002 $):** `reasoning_tokens = 118` bei `effort: high`. Das Modell entscheidet selbst, wie viel es denkt, und denkt bei diesen kurzen Belegen wenig. **"effort: high" heißt hier also nicht "lange nachgedacht".** Die Urteile nennen trotzdem die entscheidenden Zeilen und haben die echten Generatorfehler gefunden.
- **Einordnung:** Die GPT-Prüfungen sind eine brauchbare Fremdkontrolle, aber keine gründliche Zweitbegutachtung durch ein Spitzenmodell. Für kritische Hauptläufe könnte man eine Stichprobe zusätzlich mit GPT-6 Astra oder `gpt-6.1-sol-pro` prüfen (Neo entscheidet).

## Material v4.3 (E-020 v3, Hauptlauf-Seeds 6000–6023), 2026-10-23 13:39
- Nach der v4.2-Prüfung fand GPT zwei Fehler: Mehrdeutigkeit "welche Instanz" und doppelte fd-Nummern. Beides in v4.3 behoben.
- **Fremdkontrolle v4.3: 48/48**, keine Abweichung, nichts "nicht entscheidbar". Grenzfall 6021 jetzt eindeutig.
- **Lecktest v4.3: 0/42** ohne Sollwert sicher erkannt. Gegenprobe: 2 von 12 Ok-Belegen (beide `weights`) ohne Sollwert nicht belegbar.
- Reihe der GPT-Funde über die Versionen: v4.0 vier Fehler, v4.1 Leck, v4.2 zwei Fehler, v4.3 keiner. Die Fremdkontrolle hat also bis zuletzt etwas gefunden. Das spricht dafür, sie nach jeder Materialänderung zu wiederholen.
