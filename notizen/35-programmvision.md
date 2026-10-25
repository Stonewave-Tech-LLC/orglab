# Programmvision: vertrauenswürdige automatisierte Forschung (Neo, 23.10.2026 abends)

> Arbeitsdokument. Status: **Vision, kein Befund.** Darunter liegt die Leitfrage D-023. Festgehalten auf Neos Wunsch ("ja halte es fest").

## 1. Was hinter dem Projekt steckt
Neo: "Ich dachte mir, wir brauchen Antworten für Multi-Agent-Systeme, und eigentlich steckt drin: Wie automatisieren wir Research sicher bei beliebigen simulierbaren Dingen?"
- Die Multi-Agent-Frage war das **Vehikel**. Die eigentliche Frage lautet: **Wie automatisiert man Forschung so, dass man ihren Ergebnissen trauen kann, in jedem Bereich, den man simulieren kann?**
- **Das ist dieselbe Frage wie D-023, eine Ebene höher.** Forschung ist selbst ein Multi-Agent-System:
  - Entwerfer, Durchführer, Auswerter, Kritiker
  - Neo als letzter Prüfer
- Ihr typischer Fehler ist ein "bestätigt", obwohl die widersprechende Information nicht im Blick war.
- **Herkunft, nach Neos Selbstbeobachtung:** Neo schließt den Kreislauf, entscheidet als Laie nach Intuition und lernt dabei. Er kann nicht garantieren, dass sein Urteil gut ist. Die Leitfrage ist damit auch sein eigenes Vertrauensproblem. Gelöst wird es über **Prozessvertrauen statt Inhaltsvertrauen**: Wer hat unabhängig geprüft, mit welcher Information? Was hätte widerlegt? Was stand vorher fest? Was sagen die, die unsere Thesen nicht kennen?

## 2. Warum "simulierbar" der Schlüssel ist
- In einem simulierten Bereich ist die Wahrheit bekannt. Unser Generator weiß, welcher Beleg kaputt ist.
- Dadurch kann man **die Prüfer selbst prüfen**: bekannte Fehler einschleusen und messen, welche Prüfschicht sie fängt. Das ist Neos Lichttest bzw. das Plattenbild (Swiss-Cheese-Modell, Parkplatz).
- Sicher wird automatisierte Forschung erst, wenn man den Prüfern nicht vertraut, sondern ihre **Fangquote gemessen** hat.
- Nicht simulierbare Bereiche (echte Wave-Arbeit, echte Wissenschaft) bekommen nur einen Teil des Schutzes: den Prozess, nicht die gemessene Fangquote.

## 3. Zwei Ebenen, eine Leitfrage
Jeder Befund auf der Objektebene ist zugleich ein Bauteiltest für automatisierte Forschung (alle Zeilen mit dem Status ihrer Quelle):

| Befund (Objektebene) | Status | Regel für automatisierte Forschung (Metaebene) |
|---|---|---|
| Haiku übersieht ohne mitgelieferten Maßstab, wenn es Daten-Werkzeuge hat (E-024) | bestätigt, schmal | Der Auswertungs-Agent braucht die Präregistrierung als Maßstab vor sich, nicht nur "irgendwo" |
| Fremde Prüfer mit frischem Kontext korrigierten Claude dreimal (`notizen/34`) | Anekdote, ein Tag | Auswertung durch Agenten ohne die Thesen des Entwerfers |
| Gemeinsame Fehler entstehen vor allem bei fehlender Information (`notizen/34`) | Hinweis | Kritiker brauchen andere Information, nicht nur andere Modelle |
| Kontext-Drift (Parkplatz) | Hypothese | Sessions je Entscheidung klein und sauber halten |
| Alle Prüfer sahen das Material mit drei Kanälen, der gemeinsame blinde Fleck (E-020) | ein Fall | Kritiker gezielt mit *anderer* Sicht ausstatten (Einzelkanal-Prüfung) |

## 4. Engineering-Perspektive (falls es eins wird)
Neo: Daraus könnte ein **echter Research-Harness** werden, als Meta-Harness oder selbst als Multi-Agent-System.
- **Ansatz in `notizen/32`:**
  - Rollen mit strenger Informationskapselung
  - Gates, die fremde Rechner prüfen
  - Kryptographie für Commitments
  - Sandbox
- **Heute live erprobt, und zwar von Hand:**
  - Recherche-Agent und dritter Prüfer mit frischem Kontext in getrennten Ordnern
  - Rohdaten-Kopie mit neutraler Beschreibung
  - Fragen von Neo gegengelesen
  - Fremdmodell (GPT) als zweiter Auswerter
  - Hash-Commitment bei der Verblindung
- **Was ein Harness automatisieren müsste:**
  1. Kontext je Rolle zuschneiden (wer sieht was)
  2. Commitments vor dem Sehen der Daten erzwingen
  3. unabhängige Nachrechnung und Deutung
  4. Fangquote der Prüfschichten per Fehlereinschleusung messen
  5. Status jeder Aussage automatisch mitführen (Regel 15)
- **Selbst als MAS:** Dann müsste der Harness seine eigene Leitfrage beantworten: Wann ist *sein* "verifiziert" gerechtfertigt? Das ist der Lichttest auf sich selbst.

## 5. Observability: warum sie eigene Fehler billig macht
Neo erinnert an `notizen/32` §9 ("Observability macht Ehrlichkeit prüfbar statt geglaubt") und an seinen Grundsatz "log alles raw".
- Die Leitfrage ist im Kern eine Frage nach **Informationsflüssen**: Wer hat wann welche Information gesehen? Wenn das **mitprotokolliert** wird, wird die Antwort billig.
  - **Lecks werden sichtbar statt gemeldet.** Heute erfuhren wir nur, dass der Recherche-Agent eine Gedächtniszeile gesehen hatte, weil er es selbst meldete. Mit einem Protokoll aller Kontextquellen je Agent wäre es automatisch aufgefallen.
  - **Gemeinsame blinde Flecken werden sichtbar.** Das Protokoll hätte gezeigt, dass alle Material-Prüfer dieselbe Sicht hatten (drei Kanäle), bevor der Fehler teuer wurde.
  - **Überbehauptungen werden messbar.** Jede Aussage wird mit ihrem Status und ihrer Quelle protokolliert. Dann lässt sich zählen, wie oft der Status beim Weitergeben steigt. Das ist Claudes Muster von heute.
  - **Die Fangquote lässt sich ohne Zusatzaufwand berechnen.** Eingeschleuste Fehler und die Reaktionen aller Schichten liegen im selben Protokoll.
- Observability ist damit nicht nur Überwachung, sondern **die Messgrundlage für die Leitfrage**.
- Offen bleibt: Was ist "alles"? Kontextquellen, Werkzeugaufrufe, Commitments, Statuswechsel? Und wie bleibt das Protokoll selbst manipulationssicher (Hash-Kette, `notizen/32` §7)?

## 6. Wo das bremst
- Das ist eine Vision. Belegt sind ein Bereich, wenige harte Ergebnisse und viele Anekdoten eines Tages.
- **"Automatisierte Forschung" ist ein bekanntes Feld** (KI-Wissenschaftler-Systeme). Vor jeder Neuheitsbehauptung kommt eine Recherche: Was gibt es, welche Fehler sind dort bekannt, was ist an unserem Ansatz (gemessene Fangquote, Kontextkapselung) anders?
- **Die Metaebene ist verführerisch** (Neo, 22.10.; D-022: "uns nicht verkaufen"). Die Vision trägt nur, wenn die Objektebene weiter misst. Die Experimente sind das Fundament, die Vision ist das Dach.

## 7. Erstes Bindeglied (Vorschlag, nicht geplant)
**Lichttest auf die eigene Forschungspipeline:** In eine Auswertung bekannte Fehler einschleusen, etwa einen vertauschten Arm, einen Zirkelschluss, ein Leck oder einen Status, der beim Weitergeben steigt. Dann messen, welche Schicht ihn fängt: Präregistrierung, Verblindung, Nachrechnung, frischer Prüfer, Neo. Das verbindet beide Ebenen in einem Experiment.
