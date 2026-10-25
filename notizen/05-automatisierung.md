# Automatisiertes Testen: Systementwurf

**Stand:** 20.10.2026 · **Status:** Entwurf (D-007 vorgeschlagen)

## So funktioniert Harness² in einfachen Worten

1. Ein Agent erledigt eine Aufgabe mit dem aktuellen Harness. Das ist die **Referenz**.
2. Ein stärkeres Modell (Editor, bei ihnen Claude Opus) schaut sich den Verlauf an und schlägt **zwei Änderungen** an den Harness-Dateien vor: eine allgemeine und eine aufgabenspezifische.
3. Beide Varianten lösen **dieselbe Aufgabe noch einmal**. Das sind die **Probes**.
4. Ein **Composer** vergleicht die Verläufe und baut daraus den verbesserten Harness.
5. Ein **Reflector** schreibt die Lektion in eine **Bibliothek**, die bei der nächsten Aufgabe zur Verfügung steht.

Dabei ist kein Mensch beteiligt. Die Schwäche: Es gibt keine Messung, ob das Ergebnis stimmt. Gearbeitet wird nur mit dem Vergleich "anders als vorher" und dem Urteil eines LLM.

## Unser System: zwei Schleifen

### Innere Schleife: Messen (läuft vollautomatisch)

```
Szenario-Generator ──► Org-Konfiguration ──► Runner ──► Event-Log ──► Auswerter ──► Ergebnistabelle
(Seed → Instanz mit    (YAML: Rollen,        (Agent SDK,  (JSONL, jede    (Metriken gegen
 bekannter Wahrheit)    Topologie, Board,     N Agenten,   Nachricht,      Ground Truth,
                        Regeln, Gedächtnis)   Sonnet 5.5)  jeder Zustand)  Graphmetriken,
                                                                           MAST-Tags)
```

- **Szenario-Generator:** Erzeugt aus einem Seed eine konkrete Instanz, zum Beispiel "Phantom-Fertig, Domäne Business-Ops, 5 Agenten, 2 lügende Statussignale". Die richtige Lösung ist bekannt. Wegen D-005 gibt es denselben Mechanismus in mehreren Domänen.
- **Org-Konfiguration:** Eine Datei beschreibt die Organisation. Das ist unser "Harness", und nur diese Datei darf der Optimierer verändern.
- **Runner:** Startet die Agenten über das Agent SDK und spielt Störungen ein. Er protokolliert alles: Modell, Seed, Code-Version, Tokens.
- **Auswerter:**
  - Deterministisch, wo möglich, z. B. "Wurde der falsche Status bemerkt?" oder "Wie viele Commitments sind am Ende offen?".
  - Ein LLM-Judge nur dort, wo es nicht anders geht, stichprobenartig gegen menschliches Urteil geprüft.
- **Sweep-Steuerung:** Varianten mal Seeds, parallel mit begrenzter Gleichzeitigkeit (wegen der Subscription). Ein Abbruch lässt sich fortsetzen.

### Äußere Schleife: Optimieren (automatisch, mit festen Grenzen)

```
Ergebnisse + Traces der Fehlschläge
        │
        ▼
Analyst / Editor (Opus 5.5) ── schlägt 2 Kandidaten-Configs vor (invariant + szenariospezifisch)
        │
        ▼
Probe: jeder Kandidat auf den TRAININGS-Szenarien, mehrere Seeds
        │
        ▼
Gate: statistisch besser als die aktuelle Config UND keine Regression in anderen Metriken?
        │ ja                                   │ nein
        ▼                                      ▼
Composer übernimmt die Änderung       verworfen, aber protokolliert
        │
        ▼
Bibliothek: Config + EXPERIENCE.md (was wurde warum geändert, mit welchen Belegen)
        │
        ▼
regelmäßig: Test auf GEHEIMEN Szenarien (Transfer-Check, der Optimierer sieht sie nie)
```

## Unterschiede zu Harness²

| | Harness² | Wir |
|---|---|---|
| Was wird optimiert | ein einzelner Agent (8 Dateien) | die Organisation (Rollen, Topologie, Regeln, Gedächtnis, Signale) |
| Bewertung | Verhaltensvergleich + LLM-Urteil | echte Metriken gegen Ground Truth, mit mehreren Seeds |
| Overfitting-Schutz | keiner explizit | getrennte Trainings- und Test-Szenarien |
| Doku | Bibliothek | Bibliothek + automatisches Protokoll jedes Kandidaten, Diffs, Statistik |

## Leitplanken (gegen Goodhart und Selbstbetrug)

- Der Optimierer darf **nur** die Org-Konfiguration ändern. Szenarien, Auswerter, Metriken und Test-Szenarien sind für ihn tabu. Das wird technisch durchgesetzt, nicht nur per Prompt.
- Jede übernommene Änderung wird versioniert und lässt sich zurückrollen (Vorbild: RegenHarness).
- Kosten werden immer mitgemessen (Tokens pro Erfolg), damit "mehr reden" nicht automatisch gewinnt.
- Ein Mensch (Neo) gibt frei: neue Experimente (Präregistrierung), Änderungen an Metriken bzw. Auswerter und das Übernehmen von Modulen nach Wave.

## Die Schleife dokumentiert sich selbst

Jede Iteration schreibt in `experimente/E-xxx/`:
- Kandidaten-Diffs
- Probe-Ergebnisse
- Gate-Entscheidung mit Statistik
- Bibliothekseinträge

Das Laborbuch bekommt pro Lauf eine automatisch erzeugte Zusammenfassung. Interpretation und Bewertung schreiben wir selbst dazu.

## Ausbaustufen (jede für sich nutzbar)

1. **Pilot:** Event-Log-Schema, Runner, ein Szenario (Phantom-Fertig), Auswerter, zwei Regime von Hand verglichen. Klärt, ob die Messung trägt und wie viel Durchsatz die Subscription hergibt.
2. **Sweeps:** Szenario-Generator für mehrere Domänen, Sweep-Steuerung, Auswertungsskripte, alle fünf Ace-Szenarien.
3. **Optimierer:** äußere Schleife mit Gate, Bibliothek und Transfer-Check.
4. **Dauerbetrieb:** zeitgesteuert, z. B. nachts auf einem Server, mit Bericht am Morgen.

## Offen

- Wo läuft das? Neos Laptop, oder ein Server (Aces Umgebung?) für Dauerläufe.
- Wie viele Runs pro Tag erlaubt die Subscription realistisch? Das klärt der Pilot.
