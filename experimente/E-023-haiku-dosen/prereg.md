# E-023: Realität in Dosen mit Haiku – Präregistrierung

> Gleiches Experiment wie E-020 v3, **nur das Prüfer-Modell wechselt** (Sonnet 5.5 → Haiku 5.5). Neo, 23.10.: "machen wir Haiku trotzdem zuerst, aber ordnen es richtig ein, um nicht falsche Schlüsse zu ziehen." **Status: von Neo freigegeben (2026-10-23 16:04, "Ja passt").**

- **Datum:** 2026-10-23, 15:43 (aus `date`)
- **Stufe:** Entdeckung, mit gerichteten Vorhersagen
- **Hypothesen (Wortlaut eingefroren):**
  - H-033, H-034, H-035 in einem zweiten Modell. Bei Sonnet waren alle drei "nicht gestützt" (E-020).
  - **H-038** (Wechselwirkung Modell × Harness): Unterhalb einer Fähigkeitsschwelle wirkt die Harness-Gestaltung anders als darüber.

## Einordnung: Was wir aus welchem Ausgang schließen dürfen (vor den Daten festgelegt)
Das ist der wichtigste Abschnitt. Haiku dient hier als **Messinstrument unterhalb der Decke**. Es ist **kein Stellvertreter für Wave**, denn Wave läuft mit starken Modellen.

| Ausgang | Erlaubte Lesart | Nicht erlaubt |
|---|---|---|
| Haiku zeigt V1 (fehlender Sollwert → mehr Übersehen), Sonnet nicht, Wechselwirkung > 0 | Ob der Sollwert im Auftrag steht, ist **modellabhängig** wichtig: für schwächere Modelle ja, für Sonnet nicht. Stützt H-038 für diesen einen Faktor | "Sollwerte in den Auftrag schreiben ist eine Regel für Wave" |
| Haiku zeigt keinen der Effekte | Die Nullbefunde aus E-020 gelten über zwei Modellgrößen. Rahmung und Ort des Sollwerts sind dann robust egal, solange die Suche funktioniert | "Bei keinem Modell wichtig" (zwei Modelle aus einer Familie) |
| Haiku übersieht insgesamt viel mehr | Nur, dass Haiku schwächer prüft. Das ist bekannt und **keine Aussage über den Harness**. Verglichen werden Effekte (Differenzen), nicht Fehlerniveaus | jede Aussage, die nur auf Niveaus beruht |
| Haiku zeigt V2 (Selbstauskunft verführt) | Selbstauskünfte sind ein Risiko für schwächere Prüfer. Für Wave höchstens ein **Hinweis**, die Sonnet-Daten zeigen das Gegenteil | "Selbstauskünfte sind gefährlich" ohne Modellangabe |
| ZUGANG-Effekt bei Haiku größer als bei Sonnet | "Belege selbst holen" hilft schwächeren Modellen mehr. Explorativ, weil es dazu keine gerichtete Vorhersage gibt | "Holen statt Vorlegen ist belegt" |
| Haiku liegt am Boden (übersieht fast alles) oder bedient die Werkzeuge nicht | Das Experiment ist für Haiku nicht aussagekräftig. Berichtet wird nur deskriptiv | jede Effektaussage |

Weitere Grenzen, die jede Lesart trägt:
- Zwei Modelle **derselben Familie** (Anthropic). Familienübergreifend ist nichts getestet.
- Die Sonnet-Daten stammen aus einem Lauf einige Stunden früher (E-020). Material, Seeds, Prompts und Code sind identisch, nur der Zeitpunkt nicht.
- Die Materialgrenzen aus E-020 gelten weiter. Die Zielzeile steht oben auf der Runbook-Seite, und 8 Belege sind einzeln nicht entscheidbar (siehe Auswertung).

## Design
**Identisch mit E-020 v3** (`experimente/E-020-realitaet-in-dosen/prereg-v3.md` samt Abweichungen 1–3):
- 2 × 2 × 2 = 8 Zellen (SPEC × ZUGANG × AUSKUNFT), jeder Beleg in jeder Zelle
- Material v4.3, **Seeds 6000–6023** (dieselben 288 Belege wie bei Sonnet, damit gepaart je Beleg verglichen werden kann), 84 spec-reine kaputte Belege
- Prompts und Werkzeuge: dieselben Funktionen (`e020v3.build_prompt`, `tools_for`, `judge`). Die Prompttexte stehen in `experimente/E-020-realitaet-in-dosen/dryrun-v3.md`.
- Umfang: 2.304 Prüfungen, geschätzt **2–3 $** (Probe: ~0,001 $ je Prüfung)

### Weg, Modell, Einstellung (Regel 11)
- Weg: OpenRouter/API. Modell: **`anthropic/claude-haiku-5.5`** (0,10 $ bzw. 0,50 $ je Mio. Ein- bzw. Ausgabe-Tokens)
- **Kein `reasoning`-Parameter**, wie bei Sonnet. Laut Probe (unten) heißt das bei Haiku adaptives Denken.
- `max_tokens` 4000 je Aufruf, höchstens 6 Werkzeugrunden, danach ein erzwungenes Urteil
- Weggelassen: `temperature`, `top_p`, `seed`

## Manipulationscheck (Regel 10)
- **Vorab-Probe** (vor 15:43, frischer Seed 1500, 6 Belege × 2 Zellen × 2 Modelle, `daten/E-023-haiku-dosen/probe-manipulationscheck.jsonl`):
  - Haiku: 12/12 gültige Urteile, `run_check` 3/3 in allen 6 ZUGANG-Prüfungen, Denk-Tokens Median ~460 (Sonnet ~200). Ohne Parameter denkt Haiku also adaptiv, eher mehr als Sonnet.
  - **Unterschied:** Haiku schlug bei SPEC=1 nur in 3 von 6 Prüfungen nach, Sonnet in 6 von 6. Genau dort kann H-033 ("schlägt nicht nach") greifen.
- **Im Hauptlauf** (berichtet je Modell, `e023.model_profile`): Tokens, Nachschlagerate bei SPEC=1, `run_check` bei ZUGANG=1, Ausfälle.
  - Kriterium ZUGANG: im Mittel ≥ 1 `run_check` je Prüfung.
  - Kriterium Werkzeugfähigkeit: Ausfälle ≤ 5 % je Zelle.
  - Scheitert eines davon, gilt der Ausgang "nicht aussagekräftig" aus der Einordnung.
- SPEC und AUSKUNFT: Code-Tests aus E-020, unverändert.

## Material, Lecks, Fremdkontrolle (Regeln 12, 17)
Das Material ist unverändert v4.3 auf denselben Seeds. Es gelten Fremdkontrolle 48/48 und GPT-Lecktest 0/42 aus E-020. Die bekannte Lücke (Einzelkanäle nicht fremdkontrolliert) wird durch die vorab festgelegte Analyse ohne die 8 einzeln nicht entscheidbaren Belege abgedeckt.

## Vorhersagen
**Für Haiku allein** (gleiche Kontraste, gleiche Schwellen und gleiche Entscheidungsregel wie E-020, Abweichung 2; nichts an die Sonnet-Daten angepasst):

| Nr | Kontrast | Vorhersage |
|---|---|---|
| **V1** (primär) | SPEC 1 − 0, spec-reine Belege | Übersehen +0,10 oder mehr |
| **V2** | AUSKUNFT 1 − 0, alle kaputten Belege | +0,05 oder mehr |
| **V3** | `run_check`-Aufrufe AUSKUNFT 1 − 0 (ZUGANG = 1) | weniger Abfragen |
| V4, V5 | wie E-020 | deskriptiv |

**Wechselwirkung Modell × Faktor (H-038), gepaart je Beleg: Haiku-Effekt minus Sonnet-Effekt**

| Nr | Kontrast | Vorhersage | Status |
|---|---|---|---|
| **W1** | V1-Effekt Haiku − Sonnet | **> 0** (untere Grenze des 95-%-KI > 0) | gerichtet, sekundär |
| W2 | V2-Effekt Haiku − Sonnet | keine Richtung | berichtet |
| W3 | ZUGANG-Effekt Haiku − Sonnet | keine Richtung | berichtet, explorativ |

- Begründung für W1: Die Probe zeigt seltener Nachschlagen bei Haiku. Das ist eine Vorab-Beobachtung an 6 Prüfungen, kein Befund.
- Keine BH-Korrektur über W1–W3, weil nur W1 gerichtet ist.

## Teststärke
- V1–V3 für Haiku: wie E-020 (Simulation `e020v3.power`). V1 gestützt bei wahrem +0,10: 1,00. V2 bei +0,05: 0,88.
- **W1** (Simulation mit den echten Sonnet-Daten und synthetischem Haiku, Grundrate Übersehen 0,10, 30 Durchläufe, 1.000 Ziehungen):
  - Power bei wahrem Haiku-V1 von +0,10: **0,93**
  - Power bei +0,05: **0,33**
- **Ein Null-Ergebnis bei W1 schließt also eine Wechselwirkung um +0,10 recht sicher aus, eine um +0,05 nicht.**

## Auswertungsplan
- **Skript:** `orglab/e023.py` (`analyze_both`), getestet mit synthetischen Daten (`tests/test_e023.py`: Wechselwirkung erkannt, Null bei gleichen Modellen, Ausschluss entfernt die richtigen Belege). Trockenlauf mit Sonnet gegen Sonnet ergibt genau 0 und reproduziert die E-020-Zahlen.
- **V1–V5 für Haiku:** `e020v3.analyze_data` unverändert, also auch dieselben Analyse-Freiheitsgrade:
  - Bootstrap 5.000 Ziehungen, Perzentil, Startwerte 201/202 (V1/V2), 211/212 (BH)
  - letzter Datensatz je Paar zählt
  - Seed mit fehlendem Urteil fällt ganz heraus
  - jeder Beleg gleich gewichtet
  - mindestens 16 vollständige Seeds
- **Wechselwirkung:**
  - Je Beleg wird der Kontrast je Modell gebildet (Übersehen Stufe 1 − Stufe 0, gemittelt über die übrigen Faktoren). Dann die Differenz Haiku − Sonnet, Bootstrap über die gemeinsamen Belege (5.000 Ziehungen, Startwert 231).
  - Gemeinsam sind die Belege aus Seeds, die in beiden Läufen vollständig sind.
- **Vorab festgelegt: alles zweimal,** mit allen Belegen und ohne die 8 einzeln nicht entscheidbaren (Regel in `e023.UNENTSCHEIDBAR`: `db_down` × deploy, `low_traffic` × sockets). Primär ist die Analyse mit allen Belegen, damit sie mit E-020 vergleichbar bleibt.
- Sensitivitätsanalyse ohne Grenzfall 6021: wie E-020.
- **Generatorfehler-Regel:** wie E-020.
- **Transkripte:** 2 zufällige je Zelle, dazu gezielt 3 Verläufe, in denen Haiku bei SPEC=1 nicht nachschlug und übersah (falls vorhanden).
- **Doppelte Buchführung (Regel 19, freiwillig):** GPT und Gemini rechnen V1–V3 für Haiku nach (`orglab/nachrechnung.py`).
- **Verblindung (Regel 20):** nicht angewendet (Stufe Entdeckung, Arme an Werkzeugaufrufen erkennbar), wie E-020.

## Externe Kritik (Regel 18)
Der Lauf liegt unter 10 $, und es ist keine neue Kernthese, sondern dasselbe Design mit einem anderen Modell. **Kein Grok-Gutachten vorgesehen.** Groks Gutachten 3 und 4 zum Design gelten.

## Pilot (nur Technik)
- Seeds 1400–1401 = 192 Prüfungen, ~0,20 $.
- Kriterien:
  - Ausfälle ≤ 5 % je Zelle
  - `run_check` in jeder ZUGANG=1-Zelle genutzt
  - 3 Transkripte gelesen
- Fehlerraten werden nicht angesehen. Die Pilotdaten fließen nicht in die Auswertung.

## Abbruch
- Kosten des Experiments > 15 $ (im Code)
- Ausfälle > 5 % in einer Zelle → Stopp, die Lesart "nicht aussagekräftig" prüfen

## Abweichungen (nach Start)
-
