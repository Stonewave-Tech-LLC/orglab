# Methodik-Vorlesung: was du über unser Projekt formal wissen solltest

> **Korrektur 23.10. (E-021, Manipulationscheck):** Was hier "Reasoning aus" heißt, war in Wahrheit die **Standardeinstellung mit adaptivem, verborgenem Reasoning** (OpenRouter: Reasoning ist bei Sonnet 5.5 nicht abschaltbar). "Reasoning low" war **gedrosseltes** Reasoning. Alle Aussagen "Reasoning erhöht Fehlalarme" sind deshalb umzudrehen: **Gedrosseltes Reasoning erhöht Fehlalarme** (H-037). Details: `experimente/E-021-reasoning-fehlalarme/ergebnis.md`.

**Für Neo, 22.10.2026.** Jeder Begriff kommt in vier Schritten:
- **Intuition**
- **formal**
- **bei uns**, also wo er im Projekt vorkommt
- **typischer Denkfehler**

Am Ende stehen Kontrollfragen. Wenn du die beantworten kannst, verlässt du dich nicht mehr auf mich, sondern prüfst mich.

---

## Teil 1: Wie man ehrlich forscht

### 1. Präregistrierung
- **Intuition:** Du schreibst auf, was du erwartest und wie du auswertest, *bevor* du die Daten siehst. Danach kannst du dir nicht mehr unbewusst die Geschichte aussuchen, die zu den Daten passt.
- **Formal:** Sie schützt vor zwei Problemen:
  - **HARKing** ("Hypothesizing After the Results are Known", Kerr 1998)
  - dem **Garten der sich verzweigenden Pfade** (Gelman & Loken). Bei jeder Entscheidung in der Auswertung (welche Metrik, welche Ausschlüsse, welcher Test) gibt es Alternativen. Wählt man nach Ansicht der Daten, findet man fast immer *irgendeinen* Effekt.
- **Bei uns:** Jede `prereg.md`, committet vor dem Hauptlauf. Der Git-Zeitstempel ist der Beweis.
- **Denkfehler:** "Präregistrierung heißt, ich darf nichts Unerwartetes berichten." Falsch. Man darf alles berichten, man muss es nur als **explorativ** kennzeichnen.

### 2. Forscher-Freiheitsgrade
- **Intuition:** Jede Stellschraube, die du nach Ansicht der Daten drehen *könntest*.
- **Bei uns, gerade eben:** die zwei Anstupser-Sätze im E-020-Prompt.
  - Hätte ich sie nach dem Pilot still gestrichen, um einen Effekt wahrscheinlicher zu machen, wäre das ein Freiheitsgrad.
  - Die saubere Lösung ist, die Entscheidung offenzulegen, oder noch besser, die Varianten **zu messen**. Das ist der Zusatzarm.
- **Denkfehler:** "Ich habe es ja nicht absichtlich gemacht." Unabsichtlich ist der Normalfall. Genau deshalb gibt es die Regeln.

### 3. Entdeckung gegen Bestätigung
- **Intuition:** Beim Entdecken sammelt man Ideen, beim Bestätigen prüft man *eine* Idee hart.
- **Formal:**
  - Ein Befund aus explorativer Analyse ist eine Hypothese, kein Ergebnis.
  - Bestätigt ist er erst, wenn er auf **neuen Daten** (bei uns: frische Seeds) mit **vorher festgelegtem Test** repliziert.
- **Warum frische Daten:** **Fluch des Gewinners** bzw. Regression zur Mitte. Wer aus vielen Effekten den größten auswählt, wählt systematisch einen, der *auch* durch Zufall groß ausgefallen ist. Beim Nachmessen schrumpft er.
- **Bei uns:**
  - H-017 war in der Entdeckung p = 0,015 und in der Bestätigung (E-004) nicht mehr signifikant. Der Effekt schrumpfte von −0,075 auf −0,033. Das Lehrbuchbeispiel.
  - Der Reasoning-Fehlalarm-Effekt ist explorativ. Deshalb ist er in E-020 als V6 vorab festgelegt.

### 4. Hypothese, Vorhersage, Widerlegung
- **Formal (Popper):** Eine wissenschaftliche Hypothese muss sagen, welches Ergebnis sie **widerlegen** würde.
- **Bei uns:** Jede Vorhersage hat eine Spalte "widerlegt, wenn". Beispiel V1 in E-020: Liegt die Obergrenze des Konfidenzintervalls für den SPEC-Effekt unter +0,02, ist H-033 widerlegt.
- **Denkfehler:** Hypothesen so weich formulieren, dass jedes Ergebnis passt ("Spezifikation spielt eine Rolle"). Die ist unwiderlegbar und damit wertlos.

---

## Teil 2: Wie ein Experiment gebaut ist

### 5. Faktorielles Design, Haupteffekt, Interaktion
- **Intuition:** Mehrere Stellschrauben werden gleichzeitig in allen Kombinationen variiert, statt eine nach der anderen.
- **Formal:**
  - Bei k Faktoren mit je 2 Stufen gibt es 2^k Zellen. E-020 hat 2⁴ = 16.
  - **Haupteffekt** von A: der Unterschied zwischen A=1 und A=0, gemittelt über alle anderen Faktoren.
  - **Interaktion** A×B: Der Effekt von A hängt davon ab, auf welcher Stufe B steht.
- **Bei uns:** H-035 ist eine Interaktionshypothese. Der Effekt von ZUGANG soll unter AUSKUNFT=1 anders ausfallen (weniger Abfragen).
- **Vorteil:** Jede Prüfung trägt zu *allen* Haupteffekten bei. Das ist effizienter als einzelne Experimente.
- **Denkfehler:** Ist eine Interaktion stark, kann der Haupteffekt irreführend sein. Ein Mittelwert über zwei gegenläufige Effekte sieht wie "kein Effekt" aus.

### 6. Gepaartes Design
- **Intuition:** Jeder Beleg wird in *jeder* Zelle beurteilt. Man vergleicht also denselben Beleg mit sich selbst.
- **Formal:** Die Varianz zwischen den Items fällt aus dem Vergleich heraus (within-subjects). Dadurch braucht man viel weniger Daten für dieselbe Genauigkeit.
- **Bei uns:** In E-017, E-019 und E-020 laufen dieselben 240–288 Belege durch alle Zellen.

### 7. Konfundierung
- **Intuition:** Zwei Dinge ändern sich gleichzeitig, und man weiß nicht, welches den Effekt macht.
- **Bei uns:**
  - E-019 V5: Erfahrung E1 gegen E0 ist mit **Promptlänge** konfundiert, denn Episoden machen den Prompt länger. Deshalb ist nur E2 gegen E1 sauber.
  - E-020: Bei SPEC=1 kommt ein Werkzeug *dazu*. Der Faktor misst also "Sollwert fehlt **und** Werkzeug da".
  - Bei der Literatur (CONTRAMEM) war "Erfahrung aus anderen Modellen" mit "andere Modelle" konfundiert.
- **Denkfehler:** Konfundierung erst beim Schreiben des Ergebnisses bemerken. Sie gehört in die Präregistrierung unter "offene Schwächen". Das haben wir gemacht.

### 8. Kontrollen: A/A, Positivkontrolle, Manipulationscheck
- **A/A-Test:** Zwei *identische* Bedingungen unter verschiedenem Namen. Zeigt die Pipeline trotzdem einen "Effekt", ist sie kaputt oder zu rauschig. (E-005)
- **Positivkontrolle:** Eine Bedingung, die *sicher* wirken muss, z. B. ein Prüfer, dem die Fehlerspur fehlt. Erkennt die Messung das nicht, ist sie blind.
- **Manipulationscheck:** Wirkt die Manipulation überhaupt? Beispiel: Erzeugt Stapelprüfung wirklich Aufmerksamkeitsknappheit (V8, Positionseffekt)? Bei uns kaum. Das war selbst ein Befund.
- **Denkfehler:** Ein Nullergebnis berichten, ohne die Manipulation geprüft zu haben. Dann weiß man nicht, ob die Hypothese falsch ist oder die Manipulation nicht gewirkt hat.

### 9. Decken- und Bodeneffekt, Kalibrierung
- **Intuition:** Liegen alle Bedingungen bei 100 % (oder 0 %), kann man keinen Unterschied sehen, egal wie groß er "eigentlich" wäre.
- **Bei uns:** E-001 (alle Regime bei 100 %), E-016 (Prüfer bei 0 % Fehlern), E-017 und E-019. Daher D-010: erst kalibrieren, Ziel 10–40 % Fehler.
- **Denkfehler (deine Frage von vorhin):** "Decke heißt, die Aufgaben sind zu leicht." Die Decke sagt nur, dass *in diesem Setting* keine Unterschiede messbar sind. *Warum* sie leicht sind, ist eine eigene empirische Frage. Darauf antworten die Schwierigkeitslandkarte und E-020.

### 10. Validität
- **Interne Validität:** Misst der Vergleich wirklich den Effekt der Manipulation? Bedroht durch Konfundierung und Generatorfehler.
- **Konstruktvalidität:** Misst die Metrik, was wir meinen? Ist "Übersehensrate bei synthetischen Logs" wirklich "Prüfqualität"?
- **Externe Validität:** Gilt das auch außerhalb des Labors, in Wave, mit anderen Modellen, mit echten Logs?
- **Ground Truth:** Die "wahre" Antwort, gegen die gemessen wird. Ist sie falsch (Generatorfehler) oder mehrdeutig (`zero_traffic` ohne Sollwert), messen wir Unsinn. Das ist uns rund zehnmal passiert, und jedes Mal hatte das Modell recht.
- **Denkfehler:** Interne Validität maximieren (sauberes, synthetisches Labor) und vergessen, dass dabei die externe sinkt. Das ist der Kern von "Realität in Dosen".

---

## Teil 3: Wie man Zahlen liest

### 11. Fehlerarten: Übersehen und Fehlalarm
Wenn "kaputt" die Klasse ist, die man finden will:

| | Prüfer sagt "kaputt" | Prüfer sagt "ok" |
|---|---|---|
| **wirklich kaputt** | Treffer (richtig positiv) | **Übersehen** (falsch negativ) |
| **wirklich ok** | **Fehlalarm** (falsch positiv) | richtig negativ |

- **Übersehensrate** = 1 − Sensitivität
- **Fehlalarmrate** = 1 − Spezifität
- **Wichtig, die Prävalenz:**
  - Bei uns ist die Hälfte der Belege kaputt. In Wave sind es vielleicht 5 %.
  - Bei 5 % Prävalenz macht eine Fehlalarmrate von 15 % die meisten Alarme falsch: 95 % × 0,15 ≈ 14 % aller Items sind Fehlalarme, aber nur 5 % sind echte Fehler.
  - **Der Reasoning-Fehlalarm-Effekt wäre in der Praxis also noch teurer, als er im Labor aussieht.**
- **Denkfehler:** Nur auf "Fehlerrate gesamt" schauen. Sie vermischt zwei Fehlerarten mit völlig verschiedenen Kosten: Übersehen kostet Schaden, Fehlalarm kostet Menschen-Minuten.

### 12. p-Wert
- **Formal:** die Wahrscheinlichkeit, ein mindestens so extremes Ergebnis zu sehen, **wenn es in Wahrheit keinen Effekt gibt** (Nullhypothese).
- **Was er *nicht* ist:**
  - nicht die Wahrscheinlichkeit, dass die Hypothese stimmt
  - nicht die Größe des Effekts
- **Denkfehler:**
  - "p = 0,04, also ist der Effekt echt und wichtig." Ein winziger Effekt kann bei vielen Daten p < 0,001 haben.
  - "p = 0,2, also gibt es keinen Effekt." Ein großer Effekt kann bei wenig Daten p = 0,2 haben.
- Deshalb gilt bei uns: **Effektgröße vor p.**

### 13. Konfidenzintervall
- **Intuition:** der Bereich plausibler Werte für den wahren Effekt.
- **Formal (95 %):** Ein Verfahren, das bei vielen Wiederholungen in 95 % der Fälle den wahren Wert einschließt.
- **Lesen:**
  - Breites Intervall heißt wenig Information.
  - Schließt es 0 ein, ist "kein Effekt" mit den Daten vereinbar.
  - Liegt es ganz über der Relevanzschwelle, ist der Effekt wahrscheinlich *praktisch* wichtig.
- **Bei uns:** Wilson-Intervall für Anteile (das ist bei kleinen n und Raten nahe 0 genauer als die Schulformel). Bootstrap für Differenzen.

### 14. Bootstrap und Cluster-Bootstrap
- **Intuition:** Man tut so, als wäre die eigene Stichprobe die ganze Welt, zieht daraus tausendmal neu (mit Zurücklegen) und schaut, wie stark das Ergebnis schwankt.
- **Cluster-Bootstrap:** Gezogen werden ganze **Gruppen**, nicht einzelne Messungen, wenn Messungen innerhalb einer Gruppe zusammenhängen.
  - In E-020 sind das die Belege, denn derselbe Beleg wird in 16 Zellen beurteilt.
  - In E-019 sind es die Stapel, denn ein Stapel teilt Kontext und Ermüdung.
- **Denkfehler:** Abhängige Messungen wie unabhängige behandeln. Dann sind die Intervalle viel zu eng. Das steht als Warnung in `notizen/20`.

### 15. Mehrfachtests und FDR
- **Intuition:** Wer 20 Tests bei p < 0,05 macht, findet im Mittel einen "Effekt" rein durch Zufall.
- **Benjamini-Hochberg (FDR):** kontrolliert den erwarteten **Anteil falscher Entdeckungen** unter allen Entdeckungen.
  - p-Werte sortieren.
  - Der i-te kleinste p-Wert wird mit i/m · q verglichen.
  - Daraus ergeben sich die q-Werte.
- **Bei uns:** BH über die gerichteten Hauptvorhersagen jedes Experiments.

### 16. Äquivalenz und Nicht-Unterlegenheit
- **Problem:** "Nicht signifikant" heißt *nicht*, dass es keinen Unterschied gibt. Vielleicht hat man einfach zu wenig gemessen.
- **Äquivalenztest (TOST):** Man legt vorher eine Grenze ±δ fest und zeigt, dass das 90-%-Intervall des Effekts ganz innerhalb liegt.
  - Bei uns: E-019 V2, ob Etiketten-Personas "nichts" bewirken.
- **Nicht-Unterlegenheit:** Man zeigt nur, dass B nicht um mehr als δ schlechter ist als A.
  - Bei uns: E-020 V6, ob Prüfer ohne Reasoning nicht mehr übersehen.
  - E-014/E-018: ob Frist-Regel bzw. Abstimmung nicht schlechter sind als der Mensch.

### 17. Statistische Power
- **Intuition:** die Wahrscheinlichkeit, einen *wirklich vorhandenen* Effekt einer bestimmten Größe auch zu finden.
- **Treiber:** Stichprobengröße, Effektgröße, Rauschen.
- **Bei uns:** D-011. Das Optimierer-Gate mit 10 Paaren konnte nur Effekte ≳ 0,087 sehen. Realistische Verbesserungen sind kleiner. E-010 bis E-012 waren damit praktisch blind.
- **Denkfehler:** Ein Nullergebnis aus einem Experiment mit niedriger Power als "widerlegt" lesen.

---

## Teil 4: Die Konzepte hinter unserer Kernfrage

### 18. Fehlerkorrelation: φ, β, n_eff
- **φ (phi):** die Korrelation zwischen zwei Ja/Nein-Variablen, hier "Prüfer A irrt" und "Prüfer B irrt". 0 heißt unabhängig, 1 heißt immer gemeinsam.
- **β (Co-Failure):** der Anteil der Items, bei denen *alle* Prüfer irren. Das ist die harte Obergrenze jedes Mehrheitsentscheids.
- **Kish-n_eff:** Wie viele *unabhängige* Prüfer sind k korrelierte wert? n_eff = k / (1 + (k−1)·φ̄).
  - Bei k = 9 und φ̄ = 0,4 ergibt das 9 / (1 + 8 · 0,4) ≈ 2,1. Das ist das "Nine Judges, Two Effective Votes"-Ergebnis.
- **Dein Wecker-Beispiel formal:** p₁ · p₂ gilt nur bei φ = 0. Bei positiver Korrelation ist P(beide versagen) = p₁p₂ + φ·√(p₁(1−p₁)p₂(1−p₂)), also deutlich größer.

### 19. Kalibrierung der Konfidenz und Eskalation
- **Kalibriert** heißt: Von allen Urteilen mit 80 % Konfidenz stimmen etwa 80 %.
- **Risk-Coverage-Kurve** (selektive Vorhersage): Man gibt nur Urteile über einer Schwelle automatisch durch und den Rest an einen Menschen.
  - Für jede Schwelle sieht man, welcher Anteil eskaliert wird und wie viele Fehler übrig bleiben.
  - Das ist unsere "Verlässlichkeit pro Mensch-Minute". Bei uns: 37 % eskalieren fängt 85 % der Fehler.
- **Denkfehler:** Kalibrierung im Labor gilt nicht automatisch unter Druck. Die Literatur zeigt: Unter einstimmigen Peers sind Modelle *konfident falsch*.

---

## Kontrollfragen (Antworten unten, erst selbst versuchen)

1. In E-019 waren die Fehlalarme mit Reasoning 15,7 %, ohne Reasoning 3,7 %. Darfst du jetzt schreiben "Reasoning macht Prüfer übervorsichtig"? Was fehlt?
2. Warum ist E-019 V5 (Erfahrung gleich gegen keine) schwächer interpretierbar als V4 (disjunkt gegen gleich)?
3. Ein Experiment zeigt p = 0,30 für einen Effekt von +0,12. Ist der Effekt widerlegt?
4. Warum ziehen wir im Bootstrap von E-019 ganze Stapel statt einzelner Urteile?
5. Ein Prüfer hat 5 % Übersehen und 15 % Fehlalarm. In Wave sind 2 % der Arbeiten kaputt. Welcher Anteil seiner Alarme ist echt?
6. Warum ist "die Aufgaben sind zu leicht" keine gute Erklärung für die Decke, und was wäre eine bessere?
7. Was ist der Unterschied zwischen "kein signifikanter Unterschied" und "gleichwertig"?
8. Drei Prüfer mit φ̄ = 0,5. Wie viele unabhängige Prüfer sind sie wert?

---

### Antworten
1. Als **explorativen** Befund ja, als Ergebnis nein. Er wurde nicht vorab vorhergesagt und stammt aus Kalibrierungsläufen mit wenigen hundert abhängigen Urteilen. Es fehlt eine vorab festgelegte Bestätigung auf frischen Daten. Das ist E-020 V6.
2. Weil E1 gegen E0 mit Promptlänge konfundiert ist. E1 hat 6 Episoden mehr im Prompt, E0 keine. E2 und E1 sind gleich lang.
3. Nein. p = 0,30 heißt nur, dass die Daten auch ohne Effekt nicht ungewöhnlich wären. Ein Effekt von +0,12 kann trotzdem echt sein. Wahrscheinlich war die Power zu klein. Ins Konfidenzintervall schauen.
4. Urteile im selben Stapel hängen zusammen (gemeinsamer Kontext, Ermüdung, dasselbe Modellverhalten in einem Aufruf). Zieht man einzeln, tut man so, als hätte man mehr unabhängige Information, und die Intervalle werden zu eng.
5. Von 1.000 Arbeiten sind 20 kaputt. Davon fängt er 19 (95 % Sensitivität). Von 980 heilen meldet er 147 fälschlich (15 %). Echt sind also 19 von 166 Alarmen, etwa **11 %**. Neun von zehn Alarmen sind falsch.
6. Sie ist unbelegt und erklärt nichts. Besser ist eine Erklärung über **messbare Eigenschaften**: vollständige Spezifikation, vorgelegter Beleg, keine Selbstauskunft, Spurtyp. Die kann man einzeln zuschalten und messen (E-020).
7. "Nicht signifikant" kann auch "zu wenig gemessen" heißen. "Gleichwertig" verlangt, dass das ganze Intervall innerhalb einer vorher festgelegten Grenze ±δ liegt (TOST).
8. n_eff = 3 / (1 + 2 · 0,5) = 1,5. Drei Prüfer sind 1,5 unabhängige wert.

---

**Weiterlesen, falls du tiefer willst:**
- Gelman & Loken, "The garden of forking paths" (2013)
- Lakens, "Equivalence Tests" (2017)
- Efron & Tibshirani, *An Introduction to the Bootstrap* (1993)
- Kish, *Survey Sampling* (1965), für n_eff
- Für den Einstieg die frei verfügbaren Vorlesungsnotizen "Improving your statistical inferences" von Daniël Lakens (Coursera bzw. online)
