# Unabhängiger Analysebericht

## Analyseplan und Status der Auswertung

Der Bericht beruht auf dem vorgelegten Skript und seiner Ausgabe. Der im Skript dokumentierte Plan ist **keine historische Präregistrierung**. Eine gesonderte `analyseplan.md`, wie im Auftrag verlangt, wurde nicht erstellt.

Der Analyseansatz ist:

1. **Datensätze getrennt halten:** Seeds 6000–6023 und 7000–7023 enthalten unterschiedliche Belege. Innerhalb eines Datensatzes werden dieselben Belege und Bedingungen zwischen den Modellen gepaart.
2. **Urteile und Vorgehen vergleichen:** Trefferquote, Fehlerrichtung, Nachschlagen, Kanalabfragen, Konfidenz und Aufwand. Ungültige Urteile zählen zunächst als Fehler; gültige Urteilspaare dienen als Gegenprobe.
3. **Bedingungseffekte vollständig berichten:** SP, ZU, AU und ihre Wechselwirkungen, einschließlich Nullergebnissen.
4. **Schwierigkeit von Effektprüfung trennen:** Individuelle Schwierigkeit zunächst nur beschreiben. Für die Untersuchung der Effektmodifikation ausschließlich die Schwierigkeit entsprechender **Belegtypen im jeweils anderen Datensatz** verwenden.
5. **Gemeinsame Fehler zufallskorrigieren:** Nicht nur rohe Übereinstimmung, sondern insbesondere Cohen-κ und gemeinsame Fehler gegenüber der Erwartung aus den unterschiedlichen Fehlerraten auswerten.
6. **Alternativerklärungen prüfen:** Aufgabenkomposition, Einzelkanal-Mehrdeutigkeit, technische Ausfälle, Laufunterschiede, Skalenartefakte und Messprobleme.

**Kennzeichnung:** Die Gesamtvergleiche und vollständigen faktoriellen Kontraste folgen diesem Plan. Untergruppen, Schwierigkeitsregressionen, Residualkorrelationen und Mechanismusdeutungen behandle ich als **explorativ**. Da keine belastbare Präregistrierung vorliegt, sind auch die geplanten Analysen keine unabhängig vorab festgelegten Bestätigungstests.

### Wie die Unsicherheit zu lesen ist

- Beide Datensätze enthalten jeweils **288 Belege**, mit acht Bedingungen und zwei Modellen: insgesamt **9.216 Prüferurteile**.
- Alle erwarteten Beleg-Bedingungs-Kombinationen sind vorhanden.
- Angegebene Intervalle sind, sofern nicht anders bezeichnet, **punktweise 95%-Bootstrapintervalle über Belege**. Sie sind **nicht für die vielen Vergleiche korrigiert**.
- Die acht Bedingungen eines Belegs sind keine acht Wiederholungen derselben Messung. Die Intervalle ersetzen daher keine Wiederholungsläufe.
- „Prozentpunkte“ wird mit **pp** abgekürzt. Faktoreffekte bedeuten stets **Stufe 1 minus Stufe 0**.
- Ein beobachtetes Nullergebnis, besonders bei fehlerfreien Gruppen, bedeutet nicht, dass der wahre Effekt exakt null ist.

---

## 1. Wie unterscheiden sich die Modelle in Urteilen und Vorgehen?

### Urteilsqualität

**Sonnet urteilt in diesem Aufgabenraster im Durchschnitt häufiger richtig als Haiku. Der Abstand ist in beiden Datensätzen sehr ähnlich.**

| Datensatz | Sonnet korrekt | Haiku korrekt | Gepaarter Abstand Sonnet − Haiku |
|---|---:|---:|---:|
| 6000 | 2.249/2.304 = **97,61 %** | 2.097/2.304 = **91,02 %** | **+6,60 pp [5,18; 7,99]** |
| 7000 | 2.235/2.304 = **97,01 %** | 2.081/2.304 = **90,32 %** | **+6,68 pp [5,14; 8,42]** |

Der Abstand gilt nicht gleichmäßig für jede Bedingung:

- Bei **SP=0, ZU=1**, also Sollwerten im Auftrag und abrufbaren Kanälen, erreichen beide Modelle etwa **98–100 %**. Die einzelnen Modellunterschiede sind dort überwiegend klein oder unsicher.
- Bei **SP=1, ZU=1** liegt Sonnet dagegen je nach AU und Datensatz **14,93 bis 16,67 pp** vor Haiku. Beispielsweise beträgt der Abstand 7000 ohne AU **15,28 pp [10,92; 19,98]**.

### Fehlerrichtung

Sonnet übersieht hauptsächlich tatsächliche Defekte:

- Fälschliches „funktioniert“ bei kaputten Belegen: **4,77 % / 5,30 %** in 6000/7000.
- Fälschliches „kaputt“ bei intakten Belegen: **0 % / 0,26 %**.

Haiku macht häufiger Fehler in beiden Richtungen:

- Fälschliches „funktioniert“ bei kaputten Belegen: **11,11 % / 12,33 %**.
- Fälschliches „kaputt“ bei intakten Belegen: jeweils **6,77 %**.

Trotzdem unterscheiden sich die **gesamten „works“-Anteile kaum**: Der Modellabstand beträgt **+0,26 pp [−1,24; 2,00]** beziehungsweise **−0,17 pp [−1,74; 1,54]**. Ähnliche Antwortanteile verbergen hier also unterschiedliche Fehlermengen.

### Nachschlagen und Kanalabfragen

Sonnet schlägt wesentlich häufiger nach:

| Kennzahl | Sonnet 6000 / 7000 | Haiku 6000 / 7000 |
|---|---:|---:|
| Mindestens einmal nachgeschlagen | **94,44 % / 94,31 %** | **55,03 % / 54,95 %** |
| Alle drei Kanäle bei ZU=1 abgefragt | **100 % / 99,91 %** | **99,91 % / 100 %** |

Der Unterschied im Nachschlagen beträgt **39,41 pp [36,65; 42,25]** und **39,37 pp [36,60; 42,21]**.

**Die Kanalabdeckung unterscheidet die Modelle dagegen praktisch nicht:** Wenn `run_check` verfügbar ist, fragen beide fast immer sämtliche drei Kanäle ab. Haikus schlechteres Ergebnis unter SP=1, ZU=1 lässt sich deshalb nicht einfach mit zu wenigen Kanalabfragen erklären.

Die Telemetrie zur „richtigen Runbook-Sektion“ muss vorsichtig gelesen werden. Bei `primary=true` wird sie für Sonnet in **94,64 % / 95,39 %**, für Haiku in **62,65 % / 63,84 %** der Urteile ausgewiesen. Das passt zu einem Unterschied bei der Sollwertbeschaffung. Es beweist aber weder korrektes Lesen noch korrektes Verwenden der Werte. Zudem bestehen konkrete Widersprüche zwischen `right_section` und `page_returned`; dazu unten mehr.

### Konfidenz und Kalibrierung

Sonnet gibt im Mittel ungefähr **0,875**, Haiku **0,817–0,819** Konfidenz an. Der gepaarte Abstand beträgt:

- 6000: **0,058 [0,050; 0,065]**
- 7000: **0,057 [0,049; 0,063]**

Unter der Skriptannahme, dass Konfidenz die Sicherheit im gewählten Urteil bezeichnet, sind beide Modelle **im Durchschnitt eher unterkonfident**: Ihre Trefferquote liegt über ihrer mittleren Konfidenz.

Das verdeckt jedoch eine wichtige, **explorative** Besonderheit: Bei Haiku unter **SP=1, ZU=1** sind **15,7–17,7 %** der Urteile mit Konfidenz ≥0,9 falsch. Über alle Bedingungen sind es etwa **6 %**, bei Sonnet **0,58 % / 0,16 %**.

Die ausgegebene Brier-Kennzahl beträgt für Sonnet **0,035/0,036**, für Haiku **0,086/0,088**. Für diese Kalibrierungskennzahlen liefert das Skript keine Unsicherheitsintervalle; ihre Unterschiede sollten daher nicht als präzise inferenzielle Befunde gelesen werden.

### Aufwand

Sonnet verwendet mehr Werkzeugaufrufe, aber weniger ausgegebene Completion-Tokens:

- Werkzeugaufrufe im Mittel: **2,86–2,87** gegenüber **2,52–2,54**.
- Completion-Tokens: ungefähr **789** gegenüber **1.171–1.182**.
- Gepaarter Tokenunterschied: **−394 [−420; −370]** beziehungsweise **−381 [−409; −358]**.

Die protokollierten Gesamtkosten betragen je Datensatz ungefähr **34 US-Dollar für Sonnet** und **2,16–2,18 US-Dollar für Haiku**. Das ist ein Preisvergleich dieser Läufe, kein allgemeiner Effizienzvergleich; insbesondere fehlen Laufzeiten.

---

## 2. Wie wirken SP, ZU und AU – und wovon hängt ihre Wirkung ab?

### Vollständige Gesamtübersicht

Die folgende Tabelle berichtet sämtliche sieben faktoriellen Genauigkeitskontraste. Haupteffekte sind über die anderen Faktoren gemittelt; Zweifachwechselwirkungen sind Differenzen von Differenzen.

**Effekte auf die Trefferquote, pp [95%-Intervall]:**

| Kontrast | Sonnet 6000 | Sonnet 7000 | Haiku 6000 | Haiku 7000 |
|---|---:|---:|---:|---:|
| **SP** | −0,26 [−0,78; 0,09] | −0,61 [−1,39; −0,09] | **−8,07 [−10,55; −5,56]** | **−7,55 [−9,81; −5,03]** |
| **ZU** | **+4,08 [2,17; 6,47]** | **+3,91 [1,51; 6,30]** | +0,09 [−3,35; 3,35] | +1,13 [−2,39; 4,47] |
| **AU** | +0,78 [0,17; 1,65] | +0,26 [−0,26; 0,78] | −1,48 [−2,95; 0,09] | −0,61 [−1,96; 1,04] |
| **SP × ZU** | +0,52 [−0,35; 1,56] | +0,52 [−0,69; 1,74] | **−14,76 [−19,37; −10,42]** | **−13,72 [−18,23; −9,80]** |
| SP × AU | −0,52 [−1,04; 0,00] | +0,17 [−0,87; 1,56] | +0,87 [−1,91; 3,82] | +2,26 [−0,35; 5,03] |
| ZU × AU | −0,17 [−0,87; 0,69] | +0,87 [−0,17; 2,08] | +1,22 [−1,66; 3,91] | +3,65 [0,69; 6,94] |
| SP × ZU × AU | +1,04 [0,00; 2,43] | +1,04 [−1,23; 3,47] | +1,74 [−3,82; 7,29] | −3,82 [−9,03; 1,74] |

### SP: Sollwerte nur im Runbook

Für Sonnet ist der durchschnittliche SP-Nachteil klein. Das Intervall schließt in 6000 null ein, in 7000 knapp nicht. Beim Ausschluss ungültiger Urteilspaare schrumpft der 7000-Effekt auf **−0,35 pp [−0,70; 0,00]**. Eine größere allgemeine SP-Empfindlichkeit Sonnets sehe ich hier nicht.

Für Haiku ist der Nachteil wesentlich größer und hängt stark von ZU ab. Über AU gemittelt:

| Datensatz | SP-Nachteil bei ZU=0 | SP-Nachteil bei ZU=1 |
|---|---:|---:|
| 6000 | −0,69 pp | **−15,45 pp** |
| 7000 | −0,69 pp | **−14,41 pp** |

Diese einfachen Effekte sind aus den Zellzahlen berechnet; ihre gemeinsame Unsicherheit wird durch die oben berichtete SP×ZU-Wechselwirkung erfasst.

**Explorative Einordnung nach Fehlerart:** Bei `primary=true`, also Fehlern mit notwendigem Hintergrund-Sollwert, beträgt Haikus SP-Effekt:

- 6000: **−25,00 pp [−30,52; −19,35]**
- 7000: **−25,89 pp [−31,41; −21,13]**

Bei `primary=false` beträgt er dagegen **−1,10 pp [−3,06; 0,80]** beziehungsweise **0,00 pp [−1,35; 1,35]**. Allerdings enthält diese Vergleichsgruppe auch sämtliche intakten Belege; es ist kein vollständig bereinigter Vergleich zweier gleichartiger Fehlergruppen.

Das Muster ist mit einem **Engpass beim Beschaffen oder Verwenden der Sollwerte** vereinbar. Es ist noch kein Nachweis dieses Mechanismus.

### ZU: Kanäle selbst abrufen statt einen Kanal erhalten

Bei Sonnet erhöht ZU die Trefferquote in beiden Datensätzen um ungefähr vier Prozentpunkte. Der Nutzen liegt vor allem bei kaputten Coding-Belegen:

- Coding insgesamt: **+12,24 pp [6,37; 19,01]** und **+11,98 pp [5,07; 19,27]**.
- Bei `low_traffic`: **+50,00 pp [25,00; 79,58]** und **+58,33 pp [33,33; 83,33]**.
- Bei `db_down`: **+43,75 pp [20,83; 68,75]** und **+33,33 pp [0,00; 64,58]**.

Die Fehlerartanalysen sind **explorativ**, mit nur zwölf Belegen je Fehlerart.

Haikus nahezu nuller durchschnittlicher ZU-Effekt ist **kein einheitliches Nullergebnis**:

- Bei intakten Belegen: **+10,59 pp [6,42; 15,37]** und **+11,81 pp [7,64; 16,76]**.
- Bei kaputten Belegen: **−10,42 pp [−14,58; −6,15]** und **−9,55 pp [−14,06; −5,56]**.
- Bei `primary=true`: **−17,26 pp [−24,11; −10,25]** und **−16,37 pp [−22,92; −9,82]**.

Zum Vorgehen passt: ZU steigert Sonnets Nachschlagehäufigkeit um **10,94/10,85 pp**, senkt sie bei Haiku dagegen um **33,85 pp [−38,07; −29,81]** beziehungsweise **36,81 pp [−41,11; −32,90]**.

Beide Modelle sammeln also nahezu dieselbe Kanalmenge; Haiku schlägt dabei deutlich seltener zusätzlich nach. Ob die Kanalabfragen das Nachschlagen tatsächlich verdrängen, ist ohne Eingriff in die Werkzeugstrategie nicht kausal geklärt.

### AU: „Done. All checks green.“

**Eine einfache Verschiebung hin zur Behauptung „funktioniert“ zeigt sich nicht.** Die „works“-Anteile sinken vielmehr:

- Sonnet: **−0,78 pp [−1,65; −0,09]** und **−0,52 pp [−1,04; 0,00]**.
- Haiku: **−2,86 pp [−4,43; −1,39]** und **−3,47 pp [−4,86; −2,17]**.

Für Haiku bedeutet das:

- Bei intakten Belegen sinkt die Trefferquote um **4,34 pp [−6,60; −2,34]** beziehungsweise **4,17 pp [−5,90; −2,60]**.
- Bei kaputten Belegen steigt sie um **1,39 pp [−0,52; 3,30]** beziehungsweise **2,95 pp [0,60; 5,73]**.

Der Gesamteffekt auf Genauigkeit ist deshalb klein und unsicher. Sonnets kleiner positiver AU-Effekt in 6000 ist in 7000 nicht eindeutig wiederzufinden.

AU reduziert das Nachschlagen bei beiden Modellen, bei Haiku stärker:

- Sonnet: **−1,39 / −1,65 pp**.
- Haiku: **−12,33 pp [−15,10; −9,55]** und **−10,59 pp [−13,07; −8,16]**.

Das ist eine reproduzierte Verhaltensänderung, aber kein Beleg für Zustimmung zum ausführenden Agenten. Eine mögliche Skepsisreaktion ist ebenfalls nur eine Hypothese.

### Weitere Abhängigkeiten — explorativ

- **Domäne:** Haikus SP-Schaden liegt in Business bei **−14,06/−13,28 pp**, in Coding bei **−10,68/−10,16 pp**; die jeweiligen Intervalle liegen unter null. In Research liegt SP dagegen bei **+0,52 [−1,30; 2,60]** beziehungsweise **+0,78 [−0,52; 2,34]**.
- **Moderate und subtile Defekte:** Haikus SP-Nachteil betrifft beide Gruppen ähnlich stark: ungefähr **−15 bis −18 pp**. Die Zahlen stützen nicht die Behauptung, der Effekt trete ausschließlich bei subtilen Fehlern auf.
- **Harmloses Rauschen:** Haiku beurteilt `ok_noisy` seltener richtig als `ok_clear`: **89,58/89,06 %** gegenüber **96,70/97,05 %**. ZU hilft besonders bei `ok_noisy`: **+15,97 pp [9,38; 23,26]** und **+19,10 pp [11,61; 27,43]**.
- **Subtilitätsstufen:** Haikus SP-Schaden tritt in allen drei Stufen auf. Ein stabil monotoner Zusammenhang mit der numerischen Subtilität ist nicht erkennbar. Bei Sonnet wechseln die Schwierigkeitsunterschiede zwischen Stufe 2 und 3 zwischen den Datensätzen.
- **Länge:** Die Längenschichten zeigen Unterschiede, sind aber stark mit Domäne und Aufgabeninhalt vermengt. Insbesondere entspricht die Gruppe der längeren Kurzaufträge hier der Research-Gruppe. Daraus lässt sich kein eigenständiger Längeneffekt ableiten.
- **Weitere Wechselwirkungen:** SP×AU, ZU×AU und die Dreifachwechselwirkung liefern einzelne punktweise auffällige Untergruppenresultate, aber kein ähnlich klares, datensatzübergreifendes Muster wie Haikus SP×ZU-Effekt.

---

## 3. Wie schwer sind Belege und Belegtypen? Sind die Schwierigkeiten ähnlich?

### Was hier „Schwierigkeit“ bedeutet

Für einen einzelnen Beleg ist die ausgegebene Schwierigkeit die **Fehlerrate über den balancierten Acht-Bedingungen-Plan**. Sie liegt in Schritten von 12,5 Prozentpunkten vor.

Das ist eine Beschreibung dieses Versuchsplans, **keine präzise Schätzung einer bedingungsunabhängigen Lösungswahrscheinlichkeit**. Ein Beleg kann beispielsweise bei allen Einzelkanalbedingungen scheitern und bei allen Mehrkanalbedingungen gelingen. „Vier von acht falsch“ würde diesen systematischen Unterschied zusammenfassen.

Die vollständigen individuellen Werte stehen in der vorgelegten Q3-ID-Tabelle. Eine belastbare Rangliste mit Unsicherheitsintervallen pro Beleg lässt sich aus einem Lauf je Bedingung nicht erstellen.

### Schwierigkeiten sämtlicher Fehlerarten

Die folgende Tabelle zeigt **Fehler einschließlich ungültiger Urteile**. Je Fehlerart liegen zwölf Belege mit acht Bedingungen vor, also 96 Urteile — aber nicht 96 unabhängige Wiederholungen.

| Fehlerart | Sonnet 6000 | Haiku 6000 | Sonnet 7000 | Haiku 7000 |
|---|---:|---:|---:|---:|
| `amount_mismatch` | 0/96 | 0/96 | 0/96 | 0/96 |
| `bounced` | 0/96 | 0/96 | 5/96* | 1/96* |
| `cache_partial` | 2/96 | 19/96 | 3/96 | 22/96 |
| `column_loss` | 0/96 | 1/96 | 0/96 | 1/96 |
| `db_down` | **29/96** | **22/96** | **30/96** | **27/96** |
| `duplicates_partial` | 0/96 | 1/96 | 0/96 | 0/96 |
| `low_traffic` | **24/96** | **38/96** | **28/96** | **49/96** |
| `row_loss` | 0/96 | 0/96 | 0/96 | 0/96 |
| `stale_process` | 0/96 | 0/96 | 0/96 | 0/96 |
| `weights_misscaled` | 0/96 | 1/96 | 0/96 | 0/96 |
| `wrong_contact` | 0/96 | 22/96 | 0/96 | 23/96 |
| `wrong_terms` | 0/96 | 24/96 | 0/96 | 20/96 |

\* Ausschließlich ungültige Urteile, keine gültigen Fehlentscheidungen.

Bei intakten Belegen:

| Belegart | Sonnet 6000 | Haiku 6000 | Sonnet 7000 | Haiku 7000 |
|---|---:|---:|---:|---:|
| `ok_clear` | 0/576 | 19/576 | 3/576 | 17/576 |
| `ok_noisy` | 0/576 | 60/576 | 0/576 | 63/576 |

Für diese Schwierigkeitsraten hat das Skript keine eigenen Typ-Konfidenzintervalle berechnet. Insbesondere bei zwölf Belegen je Fehlerart bleibt die Unsicherheit über neue Belege erheblich. Null Fehler sind keine Garantie einer Fehlerrate von null.

**Exploratives Gesamtbild:** Für beide Modelle sind `low_traffic` und `db_down` schwierig. Haiku hat zusätzliche Schwierigkeiten mit Sollwertfehlern bei Kontakten, Zahlungsbedingungen und Cache-Abdeckung. Research ist für beide überwiegend leicht.

Auch die individuellen Beispiele zeigen Unterschiede:

- `coding-fail_subtle-6000` (`db_down`): Sonnet **6/8**, Haiku **3/8** falsch.
- `coding-fail_subtle-7007` (`low_traffic`): Sonnet **4/8**, Haiku **7/8** falsch.
- `business-fail_moderate-7016`: Sonnet **fünf ungültige Urteile**, Haiku eines. Die hohe ausgewiesene Schwierigkeit dieses Belegs ist daher nicht als nachgewiesene inhaltliche Schwierigkeit zu verstehen.

### Ähnlichkeit zwischen den Modellen

Die Schwierigkeiten sind positiv, aber keineswegs vollständig gleichgeordnet:

| Ebene | 6000 | 7000 |
|---|---:|---:|
| Individuelle Belege: Pearson-r | **0,51 [0,33; 0,64]** | **0,57 [0,41; 0,69]** |
| Individuelle Belege: Spearman-ρ | **0,34 [0,21; 0,44]** | **0,42 [0,32; 0,52]** |
| Exakte Belegtypen: Pearson-r | **0,69 [0,53; 0,74]** | **0,65 [0,45; 0,78]** |

Das spricht für gemeinsame schwierige Bereiche, nicht für eine einheitliche präzise Schwierigkeitsskala. Viele Belege sind bei Sonnet fehlerfrei; die zahlreichen Rangbindungen begrenzen die Aussagekraft zusätzlich.

### Hängen Bedingungseffekte von unabhängiger Schwierigkeit ab?

Hier wurden **keine einzelnen 6000- und 7000-Belege gleichgesetzt**. Übertragen wurde nur die Schwierigkeit exakter Typen aus Domäne, Art, Fehlerart, `primary` und Subtilität.

**Explorative Ergebnisse:**

- Sonnet, ZU-Effekt bei extern „mittelschweren“ Typen:
  - 6000→7000: **+47,62 pp [23,81; 69,05]**, 21 Zielbelege.
  - 7000→6000: **+59,09 pp [31,82; 86,36]**, elf Zielbelege.
- Bei extern leichten Sonnet-Typen beträgt ZU dagegen **+0,47 pp [−0,28; 1,51]** beziehungsweise **+1,90 pp [0,58; 3,43]**.
- Haikus SP-Effekt bei extern mittelschweren Typen:
  - **−28,28 pp [−34,24; −21,72]**
  - **−31,58 pp [−37,72; −25,20]**
- Bei extern leichten Haiku-Typen: **−2,00 pp [−4,11; −0,33]** beziehungsweise **−2,27 pp [−4,11; −0,54]**.

Es gab keine extern als sehr schwer eingestuften Gruppen mit Erfolgswahrscheinlichkeit ≤0,2. Zwei 7000-Belege waren mangels Quelltyp nicht übertragbar.

**Das belegt keinen besonderen Mechanismus „nahe der Fähigkeitsgrenze“.** Erstens sind es Typunterschiede, keine unabhängig gemessenen individuellen Schwierigkeiten. Zweitens erzeugen Boden- und Deckeneffekte unterschiedliche Prozentpunkteffekte schon bei konstanten Logit-Effekten. Drittens unterscheiden sich die Gruppen in ihrer Aufgabenkomposition.

Die zusätzlichen Logitregressionen lösen diese Probleme nicht überzeugend:

- Haikus adjustierte Grenznähe-Koeffizienten schließen für SP, ZU und AU in beiden Richtungen null ein.
- Sonnets Resultate sind instabil und teilweise durch sehr wenige oder ausschließlich gleichgerichtete Änderungen getragen.
- Beispielsweise bestehen Sonnets 47 diskordante ZU-Paare in 6000 aus **47 Verbesserungen und keiner Verschlechterung**. Die dennoch ausgegebenen endlichen Regressionskoeffizienten werden wesentlich durch die Ridge-Strafe bestimmt.

Mein Ergebnis lautet deshalb: **Effektgrößen unterscheiden sich zwischen extern eingestuften Typgruppen; ein darüber hinausgehender allgemeiner Grenznähe-Effekt ist nicht belastbar nachgewiesen.**

---

## 4. Scheitern beide Modelle an denselben Belegen beziehungsweise Zellen?

### Gemeinsame Fehler sind häufiger als unter Unabhängigkeit

Die Auswertung paart jeweils dasselbe Beleg-Bedingungs-Paar zwischen den Modellen.

| Kennzahl | 6000 | 7000 |
|---|---:|---:|
| Beide korrekt | 2.074 | 2.057 |
| Nur Sonnet falsch | 23 | 24 |
| Nur Haiku falsch | 175 | 178 |
| Beide falsch | **32** | **45** |
| Gemeinsame Fehlerrate | **1,39 %** | **1,95 %** |
| Erwartung aus Produkt der Fehlerraten | **0,21 %** | **0,29 %** |
| Überschuss gemeinsamer Fehler | **1,17 pp [0,46; 1,94]** | **1,66 pp [0,86; 2,63]** |
| Cohen-κ | **0,215 [0,093; 0,322]** | **0,275 [0,174; 0,377]** |
| Phi-Korrelation | **0,269 [0,133; 0,378]** | **0,330 [0,232; 0,423]** |

Gemeinsame Fehler treten damit ungefähr **6,5- beziehungsweise 6,7-mal so häufig** auf wie nach der globalen Unabhängigkeitsannahme. Die Ergebnisse ändern sich wenig, wenn ausschließlich gültige Urteilspaare betrachtet werden: κ beträgt dann **0,216 / 0,286**.

Der Zusammenhang konzentriert sich auf Coding, besonders auf `low_traffic` und `db_down`. Bei `low_traffic` beträgt κ **0,49 [0,27; 0,63]** beziehungsweise **0,44 [0,31; 0,52]**.

**Diese Korrektur berücksichtigt unterschiedliche Gesamtfehlerraten, aber nicht sämtliche Unterschiede der Aufgabenschwierigkeit.** Gemeinsame schwierige Belege können den Zusammenhang erklären, ohne dass die Modelle direkt voneinander abhängig wären.

Eine separate zufallskorrigierte Kennzahl für „beide machen bei diesem Beleg mindestens einen Fehler in irgendeiner der acht Bedingungen“ berechnet das Skript nicht. Die obigen Aussagen beziehen sich auf gepaarte Zellen; die Belegebene wird ergänzend durch die Schwierigkeitskorrelationen beschrieben.

### Was bedeutet das für eine Kombination beider Modelle?

Ein Orakel, das bei jeder Zelle die richtige der beiden Antworten auswählen könnte, käme auf **98,61 % / 98,05 %**. Das wären gegenüber Sonnet **0,998 beziehungsweise 1,042 pp** zusätzlich.

Das ist nur eine **Obergrenze**, kein gemessener Ensemblegewinn. Bei einer Meinungsverschiedenheit ist ohne weitere Prüfung nicht bekannt, welches Modell richtig liegt.

### Die Residualanalyse ist keine belastbare zusätzliche Bereinigung

Nach Abzug externer Typ×Zell-Risiken gibt das Skript positive Residualkorrelationen aus: **0,322 [0,226; 0,417]** und **0,237 [0,136; 0,363]**.

Diese **explorative** Analyse hat jedoch ein erhebliches Artefaktrisiko: Beide Risikoschätzungen erhalten dieselbe, bei kleinen Typgruppen starke Glättung. Dadurch können auch gemeinsame Schätzfehler korrelieren.

Ein konkretes Warnsignal: In der 6000-Zelle **SP0-ZU1-AU1 macht Sonnet überhaupt keinen Fehler**, trotzdem beträgt die ausgewiesene Residualkorrelation **0,349 [0,299; 0,450]**. Das ist keine Korrelation tatsächlich variierender Sonnet-Fehler nach sauberer Schwierigkeitsbereinigung.

Ich würde diese Residualwerte daher **nicht als Nachweis gemeinsamer Fehler über die individuelle Schwierigkeit hinaus verwenden**.

---

## 5. Wie hängen Einzelkanalurteile mit der Entscheidbarkeit laut GPT zusammen?

Diese Zusatzanalyse betrifft ausschließlich den Datensatz 7000.

GPT stuft **229 von 288 Belegen als entscheidbar** und **59 als nicht entscheidbar** ein. Die Gruppen sind unterschiedlich zusammengesetzt:

- „Nicht entscheidbar“: **42 intakte**, 17 kaputte Belege; überwiegend Coding und Research.
- „Entscheidbar“: 102 intakte, 127 kaputte Belege.

GPTs eigenes Urteil ist in der entscheidbaren Gruppe **226/229 = 98,69 %** korrekt. In der nicht entscheidbaren Gruppe sagt es **ausnahmslos „kaputt“** und trifft damit **17/59 = 28,81 %**.

Das zeigt eine starke Verknüpfung von GPTs Entscheidbarkeitsurteil und seiner Antwortstrategie. Seine Einstufung ist **kein Goldstandard objektiver Entscheidbarkeit**.

### Einzelkanalqualität

SP=0 ist der passendere Vergleich, weil GPT den vollständigen Auftrag samt Sollwerten sah.

**Trefferquote bei SP=0, ZU=0:**

| Modell | Laut GPT entscheidbar, n=229 | Laut GPT nicht entscheidbar, n=59 |
|---|---:|---:|
| Sonnet, AU=0 | **97,82 %** | **86,44 %** |
| Sonnet, AU=1 | **98,25 %** | **84,75 %** |
| Haiku, AU=0 | **96,07 %** | **77,97 %** |
| Haiku, AU=1 | **93,45 %** | **66,10 %** |

Das Skript liefert für diese einzelnen Quoten keine Intervalle. Die kleinere Gruppe mit 59 Belegen ist entsprechend unsicherer.

### Hilft ZU besonders bei „nicht entscheidbar“?

Über SP und AU gemittelt:

- Sonnet:
  - nicht entscheidbar: **+11,44 pp [3,39; 22,69]**
  - entscheidbar: **+1,97 pp [0,44; 4,04]**
  - Unterschied: **+9,48 pp [0,89; 21,11]**
- Haiku:
  - nicht entscheidbar: **+14,83 pp [5,51; 23,54]**
  - entscheidbar: **−2,40 pp [−5,69; 1,20]**
  - Unterschied: **+17,23 pp [7,65; 26,26]**

**Explorative Interpretation:** GPTs Einstufung markiert eine Gruppe, in der zusätzliche Kanäle im Mittel stärker helfen. Das ist mit einem Einzelkanal-Engpass vereinbar.

Die stärkere Behauptung wäre nicht gedeckt:

- Bei Sonnet ist die entsprechende Differenz auf der marginalen Logit-Skala unsicher: **−1,25 [−3,05; 0,74]**.
- Bei Haiku bleibt sie dort positiv: **+1,45 [0,69; 2,31]**; Aufgabenart und Wahrheitszusammensetzung sind damit aber weiterhin nicht bereinigt.
- Die ZU-Kontraste sind über beide SP-Stufen gemittelt, nicht ausschließlich unter dem GPT vergleichbaren SP=0 gerechnet.
- Hohe Trefferquoten bei angeblich „nicht entscheidbaren“ Belegen können auf zusätzliche Information im Runbook, auf Heuristiken oder auf eine zu strenge GPT-Einstufung zurückgehen.

Für eine objektive Aussage zur Entscheidbarkeit wäre eine unabhängige inhaltliche Prüfung der Belege nötig.

---

## 6. Welche Alternativerklärungen bleiben, und was spricht dagegen?

| Alternativerklärung | Was die Gegenproben zeigen | Was offenbleibt |
|---|---|---|
| **Unterschiedliche Belegauswahl** | Innerhalb jedes Datensatzes sehen beide Modelle dieselben Belege in allen Bedingungen. | Übertragbarkeit auf andere Generatoren und reale Prüfaufträge. |
| **Unterschiedliche Laufzeitpunkte** | Der ähnlich große Modellabstand und Haikus SP×ZU-Muster erscheinen auch im gemeinsamen 7000-Lauf. | Reihenfolge, Backend-Drift und zeitliche Abhängigkeiten sind nicht vollständig dokumentiert. |
| **Technische Ausfälle statt inhaltlicher Fehler** | Nur neun von 9.216 Urteilen sind ungültig; gültige Blöcke ergeben ähnliche Hauptmuster. | Einzelne kleine Effekte werden davon beeinflusst, besonders Sonnets SP-Effekt 7000. |
| **Zu wenige abgefragte Kanäle** | Beide Modelle fragen bei ZU=1 fast immer alle drei Kanäle ab. | Qualität der Interpretation und Integration dieser Kanäle. |
| **Fehlende Sollwertbeschaffung** | Haikus Schaden konzentriert sich auf Sollwertfehler; zugleich sinkt bei ZU sein Nachschlagen stark. | Nachschlagen ist nicht randomisiert; Beschaffung und Verwendung sind nicht getrennt. |
| **Budgeterschöpfung** | Keine Zeile erreicht den Tokenproxy ≥3.900; nur zwei Zeilen haben ≥6 Werkzeugaufrufe. | Das sind keine tatsächlichen Abbruch- oder Werkzeugrundenprotokolle. |
| **Reiner Prozentmaßstab/Deckeneffekt** | Der große Haiku-SP×ZU-Kontrast erscheint auch auf marginaler Logit-Skala: **−2,64 [−3,76; −1,90] / −2,19 [−2,95; −1,64]**. | Marginale Logits ersetzen kein korrekt spezifiziertes bedingtes Modell. Grenznähe bleibt ungeklärt. |
| **Zirkulär definierte Schwierigkeit** | Für Effektmodifikation stammt die Typ-Schwierigkeit aus dem anderen Datensatz. | Kleine Typgruppen, unvollständige Typkontrolle und keine unabhängige individuelle Schwierigkeit. |
| **Promptlänge statt Inhalt** | Die beobachteten Muster sind in beiden Datensätzen ähnlich. | SP verändert zugleich Sollwertplatzierung und Länge; AU Inhalt und Länge. Neutrale Längenkontrollen fehlen. |

Die Gesamtmuster sind in beiden Datensätzen ähnlich. Das ist aber keine nachgewiesene Äquivalenz: Beispielsweise beträgt der Unterschied der Haiku-SP-Effekte zwischen 7000 und 6000 **+0,52 pp [−2,83; 3,99]**. Bei der Haiku-Dreifachwechselwirkung unterscheiden sich die marginalen Logit-Kontraste sogar um **−2,36 [−4,88; −0,58]**, während die entsprechende pp-Differenz unsicher bleibt. Höhere Wechselwirkungen würde ich deshalb nicht als stabil repliziert bezeichnen.

---

## Schwächen meines eigenen Skripts

1. **Die formale Plananforderung wurde nicht erfüllt.**  
   Ein Kommentar ist keine separat vor der Rechnung erstellte `analyseplan.md`. Die Behauptung im Kommentar, der Auftrag verbiete Dateiausgaben, ist aus dem hier vorgelegten Auftrag nicht ableitbar.

2. **Möglicherweise zu kleine Bootstrap-Einheit.**  
   Das Skript resampelt Belege und hält deren Zellen zusammen. Es prüft aber nicht, ob die zwölf Belege desselben Seeds oder andere Generatorbestandteile zusätzlich abhängig sind. Ein Seed-Clusterbootstrap mit 24 Clustern je Datensatz wäre eine wichtige Sensitivitätsanalyse.

3. **Zu viele punktweise Vergleiche ohne simultane Absicherung.**  
   Die zahlreichen Untergruppen- und Interaktionsergebnisse können zufällig auffällig werden. Es gibt weder eine klare kleine primäre Testfamilie noch eine Multiplikitätskorrektur.

4. **Nur 499 beziehungsweise 199 Bootstrapziehungen.**  
   Für grobe Intervalle reicht das eher als für stabile Randquantile. Mehr Ziehungen wären insbesondere bei kleinen Gruppen sinnvoll.

5. **Degenerierte Intervalle können Präzision vortäuschen.**  
   Bei fehlerfreien Gruppen liefert der empirische Bootstrap häufig `[0; 0]`. Bei Korrelationen verwirft das Skript undefinierte Ziehungen; die verbleibenden Ziehungen können eine selektive Teilmenge sein. Solche Intervalle sind keine belastbaren Nullnachweise.

6. **Die Grenznähe-Regressionen sind überinterpretiert leicht irreführend.**  
   Sie verwenden wenige diskordante Paare, teils vollständige Separation, eine feste Ridge-Strafe einschließlich des Intercepts und teilweise redundante Prädiktoren. Es fehlen Strafparameter-Sensitivität, Identifizierbarkeitsdiagnostik und eine geeignete Nullsimulation. Einzelne enge Koeffizientenintervalle sind deshalb nicht überzeugend.

7. **„Logit-Kontraste“ sind überwiegend marginal.**  
   Sie werden aus aggregierten Trefferquoten berechnet. Sie sind nicht gleichbedeutend mit individuellen oder bedingten logistischen Behandlungseffekten und lösen die Skalenfrage nicht vollständig.

8. **Die Residualkorrelation ist durch gemeinsame Glättung anfällig.**  
   Die externen Typ×Zell-Risiken sind stark fehlkalibriert und ihre Unsicherheit wird im Intervall nicht mitgeschätzt. Die oben gezeigte positive Residualkorrelation trotz fehlerfreiem Sonnet illustriert das Problem.

9. **Widersprüchliche Runbook-Telemetrie wird nur gemeldet.**  
   Bei Haiku gibt es **elf beziehungsweise 15 Fälle „richtige Sektion“ ohne „Seite zurückgegeben“**. Das Skript klärt diese Fälle nicht anhand von Rohtranskripten. Aussagen über erfolgreichen Informationszugriff bleiben dadurch eingeschränkt.

10. **Konfidenzsemantik wird vorausgesetzt.**  
    Die Kalibrierungsanalyse ist nur passend, wenn `confidence` tatsächlich die Sicherheit im gewählten Urteil bedeutet. Das Skript prüft dies nicht anhand der Prompts und Antworten und liefert für die Kalibrierungskennzahlen keine Intervalle.

11. **Mechanismen werden nicht direkt untersucht.**  
    Das Skript zählt Werkzeuge und Themen, analysiert aber weder Reihenfolge noch tatsächliche Sollwertverwendung oder Begründungen. Die nach beobachtetem Werkzeugverhalten gebildeten Gruppen sind selektiert und erlauben keine kausale Mediationsaussage.

12. **Der Messgegenstand „Schwierigkeit“ bleibt eingeschränkt.**  
    Individuelle Werte vermischen Bedingungsempfindlichkeit und technische Ausfälle. Die Typübertragung ist sinnvoll gegen direktes Double-Dipping, erlaubt aber keine individuelle Schwierigkeitskalibrierung und kontrolliert die Fehlerart nicht vollständig in den Regressionen.

---

## Was ich daraus schließen würde, und was nicht

**Ich würde schließen:**

- In diesem synthetischen Prüfsetting urteilt Sonnet im Durchschnitt ungefähr **6,6–6,7 Prozentpunkte häufiger richtig** als Haiku.
- Der auffälligste Bedingungsbefund ist **Haikus Nachteil, wenn Sollwerte nur im Runbook stehen und zugleich die Kanäle selbst abgefragt werden müssen**. Dieses Muster erscheint in beiden Datensätzen und bleibt bei Beschränkung auf gültige Urteile bestehen.
- Beide Modelle fragen verfügbare Kanäle nahezu vollständig ab. Der Unterschied liegt eher bei zusätzlicher Informationsbeschaffung oder Informationsverwendung als bei der Zahl betrachteter Kanäle.
- ZU hilft Sonnet im Mittel; bei Haiku verdeckt der kleine Durchschnitt gegenläufige Wirkungen auf unterschiedliche Belege.
- AU verändert das Verhalten, insbesondere das Nachschlagen. Eine einfache Zustimmung zur Erfolgsmeldung wird durch die Urteile **nicht** gestützt.
- Beide Modelle teilen einen Teil ihrer Fehler stärker, als ihre unterschiedlichen Gesamtfehlerraten allein erwarten lassen.
- GPTs Entscheidbarkeitsurteil identifiziert eine schwierigere Einzelkanalgruppe, ist aber selbst ein fehlbarer und mit Antworttendenzen verknüpfter Indikator.

**Ich würde nicht schließen:**

- dass Nachschlagen als kausaler Vermittler bereits nachgewiesen sei;
- dass eine allgemeine besondere Harness-Empfindlichkeit „an der Fähigkeitsgrenze“ gezeigt sei;
- dass die Residualanalyse gemeinsame Fehler nach vollständiger Schwierigkeitsbereinigung belege;
- dass AU generell schade, helfe oder Zustimmung auslöse;
- dass beobachtete 100%-Gruppen künftig fehlerfrei bleiben;
- dass zwei Modelle ohne geprüfte Auswahlregel die Orakelquote erreichen;
- oder dass diese Rangfolge und Effektgrößen unverändert für andere Modelle, Harnesses oder reale Arbeitsaufträge gelten.