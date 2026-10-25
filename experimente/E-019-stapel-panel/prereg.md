# E-019: Stapel-Panel – Information × Stil × Erfahrung unter Aufmerksamkeitsknappheit – Präregistrierung

> **Vor dem ersten Hauptlauf committen.** Kalibrierungsläufe (Stufe 0) sind vorher erlaubt und dürfen nur die vorab festgelegte Leiter unten durchlaufen. Was danach geändert wird, steht unter "Abweichungen", mit Datum und Grund.

- **Datum:** 2026-10-22
- **Stufe:** Entdeckung, mit gerichteten Vorhersagen
- **Vorgänger:** E-017 (gleiche Faktoren, Einzelbeleg pro Aufruf). Dort ist Stufe 0 gescheitert: Sonnet 5.5 irrte bei Einzelbelegen nur zu 3–9 % (`experimente/E-017-faktorielles-panel/ergebnis-stufe0.md`).
- **Hypothesen:** H-029, H-030, H-031 (unverändert) sowie H-032 (neu, siehe unten)
- **Was sich gegenüber E-017 ändert:**
  - **Der Fehlermechanismus ist knappe Aufmerksamkeit, nicht fehlendes Wissen.** Ein Prüfer beurteilt einen **Stapel von B Belegen in einem Aufruf**, wie ein Reviewer, der eine Queue abarbeitet. Das ist realistisch für Wave/Ace und schließt an H-016 an (unter knapper Aufmerksamkeit ist Verifikation der Engpass).
  - Optional ohne Reasoning (Option D), falls die Kalibrierung das braucht. Siehe Leiter.
  - Alles andere übernimmt E-017: Generator v2 mit drei Kanälen und Spur in jedem Kanal, Faktoren, Personas, Verfahren, Rohepisoden, Primärmetrik. Die Definitionen in `experimente/E-017-faktorielles-panel/prereg.md` gelten, soweit unten nichts anderes steht.

## Neue Hypothese
- **H-032:** Fehler aus knapper Aufmerksamkeit sind zwischen Prüfern desselben Modells **schwächer korreliert** als Fehler aus fehlendem Wissen bzw. schwer lesbaren Spuren. Redundanz hilft gegen Aufmerksamkeitsfehler deshalb mehr als gegen Wissensfehler.
  - Quelle: Neo/Claude 22.10., Gegenstück zu Chen 2606.27288 und E-017 Stufe 0 (die Wissensfehler bündelten sich auf einer Spurart).
  - Hier nur **explorativ** prüfbar, siehe Sekundär 7.

## Konkrete Vorhersagen (gerichtet)

Die Kontraste, Vorhersagen V1–V7 und Widerlegungskriterien sind **identisch mit E-017**:

| Nr | Kontrast | Vorhersage |
|---|---|---|
| V1 | verschiedene Kanäle − gleicher Kanal | Δφ̄ ≤ −0,15 |
| V2 | Etiketten-Persona − neutral | Äquivalenz, 90-%-KI in [−0,10; +0,10] |
| V3 | Verfahrens-Persona − neutral | Δφ̄ ≤ −0,10, Einzelfehlerrate steigt oder bleibt gleich |
| V4 | Erfahrung disjunkt − gleich | Δφ̄ < 0 |
| V5 | Erfahrung gleich − keine | Δφ̄ ≥ 0 |
| V6 | Rangfolge | \|Δ_I\| > \|Δ_Verfahren\| > \|Δ_Erfahrung\| > \|Δ_Etikett\| ≈ 0 (deskriptiv) |
| V7 | Familie vs. Kanal | Modellwechsel senkt φ̄ weniger als Kanalwechsel |

**Zusätzlich:**
- **V8 (Position im Stapel):** Die Einzelfehlerrate steigt mit der Position im Stapel (hintere Hälfte > vordere Hälfte). Das ist ein Manipulationscheck: Wirkt Aufmerksamkeitsknappheit überhaupt?
- **Widerlegt, wenn:** die hintere Hälfte nicht höher liegt, bei KI-Obergrenze der Differenz < 0. In diesem Fall gilt der Fehlermechanismus als **nicht** Aufmerksamkeit, und alle Befunde werden entsprechend vorsichtig gedeutet.

## Design

### Material
- Generator v2 (`orglab/evidence.py`, Stand Commit a8840e7 plus Chunk-Fix), unverändert in Logik und Stellschrauben (`NOISE_BLOCKS`, `PAD_LINES`, `EXPLICIT_MODERATE=False`).
- **Hauptlauf:** Seeds 2000–2023 × 3 Domänen × 4 Arten = **288 Belege** (je 72 pro Art)
- **Kalibrierung:** Seeds 1100–1111 = 144 Belege, getrennt von E-017-Kalibrierung und Hauptlauf
- **Erfahrungspool:** Seeds 500–699 (wie E-017)

### Stapel
- Die 288 Belege werden einmal per Seed (`"E-019-stapel"`) gemischt und in **288/B Stapel** zu B Belegen geteilt. B kommt aus der Kalibrierung.
- Mischen sorgt für gemischte Domänen und Arten pro Stapel.
- Zusammensetzung **und Reihenfolge** eines Stapels sind für alle Zellen und Prüferpositionen gleich (gepaart). Damit ist die Position im Stapel kein Störfaktor zwischen Zellen.
- **Kanal je Beleg** wie in E-017: I0 → alle Prüfer denselben Kanal (Seed mod 3), I1 → Prüfer k den Kanal (k + Seed) mod 3.
- **Prompt:** Rahmen ("Du hast B abgeschlossene Arbeitsaufträge zu prüfen"), dann ggf. Persona (S1) oder Prüfverfahren (S2), dann ggf. 6 Rohepisoden (E1/E2, einmal pro Aufruf statt pro Beleg), dann die B Belege nummeriert, jeweils Auftrag und ein Kanal.
- **Antwort:**
  - S0/S1: nur ein JSON-Array `[{"item": n, "works": …, "confidence": …}, …]`
  - S2: kurze Notizen erlaubt, dann das JSON-Array als letztes
- **Parsing:** das letzte JSON-Array der Antwort. Fehlende oder ungültige Einträge fehlen, sie zählen nicht als Fehler.

### Faktoren und Arme
- **Faktoren:** I(2) × S(3) × E(3) = 18 Zellen, je 3 Prüferpositionen
- **Zusätzlich:**
  - A/A-Zelle (I0-S0-E0 nochmals)
  - Positivkontrolle (Position 3 sieht in I0-S0-E0 Kanäle ohne Fehlerspur)
  - Familienarm (Sonnet, GPT-6.1 Sol, Gemini 4 Argon; S0/E0; I0 und I1)
- **Modelle:** primär `anthropic/claude-sonnet-5.5`. Ein Haiku-Generalisierungsarm nur, wenn Haiku in der Kalibrierung auf derselben Leiterstufe im Zielbereich liegt.
- **Ein Aufruf pro Prüferposition und Stapel.**

### Umfang (bei B = 12; bei B = 8 skaliert die Aufrufzahl um 1,5)
| Teil | Rechnung | Aufrufe |
|---|---|---|
| Hauptzellen | 24 Stapel × 18 Zellen × 3 | 1.296 |
| A/A + Blind | 2 × 24 × 3 | 144 |
| Familienarm | 2 × 24 × 3 | 144, davon 96 Fremdmodelle |
| Urteile Sonnet gesamt | | ≈ 17.300 |

- **Kosten:** Schätzung ~45–60 $ (12 Belege mit ~400–700 Tokens pro Aufruf, dazu Episoden), verteilt auf 2 Tage.
- **Bestätigung durch Neo vor dem Hauptlauf**, weil das Tageslimit überschritten wird.

## Stufe 0: Kalibrierung als vorab festgelegte Leiter

Die Leiterstufen laufen in fester Reihenfolge. Die **erste Stufe, die alle Kriterien erfüllt**, wird für den Hauptlauf eingefroren.

| Stufe | Stapelgröße B | Reasoning |
|---|---|---|
| L1 | 8 | low |
| L2 | 12 | low |
| L3 | 12 | aus (Option D) |

**Je Stufe:** Sonnet, Zelle I1-S0-E0, also jede Position mit einem anderen Kanal. Jeder Kalibrierungsbeleg wird damit einmal pro Kanal beurteilt.

**Kriterien** (alle müssen erfüllt sein):
1. Einzelfehlerrate 0,10–0,40
2. Kanalbalance: Spanne der Fehlerraten über die Kanalpositionen ≤ 0,20
3. Fehlalarm- **und** Übersehensrate ≥ 0,03
4. **Neu, Lehre aus E-017:** Fehler verteilen sich. Mindestens 4 der 6 Fehlerarten haben eine Übersehensrate ≥ 0,05, und kein einzelner Beleg trägt mehr als 5 % aller Fehler.
5. Stichprobe: 10 falsch beurteilte Belege lese ich und bestätige, dass die Ground Truth stimmt. Findet sich ein Generatorfehler, wird er behoben, und **dieselbe Stufe** läuft erneut. Das zählt nicht als Leiterschritt, höchstens einmal pro Stufe.
6. Parse-Ausfall ≤ 5 % der Urteile

**Wenn keine Stufe alle Kriterien erfüllt:** kein Hauptlauf, Rücksprache mit Neo.

**Haiku:** Auf der gewählten Stufe gibt es einen Kalibrierungslauf, der nur über den Generalisierungsarm entscheidet.

Kalibrierungsdaten fließen nie in die Hauptauswertung ein.

## Metriken
- **Primär:** φ̄ je Zelle (mittlere paarweise φ der Fehlerindikatoren der 3 Positionen über alle Belege), daraus Kish-n_eff. Wie E-017.
- **Sekundär:**
  1. β und das Verhältnis β / (p₁·p₂·p₃)
  2. Panel-Fehlerrate (Mehrheit irrt)
  3. Einzelfehlerrate
  4. Escape Rate
  5. Interaktionen I×S und I×E
  6. Kalibrierung der Konfidenz
  7. **H-032, explorativ:** φ̄ der Resampling-Zelle (I0-S0-E0) im Vergleich zu E-017 Stufe 0 bzw. zu Belegen mit Wissensfehlern. Die Fehler werden nach Ursache getrennt:
     - "Spur übersehen": dieselbe Spur wird in Einzelbeurteilung ≥ 90 % erkannt, laut E-017-Kalibrierung derselben Fehlerart und Subtilität
     - "Spur schwer": < 90 %
  8. **V8 (Manipulationscheck):** Fehlerrate je Position im Stapel und Differenz hintere minus vordere Hälfte
  9. Zusatzarm Familie (2×2)
  10. Kosten

## Auswertungsplan
- Wie E-017, mit einem Unterschied: **Cluster-Bootstrap über Stapel statt über Belege** (5.000 Ziehungen). Fehler im selben Stapel hängen voneinander ab (Ermüdung, Kontext).
- BH-FDR über V1, V3, V4, V5. TOST für V2. KI für V7 und V8.
- **Effektgröße vor p.** Die Relevanzschwelle bleibt |Δφ̄| ≥ 0,10.
- **Generatorfehler-Regel** wie E-017: Belege, die über alle Zellen von ≥ 80 % der Urteile falsch beurteilt werden, prüfe ich von Hand. Ausgeschlossen werden sie nur, wenn die Ground Truth nachweislich falsch generiert ist. Die Analyse wird zusätzlich ohne Ausschlüsse berichtet.
- **A/A:** |Δφ̄| < 0,05 und KI enthält 0.
- **Positivkontrolle:** Die Fehlerrate von Position 3 steigt deutlich.
- **Transkripte:** je Zelle 2 zufällige Stapel-Antworten als Pflichtlektüre.

## Abbruchkriterien
- Gesamtkosten > 80 $ → Stopp und Rücksprache
- Parse-Ausfall > 5 % in einer Zelle → Stopp und Fix. Betroffene Zellen werden neu erhoben, die alten Daten bleiben als ungültig markiert erhalten.
- Generatorfehler in > 2 % der Belege → Stopp, neue Seeds (2100+)

## Offene Schwächen (vorab benannt)
- **Kritiker-Unabhängigkeit:** Design und Auswertung stammen von Claude, und auch die Prüfer im Hauptlauf sind Claude.
- **Erfahrung und Länge:** In E1/E2 verlängern die Episoden den Prompt und verschärfen damit die Aufmerksamkeitsknappheit. **V5 (E1 − E0) ist deshalb mit Promptlänge vermischt.** V4 (E2 − E1) ist längengleich und sauber.
- **Gleiche Reihenfolge für alle Prüfer:** Positionseffekte im Stapel treffen alle drei Prüfer gleich und können φ̄ erhöhen. Das ist ein realer Mechanismus (gleiche Queue), aber kein Kanal- oder Stileffekt. Eine Reihenfolge-Variation als eigener Faktor ist Kandidat für später.
- **Verfahrens-Personas über 12 Belege:** Möglicherweise wenden Prüfer das Verfahren nicht bei jedem Beleg an. Das wird als Transkript-Befund berichtet.

## Implementierung (vor Stufe 0)
1. `orglab/factorial.py` um einen Stapelmodus erweitern: Stapelbildung, Stapel-Prompt, Array-Parser, Kalibrierungsleiter, Lauf
2. Dry-Run aller Zellen für einen Stapel zum Gegenlesen
3. Auswertungsskript (φ̄, Kontraste, Stapel-Bootstrap) vor dem Hauptlauf, Test mit synthetischen Urteilen

## Abweichungen (nach Start)
-
- **22.10., Stufe 0 nicht erfüllt:** L1 (Lauf 2) 0,109, L2 0,102, L3 0,046. Kriterium 4 (Fehler über ≥ 4/6 Fehlerarten) wurde nie erfüllt, die Übersehen bündeln sich auf `db_down`. In L1 Lauf 1 fanden sich 3 Generatorfehler, behoben, L1 einmal wiederholt (Kriterium 5). Laut Abbruchkriterium **kein Hauptlauf**. Details in `ergebnis-stufe0.md`.
- **22.10., Neuplanung (D-016), vor jedem weiteren Lauf:**
  - Belegmaterial v3 mit 6 zusätzlichen Fehlerarten nach dem Muster "Status grün, quantitatives Detail widerspricht" (je Domäne 4 Fehlerarten).
  - Kalibrierung neu auf Seeds 1200–1211, Leiter ab L1.
  - Kriterium 4 lautet jetzt: ≥ 6 von 12 Fehlerarten mit Übersehensrate ≥ 0,05, und kein Beleg > 5 % der Fehler.
  - Hauptlauf weiter auf Seeds 2000–2023 (mit Generator v3). Sonst unverändert.
- **22.10., Material v3 ebenfalls nicht erfüllt:** L1 0,081, L2 0,081, L3 0,028. Kriterium 4 maximal 5/12. Weiterhin kein Hauptlauf, Rücksprache mit Neo. Kriterium 4 ist als fehlerhaft formuliert erkannt (5-%-Grenze pro Beleg bei wenigen Fehlern). Siehe `ergebnis-stufe0.md`, Nachtrag.
