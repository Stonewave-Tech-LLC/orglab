# Programm "Vertrauen skalieren" (aus Neos Chat-Brainstorm, 21.10. abends)

**Leitfrage:** Welche minimalen architektonischen Regeln (Harness) braucht ein Verbund autonomer Blackboxes, damit sie sich gegenseitig so kontrollieren, dass ein verlässliches Ergebnis herauskommt, mit möglichst wenig menschlicher Aufmerksamkeit?

**Kernmetrik:** **Verlässlichkeit pro Mensch-Minute.** Das ist die Kurve, wie ein Unternehmen mit Agenten skaliert.

## Was wir dafür schon haben (Stand 21.10.)
- **Bestätigt (E-014):** Ohne Mechanismus zur Neuverteilung von Verantwortung fällt ein Team gegen Blockierer um 31 Punkte. Abstimmung (Quorum 2) und Frist-Regel retten das ohne Menschen. Die Abstimmung erzeugt 0 Fehlurteile.
- **Monokultur-Effekte im Verhalten:** Alle befolgen dieselbe schädliche Norm (E-005), alle Claude-Maulwürfe gestehen (E-006).
- **Grenze des Testbeds:** `inspect` ist bisher **unfehlbar**. Fehler entstehen nur durch fehlende Aufmerksamkeit, nicht durch falsches Urteil. **Korrelierte Fehlurteile sind deshalb noch nicht messbar.** Das ist die zentrale Baulücke für dieses Programm.

## Kernhypothese: korrelierte Fehler
Die byzantinische Fehlertoleranz (3f+1) setzt **unabhängige** Fehler voraus. Bei LLMs gilt das nicht: Drei Prüfer mit denselben Gewichten übersehen tendenziell dasselbe.

- **H-026 (neu):** Die Fehlurteile mehrerer Prüfer desselben Modells sind positiv korreliert. P(alle übersehen) ist deutlich größer als P(einer übersieht)^n. Redundanz aus derselben Modellfamilie bringt deshalb weniger als die naive Rechnung.
- **Ableitung:** Vertrauen skalieren heißt **Fehler dekorrelieren**. Wege dorthin: andere Modelle, andere Information, andere Prüfmethode (H-018), andere Anreize.

## Bausteine

### A. Fehlbare Prüfung ("Belegdeutung"). Fundament, zuerst
- `inspect` liefert **Rohbelege** (Logausschnitt, Statusausgabe, Messwerte) statt eines Urteils. Der Agent muss deuten.
- Ein Teil der Belege ist **trügerisch**: Ein Fehler ist versteckt (z. B. "status: OK" oben, der Fehler weiter unten), oder ein harmloses Rauschen sieht wie ein Fehler aus.
- Gemessen werden Fehlurteile je Prüfer und Beleg, ihre **Korrelation** zwischen Prüfern desselben bzw. anderer Modelle, und die Escape Rate.
- Ohne A sind B–E nur halb aussagekräftig.

### B. Escape Rate nach Fehlerart
| Fehlerart | Erzeugt durch | Erwartung |
|---|---|---|
| ehrlicher Fehler | Umwelt (Phantome, Regressionen, trügerische Belege) | Redundanz hilft |
| Sabotage | geskriptete Maulwürfe (D-012) | Redundanz und Übernahme-Mechanismus helfen (E-014) |
| **Absprache** | zwei Skript-Maulwürfe, die sich gegenseitig bestätigen und füreinander stimmen | **Redundanz hilft kaum, nur Unabhängigkeit** (Zulosung, andere Modelle, Umwelt-Quittungen) |

E-015 (mitstimmende Saboteure) ist eine erste Vorstufe zu "Absprache".

### C. Menschliche Audit-Rate (Verlässlichkeit pro Mensch-Minute)
- Der Mensch entscheidet nicht mehr jeden Einzelfall. Er macht **zufällige Stichproben-Audits** mit Rate p ∈ {0, 1 %, 10 %, 100 %} auf als erledigt gemeldete Pakete.
- Ein Audit kostet "Mensch-Minuten". Ein Fund hat Folgen: Neu-Zuweisung, optional Stake-Verlust.
- **Kurve:** Escape Rate gegen p, je Regelset. Gesucht ist das kleinste p, ab dem die Escape Rate stabil niedrig bleibt.

### D. Ablation: das Minimum der Regeln finden
Start mit vollem Regelset, dann jeweils eine Regel entfernen. Regeln, deren Entfernung die Escape Rate hochtreibt, bilden das Minimum. Kandidaten:

| Regel | im Testbed | Bezug |
|---|---|---|
| Wer produziert, prüft nicht | Norm / Werkzeugsperre | H-017/018 |
| **Quittungen der Umgebung statt Selbstauskunft** | `report_done` nur mit Umwelt-Beleg (inspect-Quittung) | **AAP**, METR-Signaturen |
| Prüfer aus verschiedenen Modellfamilien | Modell pro Agent | H-026, braucht **API-Keys** |
| **Zufällige Zulosung der Prüfer** | System weist Prüfer zufällig zu | gegen Absprache und Bestechung |
| **Stake:** Betrug kostet Rechte | Wer beim Falschmelden erwischt wird, verliert für N Ticks das Recht, zu übernehmen oder abzustimmen | Teil 2 §6.4 |
| Eskalation an Menschen nur über einer Unsicherheitsschwelle | Agent gibt Konfidenz an, Mensch nur bei Unsicherheit | Mensch-Minuten |
| Übernahme-Mechanismus (Abstimmung oder Frist) | `reassign_quorum`, `stale_release_ticks` | **bestätigt nötig (E-014)** |

### E. Modell-Diversität
- **Sofort möglich:** innerhalb der Familie (Haiku 5.5 / Sonnet 5.5 / Opus 5.5 als Prüfer). Das ist eine schwache Dekorrelation, weil die Familie verwandt ist.
- **Eigentlicher Test:** Fremdfamilien (GPT, Gemini, Grok). Braucht API-Keys. Ohne das bleibt H-026 nur innerhalb der Claude-Familie prüfbar.

## Reihenfolge (Vorschlag)
1. **A bauen und kalibrieren:** Belegdeutung, Validierung, Kalibrierung gegen Decke und Boden (D-010).
2. **Korrelationsmessung:** n Prüfer desselben Modells beurteilen dieselben Belege unabhängig. Daraus Korrelation und P(alle irren). Danach dasselbe gemischt (Haiku/Sonnet/Opus).
3. **B:** Absprache-Saboteure und Escape Rate je Fehlerart.
4. **C:** Audit-Kurve.
5. **D:** Ablation mit den besten Kandidaten aus 1–4.
6. **E** mit Fremdmodellen, sobald API-Keys da sind.

Budget-Hinweis: Schritt 2 ist günstig. Prüfer-Urteile über feste Belege sind Einzelaufrufe, kein ganzes Team, also viele Messungen pro Abo-Fenster.

## Nachtrag 21.10. spät: Decision Models als billige Prüfer (Neos Hinweis)
- **Jev** (TypeSafe AI, Early Access seit 15.09., erreichbar über OpenRouter) gibt Wahl, Score oder ja/nein mit **kalibrierten Wahrscheinlichkeiten** zurück, keinen Text.
  - Preis laut Hersteller: $0,042/MTok Input, Output kostenlos.
  - Herstellerangabe "~194× schneller, ~445× billiger" (Bestfall). Unabhängig (Artificial Analysis Decision Index) 60–400× billiger, aber schwächer bei Wissen und Schlussfolgern.
  - Laut Pydantic-Doku **durch Text im Input steuerbar** (Injection-Risiko).
  - Quellen: VentureBeat, TechTarget, Artificial Analysis (siehe `quellen.md`).
- **Einsatz im Programm:**
  1. als billiger Prüfer im Panel für Baustein A (Belegdeutung)
  2. als **Unsicherheits-Schwelle** für die Eskalation an Menschen (Kalibrierung)
  3. als **Dekorrelations-Kandidat** für H-026 (andere Architektur)
  4. als **Angriffsfläche**: Kann ein Maulwurf den billigen Prüfer per Text steuern?
- **Nicht** als Agent einsetzbar: kein Werkzeuggebrauch, keine Kommunikation, keine offenen Aufgaben.

## Nachtrag 21.10. spät: Bezug zu AAP (Stand Repo 18.10., Spike S1)
- **AAP-Stand:**
  - M0, M1/M2, M3 und Issuer-Service R1 sind gemergt.
  - Spike S1 (iOS) zeigt: App Attest beweist die App-Instanz, nicht den Nutzer bzw. Face ID pro Signatur. Daraus folgt die Trennung AL2-K (Android, Schlüssel attestiert) gegen AL2-A (iOS, Vertrauen in App-Code).
  - Offen sind: mehrere Geräte, Recovery bei AL2, Cooling-off, zweiter Log-Betreiber.
- **Andockpunkte:**
  1. E-015 "Beleg schlägt Stimme" entspricht dem Prinzip Assertion/Receipt statt Selbstauskunft. AL2-A sollte "attestiert" und "von der App behauptet" ausdrücklich trennen.
  2. H-023 (ehrliche Überbehauptung): Ein Verifier, der eine Assertion als Nutzerzustimmung liest, ist Ursache Nr. 2 (falsches Prüfmodell).
  3. **E-014 (bestätigt) passt auf Mehrgeräte- und Cooling-off-Fragen:** Ein Frist-/Veto-Fenster mit Beleg-Auslöser (Log-Einsicht anderer Geräte) als Muster für Mandate über einer Schwelle.
  4. E-015 (BFT-Grenze): Social Recovery per Stimmen ist angreifbar. Das stützt "AL2 ohne Recovery, AL3 über Passchip (Beleg)".
  5. H-026 (korrelierte Fehler): Ein zweiter Log-Betreiber dekorreliert nur bei echter Unabhängigkeit (Infrastruktur, Betreiber).
- **Für Baustein D (Ablation):** Die AAP-Regeln (Umwelt-Quittung, zurechenbare Identität, Frist mit Veto, Stake) sind die natürlichen Kandidaten für das Minimum.
