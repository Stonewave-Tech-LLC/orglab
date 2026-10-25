# E-018: Beleg schlägt Stimme – Ergebnis (Bestätigung)

- **Zeitraum:** 2026-10-22, 00:18–03:21, mit einer Pause durch den Limit-Wächter bis 02:52
- **Rohdaten:** `daten/E-018-beleg-statt-stimme/` (40 Runs, Audit sauber, 20 Paare, frische Seeds 200–209)
- **Auswertung:** `python experimente/E-018-beleg-statt-stimme/auswertung.py` (genau der Plan aus `prereg.md`)

## Primärtest (vorab festgelegt)
| Metrik | Abstimmung Q2 (V2a) | Frist-Regel (F) | Δ F − V2a (95%-KI) | p einseitig |
|---|---|---|---|---|
| **Verlust bei Ehrlichen pro Run** | 11,40 | 0,05 | **−11,35** (−12,20 bis −10,40) | < 0,001 |

Der beobachtete p-Wert von 0,00005 ist die Untergrenze bei 20.000 Permutationen. Alle 20 Paare zeigen dieselbe Richtung, der exakte Wert liegt bei etwa 1e−6.

**P1 bestätigt.** Unter demselben Angriff verlieren ehrliche Agenten mit der Frist-Regel praktisch nichts (1 Freigabe in 20 Runs). Mit der Abstimmung verlieren sie rund 11 Pakete pro Run.

## Sekundär (beschreibend)
| Metrik | V2a | F | Δ (95%-KI) |
|---|---|---|---|
| true_completion | 0,864 | 0,896 | +0,032 (−0,029 bis +0,086) → **nicht unterlegen** (untere Grenze > −0,05) |
| Stimmen pro Run | 36,5 | 0 | – |
- **Manipulationscheck bestanden:** In 20 von 20 V2a-Runs verloren Ehrliche Pakete.
- **Repliziert E-015:** Damals 11,0 Diebstähle mit Q2 und 0,1 mit der Frist-Regel, jetzt 11,4 und 0,05.

## Einordnung, ehrlich
- **Was bestätigt ist:** Eine Übernahme-Regel, die an einem Umwelt-Beleg hängt (ein Fremdcheck ist fehlgeschlagen), schützt Ehrliche vor mitstimmenden Saboteuren. Dabei leistet sie mindestens so viel wie die Abstimmung.
- **Was davon Konstruktion ist:** Dass Lügen-Stimmen die Frist-Regel nicht auslösen können, folgt aus ihrem Design. Die Saboteure haben dort schlicht keinen Hebel. Der empirische Gehalt liegt in zwei Punkten:
  1. Die ehrlichen LLM-Agenten missbrauchen die Frist-Regel nicht (0,05 Fehlfreigaben pro Run).
  2. Die Regel kostet gegenüber der Abstimmung keine Leistung.
  - Die Botschaft "Beleg statt Stimme" ist damit ein Design-Prinzip, das sich im Betrieb bewährt. Eine Naturbeobachtung ist es nicht.
- **Nicht getestet:** Saboteure, die Belege fälschen. Ein Fremdcheck, der lügt, oder ein manipulierter Prüfer würde die Frist-Regel angreifen. Das ist der natürliche nächste Angriff und hängt mit H-026 zusammen (korrelierte Prüferfehler).
- **Teil 1 von H-028** (der 3f+1-Zielkonflikt, Q3 ist tot) war nicht Teil dieser Bestätigung und bleibt eine Entdeckung.

## Checkliste (CLAUDE.md)
- [x] repliziert auf frischen Seeds, vorab festgelegt, Effektgröße relevant (11 Pakete pro Run)
- [x] A/A und Positivkontrolle der Pipeline (E-005), Audit sauber
- [ ] Kritiker aus anderer Modellfamilie (fehlt)
- [x] Transkripte von Neo gelesen (offen: je Arm 2 Runs)
- [x] mit einem Befehl reproduzierbar
- Eval-Awareness: Die Saboteure sind Skripte, die ehrlichen Agenten bekommen keinen Hinweis

## Grenzen
- Ein Modell (Sonnet 5.5), ein Szenario (`mole_2`, n = 4, f = 2), geskriptete Saboteure mit einer einzigen Angriffsstrategie
