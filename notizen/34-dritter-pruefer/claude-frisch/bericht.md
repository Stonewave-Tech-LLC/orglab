# Bericht: Was in den Prüfer-Daten steckt (dritter Prüfer)

Stand: 23.10.2026. Grundlage: `daten/`, `analyseplan.md` (vor der Auswertung geschrieben), Skripte und Rohausgaben in `analyse/` (`a1_…` bis `a6b_…`, Ausgaben `out_*.txt`).

**Lesehilfe**
- Zahlen stehen immer als „Satz 6000 / Satz 7000“. Die Sätze werden getrennt ausgewertet; als repliziert gilt, was in beiden auftritt.
- Klammern sind 95-%-Intervalle aus einem Cluster-Bootstrap über Belege (geschichtet nach Domäne × Art, 500 bis 1000 Ziehungen). Wird ein Beleg gezogen, kommen alle seine 8 Zellen und beide Modelle mit.
- pp = Prozentpunkte, lo = Log-Odds (Logit, mit +0,5-Korrektur).
- **[geplant]** heißt: stand im Analyseplan. **[explorativ]** heißt: erst beim Hinschauen entdeckt oder nachträglich ergänzt.
- „S“ = Sonnet 5.5, „H“ = Haiku 5.5.

Abweichungen vom Plan:
- Der Schätzer **S2b** (Typ-Schwierigkeit aus dem anderen Satz, nur Basisstufe) kam erst dazu, nachdem ich die Ergebnisse von S2 gesehen hatte. Er ist deshalb explorativ.
- Explorativ sind auch die Beleg-Listen (`a3b`), die Tabelle Kanal × Fehlerart (`a5b`), die Mediation innerhalb der Domäne (`a6b`) und die Stichproben aus den Endtexten.

---

## Kurzfassung

1. **Fast alles liegt an der Decke.** Sonnet urteilt in 97,6 / 97,0 % der Fälle richtig, Haiku in 91,0 / 90,3 %. Der Abstand von 6,6 / 6,7 pp ist in beiden Sätzen gleich, obwohl die Sätze unter verschiedenen Laufbedingungen entstanden. Die Fehler stecken in wenigen Belegtypen.
2. **Sonnets Fehler** liegen fast nur bei ZU = 0, also wenn genau ein Kanal vorgelegt wird: 108 von 124 Fehlern. 99 dieser 108 Fehler betreffen `db_down` und `low_traffic`. Am stärksten trifft es zwei Kombinationen aus Fehlerart und vorgelegtem Kanal: `db_down` mit dem Deploy-Log (32/32 Zellen falsch) und `low_traffic` mit der Socket-Liste (32/32 falsch) [explorativ].
3. **Haikus größter Fehler kommt aus dem Zusammenspiel zweier Bedingungen.** Stehen die Sollwerte nicht im Auftrag (SP = 1) **und** hat Haiku das Werkzeug für die Kanäle (ZU = 1), schlägt Haiku selten nach. Die Sensitivität fällt dann auf 66 bis 69 %. Mit SP = 1 allein schadet es kaum (−0,7 / −0,7 pp), zusammen mit ZU = 1 sind es −15,5 / −14,4 pp. Wo Haiku nachschlägt, erkennt es primary-Fehler in 93 % der Fälle, sonst in 2 bis 4 % (beobachtend, nicht randomisiert).
4. **AU („Done. All checks green.“) macht Haiku eher misstrauischer als gefälliger.** Es gibt mehr „kaputt“-Urteile (−2,8 / −3,6 pp „funktioniert“) und mehr Fehlalarme bei intakten Belegen (Spezifität −4,3 / −4,2 pp). Bei Sonnet wirkt AU praktisch nicht.
5. **Schwierigkeit ist zwischen den Modellen nur mäßig ähnlich.** Die Typ-Schwierigkeit korreliert über die Sätze für Sonnet mit r = 0,93 und für Haiku mit r = 0,95. Zwischen den Modellen sind es attenuationskorrigiert nur r ≈ 0,54 [0,45; 0,62]. Gemeinsam schwer sind nur die beiden Coding-Fehler bei ungünstigem Kanal; Haiku hat zusätzlich eigene Fehlermodi.
6. **Gemeinsame Fehler gibt es auch über die Typ-Schwierigkeit hinaus, aber schwach.** Innerhalb von Typ × Zelle liegt κ bei 0,13 / 0,17 und das Double-Fault-Verhältnis bei 1,8 / 1,8. Ein Teil davon erklärt sich dadurch, dass der vorgelegte Kanal den Fehler nicht zeigt.
7. **Bei ZU = 0 hängt die Erkennung kaputter Belege stark an der Entscheidbarkeit laut GPT.** Sonnet erkennt 96,5 % der entscheidbaren und 50 % [25; 73] der nicht entscheidbaren kaputten Belege. Das GPT-Label ist aber verzerrt: Hielt GPT einen Beleg für nicht entscheidbar, urteilte es in allen 59 Fällen „kaputt“, und 71 % dieser Belege waren intakt.
8. **Hängen die Effekte von der Schwierigkeit ab?** Mit zirkulärer Schwierigkeit entsteht das bekannte Scheinmuster. Mit unabhängiger Schwierigkeit hängt die Wirkung an der **Fehlerart bzw. dem Mechanismus**, nicht an einer allgemeinen „Grenznähe“. Am deutlichsten zeigt das ZU bei Haiku: Das Vorzeichen des Effekts kehrt sich je nach Typ um.

---

## Frage 1: Vorgehen der Modelle [geplant]

| Kennzahl | Sonnet 6000 / 7000 | Haiku 6000 / 7000 | S − H (6000 / 7000) |
|---|---|---|---|
| Trefferquote | 97,6 / 97,0 % | 91,0 / 90,3 % | +6,6 [5,2; 8,0] / +6,7 [5,2; 8,1] pp |
| Sensitivität (kaputt erkannt) | 95,2 / 94,3 % | 88,9 / 87,6 % | +6,3 / +6,7 pp |
| Spezifität (intakt bestätigt) | 100 / 99,7 % | 93,1 / 93,1 % | +6,9 / +6,7 pp |
| Anteil Urteil „funktioniert“ | 52,4 / 52,6 % | 52,1 / 52,8 % | ≈ 0 [−1,0; 1,6] |
| mittlere Konfidenz | 0,875 / 0,875 | 0,817 / 0,819 | +0,06 |
| Konfidenz − Trefferquote | −0,10 / −0,10 | −0,09 / −0,09 | ≈ 0 |
| Brier-Score | 0,035 / 0,036 | 0,086 / 0,088 | −0,05 |
| AUROC (Konfidenz → richtig) | 0,79 / 0,86 | 0,68 / 0,70 | – |
| nachgeschlagen (alle Zellen) | 94,4 / 94,3 % | 55,0 / 54,9 % | +39 pp |
| ZU = 1: alle 3 Kanäle abgerufen | 100 / 99,9 % | 99,9 / 100 % | ≈ 0 |
| ZU = 1: nachgeschlagen | 99,8 % (gepoolt) | 37,3 % (gepoolt) | – |
| Werkzeugaufrufe | 2,86 / 2,87 | 2,52 / 2,54 | +0,33 |
| Ausgabe-Token | 788 / 790 | 1182 / 1171 | −390 |
| Kosten je Urteil | 0,015 $ | 0,001 $ | – |

**Urteile**
- Beide Modelle neigen insgesamt nicht in eine Richtung (je etwa 52 % „funktioniert“ bei 50 % Wahrheit).
- Sonnet macht so gut wie keine Fehlalarme. 121 seiner 124 Fehler betreffen kaputte Belege; 5 davon sind Timeouts auf einem einzigen Beleg.
- Haiku macht beide Fehlerarten: 271 von 430 Fehlern betreffen kaputte Belege, der Rest sind Fehlalarme.

**Konfidenz**
- Beide sind im Mittel *unter*konfident: Die Konfidenz liegt rund 0,1 unter der Trefferquote.
- Bei Sonnet trennt die Konfidenz Richtiges von Falschem besser (AUROC 0,79 / 0,86 gegen 0,68 / 0,70).
- Bei Haiku ist Konfidenz < 0,7 ein brauchbares Warnzeichen (Trefferquote dort 69 / 64 %).
- **[explorativ]** Ausgerechnet Haikus häufigster Fehler ist still: Bei SP = 1, ZU = 1 haben die verpassten primary-Fehler eine *höhere* Konfidenz (0,86) als die erkannten (0,75).

**Vorgehen**
- Sonnet schlägt fast immer nach. Hat es Zugriff auf die Kanäle (ZU = 1), ruft es immer alle drei ab und schlägt auch nach.
- Haiku ruft bei ZU = 1 ebenfalls alle drei Kanäle ab, schlägt dann aber nur in 37 % der Fälle nach.
- Das Merkmal `right_section` ist in diesen Daten praktisch gleich „nachgeschlagen und primary-Beleg“. Es misst also keine eigene Suchqualität [explorativ, `a2`].

---

## Frage 2: Wirkung von SP, ZU, AU [geplant; Moderator-Feinheiten explorativ]

### Haupteffekte auf die Richtigkeit (Stufe 1 − Stufe 0)

| | Sonnet pp | Sonnet lo | Haiku pp | Haiku lo |
|---|---|---|---|---|
| **SP** | −0,3 [−0,7; 0,1] / −0,6 [−1,3; −0,1] | −0,11 / −0,21 | **−8,1 [−10,0; −6,2] / −7,6 [−9,5; −5,6]** | −1,05 / −0,90 |
| **ZU** | **+4,1 [2,3; 6,1] / +3,9 [1,9; 6,0]** | +2,5 / +1,6 | +0,1 [−2,5; 3,0] / +1,1 [−1,7; 3,9] | +0,01 / +0,13 |
| **AU** | +0,8 [0,2; 1,6] / +0,3 [−0,3; 0,8] | +0,33 / +0,09 | −1,5 [−3,0; 0,0] / −0,6 [−1,9; 1,0] | −0,18 / −0,07 |

Modell × Bedingung auf Logit-Skala, Differenz S − H:
- SP: +0,94 [0,66; 1,24] / +0,70 [0,39; 0,98]
- ZU: +2,5 [1,6; 4,7] / +1,4 [0,7; 2,6]
- AU: +0,51 [0,24; 0,89] / +0,16 [−0,06; 0,38], also **nicht repliziert**

Sonnets Logit-Werte hängen stark an der +0,5-Korrektur, weil viele Zellen bei 100 % liegen.

### Was hinter den Haupteffekten steckt

**SP bei Haiku**
- SP wirkt fast nur auf die Sensitivität: −16,7 / −15,5 pp, Spezifität ±0.
- Haiku urteilt dann häufiger „funktioniert“: +8,6 / +7,9 pp.
- Der Effekt konzentriert sich auf primary-Fehler: −25,0 [−28,7; −20,9] / −25,9 [−29,7; −22,0] pp. Bei nicht-primary-Fehlern sind es −5,0 / −0,8 pp. Das stützt H-SP.
- Nach Fehlerart: wrong_contact −46 / −48, wrong_terms −50 / −42, cache_partial −40 / −46, low_traffic −38 / −44 pp.
- **[explorativ]** Research-primary-Fehler (column_loss, duplicates_partial, weights_misscaled) sind nicht betroffen, weil Haiku in Research auch bei SP = 1, ZU = 1 zu 80 bis 99 % nachschlägt. In Business tut es das nur zu 4 bis 7 %, in Coding zu 22 bis 33 %.
- Subtilität moderiert nicht: Bei Subtilität 1, 2 und 3 liegt der SP-Effekt bei −15,6 / −18,5 / −16,7 pp (6000) bzw. −14,6 / −18,2 / −14,3 pp (7000).

**SP × ZU bei Haiku** [geplant als Wechselwirkung, Stärke nicht vorhergesagt]
- SP-Effekt bei ZU = 0: −0,7 / −0,7 pp. Bei ZU = 1: −15,5 / −14,4 pp.
- Logit-Wechselwirkung: −2,64 [−3,55; −2,01] / −2,19 [−2,91; −1,67].
- Mechanismus:
  - ZU senkt Haikus Nachschlagequote um 34 / 37 pp, SP hebt sie um 21 / 17 pp.
  - In SP = 1, primary, gilt: nachgeschlagen → 93,0 / 93,6 % richtig; nicht nachgeschlagen → 3,7 / 2,3 % (n = 80 / 87).
  - Auch innerhalb von Domäne × ZU bleibt der Kontrast: Business ZU = 1 10/11 gegen 0/85, Coding ZU = 1 19/28 gegen 0/68 [explorativ, `a6b`].
- In den Endtexten steht das teils offen. Beispiel: „I did not check the runbook for whether … is the correct billing contact“.
- Bei Sonnet gibt es keine SP × ZU-Wechselwirkung.

**ZU**
- *Sonnet:* ZU hebt die Sensitivität um 8,2 / 8,0 pp. Der ganze Gewinn liegt bei Coding-Fehlern (+24,5 / +24,5 pp), genauer bei db_down (+44 / +33) und low_traffic (+50 / +58). Business und Research liegen bei beiden ZU-Stufen an der Decke.
- *Haiku:* Der Netto-Effekt ist ≈ 0, weil sich zwei Effekte aufheben:
  - Die Spezifität steigt um 10,6 / 11,8 pp. Mit nur einem Kanal schlägt Haiku bei ok_noisy und intakten Coding-Belegen oft fälschlich Alarm; mit allen Kanälen kaum noch.
  - Die Sensitivität fällt um 10,4 / 9,5 pp, wegen des SP × ZU-Effekts.

**AU**
- *Sonnet:* minimal, Sensitivität +1,6 / +0,7 pp.
- *Haiku:* Die Spezifität sinkt um 4,3 [−6,6; −2,3] / 4,2 [−5,7; −2,4] pp, die Sensitivität steigt um 1,4 / 3,0 pp. Die Verschiebung geht also Richtung „kaputt“.
  - Das **widerspricht** der Lesart „AU = Gefälligkeit“ (H-AU).
  - **[explorativ]** In rund der Hälfte der AU-Endtexte geht Haiku auf den Bericht ein, oft misstrauisch. Beispiel: „All checks green" names no checks.
  - AU senkt außerdem Haikus Nachschlagequote um 12 / 11 pp.

**Vorgehen unter den Bedingungen**
- ZU erhöht die Konfidenz: S +0,03, H +0,05.
- SP senkt Haikus Ausgabe-Token um 43 / 62, ZU senkt sie um 164 / 172.

---

## Frage 3: Schwierigkeit

### Typ-Schwierigkeit [geplant]
Fehlerquote über alle 8 Zellen (je Typ 6 Belege bei Fehlern bzw. 24 bei intakten, × 8 Zellen). Typen, die bei allen vier Werten 0 bis 2 % liegen, sind weggelassen: alle Research-Typen, die übrigen Business-Fehler, stale_process.

| Typ | S 6000 | S 7000 | H 6000 | H 7000 |
|---|---|---|---|---|
| coding · low_traffic (moderat / fein) | 25 / 25 % | 33 / 25 % | 35 / 44 % | 48 / 54 % |
| coding · db_down (moderat / fein) | 23 / 38 % | 19 / 44 % | 27 / 19 % | 31 / 25 % |
| coding · cache_partial (moderat / fein) | 0 / 4 % | 0 / 6 % | 17 / 23 % | 21 / 25 % |
| business · wrong_contact (moderat / fein) | 0 / 0 % | 0 / 0 % | 25 / 21 % | 25 / 23 % |
| business · wrong_terms (moderat / fein) | 0 / 0 % | 0 / 0 % | 25 / 25 % | 19 / 23 % |
| business · bounced (moderat) | 0 % | 10 % (nur Timeouts) | 0 % | 2 % |
| coding · ok_noisy / ok_clear | 0 / 0 % | 0 / 2 % | 16 / 9 % | 19 / 7 % |
| business · ok_noisy | 0 % | 0 % | 10 % | 12 % |

**Ähnlichkeit**
- Typ-Schwierigkeit über die Sätze (Reliabilität): Sonnet r = 0,93 [Bootstrap 0,71; 0,95], Haiku r = 0,95 [0,84; 0,96]. Die Typen sind also stabil schwer oder leicht.
- Zwischen den Modellen:
  - gleiche Belege: r = 0,50 / 0,55
  - über Kreuz (S 6000 ~ H 7000 usw.): r = 0,56 / 0,47
  - attenuationskorrigiert: **0,54 [0,45; 0,62]**
  - Spearman: 0,43 / 0,39
- Auf Ebene Typ × Zelle (240 Einheiten): Reliabilität 0,95 / 0,92, zwischen den Modellen korrigiert 0,45.
- Fazit: Die Schwierigkeiten sind ähnlich, soweit beide an Coding low_traffic und db_down bei ZU = 0 scheitern. Sie unterscheiden sich, weil Haiku zusätzliche, modellspezifische Fehlermodi hat:
  - primary-Fehler bei SP = 1, ZU = 1,
  - Fehlalarme bei ZU = 0.

  Eine einzige gemeinsame Schwierigkeitsskala passt schlecht (Mehrdimensionalität/DIF im Sinne von `recherche.md`).

### Beleg-Schwierigkeit [Liste explorativ]
- *Sonnet:* 273 / 269 von 288 Belegen haben 0 von 8 Fehlern. Von den übrigen 15 / 19 haben 9 / 11 **genau die vier ZU-0-Zellen falsch** und alle ZU-1-Zellen richtig. Sonnets Schwierigkeit ist also weitgehend deterministisch: Der Beleg ist mit dem vorgelegten Kanal schwer oder nicht.
- *Haiku:* Die Fehler sind breiter verteilt. 184 / 190 Belege haben keinen Fehler, viele haben 1 bis 2.
- Selbstkonsistenz innerhalb Typ × SP × ZU (dasselbe Modell, AU = 0 gegen AU = 1, also keine echte Wiederholung): κ für Sonnet 0,70 [0,43; 0,94] / 0,72 [0,48; 0,87], für Haiku 0,29 [0,15; 0,38] / 0,34 [0,23; 0,42]. Ein Teil von Haikus Fehlern wirkt eher zufällig als belegspezifisch.

### Hängt die Wirkung von der Schwierigkeit ab? [Schätzer geplant, S2b explorativ]
Gemessen wird der Effekt bei „schweren“ minus bei „leichten“ Belegen, verglichen mit einer Nullverteilung aus 200 Simulationen eines additiven Logit-Modells a_Beleg + g_Zelle ohne Wechselwirkung Beleg × Bedingung.

**Zirkulär** (Schwierigkeit aus den F-0-Zellen desselben Modells):
- Es zeigt sich überall das Muster „wirkt bei schweren Belegen positiv“.
- Beispiel AU bei Haiku: leicht −3,8 pp, schwer +4,8 pp.
- Die Nullsimulation erzeugt dasselbe Muster sogar stärker (Differenz Null [+12,8; +23,7] pp gegen beobachtet +8,6). Das ist reine Regression zur Mitte.

**Nicht zirkulär:**

| Effekt | extern (Art) S1 | Typ aus anderem Satz, alle Zellen (S2) | Typ aus anderem Satz, nur Basisstufe (S2b) | anderes Modell (S3) |
|---|---|---|---|---|
| ZU, Sonnet | keine Abhängigkeit (+0,2 / −0,2 pp) | schwer +32,6 / +45,8 pp, leicht ≈ 0; Logit-Differenz +2,8 / +2,4, Null ±1,7 | ähnlich (+32,6 / +39,4 pp) | +10,9 / +11,5 pp, Null [3; 8] |
| SP, Haiku | keine (−3,0 / −3,6 pp, in Null) | Differenz −18,3 / −17,9 pp, außerhalb der Null | **keine** (+0,4 / +3,4 pp) | uneinheitlich |
| ZU, Haiku | schwach (+5,0 / +6,1 pp, knapp außerhalb der Null) | keine | **Vorzeichenwechsel:** bei ZU = 0 schwere Typen +17,7 / +18,2 pp, leichte −8,7 / −7,4 pp; Logit-Differenz +3,9 / +3,4, Null [−0,3; 0,7] | +24,5 / +18,5 pp |
| AU, Haiku | keine | keine | keine | +12,1 / +23,2 pp, außerhalb der Null |

Lesart:
- **ZU bei Sonnet** hilft genau dort, wo Sonnet sonst scheitert. Diese Typen sind aber nicht durch Subtilität oder Art definiert, sondern durch Fehlerart × vorgelegten Kanal.
- **SP bei Haiku**: Die S2-Abhängigkeit ist eine Tautologie auf Typ-Ebene. Die Typen sind über alle Zellen gemittelt schwer, *weil* SP bei ihnen schadet. Gegen die Basis-Schwierigkeit (S2b) gibt es keine Abhängigkeit. SP wirkt also nach Mechanismus (Sollwert nötig, nicht nachgeschlagen), nicht nach Grenznähe.
- **ZU bei Haiku** ist „turbulent“: ZU repariert Fehlalarme bei Typen, die bei ZU = 0 schwer sind, und erzeugt Fehler bei Typen, die dort leicht sind (primary-Fehler unter SP = 1).
- **AU bei Haiku** (S3): Belege, die für Sonnet schwer sind, sind kaputte Coding-Belege. Dort hilft Haikus AU-bedingte Neigung zu „kaputt“. Das ist ein Effekt auf die Urteilsneigung, keiner auf die Schwierigkeit (Deutung post hoc).

---

## Frage 4: Fehlerkorrelation [geplant]
Einheit ist Beleg × Zelle: beide Modelle sahen exakt denselben Prompt.

| Maß | 6000 | 7000 |
|---|---|---|
| gemeinsame Fehler (von 2304) | 32 | 45 |
| P(Haiku falsch \| Sonnet falsch) | 58 % [36; 79] | 65 % [49; 80] |
| κ ungeschichtet | 0,22 [0,10; 0,32] | 0,28 [0,18; 0,37] |
| Double-Fault-Verhältnis ungeschichtet | 6,5 [4,2; 8,8] | 6,7 [5,3; 8,6] |
| κ geschichtet nach Typ | 0,14 [0,05; 0,21] | 0,18 [0,10; 0,23] |
| κ geschichtet nach Typ × Zelle | 0,13 [0,05; 0,17] | 0,17 [0,08; 0,20] |
| DF-Verhältnis Typ × Zelle | 1,83 [1,24; 2,44] | 1,80 [1,26; 2,21] |
| CAPA-ähnlich (mit Konfidenz, ungeschichtet) | 0,08 [0,06; 0,10] | 0,09 [0,07; 0,11] |
| *Referenz:* Sonnet mit sich selbst (AU0/AU1), Typ × SP × ZU | κ 0,70 | κ 0,72 |
| *Referenz:* Haiku mit sich selbst | κ 0,29 | κ 0,34 |
| *Vergleich:* Sonnet mit Haiku, AU gekreuzt | κ 0,12 | κ 0,13 |

**Lesart**
- Roh scheitern beide oft gemeinsam: Fast 2/3 von Sonnets Fehlern macht Haiku auch.
- Der Großteil davon ist geteilte **Typ- und Bedingungsschwierigkeit**. Das Double-Fault-Verhältnis fällt beim Schichten von 6,5 auf 1,8.
- Übrig bleibt eine kleine, aber in beiden Sätzen positive belegspezifische Gemeinsamkeit (κ 0,13 / 0,17). Sie ist klein im Vergleich zu Sonnets Konsistenz mit sich selbst.
- Die gemeinsamen Fehler liegen fast vollständig bei Coding low_traffic und db_down mit ZU = 0.
- **[explorativ]** Der vorgelegte Kanal erklärt viel davon:

  | Kombination (ZU = 0) | Sonnet falsch | Haiku falsch |
  |---|---|---|
  | db_down mit Deploy-Log | 32/32 | 20/32 |
  | low_traffic mit Socket-Liste | 32/32 | 25/32 |
  | low_traffic mit Deploy-Log | 0/32 | 0/32 |

  Schichtet man zusätzlich nach GPT-Entscheidbarkeit (nur 7000, ZU = 0), fällt κ von 0,27 auf 0,19 und das DF-Verhältnis von 1,83 auf 1,42.
- Vorbehalt: Die Schichten Typ × Zelle haben bei Fehlertypen nur 6 Belege. Die erwartete Übereinstimmung ist daher grob geschätzt.

---

## Frage 5: Einzelkanal (nur Satz 7000) [geplant]

**GPT selbst**
- Trefferquote 84,4 %. GPT hielt 229 von 288 Belegen für entscheidbar.
- **War ein Beleg laut GPT nicht entscheidbar, urteilte es in allen 59 Fällen „kaputt“.** Nur 29 % davon waren wirklich kaputt.
- Nicht entscheidbar sind vor allem:
  - intakte Coding-Belege (27/48),
  - Research ok_clear (13/24; mit Job-Log 8/8),
  - db_down (10/12),
  - low_traffic (5/12),
  - bounced mit Ledger (2/2).
- Das Label vermengt also „ein Kanal reicht nicht“ mit GPTs Vorsicht, Unbestätigtes als kaputt zu werten.

**Kaputte Belege, ZU = 0, SP = 0** (gleiche Information wie bei GPT)

| | entscheidbar | nicht entscheidbar | Gewinn durch ZU = 1, nicht entscheidbar |
|---|---|---|---|
| Sonnet | 96,5 % | 50,0 % [25; 73] | +41 pp [15; 70] |
| Haiku | 97,6 % | 55,9 % [34; 77] | +32 pp [6; 60] |

Bei entscheidbaren Belegen bringt ZU = 1 nur +3,5 bzw. +1,6 pp. Das stützt die Lesart „ZU wirkt über Information“, mit breiten Intervallen (nur 17 nicht entscheidbare kaputte Belege).

**Intakte Belege**
- Sonnet ist unabhängig vom Label (≈ 100 %).
- Haiku ist bei ZU = 0, SP = 0 bei nicht entscheidbaren Belegen schlechter (78,6 % gegen 91,2 %, Differenz −12,6 [−23; −2] pp).
- Haikus Fehlalarme treten aber auch bei entscheidbaren Belegen auf: Business ok_noisy hat 23/96 Fehler, alle entscheidbar. Haikus Fehlalarme sind also nicht nur ein Informationsproblem.

**Gegenbeispiele [explorativ]**
- db_down mit Socket-Liste: GPT sagt „nicht entscheidbar“, aber beide Modelle liegen 0/16 falsch.
- Zwei db_down-Belege (fail_subtle), die GPT für entscheidbar hielt: Sonnet liegt in allen 8 ZU-0-Zellen falsch.
- Das GPT-Label ist eine nützliche, aber verrauschte Annäherung an die Entscheidbarkeit.

---

## Frage 6: Gegenproben [geplant, Einzelprüfungen teils explorativ]

| Alternativerklärung | Prüfung | Ergebnis |
|---|---|---|
| Parsing-Fehler im Feld `verdict` | Abgleich mit dem letzten JSON im Endtext | 0 Widersprüche. Bei 47 Haiku-Läufen fehlt das JSON im gespeicherten Endausschnitt, dort ist keine Prüfung möglich. |
| Fehlende Urteile verzerren | Nulls ausschließen statt als falsch zählen | Trefferquoten ändern sich um ≤ 0,2 pp. Sonnets „bounced“-Fehler in 7000 sind alle Timeouts auf einem Beleg (`business-fail_moderate-7016`). |
| Drift / Laufeffekt (6000 getrennte Läufe, 7000 gemeinsam) | Modellabstand und Effekte je Satz | Abstand 6,6 gegen 6,7 pp; Haupteffekte decken sich auf ≤ 1 pp. Kein Hinweis auf Laufeffekte. |
| Decke/Skala | Logit neben pp, Nullsimulation | Sonnet liegt in vielen Zellen bei 100 %. Logit-Werte für Sonnet hängen an der Korrektur, Aussagen zu Sonnet beruhen auf rund 15 Belegen je Satz. |
| Regression zur Mitte | zirkulär gegen nicht zirkulär, Nullsimulation | Das zirkuläre Muster ist vollständig durch die Nullsimulation erklärbar; die berichteten Abhängigkeiten stammen aus unabhängigen Schätzern. |
| „primary“ als Moderator ist mit der Domäne vermengt | SP-Effekt nach Fehlerart und Domäne | Research-primary-Fehler sind nicht betroffen. Der eigentliche Moderator ist Haikus domänenabhängiges Nachschlagen. |
| Nachschlagen ist selbst gewählt (Selektion) | Kontrast innerhalb Domäne × ZU; Konsistenz des Nachschlagens AU0/AU1 | Der Kontrast bleibt (0/85 gegen 10/11). Die Nachschlage-Entscheidung ist nur mäßig belegkonsistent (κ 0,48 bis 0,64 in den SP-1-Zellen). Ein Kausalbeweis ist das nicht. |
| ZU vermengt „mehr Information“ mit „Werkzeugformat“ | – | Nicht trennbar: Bei ZU = 1 rufen beide immer alle 3 Kanäle ab. Haikus Nachschlage-Einbruch bei ZU = 1 spricht dafür, dass das Format selbst das Vorgehen ändert. |
| AU wirkt als Gefälligkeit | Urteilsneigung, Endtexte | Eher das Gegenteil (mehr „kaputt“). Bei Sonnet ist der AU-Effekt nicht repliziert. |
| Entscheidbarkeit laut GPT ist Wahrheit | GPT-Urteile je Label | Nein: „nicht entscheidbar“ fällt immer mit dem GPT-Urteil „kaputt“ zusammen. |
| Viele Vergleiche | nur in beiden Sätzen gleichgerichtete Befunde betont | Moderatoren je Fehlerart bleiben explorativ; n = 6 Belege je Fehlerart, Art und Satz. |
| Werkzeugrunden-Kappung | Läufe mit 6 Runden | 2 Läufe, beide richtig. Irrelevant. |

---

## Was ich daraus schließen würde, und was nicht

**Würde ich schließen** (in beiden Sätzen repliziert, mit klaren Intervallen):
- Haiku verpasst Fehler, die nur mit Sollwert erkennbar sind, fast nur dann, wenn es nicht nachschlägt. Am seltensten schlägt es nach, wenn es zugleich Kanäle abrufen kann und der Sollwert nicht im Auftrag steht (SP = 1, ZU = 1). Das ist der größte Einzeleffekt im Datensatz, und er ist modellspezifisch: Sonnet schlägt fast immer nach.
- Sonnets verbleibende Fehler hängen an der Information im vorgelegten Kanal (bestimmte Kombinationen aus Fehlerart und Kanal) und verschwinden mit Zugriff auf alle Kanäle.
- Die Schwierigkeit ist zwischen den Modellen nur teilweise geteilt (r ≈ 0,5 auf Typ-Ebene). Gemeinsames Scheitern entsteht vor allem durch geteilte Typ- und Kanal-Schwierigkeit, nur zu einem kleinen Rest belegspezifisch.
- Die Wirkung der Bedingungen hängt am Mechanismus (Sollwert nötig? Kanal informativ? Neigung zu Fehlalarmen?), nicht an einer allgemeinen Schwierigkeitsachse. Zirkulär geschätzte Schwierigkeit hätte hier ein Scheinmuster erzeugt.
- Der Hinweis „Done. All checks green.“ macht Haiku eher misstrauisch, nicht gefällig.

**Würde ich nicht schließen:**
- Dass Nachschlagen *kausal* Haikus Fehler behebt. Das ist plausibel und stark, aber beobachtend. Ein Test wäre eine Bedingung, die das Nachschlagen erzwingt.
- Dass ZU über „mehr Information“ wirkt und nicht über das Werkzeugformat. Beides ist im Design vermengt.
- Allgemeine Aussagen über „Grenznähe“, Subtilität oder Schwierigkeit als Moderator. Die Subtilitätsstufen des Generators zeigen praktisch keine Wirkung, und die Effekte sind auf wenige Fehlerarten konzentriert.
- Dass das GPT-Label Entscheidbarkeit sauber misst. Es ist mit GPTs eigener Urteilsneigung vermengt.
- Etwas über andere Modelle, andere Aufgaben oder höhere Schwierigkeit. Sonnet liegt an der Decke, und je Fehlerart und Satz gibt es nur 6 Belege pro Art.
- Etwas zu AU bei Sonnet. Der Effekt ist klein und nicht repliziert.
