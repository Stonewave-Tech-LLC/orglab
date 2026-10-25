# Meta-Harness für autonome Forschung: Gedankenskizze

**Stand:** 23.10.2026, späterer Vormittag. Entstanden im Gespräch zwischen Neo und Claude nach dem Regelkritik-Panel (`notizen/31`) und der doppelten Buchführung (Regel 19).
**Status:** **Ideen und Thesen**, keine Befunde. Neo: "es sind nur Gedanken". Was hier steht, braucht Daten, und das Fehlerprotokoll (`notizen/30`) ist der erste Schritt dahin.

## 0. Die Frage
Wie baut man einen Forschungsloop, in dem eine KI forscht und entdeckt, **ohne dass man ihr selbst vertrauen muss**? Neos Formulierung: Der Forscher will nichts manipulieren und wird auch nicht verrückt. Er kann nur nichts gegen die Dinge tun, die ein LLM eben so macht. Das Ziel ist also, **Vertrauen in die KI billig zu machen**: Jede Aussage bringt ihren eigenen Beleg mit, sodass es egal wird, wie sehr man der KI vertraut (vgl. E-018 "Beleg schlägt Stimme").

## 1. Grundgesetz: Unabhängigkeit, nicht Zahl der Ebenen
- Mit unabhängigen Prüfebenen läuft der Restfehler gegen 0, auch bei endlichen Kosten, wenn jede Ebene billiger wird. Vorbilder: von Neumann 1956 (zuverlässige Systeme aus unzuverlässigen Bauteilen), Threshold-Theorem der Quantenfehlerkorrektur. *Aus Trainingswissen, nicht im Original geprüft.*
- Mit korrelierten Ebenen bleibt ein Boden: **n_eff = n / (1 + (n−1)·ρ) → 1/ρ**. Unendlich viele Prüfer mit ρ = 0,5 sind höchstens 2 unabhängige wert.
- Ähnliche Warnung aus der Softwaretechnik: Bei *N-Version Programming* (Knight und Leveson, 1986) machten unabhängig entwickelte Programmversionen häufiger **gleichzeitig** Fehler, als Unabhängigkeit erwarten ließe. *Aus Trainingswissen, ungeprüft.* Das betrifft direkt unsere doppelte Buchführung.
- **Folgerung:** Die Ingenieursaufgabe ist, **ρ zu senken**, nicht Ebenen zu stapeln.

## 2. Neos Hebel (Gespräch 23.10.)
1. **Vielfalt ist Pflicht.** Präzisierung durch Claude: Wahrscheinlich zählt vor allem die Vielfalt der **Prüffunktion und der Information**, die Modellvielfalt verstärkt sie nur. Hinweise von heute: GPT fand Generatorfehler, weil es eine andere Aufgabe hatte (Beurteilung von Null an). Die Nachrechnung fand die Lücke, weil ein anderes Verfahren lief (aus der Spezifikation neu bauen). Im Panel überlappten die drei Claude-Modelle nicht stärker als die übrigen.
2. **Mischung aus frei denkendem und handelndem Modell und strukturierten Werkzeugen in einem strukturierten Loop.** Ein Meta-Harness über dem forschenden Coding-Agenten gibt je nach Phase und Zahlen nur bestimmte Werkzeuge frei.
3. **Der schmale Grat zwischen starr und sicher und dynamisch und unsicher.** Vorschlag Claude: kein globaler Regler, sondern einer **pro Phase**. Starr, wo Fehler teuer und schwer zu entdecken sind (Bestätigung). Frei, wo Fehler billig sind und später sicher auffallen (Entdeckung). Zusatz: Je überraschender ein Ergebnis, desto mehr externe Prüfung schaltet sich automatisch dazu.
4. **Nicht ein Harness, sondern ein Multi-Agent-System als Meta-Harness, mit strenger Informationskapselung.**
5. **Die Gate-Zahlen dürfen nicht von der forschenden KI kommen.** Offen: Wer rechnet sie? Deterministisch, ein anderes Modell, das nur rechnet, oder ein eigens trainiertes Modell?

## 3. Bewertung der Punkte 4 und 5 (Claude, mit Widerspruch)

### 3.1 Multi-Agent-Meta-Harness mit Kapselung: überzeugend, mit einer Korrektur
- **Korrektur zu MAST:** MAST nennt geteilten Kontext *nicht* als Fehlermodus. Es enthält im Gegenteil Fehler durch **zu wenig** Teilen: Information Withholding (FM-2.4) und Loss of Conversation History. Eine Aussage, wie viel Kontext geteilt werden soll, steht dort nicht (`notizen/19` §1).
- **Was passt:** unsere eigene Synthese in `notizen/19` §2, die **Kontext-Topologie nach Funktion**. Wer koordiniert, teilt den Kontext. Wer prüft, wird getrennt gehalten, vor allem von der Selbstauskunft des Erzeugers (HK-19-1). Neos Kapselung ist also richtig für Prüf- und Rechenrollen und falsch für Rollen, die eng zusammenarbeiten müssen.
- **E-020 testet genau diesen Teil:** Der Faktor AUSKUNFT misst, ob ein Prüfer schlechter wird, wenn er das "Done. All checks green." des Erzeugers sieht.
- **Vorbild aus der Praxis:** klinische Studien mit getrennten Rollen. Der Prüfarzt sieht die Patienten, der Statistiker ist verblindet, und ein unabhängiges Datenmonitoring-Gremium sieht als Einziges die entblindeten Zwischendaten und darf stoppen. Prinzip: Gewaltenteilung durch getrennte Information.
- **Kosten:** Jede Kapselgrenze ist eine Übergabe, an der Information verloren geht (MAST FC2), und die Koordination wird teurer. Wo sich das lohnt, ist eine **Messfrage**, keine Glaubensfrage.

### 3.2 Wer rechnet die Gate-Zahlen? Rangfolge
1. **Deterministischer Code: am besten, aber nur zusammen mit drei Bedingungen.** Code muss jemand schreiben, und das wäre wieder eine KI. Deshalb:
   - vor den Daten festgelegt (Präregistrierung, Hash)
   - **verblindet**: Der Code sieht die Arme nur als A/B/C/D und kennt die Hypothese nicht
   - unabhängig doppelt implementiert (Regel 19), mit dem Wissen, dass auch zwei Versionen korreliert irren können (Abschnitt 1)

   Vorteil: Code muss man **einmal** prüfen, ein Urteil jedes Mal neu.
2. **Ein anderes Modell, das nur rechnet: gut als Rolle, nicht als Rechner.** LLMs rechnen direkt unzuverlässig. Als *Rechen-Agent*, der aus der Spezifikation Code schreibt und ihn ausführt, ohne Hypothese und ohne Armnamen zu kennen, fällt das mit Punkt 1 zusammen. Der Wert liegt in der **Kapselung**, nicht im Modell.
3. **Ein eigens trainiertes Modell: vorerst nein.** Die Trainingsdaten kämen aus unserer eigenen KI-Pipeline und erben damit ihre Schieflagen. Es wäre teuer und datenhungrig, und ein kleines Spezialmodell ist meist schwächer. Denkbar ist es später nur für eng umrissene Prüfungen mit fremd erzeugten Labels, etwa einen Leck-Detektor.

### 3.3 Was an Neos Gedanken stark ist, und was offen bleibt
- **Stark:** Regeln werden zu **Mechanik**. Unsere Regeln 10–19 sind heute Text und gelten, solange Claude sich daran hält. Die 16-Stapel-Lücke ist ein Beispiel dafür, wie das ohne Absicht scheitert.
- **Offen:**
  - Wer entwirft den Meta-Harness? Wenn wieder die KI, ist das der nächste Regress. Er lässt sich nur durch Außenanker durchbrechen: Mensch, Realität, Fremdkritik am Design (wie das Panel).
  - Goodhart: Auch extern berechnete Zahlen kann man ungewollt "trainieren", wenn die KI sieht, welche Schwelle was freischaltet. Deshalb sollten die Schwellen der forschenden KI verborgen bleiben.
  - **Neo zur eigenen Rolle:** "gut möglich, dass ich viel unzuverlässiger bin als du". Für das System zählt weniger, wie oft jemand irrt, sondern **ob anders**. Ein Mensch, dessen Fehler nicht mit denen der KI korrelieren, senkt ρ, auch wenn er öfter danebenliegt. Beispiel von heute: Neos Frage "wie kann das so günstig sein?" hat aufgedeckt, dass die GPT-Fremdkontrolle kaum nachdenkt.

## 4. Skizze: Rollen und Werkzeuge je Phase (Entwurf)

| Phase | Rolle | sieht | darf | sieht nicht |
|---|---|---|---|---|
| Entdecken | Forscher-Agent (frei) | alles Bisherige | explorieren, Kandidaten vorschlagen | – |
| Festlegen | Forscher-Agent, danach Kritiker (andere Familie) | Kandidat, Design | Präregistrierung schreiben bzw. kritisieren | **neue Rohdaten** (gesperrt bis zum Commit) |
| Material prüfen | Fremdkontrolle (andere Familie) | Belege einzeln | Wahrheit und Lecks beurteilen | Hypothese, Fehlerart |
| Laufen | Executor (Code) | Präregistrierung | nur das eingefrorene Skript ausführen | – |
| Auswerten | Rechen-Agent(en), verblindet | Präregistrierung, Rohdaten mit Armen A/B/C/D | rechnen | Armnamen, Hypothese, Claudes Code |
| Gate | deterministischer Gate-Code | Zahlen der Rechen-Agenten | stoppen, entblinden, mehr Prüfung verlangen | – |
| Deuten | Forscher-Agent | entblindete Zahlen | Ergebnis schreiben | – |
| Außenanker | Neo, Realität (Wave), Panel | Stichproben, die Neo selbst zieht | schlichten, Regeln freigeben | – |

## 5. Erster billiger Baustein (Vorschlag)
**Verblindete Auswertung:** Die Arme heißen bis zum Einfrieren der Auswertung nur A/B/C/D. Die Zuordnung liegt in einer Datei, die erst das Gate öffnet. Das kostet fast nichts, ist in der Medizin Standard und nimmt dem Forscher-Agenten die Möglichkeit, die Auswertung unbewusst in Richtung der Hypothese zu biegen (vgl. die K1/K5-Schieflage in `notizen/30`).

## 6. Wie man das später messen könnte (Idee, nicht geplant)
Eine Forschungsaufgabe mit bekannter Wahrheit und eingebauten Fallen (Lecks, Fehlbeschriftungen, verlockende Scheineffekte) wird von drei Harness-Varianten bearbeitet: frei, starr und phasengesteuert. Gemessen wird, wie viele Fallen durchrutschen, wie viel es kostet und wie viele Mensch-Minuten nötig sind. Das ist dieselbe Frage wie bei Wave, eine Ebene höher, und "Harness als unabhängige Variable" wie in der ursprünglichen Projektidee.

## 7. Nachtrag (Gespräch, gleicher Tag): Kryptographie, Sandbox, Specification Gaming
- **Kryptographie** ist das Fachgebiet "Vertrauen, ohne zu vertrauen". Sie sichert die **Integrität des Ablaufs** (wer hat was wann gemacht, nichts nachträglich verändert), aber **nicht die Richtigkeit des Urteils**. Gegen gemeinsame blinde Flecken (ρ) hilft sie nicht. Kandidaten:
  - **Commitment:** Präregistrierung und Blindschlüssel als Hash festlegen, mit öffentlichem Zeitstempel. Git allein ist lokal umschreibbar.
  - **Secret Sharing (Shamir):** Der Entblindungsschlüssel braucht k von n Parteien, etwa Neo, Ace und einen Dienst.
  - **Hash-Kette und Signaturen:** Das Laborbuch wird mechanisch append-only, und es ist nachvollziehbar, welcher Agent welches Artefakt erzeugt hat. Das ist die Brücke zu AAP (Front F).
  - Prüfbare Berechnung (Zero-Knowledge) ist für uns überdimensioniert.
- **Rechtetrennung per Sandbox oder getrenntem Prozess** ist softwaretechnisch lösbar, für einen wie für mehrere Agenten (Neo). Das Vertrauen wandert dabei in die Konfiguration, und die prüft man einmal, sie skaliert nicht negativ.
- **Realistisches Risiko** ist nicht der Ausbruch, sondern *Specification Gaming*: Abkürzungen innerhalb der eigenen Rechte, etwa einen Test anpassen statt den Fehler zu beheben. Das ist ein bekanntes Alignment-Thema (aus Trainingswissen). Dagegen hilft genau die Rechtetrennung.
- Umgesetzt: Regel 20, einfache Verblindung (D-021). Offen: harte Sperre per Sandbox.

## 8. Sandbox-Prüfung (D-021, Schritt 2): Ergebnis aus der Claude-Code-Dokumentation
Quelle: code.claude.com/docs/en/sandboxing, abgerufen am 23.10.2026.
- **Es gibt eine echte, vom Betriebssystem durchgesetzte Lesesperre für Shell-Befehle:** `sandbox.filesystem.denyRead`, mit `allowRead` für Ausnahmen.
- **Aber nur auf macOS, Linux und WSL2.** Wörtlich: "On native Windows, Claude Code runs commands unsandboxed." Neos Setup ist natives Windows, **hier gibt es also keine Sandbox.**
- Die Datei-Werkzeuge (Read, Edit, Write) laufen außerhalb der Sandbox und folgen den Berechtigungsregeln (`permissions.deny`, z. B. `Read(//pfad/**)`). Eine `denyRead`-Regel stoppt das Read-Werkzeug nicht. Für eine dichte Sperre braucht es also **beides**.
- Es gibt eine Ausweichtür: Claude kann einen blockierten Befehl ohne Sandbox wiederholen (`dangerouslyDisableSandbox`). Abschalten lässt sie sich mit `"allowUnsandboxedCommands": false`, und mit `failIfUnavailable` startet nichts ohne Sandbox.
- **Optionen für eine harte Sperre:**
  1. Claude Code unter **WSL2** betreiben, mit `denyRead` auf den Schlüsselordner, `permissions.deny` für Read und `allowUnsandboxedCommands: false`. Das ist dicht, aber ein Umzug der Arbeitsumgebung.
  2. **Schlüssel extern verwahren:** etwa als GitHub-Actions-Secret (per API nicht auslesbar) mit einem Workflow, der erst nach dem Commit von `auswertung-verblindet.md` entblindet. Oder bei einem Dienst auf Aces Server. Ehrliche Grenze: Wer den Workflow ändern darf, könnte ihn das Secret ausgeben lassen. Das wäre absichtlich und liegt damit außerhalb unseres Bedrohungsmodells.
  3. **Teilsperre auf Windows:** eine `permissions.deny`-Regel für das Read-Werkzeug auf `~/.orglab-schluessel`. Sie wäre sofort möglich und schützt vor versehentlichem Öffnen mit dem Datei-Werkzeug, nicht vor der Shell.
- **Einschätzung:** Für das Bedrohungsmodell "unbewusstes Biegen und versehentliches Sehen" reicht die einfache Variante plus Teilsperre (3). Für ein späteres Autoresearch-System mit mehreren Agenten wären (1) oder (2) der richtige Weg. Jede Einstellungsänderung entscheidet Neo.

- **Teilsperre eingerichtet (23.10., ~12:10, Neo: "Ja mach das"):** `permissions.deny: ["Read(~/.orglab-schluessel/**)"]` in `.claude/settings.json` des Repos (versioniert) und des Workspace-Ordners (diese Session startete dort). Getestet mit einer Probedatei: Das Read-Werkzeug wird verweigert ("denied by your permission settings"). Die Shell kann den Ordner auf nativem Windows weiterhin lesen, das ist bekannt und so gewollt (Bedrohungsmodell). Probedatei gelöscht.

## 9. Ehrlichkeit und Korrigierbarkeit als Kernwerte für Autoresearch (Gespräch 23.10., These)
- **Ehrlichkeit** heißt hier vor allem **Kalibrierung und Herkunft**: wie sicher, und woher das Wissen stammt. Positivbeispiel: Ace trennte [Quelle], [Erinnerung] und [Einschätzung], schrieb "nicht gefunden" hin und nannte die eigene mögliche Beschönigung. Negativbeispiel: Claudes "belegt" in der Morgenzusammenfassung, ein Kalibrierungsfehler ohne Täuschung.
- **Korrigierbarkeit** heißt hier, dass ein System seine eigenen Prüfkanäle nicht wegoptimiert: keine Tests passend machen, nicht am Blindschlüssel vorbeischauen, keine Abweichung verschweigen. Verblindung, Abweichungsprotokoll, doppelte Buchführung und Leseverbot machen daraus eine **Eigenschaft der Infrastruktur** statt einer Haltung des Agenten.
- **Grenzen:**
  - **Ehrlich ist nicht richtig.** Fast alle Fehler am 23.10. waren ehrlich. Ehrlichkeit macht Fehler auffindbar, verhindert sie aber nicht.
  - **Korrigierbar ist nicht gefügig.** Wer jede Korrektur annimmt, ist sykophantisch. Richtig ist: Korrekturen annehmen, die auf Belegen beruhen, und begründet widersprechen, wenn sie es nicht tun. Bei Claude ist das Risiko eher zu viel Zustimmung.
  - **Observability macht Ehrlichkeit prüfbar statt geglaubt.**
- Verwandtes Forschungsfeld: *Scalable Oversight* (Trainingswissen, nicht geprüft).

## 10. Ehrlich, aber falsch: aus welcher Quelle? Fehlertyp bestimmt die passende Platte (Neo, These)
Neos Frage: Ist "ehrlich, aber falsch" ein eingebauter Fehler desselben Systems oder ein anderer Fehlermodus, etwa Informationsmangel? Vorschlag einer Einteilung nach **Fehlerquelle**. Jede Quelle wird durch eine **andere Art** von Platte entkoppelt:

| Fehlerquelle | Was dahintersteckt | Was ihn entkoppelt | Beispiele vom 23.10. (rückblickend von Claude zugeordnet, nur Hinweis) | Gefunden durch |
|---|---|---|---|---|
| **Zufall / Ausrutscher** | Unaufmerksamkeit, Zählfehler | jede zweite Prüfung, auch dieselbe Art (nachzählen) | Aces Summenzeile, Claudes Uhrzeit, Lecktest misst falsches Maß | Nachzählen, selbst |
| **Informationsmangel** | dem Agenten fehlt eine Tatsache über die Welt | **andere Informationsquelle**: messen, Doku, Realität. Ein anderes Modell mit denselben Infos hilft nicht | `medium` = `low`, "Reasoning aus" gibt es nicht, GPT denkt bei `high` kaum | Manipulationscheck (Messung), Neos Frage |
| **Kontext-Bias** | Was der Agent gerade im Kopf hat, färbt das Urteil (Hypothese, eigener Plan) | **anderer Kontext**: Verblindung, Prüfer ohne Hypothese | Claudes K1/K5-Schieflage kurz nach dem Formulieren der Hypothesen. Ace (vermutlich gleiche Familie, aber ohne frischen Hypothesen-Kontext) zeigte sie nicht | blinde Kodierer anderer Herkunft |
| **Modell-Bias** | gemeinsame blinde Flecken durch Training (Familie oder alle LLMs) | **andere Familie, Mensch, Realität** | Pipeline-Blindheit (0 von 3 Claude-Modellen im Panel), Konventionsleck "Rechnung ohne PDF" | Fremdmodelle, Panel |
| **Spezifikationslücke** | Regel oder Plan sagt etwas, der Code setzt es nicht um | **unabhängige Neuimplementierung aus der Spezifikation** | 16-Stapel-Regel fehlte im Skript | doppelte Buchführung |

- **Auffällig, aber nachträglich zugeordnet:** Jeder Fehler wurde von der Plattenart gefunden, die zu seiner Quelle passt. Das kann eine echte Regel sein oder eine Erzählung, die Claude hinterher so gelegt hat. Status: **Hinweis**.
- **Interessant am K1/K5-Fall:** Ace ist vermutlich Claude-basiert, zeigte die Schieflage aber nicht. Das spricht eher für **Kontext-Bias** als für Modell-Bias, also dafür, dass Verblindung hilft und kein Familienwechsel nötig ist. n = 1.
- **Folgerung für den Meta-Harness:** Erst die Fehlerquelle diagnostizieren, dann die Platte wählen. Mehr Plattenvielfalt bringt nur dort etwas, wo sie zur Quelle passt. Ein zweites Modell mit denselben Informationen hilft bei Informationsmangel nicht, Verblindung hilft nicht gegen Modell-Bias.
- **Prüfbar machen:** Das Fehlerprotokoll (`notizen/30`) bekäme ein Feld "Fehlerquelle", **blind kodiert** (GPT oder Neo). Dazu ein Lichttest, der je Quelle Fehler einschleust und misst, welche Platte sie fängt. Vorhersage: Fangquote ist hoch bei passender Platte und niedrig bei unpassender.
