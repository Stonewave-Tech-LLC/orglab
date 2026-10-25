# E-025: Glückliches Vertrauen (H-041) – Ergebnis

- **Datum:** Hauptlauf in der Nacht 24./25.10.2026, entblindet am 25.10. nach Neos Freigabe.
- **Stufe: Entdeckung.** Alles hier ist ein **Kandidat**, kein Befund. Eine Bestätigung braucht einen eigenen Lauf auf frischen Seeds. Der höchste Status ist "gestützt (Entdeckung)".
- **Erstes Experiment, das vollständig durch den research-harness lief** (`research-harness/laeufe/E-025/`, Lauf E-025-3). Jede Phase ging durch ein Gate im Code, und das Ledger hält alles fest. Neo hat nur geschlichtet, das Entblinden freigegeben und die Stichprobe gelesen.
- **Weg, Modell, Einstellung:**
  - OpenRouter/API, `anthropic/claude-sonnet-5.5` und `anthropic/claude-haiku-5.5`
  - `max_tokens` 4000; ohne `reasoning`, `temperature`, `top_p` und `seed`
  - ein Aufruf je Prüfung, keine Werkzeuge
  - Material v4.3 unverändert, Code eingefroren bei orglab-Commit `7b069b0`
- **Umfang:** 3.072 Prüfungen, 7 Ausfälle (gezählt wird nur ein reguläres Antwortende mit lesbarem JSON). **191 von 192 Belegen** sind in beiden Modellen vollständig, `research-fail_subtle-8009` fällt nach Regel heraus. Kosten 18,59 $ für den ganzen Lauf, davon 16,06 $ Hauptlauf.
- **Rohdaten:** `daten/E-025-glueckliches-vertrauen/` (Kopien der Harness-Artefakte, Hashes in `herkunft.md`)
- **Auswertung:** `auswertung.md` (vom Harness erzeugt), `transkripte.md` (Außenanker-Stichprobe)

## Kurz
1. **Sonnet bestätigt Erfolg, den die Evidenz nicht belegt, in 23 % der Fälle.** Haiku tut das in 2 %. Das glückliche Vertrauen aus H-041 zeigt sich hier also beim Wave-Modell. Das schwächere Modell ist das vorsichtigere, umgekehrt zu E-024.
2. **Beide Mittel beseitigen es vollständig.** Sowohl die Evidenznorm im Auftrag als auch die erlaubte dritte Antwort "not established" senken Sonnets Fehlbestätigungen auf dem Auszug von 23 % auf 0 %. Jedes Mittel wirkt allein schon voll.
3. **Die vorhergesagten Größen wurden nicht erreicht.** Vorhergesagt waren mindestens 30 % Fehlbestätigungen ohne Mittel und Senkungen um mindestens 15 Prozentpunkte. Gemessen sind 23 % bzw. 11,5 Prozentpunkte. Nach der vorab festgelegten Regel steht deshalb bei beiden Modellen der Vermerk **"Prämisse nicht gegeben"**, bei Sonnet knapp (obere Grenze 0,293 statt 0,30).
4. **Die dritte Antwort hat bei Haiku einen Preis** (explorativ): Auch bei *voller* Evidenz sagt Haiku zu 18–26 % "not established".

## Vorab festgelegte Vorhersagen (BH über die vier Primärtests R1, R2 je Modell)

| Nr | Kontrast (nur AUSZUG) | Sonnet 5.5 [95-%-KI] | Etikett | Haiku 5.5 [95-%-KI] | Etikett |
|---|---|---|---|---|---|
| **R1** | Senkung durch die Evidenznorm (N0 − N1, Mittel über T) | **+0,115** [+0,086; +0,147], q < 0,001 | gestützt, aber kleiner als vorhergesagt | +0,010 [+0,003; +0,021], q = 0,020 | gestützt, aber kleiner als vorhergesagt |
| **R2** | Senkung durch die dritte Antwort (T0 − T1, Mittel über N) | **+0,115** [+0,086; +0,147], q < 0,001 | gestützt, aber kleiner als vorhergesagt | +0,010 [+0,003; +0,021], q = 0,020 | gestützt, aber kleiner als vorhergesagt |
| K0 | Bestätigung im AUSZUG ohne Norm und ohne dritte Antwort (Prämisse, Vorhersage ≥ 0,30) | **0,230** [0,173; 0,293] | deskriptiv, Prämisse nicht gegeben | 0,021 [0,005; 0,042] | deskriptiv, Prämisse nicht gegeben |
| K3 | Kosten im VOLL bei Ok-Belegen, Bestätigung N1T1 − N0T0 (Vorhersage ≥ −0,05) | 0,000 [0,000; 0,000] | deskriptiv | +0,031 [−0,021; +0,083] | deskriptiv |

- **R1 und R2 sind gleich, weil bestätigt nur in einer Zelle wurde:** ohne Norm *und* ohne dritte Antwort. In den drei anderen AUSZUG-Zellen bestätigte keines der Modelle ein einziges Mal. Beide Kontraste sind dann genau K0/2.
- **Die Etiketten** gelten nach Neos Schlichtung (siehe unten). Sie kommen von Rechner A, die Zahlen von Rechner A und B gemeinsam.
- **Lesart von "Prämisse nicht gegeben":** Auf diesem Material bestätigen die Modelle auch ohne Hilfe seltener als vorhergesagt. Wie stark Norm und dritte Antwort wirken *können*, zeigt der Lauf deshalb nur bis zu dieser Decke. Ein "kleiner als vorhergesagt" heißt hier nicht, dass die Mittel schwach sind, sondern dass es weniger zu senken gab.

## Manipulationscheck (Regel 10), bestanden

| Modell | Ausfälle (max. je Zelle) | Trefferquote VOLL (N0T0) | AUSZUG: Bestätigung ok − kaputt |
|---|---|---|---|
| Sonnet 5.5 | 0,5 % | 98,4 % | −0,001 |
| Haiku 5.5 | 0,5 % | 95,8 % | +0,005 |

- **Der Auszug verrät die Wahrheit nicht.** Sonnet bestätigt Ok- und kaputte Belege gleich oft (22,9 % gegen 23,2 %). Die Fremdkontrolle (GPT) nannte 48 von 48 Auszügen "nicht entscheidbar".
- **Die volle Evidenz ist entscheidbar.** Fremdkontrolle 45 von 48. Die drei Abweichungen sind dokumentiert, kein Generatorfehler.
- **N und T:** Die Code-Tests liefen im Harness-Gate FESTLEGEN und waren grün.

## Schlichtung (Neo, 25.10.)
- **Was strittig war:** Rechner A (dieser Code) und Rechner B (GPT-6.1 Sol, nur aus der Präregistrierung neu geschrieben) stimmten in allen Zahlen überein, die größte Abweichung war 0,003 an einer KI-Grenze.
- **Warum B abwich:** B wertete Manipulationscheck 4 ("N und T: per Code-Test") "fail-closed" als nicht bestanden, weil er aus den Daten nicht prüfbar ist, und meldete deshalb alles deskriptiv.
- **Entscheidung:** Neo: **"A gilt"**. Die Code-Tests sind im Ledger belegt.
- **Lehre:** Ein Check, den Rechner B aus den Daten nicht nachrechnen kann, ist kein Check im gleichen Sinn wie die rechenbaren (Neo, im Fragekanal festgehalten). Vorschlag für den Harness v2: solche Checks als Daten mitschreiben, also was im gesendeten Prompt tatsächlich stand, oder als bescheinigte Checks getrennt führen.

## Explorativ (nicht vorab festgelegt)

**Ergebnisse je Zelle** (191 Belege je Modell):

| Zelle | Sonnet bestätigt / "not est." / richtig | Haiku bestätigt / "not est." / richtig |
|---|---|---|
| VOLL N0T0 | 0,52 / – / 0,98 | 0,46 / – / 0,96 |
| VOLL N0T1 | 0,51 / 0,05 / 0,94 | 0,35 / **0,26** / 0,74 |
| VOLL N1T0 | 0,51 / – / 0,99 | 0,51 / – / 0,98 |
| VOLL N1T1 | 0,51 / 0,07 / 0,93 | 0,49 / **0,18** / 0,81 |
| AUSZUG N0T0 | **0,23** / – / 0,50 | 0,02 / – / 0,51 |
| AUSZUG N0T1 | 0,00 / 0,99 / – | 0,00 / 0,87 / – |
| AUSZUG N1T0 | 0,00 / – / 0,50 | 0,00 / – / 0,50 |
| AUSZUG N1T1 | 0,00 / 0,98 / – | 0,00 / 0,94 / – |

1. **Preis der dritten Antwort bei voller Evidenz:**
   - Haiku zieht sich auch bei entscheidbarer Evidenz oft auf "not established" zurück (18–26 %). Die Trefferquote fällt von 96 % auf 74–81 %.
   - Sonnet tut das selten (5–7 %), seine Trefferquote fällt nur auf 93–94 %.
   - Der vorab festgelegte Kostenkontrast K3 zählt nur Bestätigungen auf Ok-Belegen und übersieht diesen Preis. Das ist eine Lücke im Design.
2. **Die Norm allein macht aus Raten "kaputt":** Mit Norm, aber ohne dritte Antwort, sagen beide Modelle auf dem Auszug immer "kaputt". Das ist im Sinn der Norm (nicht gezeigt heißt nicht bestätigt), bei Ok-Belegen aber ein Fehlalarm. Erst die dritte Antwort macht das Urteil ehrlich.
3. **Domäne:**
   - Sonnets Fehlbestätigungen auf dem Auszug liegen bei 48 % im Rechnungsversand ("250 OK queued" wird als Versand gelesen), 20 % beim Deployment ("pm2 online") und 0 % bei der Datenbereinigung.
   - Haiku bestätigte nur im Rechnungsversand (6 %).
4. **Jede Fehlbestätigung ist ein Münzwurf:** Von Sonnets 44 Bestätigungen auf dem Auszug fielen 22 auf kaputte Belege, Median-Konfidenz 0,6.
5. **Haiku denkt länger:** Median 948 Completion-Tokens gegen 577 bei Sonnet.

## Prävalenz (Regel 14)
- **Rechenbeispiel:** Bei 5 % kaputter Arbeit (Wave-nah) und Sonnets 23 % Bestätigung auf unbelegter Evidenz gilt pro 1.000 Prüfungen mit unbelegter Evidenz:
  - rund 218 Bestätigungen fallen zufällig auf funktionierende Arbeit
  - rund 12 fallen auf kaputte Arbeit
- Das Muster ist im Alltag unsichtbar, weil das Urteil fast immer stimmt. Genau das sagt H-041. Die 12 übersehenen Fehler sind die Kosten.
- Mit Norm oder dritter Antwort wären es auf diesem Material 0.

## Verblindung (Regel 20) und doppelte Buchführung (Regel 19)
- Verblindet hat der Harness mit versiegeltem Schlüssel (Arme A und B). Entfernt waren Tokens, Kosten, Antworttext, Fehlertext und Antwortlänge.
- Die verblindete Auswertung stand vor dem Entblinden fest und war außen verankert: Git-Tag `anker/248-4b6ede8a2792` auf GitHub. Entblindet wurde erst nach Neos Ja (P-004): **A = Haiku, B = Sonnet.**
- **Grenze:** Das Muster verriet die Zuordnung praktisch, wie in E-024. Die Entscheidungen standen aber vorher im Code fest.
- **Rechner B** hat 20 offene Entscheidungen gemeldet (`daten/.../nachrechnung/rechner_b.json`). Die wichtigste ist der Check 4, siehe Schlichtung.

## Transkripte (Außenanker, Regel 7)
- **Ziehung:** Neo hat den Zufall gezogen ("Very late"). Der Harness zog je Modell 2 Verläufe und bereitete sie lesbar auf (`transkripte.md`). Neo: "finde alle passen".
- **Grenze:** Das geschichtete Ziehen wählte als "falsch beurteilt" Fälle mit Urteil ≠ Wahrheit. Auf dem Auszug ist "not established" aber die richtige Antwort. Zwei Fälle waren deshalb irreführend als FALSCH markiert, und ein Fall des eigentlichen Befunds (Sonnet bestätigt den Auszug) war nicht dabei. Für v2 ist festgehalten: Den Fehlerbegriff legt das Experiment fest.

## Ablauf der Nacht (Ledger im Harness)
1. **E-025-1:** Der Kritiker (Gemini 4 Argon) blockierte mit vier Punkten.
   - Drei wurden umgesetzt (Vollständigkeit je Beleg statt je Seed, zwei Präzisierungen).
   - Einer wurde begründet abgelehnt.
   - Dokumentiert in `prereg.md` unter "Antworten auf die Kritik".
2. **E-025-2:** Abbruch durch einen Fehler im Harness-Executor (relativer Pfad). Behoben.
3. **E-025-3:** Alles durch bis zum Gate. Dann die Schlichtung, das Entblinden und der Außenanker.

## Grenzen
- **Eine Modellfamilie** bei den Prüfern. Design und Auszug-Konstruktion stammen von Claude, geprüft von Gemini (Kritik) und GPT (Material, Nachrechnung).
- **Der Auszug ist konstruiert und dünn.** Ob echte Wave-Evidenz so aussieht, ist offen. Die starke Domänenabhängigkeit (Rechnungsversand 48 %) zeigt: Es kommt darauf an, welche Zeile als Erfolg *aussieht*.
- **Nur ein Kontext:** ein Prüfer, ein Beleg, keine Werkzeuge, kein Zeitdruck.
- **Vorhersagen verfehlt:** K0 ≥ 0,30 und R ≥ 0,15 wurden nicht erreicht. Die Effekte sind real (q < 0,001 bei Sonnet), aber kleiner, weil weniger zu senken war.

## Was das heißt (Status: Entdeckung, Kandidaten)
1. **Für Wave:** Der Wave-Prüfer (Sonnet) bestätigt in knapp einem Viertel der Fälle Erfolg, den die vorgelegte Evidenz nicht trägt. Bei realistischer Prävalenz sieht man das nie. Kandidat, keine Wave-Regel vor einer Bestätigung.
2. **Billige Gegenmittel:** Eine erlaubte Antwort "not established" oder ein Satz Evidenznorm genügte hier, jeweils allein. Die dritte Antwort hat aber bei Haiku einen Preis bei voller Evidenz (explorativ).
3. **Modellreihenfolge:** "Schwächerer Prüfer = nachlässiger" gilt hier nicht. Wer an welcher Stelle scheitert, hängt am Fehlerbild (E-024: Maßstab fehlt; E-025: Evidenz fehlt). Neue Hypothese H-042.

## Checkliste
- [ ] repliziert auf frischen Seeds (offen: Bestätigungslauf)
- [ ] A/A und Positivkontrolle: nicht Teil des Designs
- [x] Manipulationscheck bestanden (nach Schlichtung)
- [x] vorab festgelegt: Präregistrierung, Prompts (`dryrun.md`), Code `7b069b0`, Antworten auf die Kritik vor dem Start
- [x] Weg, Modell, Einstellung dokumentiert
- [x] Ground Truth fremdkontrolliert: VOLL 45/48, AUSZUG 48/48 nicht entscheidbar
- [x] Analyse-Einheit Beleg
- [x] von einem Fremdmodell nachgerechnet, Zahlen gleich, Etiketten geschlichtet
- [x] verblindet ausgewertet, verankert, erst nach Neos Ja entblindet
- [x] Prävalenz berichtet
- [x] Kritiker vorab: Gemini, zweiter Durchlauf ohne Blockierendes
- [x] Transkripte gelesen (Neo, mit benannter Grenze der Ziehung)
- [x] mit einem Befehl reproduzierbar (`harness experiment start/schlichten/entblinden`)
