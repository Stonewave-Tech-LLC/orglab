# E-026: Bestätigung "Glückliches Vertrauen" (H-041, H-042) – Ergebnis

- **Datum:** 2026-10-25. Hauptlauf am Nachmittag, entblindet nach Neos Freigabe.
- **Stufe: Bestätigung.** Frische Seeds 9000–9015, vorab festgelegte gerichtete Vorhersagen, verblindete Auswertung, doppelte Buchführung, alles durch den research-harness erzwungen (Lauf E-026-2).
- **Weg, Modell, Einstellung:**
  - OpenRouter/API, `anthropic/claude-sonnet-5.5` (Ziel) und `anthropic/claude-haiku-5.5` (Vergleich)
  - `max_tokens` 4000; ohne `reasoning`, `temperature`, `top_p` und `seed`
  - ein Aufruf je Prüfung, keine Werkzeuge
  - Prompts Zeichen für Zeichen wie E-025 (Test). Material v4.3 unverändert, Code eingefroren bei orglab-Commit `f9be353`.
- **Umfang:** 3.072 Prüfungen, 1 Ausfall, **191 von 192 Belegen** vollständig (`research-ok_noisy-9012` fällt nach Regel heraus). Kosten 18,74 $ für den Lauf, dazu 0,05 $ für den ersten, vom Kritiker gestoppten Lauf.
- **Rohdaten:** `daten/E-026-bestaetigung-vertrauen/` (Kopien der Harness-Artefakte, Hashes in `herkunft.md`)
- **Auswertung:** `auswertung.md` (vom Harness erzeugt), `transkripte.md` (Außenanker)

## Kurz
**Alle vier vorab festgelegten Vorhersagen sind auf frischen Seeds bestätigt.** Die Effekte sind so groß wie in der Entdeckung (E-025) oder größer, nicht geschrumpft.
1. **Sonnet bestätigt Erfolg, den die Evidenz nicht belegt, deutlich öfter als Haiku:** 27,7 % gegen 5,2 % (B1, H-042).
2. **Die Evidenznorm senkt das bei Sonnet** (B2), **ebenso die dritte Antwort "not established"** (B3). Beide drücken Sonnets Fehlbestätigungen von 28 % auf 0–0,5 %.
3. **Die dritte Antwort kostet Haiku bei voller Evidenz Treffer:** Die Trefferquote fällt von 94 % auf 71 % (B4). Haiku zieht sich auch bei entscheidbarer Evidenz zu 28 % auf "not established" zurück.

## Vorab festgelegte Vorhersagen (Ziel Sonnet, Vergleich Haiku; BH über vier)

| Nr | Kontrast (Einheit: Beleg) | **E-026** [95-%-KI] | Etikett | Vorhersage | E-025 |
|---|---|---|---|---|---|
| **B1** | Bestätigung im AUSZUG ohne Norm und ohne dritte Antwort: Sonnet − Haiku | **+0,225** [+0,168; +0,288] | BESTÄTIGT | ≥ +0,08 | +0,21 |
| **B2** | Sonnet: Senkung durch die Evidenznorm | **+0,136** [+0,105; +0,168] | BESTÄTIGT | ≥ +0,05 | +0,115 |
| **B3** | Sonnet: Senkung durch die dritte Antwort | **+0,141** [+0,110; +0,175] | BESTÄTIGT | ≥ +0,05 | +0,115 |
| **B4** | Haiku: Trefferquote bei voller Evidenz ohne Norm, T0 − T1 | **+0,230** [+0,168; +0,293] | BESTÄTIGT | ≥ +0,08 | +0,22 |

- Alle Etiketten lauten "BESTÄTIGT (Vorhersagewert nicht ausgeschlossen)", alle q < 0,001.
- **Rechner A und B** stimmen in allen Schätzern, Intervallen und Etiketten exakt überein.
- **Im Status-Register des Harness** stehen C-E026-B1 bis C-E026-B4 als **belegt**. Es ist der erste Befund, der dort diesen Status trägt.

**Deskriptiv:**

| | Sonnet | Haiku |
|---|---|---|
| Bestätigung im AUSZUG ohne Norm und ohne dritte Antwort (K0) | 0,277 [0,215; 0,340] | 0,052 [0,026; 0,084] |
| Senkung durch Norm / dritte Antwort | siehe B2/B3 | +0,026 / +0,026 |
| Trefferverlust durch die dritte Antwort bei voller Evidenz | +0,042 [+0,016; +0,073] | siehe B4 |

## Manipulationscheck (Regel 10), bestanden

**Rechenbar**, von beiden Rechnern aus den Daten berechnet:
- **Ausfälle:** höchstens 0,5 % je Zelle.
- **VOLL informativ:** Sonnet 100 %, Haiku 94 % Treffer (N0T0).
- **AUSZUG uninformativ:** Bestätigung Ok − kaputt nahe 0. Von Sonnets 53 Bestätigungen auf dem Auszug fielen 28 auf kaputte Belege.
- **Norm und dritte Antwort standen im gesendeten Prompt** genau in den Zellen, deren Name es sagt. Neu: aus dem tatsächlichen Prompttext mitgeschrieben, damit Rechner B es nachrechnen kann (Lehre aus der E-025-Schlichtung).

**Bescheinigt**, vom Harness in eigenen Gates geprüft und Rechner B als festgestellt mitgeteilt:
- Code-Tests grün, darunter "E-026 baut dieselben Prompts wie E-025"
- Fremdkontrolle VOLL 45 von 48, AUSZUG 48 von 48 nicht entscheidbar

## Schlichtung (Neo, 25.10.)
- **Was abwich:** Das Gate stoppte, obwohl alle Zahlen und Etiketten gleich waren. Abweichend war nur die Zahl "vollständige Seeds": A zählt 15 (Seeds mit allen 12 Belegen), B zählt 16 (beobachtete Seeds).
- **Entscheidung:** Neo: **"A gilt. Die Seed-Zahl ist in E-026 nicht präregistriert, entscheidend sind 191 vollständige Belege."**
- **Lehre für den Harness:** Das Gate darf nur vergleichen, was die Präregistrierung als Entscheidungsgröße nennt. Ein zweiter Fehler wurde dabei gefunden und behoben: Die Schlichtung hätte an derselben Zahl scheitern können.

## Kritik vorab (Regel 18)
- Gemini 4 Argon stoppte den ersten Lauf (E-026-1) mit fünf Punkten. Vier betrafen die Nachrechenbarkeit durch Rechner B: verbleibende Felder, Kodierung von N und T, Definitionen, p-Wert. Sie wurden mit einem Abschnitt "Daten und Definitionen" beantwortet, der Code blieb unverändert.
- Der fünfte (Verblindung durch Muster brechbar) wurde begründet abgelehnt.
- Der zweite Lauf ging ohne Blockierendes durch.

## Explorativ (nicht vorab festgelegt)
1. **Domäne:**
   - Sonnets Fehlbestätigungen liegen bei 50 % im Rechnungsversand ("250 OK queued"), 33 % beim Deployment ("pm2 online") und 0 % bei der Datenbereinigung.
   - Haiku bestätigt nur im Rechnungsversand (16 %).
   - Das gleiche Muster wie in E-025.
2. **Die Norm allein macht aus Raten "kaputt":** Mit Norm, aber ohne dritte Antwort, urteilen beide Modelle auf dem Auszug fast immer "kaputt" (Sonnet 0,5 % Bestätigung). Bei Ok-Belegen ist das ein Fehlalarm im binären Sinn. Erst die dritte Antwort macht das Urteil ehrlich.
3. **Sonnet zahlt einen kleinen Preis für die dritte Antwort:** −4 Prozentpunkte Treffer bei voller Evidenz, gegen −23 bei Haiku.

## Transkripte (Außenanker, Regel 7)
- **Ziehung:** Neo hat den Zufall gezogen ("Horizon"). Je Modell zwei Verläufe, darunter je ein Fehler im Sinne dieses Experiments. Der Fehlerbegriff kam diesmal aus der Präregistrierung: Bestätigung auf dem Auszug oder falsches Urteil bei voller Evidenz.
- **Fall 3** zeigt den Befund selbst:
  - Sonnet zählt alle Lücken auf (kein Empfänger, keine Zustellung, "queued" ist nicht "zugestellt").
  - Dann schließt es: "a queue acceptance with the correct attachment usually means the send worked", und urteilt "funktioniert". Die Rechnung war kaputt.
- **Neo:** "Gelesen, passt." Gemessen 2,0 Minuten.

## Prävalenz (Regel 14)
- **Ohne Gegenmittel:** Bei 5 % kaputter Arbeit und Sonnets 28 % Bestätigung auf unbelegter Evidenz gilt je 1.000 Prüfungen mit unbelegter Evidenz:
  - etwa 263 Bestätigungen fallen zufällig auf funktionierende Arbeit
  - etwa 14 fallen auf kaputte Arbeit, das sind übersehene Fehler
- **Mit Norm oder dritter Antwort:** 0 bis 1.
- Das Muster ist im Alltag unsichtbar, weil fast jede dieser Bestätigungen zufällig stimmt (H-041).

## Grenzen
- **Eine Modellfamilie** (Anthropic). Ein Aufbau: ein Prüfer, ein Beleg, keine Werkzeuge, kein Zeitdruck.
- **Konstruierter Auszug:** Er enthält per Konstruktion keine belegende Zeile. Wie oft echte Wave-Evidenz so dünn ist, ist offen. Die starke Domänenabhängigkeit zeigt, dass es darauf ankommt, welche Zeile wie Erfolg *aussieht*.
- **Die Verblindung war schwach:** Das Muster verriet die Zuordnung, wie in E-024 und E-025. Die Entscheidungen standen aber vorher im Code fest, und die verblindete Auswertung war vor dem Entblinden außen verankert (`anker/378-8ee8542cc0cb`).
- **H-042 ist in zwei getrennten Aufbauten bestätigt** (E-024: Maßstab fehlt; E-026: Evidenz fehlt). Ein gemeinsames Design, das beide Fehlerbilder direkt gegeneinander stellt, fehlt.

## Was das heißt (Status: bestätigt für Sonnet 5.5 und Haiku 5.5 in diesem Aufbau)
1. **Für Wave:** Der Wave-Prüfer (Sonnet) bestätigt in gut einem Viertel der Fälle Erfolg, den die vorgelegte Evidenz nicht trägt. Bei realistischer Prävalenz sieht man das nie, und bei kaputter Arbeit ist es ein übersehener Fehler.
2. **Gegenmittel für Sonnet:** Die erlaubte Antwort "not established" senkt das auf praktisch null, bei kleinem Preis bei voller Evidenz (−4 Prozentpunkte). Eine Evidenznorm im Auftrag wirkt ebenso, macht aus unbelegten Fällen aber "kaputt" statt "nicht belegt".
3. **Kein Universalrezept:** Bei Haiku kostet dieselbe dritte Antwort 23 Prozentpunkte Treffer bei voller Evidenz. Harness-Regeln sind hier nachweislich modellabhängig, und zwar für diesen einen Faktor in diesem Aufbau.
4. **Wer scheitert, hängt am Fehlerbild:** Fehlt der Maßstab, übersieht Haiku mehr (E-024). Fehlt die Evidenz, bestätigt Sonnet mehr (E-025/E-026).

## Checkliste
- [x] repliziert auf frischen Seeds (E-025 → E-026)
- [ ] A/A und Positivkontrolle: nicht Teil des Designs
- [x] Manipulationscheck bestanden, alle rechenbaren Checks von beiden Rechnern nachgerechnet
- [x] vorab festgelegt: Präregistrierung mit Neos Freigabe, Prompts identisch mit E-025, Code `f9be353`
- [x] Weg, Modell, Einstellung dokumentiert
- [x] Ground Truth fremdkontrolliert: VOLL 45/48, AUSZUG 48/48 nicht entscheidbar
- [x] Analyse-Einheit Beleg, B1 gepaart
- [x] von einem Fremdmodell nachgerechnet, Zahlen und Etiketten gleich
- [x] verblindet ausgewertet, verankert, erst nach Neos Ja entblindet
- [x] Prävalenz berichtet
- [x] Kritiker vorab (Gemini), zweiter Lauf ohne Blockierendes
- [x] Transkripte gelesen (Neo, geschichtete Ziehung mit Fehlerbegriff aus der Präregistrierung)
- [x] mit einem Befehl reproduzierbar (`harness experiment start/schlichten/entblinden`)
