# E-024: Bestätigung "Der Maßstab muss mit" – Ergebnis

- **Datum:** 2026-10-23, Hauptlauf 19:41 bis vor 21:20, Auswertung bis 21:24 (Zeiten aus `date`)
- **Stufe: Bestätigung.** Frische Seeds 7000–7023, vorab festgelegte gerichtete Vorhersagen, verblindete Auswertung, doppelte Buchführung.
- **Weg, Modell, Einstellung:** OpenRouter/API, `anthropic/claude-haiku-5.5` (Ziel) und `anthropic/claude-sonnet-5.5` (Vergleich), beide ohne `reasoning`-Parameter, `max_tokens` 4000, höchstens 6 Werkzeugrunden. Material v4.3 unverändert. Code eingefroren bei Commit d3f6d31.
- **Umfang:** 4.608 Prüfungen, 36,10 $. 8 Ausfälle (Haiku 3, Sonnet 5). Damit sind **21 von 24 Seeds in beiden Modellen vollständig** (7010, 7015, 7016 fallen nach Regel heraus, ohne Wiederholung).
- **Reproduktion:**
  - `python -m orglab.e024 verblindet` (verblindet)
  - `python -m orglab.e024 analyze` (entblindet)
  - Ausgaben: `auswertung-verblindet.md`, `auswertung.md`

## Kurz
**Alle fünf vorab festgelegten Vorhersagen sind auf frischen Seeds bestätigt.** Die Effekte sind so groß wie in der Entdeckung (E-023), nicht geschrumpft.
- **H-033 für Haiku bestätigt:** Fehlt der Sollwert im Auftrag, übersieht Haiku deutlich mehr. Sonnet nicht.
- **H-038 für diesen Faktor bestätigt:** Ob der Maßstab im Auftrag steht, wirkt modellabhängig (Wechselwirkung +0,26).
- **H-039 für Haiku bestätigt, mit Präzisierung:** Datenwerkzeuge verdrängen bei Haiku das Nachschlagen des Maßstabs, und dadurch übersieht es mehr. **Der Schaden entsteht aber nur, wenn der Maßstab fehlt.** Steht er im Auftrag, helfen die Werkzeuge beiden Modellen.
- **H-040 bestätigt, klein:** Die Selbstauskunft erhöht bei Haiku die Fehlalarme (+0,03). Die Deutung ist offen, siehe unten.

## Vorab festgelegte Vorhersagen (Haiku, BH über fünf)

| Nr | Kontrast | **E-024** [95-%-KI] | Etikett | Sonnet | E-023 (Entdeckung) |
|---|---|---|---|---|---|
| **V1** | Übersehen SPEC 1 − 0, spec-rein (n = 76) | **+0,263** [+0,207; +0,322] | BESTÄTIGT | +0,003 | +0,253 |
| **W1** | V1 Haiku − V1 Sonnet, gepaart | **+0,260** [+0,204; +0,316] | BESTÄTIGT | – | +0,247 |
| **C1** | Nachschlagen ZUGANG 0 − 1 bei SPEC = 1 (n = 252) | **+0,472** [+0,417; +0,530] | BESTÄTIGT | −0,046 | +0,424 |
| **C2** | Übersehen ZUGANG 1 − 0 bei SPEC = 1, spec-rein | **+0,408** [+0,309; +0,513] | BESTÄTIGT | −0,092 | +0,404 |
| **F1** | Fehlalarm AUSKUNFT 1 − 0, einzeln entscheidbare Ok-Belege (n = 87) | **+0,029** [+0,014; +0,046] | BESTÄTIGT | 0,000 | +0,042 (alle Ok-Belege) |

Alle q < 0,001. Etiketten aus `e024.label`, nach Grok-Gutachten 5 auf die Präregistrierung abgebildet.

- **Ohne die 62 einzeln nicht entscheidbaren Belege:**
  - V1 +0,257, W1 +0,254, C1 +0,472, C2 +0,443, F1 +0,029, alle BESTÄTIGT
  - Sonnet-C2 dort −0,014, also etwa 0
- **Ohne Grenzfall 7009:** unverändert, alle BESTÄTIGT.
- **F1 deskriptiv auf allen Ok-Belegen** (wie in E-023): +0,046 [+0,030; +0,063].
- **Generatorfehler-Regel:** kein Beleg betroffen.

## Manipulationscheck (Regel 10), bestanden
| Modell | Ausfälle | höchster Ausfall je Zelle | `run_check` bei ZUGANG=1 | nachgeschlagen bei SPEC=1 | Tokens (Median) |
|---|---|---|---|---|---|
| Haiku 5.5 | 3 | 0,7 % | 3,00 | 0,64 | 1.072 |
| Sonnet 5.5 | 5 | 0,3 % | 3,00 | 0,97 | 766 |

## Verblindung (Regel 20)
- Verblindet um 21:20, die Modelle hießen A und B. Hash des Schlüssels: `verblindung.sha256`.
- Die Entscheidungen standen verblindet fest und wurden **vor** dem Entblinden committet (af3fb43, `auswertung-verblindet.md`):
  - 21 Seeds
  - Manipulationscheck bestanden
  - Generatorfehler-Regel ohne Treffer
  - für beide möglichen Zuordnungen festgehalten, was gilt
- Entblindet: **A = Haiku.**
- **Grenze**, wie vorab benannt: Das Muster verriet die Zuordnung praktisch. Ein Arm zeigte große Effekte, der andere keine. Die Verblindung hat hier die Ermessensentscheidungen geschützt, nicht die Unwissenheit.

## Doppelte Buchführung (Regel 19)
GPT-6.1 Sol und Gemini 4 Argon haben die Auswertung nur aus der Präregistrierung und drei Beispielzeilen neu geschrieben. Ich habe beide Skripte vollständig gelesen (nur Standardbibliothek, nur Lesezugriff) und isoliert ausgeführt (`python -I`). Ablage: `daten/E-024-bestaetigung-massstab/nachrechnung/`.

| | Claude | GPT | Gemini |
|---|---|---|---|
| vollständige Seeds | 21 | 21 | 21 |
| V1 | +0,263 [+0,207; +0,322] | +0,263 [+0,207; +0,322] | +0,263 [+0,207; +0,319] |
| W1 | +0,260 [+0,204; +0,316] | +0,260 [+0,207; +0,316] | +0,260 [+0,204; +0,316] |
| C1 | +0,472 [+0,417; +0,530] | +0,472 [+0,417; +0,528] | +0,472 [+0,417; +0,528] |
| C2 | +0,408 [+0,309; +0,513] | +0,408 [+0,309; +0,507] | +0,408 [+0,303; +0,513] |
| F1 | +0,029 [+0,014; +0,046] | +0,029 [+0,011; +0,046] | +0,029 [+0,014; +0,046] |
| Etiketten | 5 × BESTÄTIGT | gleich | gleich |
| Sonnet V1/C1/C2/F1 | +0,003 / −0,046 / −0,092 / 0,000 | gleich | gleich |

- **Offene Entscheidungen, die die Fremdmodelle gemeldet haben** (GPT 16, Gemini 5). Für die Zahlen ohne Folgen:
  - p-Wert mit oder ohne +1-Korrektur
  - `random.choices` oder `randrange`
  - Format der Ausschlussdatei, das nicht festgelegt war
  - Nenner der Ausfallquote: geplante oder beobachtete Belege
  - Reihenfolge der Belege vor dem Bootstrap
- GPT merkt zudem an, dass die SPEC- und AUSKUNFT-Codetests und die Rundenauswertung aus den Urteilen allein nicht nachprüfbar sind. Das ist richtig, beides hängt am Code und an den Transkripten.

## Diagnose (vorab festgelegt, deskriptiv, ohne BH)
- **ZUGANG 1 − 0 auf Übersehen bei SPEC = 0** (Maßstab im Auftrag), spec-rein:
  - Haiku −0,066 [−0,125; −0,020]
  - Sonnet −0,086 [−0,151; −0,026]
  - **Folge:** Mit Maßstab im Auftrag *helfen* die Kanal-Werkzeuge beiden Modellen. Der C2-Schaden bei Haiku hängt am fehlenden Maßstab, nicht am Zugang an sich. Das war Groks Alternativerklärung (`notizen/23e`), und sie trifft zu.
- **Rundengrenze:** Von 341 Haiku-Prüfungen mit SPEC=1 und ZUGANG=1 ohne Nachschlagen hat **keine** die Grenze von 6 Werkzeugrunden erreicht. Haiku hört freiwillig auf und hat noch Runden übrig.
- **V4, deskriptiv:** Haiku mit Normabschnitt übersieht 6,7 %, ohne Normabschnitt 97,5 % (wie E-023: 7 % gegen 96 %).

## Transkripte
`transkripte.md`: je Modell 1 zufälliger Verlauf je Zelle, dazu je Modell 3 gezielte (SPEC=1, ZUGANG=1, nicht nachgeschlagen).
- Die gezielte Ziehung traf zufällig Fälle, die auch ohne Maßstab lösbar sind, etwa `row_loss` oder `bounced`. Deshalb habe ich zusätzlich einen typischen Fehlschlag gelesen.
- **Typischer Fehlschlag, Haiku, `coding-fail_subtle-7023`, `low_traffic`:**
  - Haiku ruft `deploy`, `probe` und `sockets` ab und schlägt nie im Runbook nach.
  - Schluss: "the new version is serving production traffic correctly", Konfidenz 0,87.
  - Welche Last normal wäre, weiß es nicht.
  - Dieses Muster gab es 81 Mal (SPEC=1, ZUGANG=1, nicht nachgeschlagen, spec-rein übersehen).

## Was das heißt (Status: bestätigt für Haiku 5.5 in diesem Aufbau)
1. **Harness-Regeln sind modellabhängig.** Ob der Maßstab im Auftrag stehen muss, ist für Sonnet egal und für Haiku entscheidend. Das ist jetzt kein Hinweis mehr, sondern auf frischen Seeds bestätigt. Gilt innerhalb einer Modellfamilie.
2. **Der Mechanismus ist "Daten statt Maßstab".** Das schwächere Modell holt sich Daten, sieht, dass sie zusammenpassen, und hört auf. Die Frage "verglichen womit?" stellt es nicht von selbst. Sonnet stellt sie fast immer (Nachschlagen 97 %).
3. **Die praktische Regel lautet nicht "weniger Werkzeuge".** Mit Maßstab im Auftrag helfen die Werkzeuge beiden Modellen. Die Regel lautet: **Bei schwächeren Prüfern gehört der Maßstab in den Auftrag**, oder das Nachschlagen muss erzwungen werden. Daten holen lassen ist gut, den Maßstab holen lassen ist riskant.
4. **F1 ist klein und mehrdeutig.** "All checks green" erhöht Haikus "kaputt"-Urteile bei Ok-Belegen um 3 Prozentpunkte, auch auf den einzeln entscheidbaren. Das kann Misstrauen gegen die Selbstauskunft sein. Es kann auch Strenge sein, weil der Erfolg zwar entscheidbar, aber nicht vollständig belegt ist. Das trennt erst das geplante Vertrauens-Experiment (H-041), mit der dritten Antwort "nicht belegt".
5. **Für Wave (alles auf Sonnet):** Direkt übertragbar ist nichts. Sonnet zeigt keinen der Effekte. Übertragbar ist das **Fehlerbild**: Ein Prüfer, der Daten holt, Übereinstimmung sieht und aufhört, ohne gegen den Maßstab zu prüfen. Ob Sonnet unter Last so wird, ist die offene Wave-Frage.

## Grenzen
- Eine Modellfamilie (Anthropic), ein Aufbau (ein Prüfer, ein Beleg, kein Zeitdruck).
- Material mit bekannten Schwächen: 62 Belege einzeln nicht entscheidbar, Zielzeile oben auf der Runbook-Seite. Die Analysen ohne die 62 ändern nichts.
- Die Verblindung war hier schwach (Muster eindeutig), die Entscheidungen standen aber vorher fest.
- F1 hatte vorab nur eine Power von 0,3. Der Treffer ist echt (q < 0,001 auf frischen Seeds), aber klein.
- Kritiker-Unabhängigkeit: Design und Prüfer sind Claude. Das Design haben Grok (Gutachten 3–5) und GPT (Material) geprüft, die Auswertung GPT und Gemini nachgerechnet.

## Checkliste
- [x] repliziert auf frischen Seeds (E-023 → E-024)
- [x] Manipulationscheck bestanden
- [x] vorab festgelegt: Präregistrierung, Code eingefroren d3f6d31, Etiketten nach Gutachten korrigiert vor dem Start
- [x] Weg, Modell, Einstellung dokumentiert
- [x] Ground Truth fremdkontrolliert: alle Kanäle 47/48, Einzelkanal 226/288, Lecktest 0/42
- [x] Analyse-Einheit Beleg, gepaart über Modelle
- [x] von zwei Fremdmodellen nachgerechnet, Zahlen gleich
- [x] verblindet ausgewertet, erst danach entblindet (mit benannter Grenze)
- [x] Prävalenz: entfällt für die Kontraste. Fehlalarmniveau Haiku siehe E-023
- [x] Kritiker vorab: Grok-Gutachten 5
- [x] Transkripte gelesen
- [x] mit einem Befehl reproduzierbar
- [ ] A/A und Positivkontrolle: nicht Teil dieses Designs. Die Sonnet-Spalte wirkt als Gegenprobe (keine Effekte).

## Nachtrag 23.10.2026 22:44: Dritter Prüfer (`notizen/34-dritter-pruefer/00-vergleich.md`)
Ein frischer Claude und GPT haben die Rohdaten aus E-020, E-023 und E-024 unabhängig ausgewertet, ohne unsere Ergebnisse und Thesen zu kennen. Korrekturen und Schärfungen an diesem Ergebnis:
- **V1 ist bei Haiku praktisch ganz eine Wechselwirkung mit ZUGANG.**
  - Bei ZUGANG = 0 kostet der fehlende Sollwert nur −0,7 pp.
  - Bei ZUGANG = 1 sind es −15 pp.
  - Die SP × ZU-Wechselwirkung hält auch auf der Logit-Skala (−2,6 / −2,2), sie ist also kein Skalenartefakt.
  - Die Lesart oben ("fehlender Sollwert → mehr Übersehen") ist deshalb zu ungenau. Richtig ist: **Der fehlende Sollwert schadet Haiku nur, wenn es zugleich Daten-Werkzeuge hat.**
- **Die Kompetenzgrenzen-Lesart ist nicht gestützt.** Mit unabhängigen Schwierigkeitsschätzern hängt die Wirkung an Fehlerart und Mechanismus, nicht an einer Schwierigkeitsachse. Ein naives Muster entsteht durch Regression zur Mitte (Nullsimulation).
- **Das GPT-Einzelkanal-Label ist mit GPTs Urteilsneigung vermengt** ("nicht entscheidbar" fiel immer mit "kaputt" zusammen). Die Ausschlussliste der 62 Belege bleibt als vorab festgelegte Sekundäranalyse gültig, misst aber nicht sauber "Entscheidbarkeit".
- **Neu:**
  - Die Selbstauskunft senkt Haikus Nachschlagen um 11–12 pp (beide Seed-Sätze).
  - Haiku verpasst spec-reine Fehler mit höherer Konfidenz als die erkannten (explorativ).

## Nachtrag 23.10.2026 23:01: Statuskorrektur zu "Was das heißt", Punkt 1
- "Harness-Regeln sind modellabhängig … jetzt kein Hinweis mehr, sondern bestätigt" ist zu weit gefasst.
- Bestätigt ist die **Wechselwirkung eines Faktors (Sollwert im Auftrag × Daten-Werkzeuge) mit dem Modell**, für Haiku 5.5 gegen Sonnet 5.5, im synthetischen Aufbau.
- Eine allgemeine Aussage "Harness-Regeln sind modellabhängig" ist ein Hinweis, keine Bestätigung.
- Status aller Kernaussagen: `notizen/34-dritter-pruefer/00-vergleich.md`, Abschnitt "Status der Kernaussagen".

## Nachtrag 24.10.2026 23:32: Kritiker-Einwände aus dem Lichttest geprüft (`notizen/36-kritiker-einwaende-e024.md`, explorativ)
Status: **explorativ**, nachträgliche Analyse, keine neue Bestätigung. Kein Etikett und kein Status ändert sich. Freigegeben von Neo.
- **Cluster-Bootstrap über die 21 Seeds statt über Belege:**
  - Alle fünf Etiketten bleiben unverändert.
  - Die Intervalle sind schmaler (60–90 % der Breite).
  - Die ICC innerhalb eines Seeds ist negativ, weil jeder Seed eine ausgewogene Schicht Domäne × Art ist.
  - Der präregistrierte Bootstrap über Belege ist damit der vorsichtigere.
- **`prereg.md` Z. 134 ("Primär: alle Belege")** ist ein Überbleibsel aus dem Entwurf, der vor der F1-Einschränkung entstand.
  - Gemeint und umgesetzt ist F1 auf den einzeln entscheidbaren Ok-Belegen (Z. 42, 59, 97, 110), von beiden Nachrechnungen so gelesen.
  - F1 auf allen Ok-Belegen wäre ebenfalls bestätigt.
  - Für F1 ist die Sekundäranalyse "ohne die 62" mit der primären identisch.
