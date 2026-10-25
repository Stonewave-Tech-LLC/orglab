# E-023: Realität in Dosen mit Haiku – Ergebnis

- **Datum:** 2026-10-23
  - Hauptlauf endete vor 16:54, Auswertung bis 16:58 (Zeiten aus `date`)
- **Stufe:** Entdeckung mit gerichteten Vorhersagen (`prereg.md`, freigegeben 16:04)
- **Weg, Modell, Einstellung (Regel 11):**
  - Weg und Modell: OpenRouter/API, `anthropic/claude-haiku-5.5`
  - kein `reasoning`-Parameter, laut Probe und Lauf adaptives Denken: Median 1.092 Completion-Tokens je Prüfung, bei Sonnet 754
  - `max_tokens` 4000, höchstens 6 Werkzeugrunden
  - weggelassen: `temperature`, `top_p`, `seed`
  - Material v4.3, Seeds 6000–6023
  - Prompts und Code wie E-020 v3
- **Umfang:**
  - 2.304 Prüfungen, 2,18 $
  - **1 Ausfall** (Netzwerk-Timeout, `business-ok_noisy-6014`, SP0-ZU1-AU1). Nach der vorab festgelegten Regel fällt Seed 6014 ganz heraus. Ausgewertet werden **23 von 24 Seeds**, ohne Wiederholung des Aufrufs.
- **Reproduktion:** `python -m orglab.e023 analyze` (vollständige Ausgabe in `daten/E-023-haiku-dosen/auswertung.md`)

## Kurz
**Bei Haiku ist die Lage anders als bei Sonnet. Der Unterschied liegt nicht im allgemeinen Fehlerniveau, sondern darin, *welche* Faktoren wirken.**
- **V1 gestützt:** Fehlt der Sollwert im Auftrag, übersieht Haiku deutlich mehr. Der Effekt beträgt **+0,25**, bei Sonnet +0,006.
- **W1 gestützt (H-038):** Die Wechselwirkung Modell × SPEC beträgt **+0,25 [+0,19; +0,30]**. Ob der Sollwert im Auftrag steht, ist für Haiku wichtig, für Sonnet egal.
- **Mechanismus sichtbar (deskriptiv):** Haiku übersieht fast genau dann, wenn es nicht nachschlägt.
  - Normabschnitt erhalten: 7 % übersehen.
  - Nicht erhalten: 96 % übersehen.
  - Das ist der Mechanismus, den H-033 vermutet hat ("schlägt nicht nach").
- **Überraschung (explorativ):** Bekommt Haiku Werkzeuge, um die Kanäle selbst abzufragen, schlägt es im Runbook **seltener** nach (99 % → 54 %). Bei fehlendem Sollwert übersieht es dadurch *mehr*. Die Werkzeuge verdrängen das Nachschlagen.
- **V2 (Selbstauskunft → mehr Übersehen) bleibt null**, wie bei Sonnet. Stattdessen erhöht "All checks green" bei Haiku die **Fehlalarme** (+0,04). Haiku wird misstrauisch statt nachlässig.

## Vorab festgelegte Kontraste für Haiku

| | Kontrast | Schätzung [95-%-KI] | Vorhersage | Etikett | Sonnet (E-020) |
|---|---|---|---|---|---|
| **V1** | SPEC 1 − 0, 83 spec-reine Belege | **+0,253 [+0,202; +0,304]**, q < 0,001 | ≥ +0,10 | **Vorhersage gestützt** | +0,006, praktisch null |
| **V2** | AUSKUNFT 1 − 0, 138 kaputte Belege | −0,014 [−0,034; +0,005], q = 0,93 | ≥ +0,05 | praktisch null (Vorhersage widerlegt) | −0,016, praktisch null |
| V2 sekundär | nur spec-rein | −0,006 [−0,036; +0,021] | – | – | 0,000 |
| V2 Nebenvorhersage | Fehlalarm AUSKUNFT 1 − 0 | **+0,042 [+0,020; +0,065]** | sinkt | Gegenrichtung | 0,000 |
| **V3** | `run_check` AUSKUNFT 1 − 0 (ZUGANG = 1) | −0,01 [−0,01; +0,00] | < 0 | nicht gestützt (Decke 3,00 von 3) | −0,002 |
| V4 (deskriptiv) | SPEC = 1, spec-rein | Normabschnitt erhalten (252×): Übersehen 0,071. Nicht erhalten (80×): 0,963 | – | – | 336× erhalten, 0,042 |
| V5 (deskriptiv) | Eskalation bei Konfidenz < 0,80 | AU0: 22 % eskaliert, fängt 44 % der Fehler. AU1: 26 % eskaliert, fängt 54 % | – | – | 8 %, fängt 38 % / 17 % |

- **Ohne die 8 einzeln nicht entscheidbaren Belege** (vorab festgelegt): V1 +0,250 [+0,199; +0,304], gestützt. V2 −0,010 [−0,029; +0,010], praktisch null.
- **Sensitivität ohne Grenzfall 6021** (vorab festgelegt): V1 +0,250 [+0,198; +0,302], gestützt. V2 −0,015 [−0,035; +0,005], praktisch null.
  - **Lücke im eingefrorenen Skript:** `e023.analyze_both` rechnet diese Analyse nicht, obwohl die Präregistrierung sie "wie E-020" verspricht. Ich habe sie nach dem Lauf mit derselben Funktion nachgerechnet (`e020v3.analyze_data(…, exclude=GRENZFAELLE)`). Gefunden habe ich das selbst beim Schreiben dieses Ergebnisses. Das Ergebnis ändert sich nicht.
- **Generatorfehler-Regel:** Kein Beleg ist betroffen.

## Wechselwirkung Modell × Faktor (H-038), gepaart je Beleg: Haiku-Effekt − Sonnet-Effekt

| | Kontrast | Haiku | Sonnet | **Differenz [95-%-KI]** | Belege | Status |
|---|---|---|---|---|---|---|
| **W1** | V1 SPEC (spec-rein) | +0,253 | +0,006 | **+0,247 [+0,193; +0,298]** | 83 | gerichtet vorhergesagt (> 0): **erfüllt** |
| W2 | V2 AUSKUNFT | −0,014 | −0,016 | +0,002 [−0,020; +0,022] | 138 | keine Richtung, kein Unterschied |
| W3 | ZUGANG | **+0,105** | −0,085 | **+0,190 [+0,147; +0,237]** | 138 | keine Richtung, explorativ |

Ohne die 8 einzeln nicht entscheidbaren Belege: W1 +0,244 [+0,190; +0,297], W2 +0,004, W3 +0,169 [+0,127; +0,212].

### Zellen (sekundär)
| Zelle | Fehlalarm | Übersehen (alle) | Übersehen (spec-rein) | run_check | nachgeschlagen | PPV bei 5 % |
|---|---|---|---|---|---|---|
| SP0-ZU0-AU0 | 0,094 | 0,065 | 0,072 | 0,00 | 0,61 | 0,34 |
| SP0-ZU0-AU1 | 0,159 | 0,043 | 0,048 | 0,00 | 0,54 | 0,24 |
| SP0-ZU1-AU0 | 0,000 | 0,007 | 0,012 | 3,00 | 0,45 | 1,00 |
| SP0-ZU1-AU1 | 0,029 | 0,000 | 0,000 | 3,00 | 0,18 | 0,64 |
| SP1-ZU0-AU0 | 0,087 | 0,080 | 0,096 | 0,00 | 0,88 | 0,36 |
| SP1-ZU0-AU1 | 0,152 | 0,058 | 0,072 | 0,00 | 0,87 | 0,25 |
| **SP1-ZU1-AU0** | 0,007 | **0,333** | **0,470** | 3,01 | 0,51 | 0,83 |
| **SP1-ZU1-AU1** | 0,014 | **0,326** | **0,506** | 3,00 | 0,38 | 0,71 |

- Übersehen je Fehlerart, über alle Zellen:
  - stark: `low_traffic` 0,40, `wrong_terms` 0,25, `wrong_contact` 0,23, `db_down` 0,23, `cache_partial` 0,20
  - fast nie: die übrigen Fehlerarten (≤ 0,01)
- **Prävalenz (Regel 14):** Mit nur einem vorgelegten Kanal liegt der PPV eines Haiku-Alarms bei 5 % Prävalenz bei **0,24–0,36**. Zwei von drei Alarmen wären in der Praxis Fehlalarme. Mit allen Kanälen sind es 0,64–1,00.

## Manipulationschecks (Regel 10)
- **ZUGANG:** bestanden. `run_check` im Mittel 3,00 je Prüfung in allen ZUGANG=1-Zellen.
- **Werkzeugfähigkeit:** bestanden, 1 Ausfall von 2.304 (Timeout), höchstens 0,3 % je Zelle.
- **SPEC, AUSKUNFT:** Code-Tests aus E-020, unverändert.
- **Denken:** Haiku denkt ohne Parameter adaptiv (Probe: Denk-Tokens Median ~460, Sonnet ~200). Der Unterschied zu Sonnet ist also nicht "Haiku denkt nicht".
- **Ausgang laut Einordnungstabelle:** weder Boden noch Werkzeugproblem. Das Experiment ist für Haiku aussagekräftig.

## Doppelte Buchführung (Regel 19, freiwillig)
GPT-6.1 Sol und Gemini 4 Argon haben die Auswertung aus beiden Präregistrierungen (E-020 v3 und E-023) und drei Beispielzeilen neu geschrieben. Ich habe beide Skripte vollständig gelesen (nur Standardbibliothek, nur Lesezugriff) und isoliert ausgeführt (`python -I`). Ablage: `daten/E-023-haiku-dosen/nachrechnung/`.

| | Claude | GPT | Gemini |
|---|---|---|---|
| vollständige Seeds | 23 | 23 | 23 |
| V1 | +0,253 [+0,202; +0,304], gestützt | +0,253 [+0,202; +0,304], gestützt | +0,253 [+0,202; +0,307], gestützt |
| V2 | −0,014 [−0,034; +0,005], praktisch null | gleich | gleich |
| V3 | −0,01 [−0,01; +0,00] | −0,005 [−0,013; 0,000] | −0,005 [−0,013; 0,000] |
| Zellraten (Übersehen, Fehlalarm) | – | identisch | identisch |

Die gemeldeten offenen Entscheidungen sind dieselben wie bei E-020: Startwert für V3, p-Wert-Methode für BH, Rangfolge der Etiketten. GPT nannte zusätzlich: Ab welcher Fehlerrate gilt "Haiku liegt am Boden"? Die Einordnungstabelle nennt dafür keine Zahl, das ist ein Freiheitsgrad. Hier ohne Folgen, weil Haiku klar nicht am Boden liegt.

## Explorativ: Die Werkzeuge verdrängen das Nachschlagen
Gemeint sind spec-reine kaputte Belege mit SPEC = 1, also Sollwert nur im Runbook:

| | nachgeschlagen | Übersehen mit Nachschlagen | Übersehen ohne |
|---|---|---|---|
| ZUGANG = 0 (ein Kanal vorgelegt, nur das Runbook-Werkzeug) | **99 %** (164/166) | 0,07 | 1,00 (n = 2) |
| ZUGANG = 1 (Kanal-Werkzeuge plus Runbook) | **54 %** (89/166) | 0,08 | **0,96** (n = 77) |

- Hat Haiku nur das Runbook als Werkzeug, benutzt es das fast immer. Hat es dazu drei Kanal-Werkzeuge, ruft es die drei Kanäle ab, sieht übereinstimmende Daten und hört auf. Die Norm, gegen die die Daten zu prüfen wären, holt es dann nicht mehr.
- Transkript `business-fail_moderate-6013` (SP1-ZU1-AU1): SMTP, Zustellung, Buchhaltung und CRM stimmen überein, also urteilt Haiku "funktioniert" mit Konfidenz 0,9. Dass f.kraus nicht der Rechnungskontakt von K-30 ist, stünde im Runbook.
- **Für die Projektfrage ist das der wichtigste Hinweis des Tages:** "Mehr Werkzeuge" ist für ein schwächeres Modell kein reiner Gewinn. Ein Werkzeug, das *Daten* liefert, kann das Werkzeug verdrängen, das den *Maßstab* liefert. Bei Sonnet passiert das nicht (Nachschlagen 100 % auch mit Zugang).
- Das relativiert die Idee "Prüfer sollen Belege selbst holen" aus dem Gespräch nach E-020. Für Sonnet half das Holen (−0,03 ohne die nicht entscheidbaren Belege). Für Haiku schadet es, solange der Maßstab nicht im Auftrag steht. Die Lehre lautet also nicht "holen statt vorlegen", sondern: **Daten holen ja, aber der Maßstab muss mitkommen oder erzwungen werden.**

## Explorativ: Selbstauskunft macht Haiku misstrauisch, nicht nachlässig
- Die Fehlalarme sitzen fast nur bei verrauschten Ok-Belegen mit einem einzigen Kanal. Ohne Selbstauskunft sind es 19 von 138, mit Selbstauskunft 33 von 138. Mit allen Kanälen sind es 1 bzw. 4.
- Transkripte `coding-ok_noisy-6009` und `-6023`: Haiku antwortet auf "All checks green" mit Gegenrede ("is not backed by any response check"). Es wertet fehlende Belege und Rauschen als Fehler.
- Mögliche Materialfrage, ein **Hinweis**, kein Befund: Bei `coding-ok_noisy-6009` liest Haiku mehrere Boot-Sequenzen im Rauschen als Verstoß gegen "single production instance". Diese Formulierung kam erst mit v4.3 dazu. Sonnet hatte dort 0 Fehlalarme. Vor einem Folgeexperiment mit Haiku sollten die Rauschblöcke der Ok-Belege gegen die v4.3-Norm geprüft werden.

## Transkripte (Pflichtlektüre)
`transkripte.md`: 2 zufällige je Zelle (Seed 2020), dazu 3 gezielte Übersehen ohne Nachschlagen und 2 gezielte Fehlalarme unter Selbstauskunft. Gelesen habe ich die gezielten fünf. Sie zeigen die beiden Mechanismen oben.

## Einordnung (vorab festgelegte Lesarten, angewandt)
- **Erlaubt:**
  - Ob der Sollwert im Auftrag steht, ist **modellabhängig** wichtig: für Haiku 5.5 stark (+0,25), für Sonnet 5.5 nicht. Das stützt H-038 für diesen einen Faktor, innerhalb einer Modellfamilie, Stufe Entdeckung.
  - Die Selbstauskunft verführt auch Haiku nicht zum Übersehen.
- **Nicht erlaubt:**
  - "Sollwerte in den Auftrag schreiben ist eine Regel für Wave." Wave läuft mit starken Modellen, und dort zeigte sich nichts.
  - "Selbst holen schadet." Das gilt explorativ und nur für Haiku bei fehlendem Maßstab.
- **Für Wave daraus (Hinweis):** Wo schwächere oder billigere Modelle prüfen, etwa zur Kostensenkung, muss der Maßstab im Auftrag stehen oder das Nachschlagen erzwungen werden. Sonst hängt die Prüfqualität davon ab, ob das Modell zufällig nachschlägt.

## Grenzen
- Zwei Modelle derselben Familie. Der Sonnet-Lauf war einige Stunden früher.
- 23 statt 24 Seeds (ein Timeout).
- Materialgrenzen aus E-020: Zielzeile oben auf der Seite, 8 einzeln nicht entscheidbare Belege, möglicherweise mehrdeutiges Rauschen gegen "single instance".
- Die beiden Verdrängungs- und Misstrauensbefunde sind explorativ, also post hoc, und müssten auf frischen Seeds bestätigt werden.
- Kritiker-Unabhängigkeit: wie E-020. Neu ist kein Grok-Gutachten, weil der Lauf unter 10 $ blieb und sich nur das Modell geändert hat.

## Checkliste
- [ ] repliziert auf frischen Seeds (offen: V1 und W1 sind Kandidaten für einen Bestätigungslauf)
- [x] Manipulationscheck bestanden
- [x] vorab festgelegt (Präregistrierung mit Einordnungstabelle, Skript getestet)
- [x] Weg, Modell, Einstellung dokumentiert
- [x] Ground Truth fremdkontrolliert (aus E-020, gleiches Material)
- [x] Analyse-Einheit Beleg, gepaart über Modelle
- [x] von zwei Fremdmodellen nachgerechnet, Zahlen gleich
- [ ] verblindet (laut Präregistrierung nicht vorgesehen)
- [x] Prävalenz berichtet
- [x] Transkripte gelesen
- [x] mit einem Befehl reproduzierbar
