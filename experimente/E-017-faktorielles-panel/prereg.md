# E-017: Faktorielles Prüfer-Panel (Information × Stil × Erfahrung) – Präregistrierung

> **Vor dem ersten Hauptlauf committen.** Kalibrierungsläufe (Stufe 0) sind vorher erlaubt und ändern nur die Belegschwierigkeit, nichts an Faktoren, Metriken oder Tests. Was danach geändert wird, steht unten unter "Abweichungen", mit Datum und Grund.

- **Datum:** 2026-10-22
- **Stufe:** Entdeckung, mit gerichteten Vorhersagen. Eine Bestätigung folgt bei Bedarf auf frischen Seeds (3000+) als eigenes Experiment.
- **Hypothesen:** H-029 (verfeinert H-026), H-030 (verfeinert H-018), H-031. Siehe `hypothesen.md`.
- **Hintergrund:**
  - E-016 hatte einen Deckeneffekt, weil die Belege zu leicht waren.
  - Die Literatur zeigt starke Fehlerkorrelation auch über Modellfamilien hinweg. Dekorrelation kommt dort eher aus Information und Prüfverfahren als aus Persona oder Modellwechsel (`notizen/18-recherche/00-synthese.md`).
  - **Kein Paper kreuzt diese Faktoren im selben Design.** Genau das macht E-017.

## Frage

Was macht mehrere Prüfer *desselben Modells* unabhängiger, also weniger gemeinsam falsch?

1. Verschiedene **Information**: verschiedene Beobachtungskanäle desselben Vorgangs
2. Verschiedener **Stil**: Etiketten-Persona
3. Verschiedenes **Verfahren**: Prüfmethode
4. Verschiedene **Erfahrung**: private Rohepisoden

Und wie viel davon kommt in der Panel-Genauigkeit an?

## Konkrete Vorhersagen (gerichtet)

Primärgröße ist φ̄, die mittlere paarweise Fehlerkorrelation im 3er-Panel (Definition unter Metriken). Δ bezeichnet die Differenz der Faktorstufen, gemittelt über die übrigen Faktoren und gepaart über Belege.

| Nr | Kontrast | Vorhersage | Widerlegt, wenn |
|---|---|---|---|
| V1 | Information: verschiedene Kanäle (I1) − gleicher Kanal (I0) | Δφ̄ ≤ −0,15 | Obergrenze 95-%-KI ≥ 0 |
| V2 | Etikett: Persona (S1) − neutral (S0) | kein relevanter Effekt: 90-%-KI liegt in [−0,10; +0,10] (Äquivalenz) | Δφ̄ ≤ −0,10 mit KI-Obergrenze < 0 (Etiketten dekorrelieren doch) |
| V3 | Verfahren: verschiedene Prüfverfahren (S2) − neutral (S0) | Δφ̄ ≤ −0,10, **und** die Einzelfehlerrate steigt oder bleibt gleich | Obergrenze 95-%-KI ≥ 0 |
| V4 | Erfahrung: disjunkt (E2) − gleich (E1) | Δφ̄ < 0 (≈ −0,05) | Obergrenze 95-%-KI ≥ 0 |
| V5 | Erfahrung: gleich (E1) − keine (E0) | Δφ̄ ≥ 0 (geteilte Erfahrung homogenisiert) | Δφ̄ < 0 mit KI-Obergrenze < 0 |
| V6 | Rangfolge der Dekorrelation | \|Δ_I\| > \|Δ_Verfahren\| > \|Δ_Erfahrung\| > \|Δ_Etikett\| ≈ 0 | deskriptiv; wird ohne Test berichtet |
| V7 | Zusatzarm: Modelldiversität vs. Kanaldiversität (S0/E0) | Der Wechsel von 3× Sonnet auf 3 Familien senkt φ̄ **weniger** als der Wechsel von gleichem auf verschiedene Kanäle | Δφ̄(Familie) − Δφ̄(Kanal) < 0 mit KI-Obergrenze < 0 |

**Gesamtbild, das H-029 bis H-031 stützen würde:** Information und Verfahren dekorrelieren, Etiketten nicht, private Erfahrung schwach. Geteilte Erfahrung homogenisiert, ein Modellwechsel bringt weniger als ein Kanalwechsel.

**Gesamtbild, das sie widerlegen würde:**
- I1 dekorreliert nicht (V1 widerlegt), **oder**
- Etiketten dekorrelieren so stark wie Information.

## Design

### Material: Belege v2 (Mehrkanal), `orglab/evidence.py` erweitert

Für jeden Vorgang gibt es **drei unabhängige Beobachtungskanäle**. Jeder ist für sich allein entscheidbar:

| Domäne | Kanal A | Kanal B | Kanal C |
|---|---|---|---|
| coding | Deploy/Prozessmanager-Ausgabe | HTTP-Sonden (/version, /health) | Socket-/Prozesstabelle (ss, ps) |
| business | SMTP-/Versand-Log | Zustell-/DSN-Bericht | Buchhaltungs-/CRM-Eintrag |
| research | Job-Log | Ausgabedatei-Statistik | nachgelagerte Schema-/Plausibilitätsprüfung |

Anforderungen an den Generator:

- **Jeder Fehler hinterlässt in jedem Kanal eine eigene, unabhängig formulierte Spur.** Das ist Pflicht, sonst wäre "verschiedene Kanäle" mit "manche Prüfer sind blind" vermischt.
- Ein Test (`tests/test_evidence.py`) prüft je Fehlerart und Kanal, dass die Spur vorhanden ist und Ok-Belege keine haben.
- **Belegarten:** `ok_clear`, `ok_noisy` (beunruhigendes, aber harmloses Rauschen), `fail_moderate`, `fail_subtle`. Die Subtilität wird in Stufe 0 kalibriert.
- **Keine Injection-Belege.** Manipulation hat E-016 behandelt, hier würde sie die Korrelation vermischen.
- Jeder Beleg führt ein Feld `subtlety` (1–3) für die Sekundäranalyse "Ort der Korrelation" (HK-A4).
- **Hauptlauf:** Seeds 2000–2019 × 3 Domänen × 4 Arten = **240 Belege** (je 60 pro Art, also 50 % ok und 50 % kaputt).
- **Erfahrungspool:** Seeds 500–699, getrennt von Haupt- und Kalibrierungsseeds.

### Panel: immer 3 Prüfer, ein Aufruf pro Prüfer und Beleg

| Faktor | Stufen | Umsetzung |
|---|---|---|
| **I – Information** | I0 gleicher Kanal · I1 verschiedene Kanäle | **I0:** Alle drei sehen denselben Kanal. Welcher, rotiert über die Belege (Seed mod 3), damit jeder Kanal gleich oft vorkommt. **I1:** Prüfer k sieht Kanal (k + Seed) mod 3. Die Informationsmenge pro Prüfer ist in beiden Stufen gleich. |
| **S – Stil/Verfahren** | S0 neutral · S1 Etiketten-Persona · S2 Verfahrens-Persona | **S0:** Prompt wie E-016. **S1:** drei Personas, die sich nur in Name, Hintergrund und Temperament unterscheiden. Keine Wörter wie "careful", "skeptical" oder "thorough". **S2:** drei Prüfverfahren, siehe unten. In S1 und S2 bekommt Prüfer k Persona bzw. Verfahren k. |
| **E – Erfahrung** | E0 keine · E1 gleiche · E2 disjunkte | Je **6 Rohepisoden** aus dem Pool (3 ok, 3 kaputt, gemischte Domänen). Jede Episode enthält Arbeitsauftrag, Ausgabe *eines* Kanals, das später festgestellte Ergebnis und einen Satz zum *Befund* (keine verallgemeinerte Lehre, siehe `notizen/18`, Cluster E). **E1:** pro Beleg ein Episodenset, das alle drei teilen. **E2:** pro Beleg drei disjunkte Sets. Ziehung per Seed aus Beleg-ID und Prüferposition. |

**S2-Verfahren** (englisch im Prompt, sinngemäß):

1. **Falsifizieren:** Erst drei konkrete Wege nennen, wie der Auftrag trotz gutem Anschein gescheitert sein könnte. Dann jeden prüfen.
2. **Commit first:** Vor dem Lesen der Ausgabe aufschreiben, was zu sehen sein müsste, wenn es funktioniert hat. Dann abgleichen.
3. **Konsistenzprüfung:** Jede Stelle finden, an der die Ausgabe dieselbe Tatsache zweimal nennt (Version, ID, Anzahl, Empfänger). Dann prüfen, ob die Angaben übereinstimmen.

**Antwortformat:**
- Alle Prompts enden mit derselben JSON-Anweisung wie in E-016.
- Vorher ist Text erlaubt, das ist für S2 nötig.
- Geparst wird das **letzte** JSON-Objekt der Antwort. Der Parser aus E-016 nimmt das erste `{` bis zum letzten `}` und bricht deshalb bei Text vor dem JSON.

**Zellen:** I(2) × S(3) × E(3) = **18 Zellen**, alle auf denselben 240 Belegen (gepaart).

**Zusatzarm Familie:**
- Panel: `anthropic/claude-sonnet-5.5`, `openai/gpt-6.1-sol`, `google/gemini-4-argon`.
- Bedingungen: S0/E0, jeweils mit I0 und I1. Das sind 2 Zellen.
- Zusammen mit den Sonnet-Zellen S0/E0/I0 und S0/E0/I1 entsteht ein 2×2-Vergleich: Modelldiversität × Kanaldiversität.

**Generalisierung (sekundär):**
- Das volle 18-Zellen-Design wird mit `anthropic/claude-haiku-5.5` wiederholt (geschätzt ~3 $).
- Nur wenn Haiku in Stufe 0 im Zielbereich liegt.

### Konstant gehalten
- Prompt-Rahmen ohne "test"/"benchmark" (Eval-Awareness)
- Standard-Temperatur, Reasoning-Effort "low" wo unterstützt, `max_tokens` 1500
- **Eine Stichprobe pro Prüferposition.** In der Zelle I0/S0/E0 sind die drei Prüfer drei Stichproben desselben Prompts. Das ist die Resampling-Baseline wie in E-016.

### Modelle (exakte IDs, über OpenRouter)
- **Primär:** `anthropic/claude-sonnet-5.5`
- **Zusatzarm:** `openai/gpt-6.1-sol`, `google/gemini-4-argon`
- **Generalisierung:** `anthropic/claude-haiku-5.5`

### Umfang
| Teil | Rechnung | Urteile |
|---|---|---|
| Hauptlauf Sonnet | 240 × 18 × 3 | 12.960 |
| Zusatzarm | 240 × 2 × 3 | 1.440 (davon 960 Fremdmodelle) |
| Haiku | 240 × 18 × 3 | 12.960 |

### Kosten
- **Grundlage:** E-016-Ledger (Sonnet 0,00155 $ pro Aufruf bei ~310 Input-Tokens) und hier im Mittel ~3× längere Prompts.
- **Schätzung:** Sonnet ≈ 40 $, Fremdmodelle ≈ 2 $, Haiku ≈ 3 $, Kalibrierung ≈ 5 $.
- Läuft wegen des Tageslimits von 50 $ verteilt auf 2 Tage.

## Stufe 0: Kalibrierung (vor dem Hauptlauf, D-010)

- **Seeds:** 1000–1009 × 3 Domänen × 4 Arten = 120 Belege.
- **Modell:** Sonnet 5.5, Zelle I0/S0/E0, ein Urteil pro Beleg und Kanal (also 360 Urteile).

**Annahmekriterien** (alle müssen erfüllt sein):
1. Einzelfehlerrate von Sonnet über alle Belege zwischen **0,10 und 0,40**
2. Fehlerraten der drei Kanäle innerhalb einer Spanne von **±0,10** zueinander (Kanalbalance, sonst ist I mit Kanalschwierigkeit vermischt)
3. Sowohl Ok- als auch Fail-Belege mit Fehlerrate ≥ 0,03 (Fehlalarme *und* Übersehen kommen vor)
4. Stichprobe: Ich lese 10 falsch beurteilte Belege und bestätige, dass die Ground Truth stimmt (Lehre aus dem E-016-Pilot)

**Ablauf:**
- Höchstens 3 Iterationen. Jede Iteration ändert nur Subtilitätsparameter des Generators und steht mit Begründung im Laborbuch.
- Bleibt das Kriterium nach 3 Iterationen verfehlt, wird abgebrochen und neu geplant.
- Kalibrierungsdaten fließen **nie** in die Hauptauswertung ein.
- Für Haiku gilt dieselbe Kalibrierung mit denselben Kriterien, aber nur als Ja/Nein-Entscheid über den Generalisierungsarm. Es wird nicht separat nachjustiert.

## Metriken

Fehlerindikator: e = 1, wenn das Urteil `works` ≠ Wahrheit ist. Unparsbare Antworten zählen nicht als Fehler, sondern fehlen.

### Primär (genau eine)

**φ̄ je Zelle**
- **Definition:** Mittelwert der drei paarweisen φ-Koeffizienten der Fehlerindikatoren der Prüferpositionen (1,2), (1,3), (2,3). Berechnet über alle Belege, für die alle drei Urteile vorliegen.
- **Abgeleitet:** Kish-n_eff = 3 / (1 + 2·φ̄).
- **Relevanzschwelle:** |Δφ̄| ≥ 0,10. Bei φ̄ ≈ 0,5 heißt das n_eff von 1,5 auf ≥ 1,7.

### Sekundär
1. **Exzess-Kofehler:** β = P(alle drei irren), dazu das Verhältnis β / (p₁·p₂·p₃).
2. **Panel-Fehlerrate:** Die Mehrheit von 3 irrt. Das ist die praktische Frage, ob Dekorrelation in Genauigkeit ankommt (Ambiguity-Zerlegung: Diversität gegen Einzelgenauigkeit).
3. **Einzelfehlerrate** je Zelle und Position. Das sind die Kosten der Diversität, Teil von V3.
4. **Escape Rate:** Die Mehrheit winkt einen kaputten Beleg durch.
5. **Interaktionen** I×S und I×E (explorativ).
6. **Ort der Korrelation:** φ̄ getrennt nach `subtlety` und Belegart (HK-A4, explorativ).
7. **Kalibrierung:** Fehlerrate nach Konfidenzband je Zelle. Bleibt Konfidenz ein Eskalationssignal (E-016)?
8. **Zusatzarm:** 2×2 Modell × Kanal, Effekt auf φ̄ und Panel-Fehlerrate.
9. **Haiku:** Vorzeichen und Größe von Δ_I, Δ_S1, Δ_S2, Δ_E2−E1 im Vergleich zu Sonnet.
10. **Kosten:** $ und Tokens je Zelle, $ pro korrektem Panel-Urteil.

## Auswertungsplan

- **Skript:** `python -m orglab.panel analyze --experiment E-017-faktorielles-panel`. Erweitert um Faktorzellen, Kontraste und Bootstrap. Die Auswertung läuft nur aus `daten/E-017-faktorielles-panel/judgments.jsonl`.
- **Kontraste V1–V5:** Für jeden Haupteffekt wird φ̄ je Zelle berechnet und die Stufendifferenz über die übrigen Zellen gemittelt.
- **Unsicherheit:** Cluster-Bootstrap über **Belege** mit 5.000 Ziehungen. Alle Zellen werden mit demselben Beleg-Resample neu berechnet, das erhält die Paarung. Berichtet werden 95-%-KI (V2: 90-%-KI für die Äquivalenz) und einseitige Bootstrap-p-Werte für die gerichteten Vorhersagen.
- **Mehrfachtests:** Benjamini-Hochberg über V1, V3, V4, V5, berichtet als q-Werte. V2 ist ein Äquivalenztest (TOST mit Grenzen ±0,10). V6 ist deskriptiv. V7 hat ein eigenes 95-%-KI.
- **Effektgröße vor p.** Die Leitfrage lautet: Ändert sich n_eff so, dass ein 3er-Prüfpanel in Wave/Ace spürbar mehr fängt (Panel-Fehlerrate)?
- **Ausschlüsse:**
  - Technisch fehlgeschlagene Aufrufe werden bis zu zweimal wiederholt, danach fehlen sie.
  - Fehlen in einer Zelle > 5 % der Urteile, gilt der Abbruch unten.
  - **Generatorfehler-Regel:** Belege, die über alle Zellen von ≥ 80 % der Urteile falsch beurteilt werden, prüfe ich vor der Auswertung von Hand. Ausgeschlossen wird nur, wenn die Ground Truth nachweislich falsch generiert ist. Schwierigkeit allein ist kein Grund. Jeder Ausschluss wird dokumentiert, und die Analyse wird zusätzlich ohne Ausschlüsse berichtet.
- **Pipeline-Kontrollen:**
  - **A/A:** Die Zelle I0/S0/E0 wird ein zweites Mal unter anderem Zellnamen erhoben, also 720 zusätzliche Sonnet-Urteile (~2 $). Erwartung: |Δφ̄| < 0,05 und KI enthält 0.
  - **Positivkontrolle:** In einer Zelle "I0-Blind" sieht Prüfer 3 einen Kanal, aus dem die Fehlerspur entfernt wurde. Das muss φ̄ messbar verändern und seine Fehlerrate erhöhen. Explorativ, ~720 Urteile.
- **Transkripte:** Je Zelle 3 zufällige Belege mit allen drei Begründungen, auch für I0/S0/E0, als Pflichtlektüre für Neo (`orglab.digest`, analog).

## Abbruchkriterien
- Gesamtkosten > 80 $ → Stopp und Rücksprache mit Neo.
- Parse- oder Fehlerquote > 5 % in einer Zelle → Stopp, Fix, und betroffene Zellen neu (Rohdaten bleiben erhalten, die alte Erhebung wird als ungültig markiert).
- Ein Generatorfehler in mehr als 2 % der Belege → Stopp. Neuer Generator, **neue Seeds** (2100+), Abweichung dokumentieren.
- Kalibrierung nach 3 Iterationen nicht erfüllt → kein Hauptlauf.

## Offene Schwächen (vorab benannt)
- **Kritiker-Unabhängigkeit:** Design, Belege und Auswertung stammen von Claude, die Prüfer im Hauptlauf sind ebenfalls Claude. Der Zusatzarm mildert das nur für die Prüferseite.
- **Externe Validität:** Synthetische Belege mit drei sauber getrennten Kanälen sind sauberer als echte Logs. Ein Effekt hier ist eine Obergrenze dafür, was Kanaltrennung in Wave bringen kann.
- **Erfahrung als Few-Shot:** Episoden im Prompt sind Gedächtnis in seiner einfachsten Form. Abstrahierte Lehren und echtes Langzeitgedächtnis sind nicht getestet (siehe HK-E3).
- **Eine Stichprobe pro Position:** Positionseffekte in S1/S2 (Persona k gleich Position k) sind mit Persona-Identität vermischt. Für φ̄ ist das unkritisch, für die Einzelfehlerrate je Persona nur deskriptiv.

## Implementierung (vor Stufe 0)
1. `evidence.py`: Mehrkanal-Generator v2 mit `subtlety`, Tests für Spurvollständigkeit.
2. `panel.py`: Faktorzellen, Episoden-Ziehung, Personas und Verfahren, Parser für das letzte JSON, Kontrast- und Bootstrap-Auswertung. Der E-016-Pfad bleibt lauffähig.
3. Dry-Run ohne API-Aufrufe: Prompts aller 18 Zellen für 2 Belege ausgeben. Ich lese sie gegen und Neo bekommt sie zur Ansicht.

## Abweichungen (nach Start)
- **22.10., Präzisierungen beim Bau, vor dem ersten Kalibrierungslauf:**
  - Das Kommando heißt `python -m orglab.factorial …` statt `orglab.panel`, eigenes Modul, E-016 bleibt unberührt.
  - **S2 erlaubt Text vor dem JSON, S0/S1 verlangen "JSON only" wie E-016.** Damit enthält S2 auch "erst nachdenken". Laut Kohli 2605.29800 *erhöht* CoT die Korrelation. Das wirkt gegen V3, die Vorhersage wird dadurch konservativer.
  - Das S2-Verfahren steht **vor** dem Beleg, sonst wäre "commit first" nicht ausführbar.
  - Die Erfahrungs-Episoden zeigen je einen zufälligen Kanal ihres Vorgangs.
  - Der Generator v2 hat je Domäne 2 Fehlerarten (coding: stale_process, db_down; business: bounced, wrong_recipient; research: row_loss, weights_broken). Formatvarianten (verschachteltes JSON, Prüfhaken ✓) werden unabhängig von der Belegart gezogen.
  - **Kalibrierung:** Kanalbalance wird über die Kanalposition (Index 0–2, über Domänen gemittelt) gemessen, weil I0 und I1 über diese Position rotieren. Die Spanne über alle 9 Einzelkanäle wird nur deskriptiv berichtet.
- **22.10., Stufe 0 nicht erfüllt:** 3 Kalibrierungsiterationen mit Sonnet (Fehlerrate 0,094 / 0,031 / 0,031) und eine mit Haiku (0,075). Ziel 0,10–0,40 verfehlt, laut Abbruchkriterium **kein Hauptlauf**. Details in `ergebnis-stufe0.md`. Eingesetzte Stellschrauben: `NOISE_BLOCKS`, `PAD_LINES`, `EXPLICIT_MODERATE` und Subtilität der Spuren. Dazu kamen 3 Generatorfehler-Korrekturen aus der Stichprobenprüfung (Kriterium 4).
