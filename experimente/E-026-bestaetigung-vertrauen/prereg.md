# E-026: Bestätigung "Glückliches Vertrauen" (H-041, H-042) – Präregistrierung

> Bestätigungslauf zu E-025 (Neo, 25.10.: Plan "geht los"). Gleiches Design, Material und gleiche Prompts wie E-025, **frische Seeds**. Die Befunde aus E-025 werden hier zu vorab festgelegten, gerichteten Vorhersagen. Läuft durch den research-harness (`research-harness/laeufe/E-026/prereg.yaml`). **Status: freigegeben (Neo, 25.10.: "Freigegeben, starte E-026.").**

- **Datum:** 2026-10-25
- **Stufe: Bestätigung.** Damit gelten die Regeln 18 (Kritik vorab), 19 (doppelte Buchführung) und 20 (Verblindung), alle durch den Harness erzwungen.
- **Hypothesen:**
  - H-041 (glückliches Vertrauen; Norm und dritte Antwort senken es)
  - H-042 (Fehlerbild statt Modellstärke: bei fehlender Evidenz bestätigt das stärkere Modell mehr)
  - Wortlaut jeweils in `hypothesen.md`

## Was diese Bestätigung leisten soll, und was nicht
- **Ziel:** Halten die E-025-Befunde auf neuen Belegen?
  - Sonnet bestätigt unbelegten Erfolg öfter als Haiku.
  - Norm und dritte Antwort senken das bei Sonnet.
  - Die dritte Antwort kostet Haiku bei voller Evidenz Treffer.
- **Nicht Ziel:**
  - Übertragung auf echte Wave-Evidenz. Der Auszug ist konstruiert.
  - Neue Faktoren. Design und Material bleiben bewusst unverändert, damit die Bestätigung unter denselben Bedingungen misst wie die Entdeckung.

## Design (unverändert aus E-025)
- **Material:** Generator v4.3 unverändert, **Seeds 9000–9015** (frisch, in keinem Experiment benutzt), 192 Belege.
- **Darstellungen:** VOLL (alle drei Kanäle) und AUSZUG (`e025.excerpt`, ein Kanal ohne jede Zeile mit Fehlerspur).
- **Faktoren:** Evidenznorm (N) × dritte Antwort "not established" (T), Selbstauskunft immer dabei. 8 Zellen, keine Werkzeuge, ein Aufruf je Prüfung.
- **Prompts:** dieselbe Funktion wie in E-025 (`orglab.e025.build_prompt`). Ein Test prüft, dass E-025 und E-026 Zeichen für Zeichen dieselben Prompts bauen (`tests/test_e026.py`). Wortlaut in `dryrun.md`.
- **Umfang:** 192 × 8 × 2 = **3.072 Prüfungen**, geschätzt etwa 18 $.

### Weg, Modell, Einstellung (Regel 11)
- OpenRouter/API: `anthropic/claude-sonnet-5.5` und `anthropic/claude-haiku-5.5`
- Gesetzt: `max_tokens` 4000
- Weggelassen: `reasoning` (adaptives Denken), `temperature`, `top_p`, `seed`

## Vorhersagen (gerichtet; BH über die vier)
Die Vorhersagewerte liegen bei etwa der Hälfte der E-025-Werte, weil entdeckte Effekte beim Nachmessen fast immer schrumpfen.

| Nr | Hypothese | Kontrast (Einheit: Beleg) | Vorhersage | E-025 |
|---|---|---|---|---|
| **B1** | H-042 | Bestätigung im AUSZUG ohne Norm und ohne dritte Antwort: Sonnet − Haiku, gepaart je Beleg | ≥ +0,08 | +0,21 |
| **B2** | H-041 | Sonnet: Senkung dieser Bestätigung durch die Evidenznorm (N0 − N1 im AUSZUG, Mittel über T) | ≥ +0,05 | +0,115 |
| **B3** | H-041 | Sonnet: Senkung durch die dritte Antwort (T0 − T1 im AUSZUG, Mittel über N) | ≥ +0,05 | +0,115 |
| **B4** | H-041 (Preis) | Haiku: Trefferquote bei voller Evidenz ohne Norm, T0 − T1 (positiv = die dritte Antwort kostet Treffer) | ≥ +0,08 | +0,22 |

- **Entscheidungsregel** (wie E-024):
  - zweiseitiges 95-%-KI per Bootstrap über Belege
  - q aus einseitigem Bootstrap-p ("Mittel > 0"), BH über B1–B4
  - **bestätigt** = untere Grenze > 0 und q ≤ 0,05. Mit dem Zusatz "Vorhersagewert nicht ausgeschlossen", wenn die obere Grenze ≥ Vorhersagewert, sonst "aber kleiner als vorhergesagt".
  - **praktisch null (widerlegt)** = obere Grenze < 0,02
  - **Vorhersagewert ausgeschlossen (widerlegt)** = obere Grenze < Vorhersagewert, ohne Nachweis
  - sonst **nicht entschieden**
- **Ein Befund gilt als bestätigt**, wenn sein Etikett mit "BESTÄTIGT" beginnt.
- **Rechnung je Zuordnung:** Weil B1 ein Modellkontrast ist, rechnet die Auswertung verblindet beide Zuordnungen vollständig: "Arm A = Sonnet" und "Arm B = Sonnet". Erst nach dem Entblinden gilt die richtige (wie E-024 mit Haiku als Ziel).
- **Deskriptiv:**
  - Bestätigung im AUSZUG je Modell (K0)
  - Haikus R1/R2 (in E-025 am Boden)
  - Sonnets Preis bei voller Evidenz
  - Anteile "not established"
  - Ergebnisse je Zelle und Domäne

## Manipulationscheck (Regel 10)

### Rechenbar (beide Rechner rechnen sie aus den Daten, das Gate vergleicht)
1. **Ausfälle:** höchstens 5 % je Zelle und Modell (gezählt wird nur reguläres Ende mit lesbarem JSON).
2. **VOLL informativ:** Trefferquote in D0-N0-T0 ≥ 0,80 je Modell.
3. **AUSZUG uninformativ:** Bestätigungsrate Ok − kaputt im Betrag ≤ 0,15. Je Modell, gepoolt über alle vier AUSZUG-Zellen, auf vollständigen Belegen.
4. **Norm und dritte Antwort standen wirklich im Prompt:**
   - Jede Zeile trägt `norm_im_prompt` und `dritte_antwort_im_prompt`, gelesen aus dem tatsächlich gesendeten Prompt.
   - Beide müssen in jeder Zeile zum Zellnamen passen.
   - **Neu gegenüber E-025.** Dort war dieser Check nur als Code-Test formuliert und deshalb für Rechner B nicht nachprüfbar (Schlichtung P-003, Neo: "kein Check im gleichen Sinne").

### Bescheinigt (der Harness prüft sie in eigenen Gates, die Rechner prüfen sie nicht)
- Code-Tests grün (Gate FESTLEGEN), darunter "E-026 baut dieselben Prompts wie E-025".
- Fremdkontrolle über den Schwellen (Gate MATERIAL).

Scheitert ein rechenbarer Check bei einem Modell, sind alle Kontraste nur deskriptiv.

## Analyse-Freiheitsgrade (vorab)
- Bootstrap 5.000 Ziehungen, Perzentil wie E-024.
- Startwerte: KI B1–B4 = 441–444, p B1–B4 = 451–454, deskriptiv 445–449.
- Je (Modell, Beleg, Zelle) zählt der letzte Datensatz. Ausfälle werden nicht wiederholt.
- **Ein Beleg zählt nur, wenn er in beiden Modellen in allen 8 Zellen gezählt ist** (wie E-025 nach der Kritik). Mindestens 144 vollständige Belege (75 %), sonst nur deskriptiv.
- Jeder Beleg ist gleich gewichtet.
- Bei T0 gilt "not established" als Nicht-Bestätigung. Für die Trefferquote gilt "not established" als nicht getroffen.

## Teststärke (`python -m orglab.e026 power`, 30 Durchläufe, 1.000 Ziehungen)
- **Annahme:** halbierte E-025-Effekte. Sonnet bestätigt den Auszug in 11,5 %, Haiku in 1 %. Haikus "not established" bei voller Evidenz liegt bei 11 %, Sonnets bei 3 %.
- **Power für "bestätigt":** B1 1,00, B2 1,00, B3 1,00, B4 0,97.

## Material (Regeln 12, 17), vor dem Pilot
- **Code-Tests:**
  - Kein Auszug enthält die Fehlerspur seines Belegs.
  - Die Zeilenarten im Auszug hängen nicht an der Wahrheit (`tests/test_e025.py`, gilt für alle Seeds desselben Generators).
- **Fremdkontrolle** (`openai/gpt-6.1-sol`, `effort: high`): 48 Belege, geschichtet, je VOLL und AUSZUG.
  - VOLL: Übereinstimmung ≥ 90 %, entscheidbar.
  - AUSZUG: "nicht entscheidbar" ≥ 90 %.
- **Regel für Abweichungen:**
  - Rechnet der Generator nachweislich falsch, wird repariert (dann neue Präregistrierung).
  - Sonst wird der Beleg vorab als Grenzfall ausgeschlossen, höchstens 10 %.
  - Jede Einordnung steht im Ledger, Neo prüft sie.

## Pilot (nur Technik)
- Seeds 1702–1703 (frisch), beide Modelle, 384 Prüfungen.
- Kriterien: Ausfälle ≤ 5 % je Zelle, Fehlerspur vollständig, Prompt-Flags gesetzt. Fehlerraten werden nicht angesehen.

## Verblindung (Regel 20)
- Feld `model`, Arme Sonnet und Haiku.
- Entfernt werden: `completion_tokens`, `cost_usd`, `final`, `error`, `answer_chars`.
- Die Prompt-Flags bleiben drin. Sie hängen an der Zelle, nicht am Modell.
- **Entblindet wird erst nach Neos Freigabe** (Postfach, unumkehrbar), nach dem Außenanker per Git-Tag.

## Doppelte Buchführung (Regel 19) und Kritik (Regel 18)
- **Rechner A:** `orglab.e026 blind-json` auf der verblindeten Kopie.
- **Rechner B:** `openai/gpt-6.1-sol` schreibt die Auswertung nur aus dieser Präregistrierung und drei verblindeten Zeilen neu. Er bekommt die bescheinigten Checks vom Harness als festgestellt mitgeteilt.
- **Gate:**
  - Schätzer ± 0,0005, KI-Grenzen ± 0,02, gleiche Entscheidungen.
  - Bei Widerspruch wird nicht entblindet, die Schlichtung macht Neo.
- **Kritik:**
  - `google/gemini-4-argon` liest diese Präregistrierung vor dem Pilot.
  - Meldet er Blockierendes, wird einmal nachgebessert (mit Begründung), dann erneut geprüft.
  - Blockiert er danach wieder, kein Hauptlauf.
  - Regel 18 verlangt einen Kritiker aus anderer Familie. Gemini erfüllt das, Grok ist hier nicht vorgesehen (sparsam, Session-Limits).

## Abbruch und Kosten
- Kostenstopp 60 $ im Code, 80 $ im Harness. Geschätzt etwa 18 $.
- Ausfälle > 5 % in einer Zelle: Stopp.
- Fremdkontrolle unter den Schwellen nach einer Nachbesserung: kein Hauptlauf.

## Prävalenz (Regel 14)
- **Rechenbeispiel:** Bei 5 % kaputter Arbeit fallen von Sonnets Bestätigungen auf unbelegter Evidenz rund 95 % zufällig auf funktionierende Arbeit.
- Berichtet werden je 1.000 Prüfungen mit unbelegter Evidenz die erwarteten übersehenen Fehler, mit und ohne Gegenmittel.

## Offene Schwächen
- Eine Modellfamilie bei den Prüfern.
- Der Auszug ist konstruiert. Domänen unterscheiden sich stark (E-025: Rechnungsversand 48 %, Datenbereinigung 0 % bei Sonnet).
- B4 misst einen Preis, der in E-025 nur explorativ gesehen wurde. Das ist ein Grund mehr, ihn hier vorab festzulegen.
- Kein A/A-Test in diesem Design.

## Daten und Definitionen (für die Nachrechnung; ergänzt nach Kritik E-026-1, vor dem Pilot)
- **Eine Zeile je (Modell, Beleg, Zelle).** Felder, die nach der Verblindung bleiben:
  - Zuordnung: `model` (A/B), `id`, `seed`
  - Zelle: `cell` (z. B. `D1-N0-T1`), dazu `D`, `N`, `T` als 0/1
  - Beleg: `truth`, `kind`, `domain`, `fault`, `primary`, `subtlety`
  - Urteil: `verdict`, `confidence`, `parse_ok`, `finish_reason`
  - Prompt: `norm_im_prompt`, `dritte_antwort_im_prompt`
- **Kodierung der Faktoren:**
  - `D1` = AUSZUG, `D0` = VOLL
  - `N1` = mit Evidenznorm, `N0` = ohne
  - `T1` = "not established" erlaubt, `T0` = nur true/false
- **Gezählt** wird ein Urteil genau dann, wenn `verdict` nicht null ist, `parse_ok` wahr ist und `finish_reason` "stop" oder "end_turn" ist.
- **Ausfall** ist jede geplante Prüfung, die so nicht gezählt ist. Die Ausfallquote je Zelle und Modell ist 1 − (gezählte Prüfungen / Zahl der Belege dieses Modells), berechnet vor dem Ausschluss unvollständiger Belege. `final` und `error` braucht man dafür nicht.
- **Bestätigung** = `verdict` ist true. **Treffer** = `verdict` gleich `truth` ("not established" ist nie ein Treffer). **Ok-Beleg** = `truth` true, **kaputt** = `truth` false.
- **Je Beleg** werden zuerst die Mittel über die genannten Zellen gebildet, dann über Belege gebootstrappt:
  - K0 = Bestätigung in D1-N0-T0
  - R1 = Mittel(D1, N0) − Mittel(D1, N1), über T gemittelt
  - R2 = Mittel(D1, T0) − Mittel(D1, T1), über N gemittelt
  - KV = Treffer(D0-N0-T0) − Treffer(D0-N0-T1)
  - B1 = K0(Ziel) − K0(Vergleich) auf den gemeinsamen Belegen
- **Bootstrap:**
  - `random.Random(Startwert)`, je Ziehung `rng.choices(werte, k=n)` über die nach `id` sortierten Belegwerte, 5.000 Ziehungen
  - KI = sortierte Ziehungsmittel an den Indizes ⌊0,025·B⌋ und ⌊0,975·B⌋−1
  - **Einseitiges p** = Anteil der Ziehungsmittel ≤ 0, ohne Korrektur (+1) und ohne verschobene Nullverteilung
  - q = BH über B1–B4 innerhalb einer Zuordnung

## Antworten auf die Kritik vor dem Start (Gemini 4 Argon, Lauf E-026-1, 25.10.)
Der Kritiker meldete fünf blockierende Punkte. Nach der Regel wird einmal nachgebessert, dann prüft er erneut (Lauf E-026-2).
1. **Ausfälle seien aus den verblindeten Daten nicht berechenbar.** Teilweise berechtigt: Die Präregistrierung nannte die verbleibenden Felder nicht. Die Ausfälle sind über `verdict`, `parse_ok` und `finish_reason` berechenbar, und die bleiben. **Präzisiert** (Abschnitt "Daten und Definitionen").
2. **Kodierung von N und T unklar.** Berechtigt. **Präzisiert:** N1/T1 = vorhanden bzw. erlaubt.
3. **Spalten und Definitionen von Bestätigung, Treffer und Zellen fehlen.** Berechtigt. **Ergänzt.**
4. **Die Verblindung sei durch erwartbare Muster zu brechen.** Formal richtig, **nicht geändert**, Begründung:
   - Wie in E-024 und E-025 als Grenze benannt.
   - Verblindung schützt Ermessensentscheidungen, und hier gibt es keine: Alle Kontraste, Etiketten und Ausschlüsse rechnet eingefrorener Code, ein Fremdmodell rechnet nach, entblindet wird erst nach dem Gate und dem Außenanker.
5. **Einseitiges Bootstrap-p nicht eindeutig.** Berechtigt. **Präzisiert:** Anteil der Ziehungsmittel ≤ 0, ohne +1, ohne Verschiebung (so rechnet der Code seit E-020).

Kleine Punkte ohne Änderung:
- "Bestätigt, aber kleiner als vorhergesagt": vorab so festgelegt wie in E-024, mit Größenangabe im Ergebnis.
- Ausschluss bis 10 % nach der Fremdkontrolle: feste Regel, jede Einordnung im Ledger, Neo prüft sie.
- Antworten ohne `seed`: weggelassene Parameter sind dokumentiert, und der Harness zeichnet jede Antwort auf.

## Abweichungen (nach Start)
-
