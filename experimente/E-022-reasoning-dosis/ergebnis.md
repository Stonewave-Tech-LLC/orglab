# E-022: Ergebnis – Kontrast repliziert, Dosis-Stufe fehlt, H-037 formal nicht bestätigt

- **Lauf:** 23.10.2026, 08:50–~09:40. 288 Aufrufe, 3.456 Urteile, 0 fehlend, 0 Wiederholungen, 24 von 24 Stapeln vollständig. Kosten 6,18 $.
- **Präregistrierung:** `prereg.md` (Commit 9891133, Freigabe a9978c9). Auswertung: `python -m orglab.e022 analyze` (eingefroren), Rohausgabe `daten/E-022-reasoning-dosis/auswertung.md`.
- **Weg, Modell, Einstellung (Regel 11):** OpenRouter, `anthropic/claude-sonnet-5.5`, `max_tokens` 4000, Temperatur Anbieter-Standard. Arme: `reasoning.effort` low, medium, high bzw. weggelassen.

## Vorab festgelegte Tests

| Test | Ergebnis | Kriterium |
|---|---|---|
| **Manipulationscheck** (Bedingung) | Median-Tokens low **257**, medium **257**, high **896**, ohne 903 | low < medium < high: **nicht erfüllt** (medium = low). high ≥ 1,5 × low: erfüllt |
| **P1** Δ Fehlalarm low − high, Cluster-Bootstrap über Stapel | **+0,044**, untere Grenze **+0,025** | erfüllt (> 0), **unter der Relevanzgrenze** +0,05 |
| **P2** Δ Übersehen high − low | **−0,019**, obere Grenze 0,000 | erfüllt (≤ +0,03) |
| **H-037** | **nicht bestätigt** | P1, P2 **und** Manipulationscheck gemeinsam |

**Nach Präregistrierung ist H-037 nicht bestätigt.** Der Manipulationscheck war als Bedingung festgelegt und ist gescheitert. Das lockern wir hinterher nicht.

## Was tatsächlich manipuliert wurde
- **`low` und `medium` sind bei Sonnet 5.5 über OpenRouter in diesem Setting identisch.** Jeder einzelne der 144 Aufrufe liegt bei 244–257 Completion-Tokens. Das JSON-Array für 12 Belege braucht allein schon ~240 Tokens. **Faktisch gibt es in diesen Armen kein verborgenes Denken.**
- `high` und ohne Parameter sind praktisch gleich (Median 896 bzw. 903 Tokens, Spanne 244–2.085). Das Modell denkt adaptiv, manchmal gar nicht.
- Es gab also **zwei Stufen statt drei: "Denken gedeckelt" (low/medium) und "Denken frei" (high/ohne).** Die Dosis-Frage ist mit diesem Design nicht beantwortbar.

## Was die Daten unter der tatsächlichen Manipulation zeigen (deskriptiv, vorab festgelegte Sekundärgrößen)

| Arm | Tokens (Median) | Fehlalarm [95-%-KI] | Übersehen [95-%-KI] | PPV bei 5 % Prävalenz |
|---|---|---|---|---|
| low | 257 | 0,067 [0,044; 0,094] | 0,062 [0,040; 0,085] | 0,42 |
| medium | 257 | 0,062 [0,039; 0,089] | 0,056 [0,037; 0,073] | 0,44 |
| high | 896 | 0,023 [0,011; 0,038] | 0,044 [0,025; 0,064] | 0,68 |
| ohne | 903 | 0,023 [0,009; 0,040] | 0,051 [0,031; 0,073] | 0,68 |

- **Gedeckeltes Denken erzeugt etwa dreimal so viele Fehlalarme wie freies Denken.** Das ist das zweite Mal auf frischen Seeds (E-021: 0,102 gegen 0,032, hier 0,067 gegen 0,023).
- Freies Denken übersieht dabei **nicht mehr**, eher weniger (P2).
- **S2:** "ohne Parameter" und `high` sind ununterscheidbar (Δ FA 0,000 [−0,007; +0,007]). Damit ist die E-021-Deutung bestätigt: Ohne Parameter heißt adaptives Denken auf `high`-Niveau.
- **Der Effekt ist kleiner als in E-021** (+0,044 gegen +0,069) und liegt unter der vorab gesetzten Relevanzgrenze.
- **Prävalenz (Regel 14):** Bei 5 % kaputten Arbeiten ist mit gedeckeltem Denken nur etwa **4 von 10 Alarmen echt**, mit freiem Denken etwa 7 von 10.
- **S3 Eskalation:** Konfidenz < 0,80 eskaliert 10–14 % und fängt bei `low` 55 % der Fehler, bei freiem Denken nur 31–38 %. Die verbleibenden Fehler beim freien Denken sind seltener und schlechter an niedrige Konfidenz gebunden, wie schon in E-021.
- **S4:** Am stärksten wirkt es bei Rechnungen (business: 0,118 gegen 0,049).
- Generatorfehler-Regel: kein Ok-Beleg, den alle Arme in allen Kanälen als kaputt beurteilen.

## Einordnung
- **H-037 bleibt "gestützt", nicht "belegt".** Der Kontrast "gedeckelt gegen frei" hat sich jetzt zweimal auf frischen Seeds gezeigt, gerichtet und vorab festgelegt. Die präregistrierte Bestätigungsbedingung (Dosis mit drei messbar verschiedenen Stufen) ist aber nicht erfüllt, und der Effekt liegt unter der Relevanzgrenze.
- **Präzisere Lesart für Wave:** Es geht nicht um "etwas weniger Denken", sondern um **"Denken abgeschaltet"**. Ein Prüfer, der vor dem Urteil faktisch nicht nachdenken darf, alarmiert rund dreimal so oft unnötig, und er findet keinen einzigen Fehler mehr.
- **Methodische Lehre (Regel 11):** `effort: medium` ist bei Sonnet 5.5 über OpenRouter kein Mittelwert, sondern verhält sich wie `low`. Ohne Manipulationscheck hätten wir eine Dosis-Wirkung "gesehen", die es gar nicht gab. Das ist der zweite Fall nach E-021, in dem eine API-Einstellung nicht tut, was ihr Name sagt.
- Für eine echte Dosis bräuchte es eine Steuerung, die messbar abstuft, etwa ein explizites Token-Budget statt `effort`, sofern OpenRouter das bei Sonnet 5.5 unterstützt. Ungeprüft.

## Transkripte (Methodik 7)
`transkripte.md`: 2 zufällige Stapel-Antworten je Arm. In allen Armen sieht man nur das JSON-Array, das Denken bleibt verborgen. Auffällig: Die Konfidenzen sind in allen Armen ähnlich hoch (0,6–0,97). Gedeckeltes Denken macht den Prüfer also nicht vorsichtiger in seiner Selbsteinschätzung.

## Grenzen
- Nur Sonnet 5.5 über OpenRouter, Stapel 12, synthetisches Material v3.1.
- Was der Anbieter bei `effort` genau tut, ist nicht dokumentiert. Gemessen sind nur Tokens.
- Kritiker-Unabhängigkeit: Design, Material und Prüfer sind Claude. Nur die Ground-Truth-Stichprobe hat GPT kontrolliert.

## Nachtrag 23.10.: Doppelte Buchführung (Empfehlung aus `notizen/31`)
GPT-6.1 Sol und Gemini 4 Argon haben die Auswertung unabhängig neu geschrieben, **nur aus dieser Präregistrierung und je 3 Beispielzeilen der Rohdaten**, ohne Claudes Code (`orglab/nachrechnung.py`). Claude hat die Skripte vor dem Ausführen gelesen: nur Standardbibliothek, nur Lesezugriffe. Ausgeführt wurden sie isoliert (`python -I`). Skripte und Ausgaben liegen in `daten/E-022-reasoning-dosis/nachrechnung/`. Kosten 0,09 $.

| Größe | Claude (`orglab/e022.py`) | GPT | Gemini |
|---|---|---|---|
| vollständige Stapel | 24 | 24 | 24 |
| Median-Tokens low / medium / high / ohne | 257 / 257 / 896 / 903 | gleich | gleich |
| Manipulationscheck | nicht bestanden | nicht bestanden | nicht bestanden |
| P1 Schätzung | +0,04398 | +0,04398 | +0,04398 |
| P1 untere Grenze | +0,0255 | +0,0256 | +0,0256 |
| P2 Schätzung / obere Grenze | −0,0185 / 0,000 | gleich | gleich |
| FA und Übersehen je Arm | – | identisch | identisch |
| H-037 bestätigt | nein | nein | nein |

- **Die Zahlen sind reproduziert.** Die Unterschiede in den Bootstrap-Grenzen erklären sich durch andere Zufallsstartwerte und eine andere Quantilmethode.
- **Gefundene Lücke in Claudes eingefrorenem Skript:** Die Präregistrierung sagt "unter 16 vollständigen Stapeln nur deskriptiv". `analyze_data` setzt das **nicht** um, beide Fremd-Implementierungen schon. Hier ohne Folgen (24 Stapel), bei einem Abbruch hätte das Skript aber eine unzulässige Bestätigung melden können.
- **Forscher-Freiheitsgrade, die beide Fremdmodelle als offen gemeldet haben (Regel 16):**
  - Startwert und Quantilmethode des Bootstraps
  - welcher Versuch bei Wiederholungen gilt
  - Umgang mit fehlenden Urteilen
  - Gewichtung nach Beleg statt nach Stapel
  - dass die Generatorfehler-Regel ohne manuelle Klärung nicht automatisch anwendbar ist

  Keine davon hat hier das Ergebnis berührt, alle gehören aber künftig in die Präregistrierung.
