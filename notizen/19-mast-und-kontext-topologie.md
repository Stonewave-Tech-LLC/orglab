# MAST und die Frage "geteilter Kontext: wo nützt er, wo schadet er?"

**Stand:** 22.10.2026 · Anlass: Neos Frage, ob MAST etwas zu geteiltem Kontext sagt und ob wir MAST-Themen einbeziehen.

## 1. Was MAST wirklich sagt (im Original geprüft)

**Quelle:** Cemri, Pan, Yang, … Zaharia, Gonzalez, Stoica: "Why Do Multi-Agent LLM Systems Fail?", arXiv 2503.13657, v3 26.10.2025. Gelesen per WebFetch, die ersten 100.000 von 162.000 Zeichen.

- **Umfang:** 1.600+ annotierte Traces aus 7 Frameworks, 14 Fehlermodi in 3 Kategorien.
  - **FC1 System Design:** FM-1.1 bis 1.5. Darunter Step Repetition 15,7 %, Unaware of Termination 12,4 % und Loss of Conversation History 2,8 %.
  - **FC2 Inter-Agent Misalignment:** FM-2.1 bis 2.6. Darunter Reasoning-Action Mismatch 13,2 %, Task Derailment 7,4 % und Information Withholding 0,85 %.
  - **FC3 Task Verification:** Premature Termination 6,2 %, No or Incomplete Verification 8,2 %, Incorrect Verification 9,1 %.
- **Zu Kontext sagt MAST überraschend wenig Richtungsweisendes:**
  - Lösungen über Kontext oder Kommunikationsprotokolle seien für FC2 "often insufficient". Gebraucht werde tieferes "social reasoning".
  - Empfohlen werden standardisierte Protokolle sowie "memory and state management".
  - **Eine Aussage, wie viel Kontext Agenten teilen sollen, steht nicht im Paper.**
- **Zur Verifikation ist MAST deutlich:**
  - Verifier prüfen "often superficial". Prüfungen nur am Ende und auf niedriger Ebene reichen nicht.
  - Ein Verifier ist "not a silver bullet".
  - Fallstudie ChatDev: Rollenspezifikation +9,4 %, eine Verifikation auf Aufgabenebene +15,6 %.
- **Vorsicht beim Vergleich mit Wave:** Unsere Zahl "FM-3.2 in 62 % der Austausche" (`notizen/06`) hat einen anderen Nenner als die 8,2 % bei MAST (Anteil an allen Fehlerannotationen).

**Ehrliche Einordnung:** Der Gedanke "geteilten Kontext vermeiden oder ausloten" stammt vermutlich aus zwei anderen Texten von 2025, nicht aus MAST. Beide sind im Projekt nicht abgerufen, Status Wissen:
- **Cognition, "Don't Build Multi-Agents" (Juni 2025):** Vollen Kontext und volle Traces teilen, weil jede Handlung implizite Entscheidungen trägt. Parallele Agenten mit getrenntem Kontext treffen widersprüchliche Annahmen.
- **Anthropic, "How we built our multi-agent research system" (Juni 2025):** Subagenten mit *eigenem* Kontextfenster für parallele, breite Erkundung. Für eng gekoppelte Aufgaben wie Coding ist das laut Anthropic weniger geeignet.

## 2. Synthese: Kontext-Topologie nach Funktion

Beide Positionen stimmen, aber für verschiedene Funktionen. Die Frage lautet nicht "teilen ja/nein", sondern **welche Funktion welchen Kontext braucht**.

| Funktion | Kontext | Was schiefgeht, wenn falsch | Belege |
|---|---|---|---|
| **Koordinieren** (abhängige Handlungen) | **teilen** | MAST FM-2.4 (Information Withholding), FM-1.4/2.1 (verlorene Historie), widersprüchliche implizite Entscheidungen (Cognition) | H-015 (Board ersetzt Rollen, E-001 explorativ), HK-D7 (Abhängigkeit als Moderator, Mieczkowski 2603.12229) |
| **Erkunden** (parallele, unabhängige Suche) | **trennen** | Herding: Bei geteilter Evidenz kollabiert Deliberation (InfoDelphi, geprüft). Zu wenig Geteiltes schadet aber auch | Anthropic-Research-System; InfoDelphi 2607.01661 |
| **Prüfen** | **trennen, vor allem von der Selbstauskunft des Erzeugers** | MAST FM-3.2/3.3 (oberflächliche bzw. falsche Prüfung). Ein Prüfer, der den Erfolgsbericht liest, wird geprimt; ein gemeinsamer Prime wirkt als Common Cause korrelierter Fehler | H-023 (ehrliche Überbehauptung), H-029 (Kanaldiversität), HK-A7 (Board homogenisiert Prüfung), "commit first" (2607.05904, Abstract) |

**Für Wave/Ace:** Zustand und Historie für die *Arbeit* teilen. Der *Prüfer* sieht Umweltbelege und nicht den Bericht "erledigt, alles grün" des Erzeugers. Mehrere Prüfer sehen verschiedene Kanäle.

## 3. Wie MAST ins Projekt kommt (Vorschläge, noch nichts umgesetzt)

1. **E-017 bleibt unverändert.** Es ist präregistriert und testet die Prüf-Zeile der Tabelle (Kanaltrennung) schon direkt.
2. **Kandidat HK-19-1 "Kontext-Kontamination des Prüfers":**
   - Prüfer, die zusätzlich den Abschlussbericht des Erzeugers sehen ("deployed successfully, all checks green"), übersehen mehr Fehler. Ihre Fehler korrelieren stärker, weil der Bericht als gemeinsamer Prime wirkt.
   - Billig im Panel testbar: E-017-Belege mit und ohne Bericht, Faktor "Selbstauskunft sichtbar". Kandidat für E-019.
   - Bezug: MAST FM-3.3, H-023, AAP (Beleg statt Behauptung).
3. **Kandidat HK-19-2 "Kontext-Topologie in der Organisation":**
   - Im orglab-Testbed gegenüberstellen: Board für alle sichtbar, *Prüfer aber blind* für Board-Behauptungen, gegen alles sichtbar.
   - Vorhersage: gleiche Koordinationsleistung, weniger durchgerutschte Regressionen.
4. **MAST als Kodierschema für unsere Transkripte:**
   - Ein Teil der `orglab.digest`-Verläufe wird nach FM-Kategorien annotiert. Das ist eine Sekundärmetrik, die unsere Befunde mit der MAST-Literatur vergleichbar macht.
   - Einschränkung: Ein LLM-Annotator ist selbst ein korrelierter Prüfer (Cluster A). Deshalb eine Stichprobe von Hand bzw. von Neo.
