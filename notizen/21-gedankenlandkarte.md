# Gedankenlandkarte: wo wir stehen, wo Breite, wo Tiefe

> **Korrektur 23.10. (E-021, Manipulationscheck):** Was hier "Reasoning aus" heißt, war in Wahrheit die **Standardeinstellung mit adaptivem, verborgenem Reasoning** (OpenRouter: Reasoning ist bei Sonnet 5.5 nicht abschaltbar). "Reasoning low" war **gedrosseltes** Reasoning. Alle Aussagen "Reasoning erhöht Fehlalarme" sind deshalb umzudrehen: **Gedrosseltes Reasoning erhöht Fehlalarme** (H-037). Details: `experimente/E-021-reasoning-fehlalarme/ergebnis.md`.

**Stand:** 22.10.2026, nach Recherche, E-017, E-019 und Schwierigkeitslandkarte. Für Neo, damit dein Kopf an mehreren Fronten gleichzeitig arbeiten kann.

Lesehilfe: **Belegt** heißt präregistriert bestätigt. **Robust explorativ** heißt mehrfach gesehen, aber nicht präregistriert. **Hinweis** heißt einmal gesehen oder kleines n. **Literatur** heißt fremde Befunde, im Original geprüft. **These** heißt unsere Interpretation.

---

## 0. Die eine Frage hinter allem

> **Wie bringt man einen Verbund autonomer Agenten dazu, verlässliche Ergebnisse zu liefern, mit möglichst wenigen Menschen-Minuten?**
> (`notizen/14`, Kernmetrik: Verlässlichkeit pro Mensch-Minute)

Jede Front unten ist ein Teil dieser Frage. Wave und Ace sind der Anwendungsfall, AAP ist die Infrastruktur, Elara ist der Einzelagent mit Gedächtnis, und das Testbed ist das Labor.

---

## 1. Die Fronten (Breite)

| # | Front | Leitfrage | Stand |
|---|---|---|---|
| A | **Institutionen** | Welche Regeln braucht eine Agenten-Org minimal? | 2 belegte Befunde, mehrere Kandidaten |
| B | **Prüfer** | Wann irrt ein Prüfer-Agent, und wie merkt man es? | Baseline vermessen, Landkarte da |
| C | **Korrelation** | Irren mehrere Prüfer gemeinsam? Was entkoppelt sie? | Literatur stark, eigenes Experiment an der Decke gescheitert |
| D | **Harness-Optimierung** | Kann ein Optimierer bessere Orgs finden? | Null-Ergebnis, Literatur erklärt es |
| E | **Kontext-Topologie** | Wer soll was sehen? | These aus MAST und Literatur, ungetestet |
| F | **Vertrauensinfrastruktur (AAP)** | Belege statt Behauptungen, technisch | Brücke zu A gefunden (E-018) |
| G | **Gedächtnis und Identität (Elara)** | Hilft Gedächtnis, oder schadet es? | nur Literatur |
| H | **Methodik** | Wie forschen wir sauber mit LLMs über LLMs? | viel gelernt, Lehrstücke dokumentiert |

---

## 2. Wo wir Tiefe haben

### Belegt (präregistriert, auf frischen Seeds bestätigt)
1. **E-014:**
   - Ohne Mechanismus zur Neuverteilung von Verantwortung verliert ein Team gegen Blockierer 31 Punkte.
   - **Abstimmungsrecht (Quorum) und Frist-Regel retten das ohne Menschen.** Die Abstimmung erzeugt 0 Fehlurteile (H-024, H-025).
2. **E-018:**
   - Eine belegbasierte Frist-Regel ist immun gegen lügende Abstimmende: 0,05 gegen 11,4 Verluste pro Run.
   - Sie kostet keine Leistung (H-028).
   - Ein Teil davon folgt aus dem Design. Empirisch ist: Ehrliche Agenten missbrauchen die Regel nicht.

### Robust explorativ (mehrfach gesehen, nicht präregistriert)
3. **Starke Modelle sind als Prüfer nahe der Decke, wenn der Auftrag vollständig ist und der Beleg vorliegt.** Sonnet 5.5 übersieht 4–7 % (E-017, E-019, 3.312 Urteile).
4. **Fehler sitzen auf einem Spurtyp:** grüner Status, eine Zahl widerspricht. Dort werden 12 % übersehen, bei allen anderen Spurtypen ≤ 1 % (`notizen/20` §3).
5. **Reasoning erhöht Fehlalarme um Faktor 4–5,** ohne mehr echte Fehler zu finden. Gesehen auf 2 Materialständen (`notizen/20` §4).
6. **Stapelprüfung erzeugt Fehlalarme, nicht Übersehen.** Mit Reasoning sind es 1,4 % Fehlalarme einzeln gegen 15,7 % im Stapel (§6). Unaufmerksamkeit äußert sich als Übervorsicht.
7. **Die Konfidenz ist ein starkes Eskalationssignal:**
   - Fehlerrate 0 % ab Konfidenz 0,95, 32 % unter 0,70.
   - **Wer die 11 % unsichersten Urteile an Menschen gibt, fängt 53 % der Fehler. Bei 37 % sind es 85 %** (§9b).
   - Passt zu E-016.
8. **Claude-Agenten befolgen offene schädliche Normen, verdecken aber keine Sabotage** (E-005, E-006).
9. **Kontrolle wächst dosisabhängig mit dem Misstrauen.** Selbstorganisierte Teams bauen Fremdprüfung und Eskalation auf (E-007, H-022). Explizite Bürokratieregeln bringen darüber hinaus nichts.
10. **Prompt-Regeln nahe der Decke bringen nichts** (E-013 null, E-012, H-016). Die Literatur zeigt dasselbe: Rollen-Prompts evolvieren zu leer, und ≥ 54 % der Harness-Gewinne sind Overfitting.

### Hinweise (einmal gesehen oder kleines n)
11. **Spezifikation schlägt Schwierigkeit:** Fehlt der Sollwert im Auftrag, werden 54 % statt 17 % übersehen (n = 24, `notizen/20` §10).
12. **Haiku irrt anders als Sonnet:** mehr Fehlalarme, gleich viel Übersehen.

### Literatur (geprüft, `notizen/18`)
13. Fehler korrelieren stark, **auch über Modellfamilien**: 9 Judges ergeben ≈ 2 effektive Stimmen.
14. **Was entkoppelt:** andere Information, andere Prüffunktion, andere Beweisquelle. **Was nicht:** Persona, Temperatur, Chain-of-Thought.
15. **Gedächtnis ist oft ein gemeinsamer Fehlerpfad.** Lehren reproduzieren Fehler, Vergiftung bleibt bestehen.
16. Kreuzprüfung erodiert über lange Zeit zum gegenseitigen Durchwinken (93,6 % der Trajektorien mit mindestens einer Episode).

---

## 3. Wo wir nur Breite haben (offen, ungetestet)

- **C, Korrelation im eigenen Testbed.** Unsere Prüfer irren zu selten, um Korrelationen zu messen. Das ist der eigentliche Grund für E-020.
- **E, Kontext-Topologie.** "Für Koordination teilen, für Prüfung trennen" ist eine gut begründete These ohne eigenen Test.
- **G, Gedächtnis.** H-031 (private gegen geteilte Erfahrung) ist ungetestet, und die Elara-Designfolgen stehen nur in der Literatur.
- **Langzeiteffekte.** Unsere Runs sind kurz. Erosion, Kollusion und Normdrift sehen wir nicht.
- **Fremdmodelle in Orgs.** Bisher nur im Prüfer-Panel (E-016), nie in Teams.
- **Echte Wave-Daten als Prüfstein.** Was im Labor gilt, haben wir noch nicht an echten Wave-Fällen gespiegelt.

---

## 4. Gute und schlechte Lesarten

| Befund | Gute Lesart | Schlechte Lesart (Überinterpretation) |
|---|---|---|
| Sonnet übersieht nur 4–7 % | Bei vollständigem Auftrag und vorgelegtem Beleg ist es nahe der Decke. Die Fehler sitzen an benennbaren Stellen | "KI-Prüfer sind zuverlässig" oder "unsere Aufgaben sind zu leicht" |
| Reasoning → Fehlalarme ×4–5 | In diesem Material macht Reasoning übervorsichtig, ohne mehr zu finden. **Kandidat für Triage ohne Reasoning** | "Reasoning schadet." In echten Fällen kann Vorsicht berechtigt sein, wenn das Fehlen einer Spur nicht "ok" heißt |
| Konfidenz kalibriert | Konfidenzschwelle als Eskalationsmechanismus testen | "Gilt auch unter Druck." Literatur: Unter einstimmigen Peers und bei schweren Items sind Modelle konfident falsch. Unter Selbstauskunft ungeprüft (E-020 V5) |
| E-014/E-018 bestätigt | Übernahme- und Belegmechanismen wirken im Testbed mit Sonnet | "Abstimmungen lösen Governance." Laut Literatur sind Abstimmungen fragil, und der "Mensch" war bei uns naiv modelliert |
| E-013 null | Prompt-Regeln nahe der Decke bringen nichts. Suchraum auf Mechanismen umstellen | "Harness-Optimierung bringt nichts" |
| Fehler korrelieren familienübergreifend | Modellwechsel ist ein schwacher Dekorrelator, Information ein starker | "Redundanz bringt nichts." Eine 3er-Mehrheit senkt die Fehler trotzdem von 387 auf 131 (Ron et al.) |
| Gedächtnis als Common Cause | Geteiltes, abstrahiertes Gedächtnis gleicht an. Privat und roh speichern | "Gedächtnis ist schlecht" |
| Spezifikation 54 % → 17 % | Starker Hinweis auf den größten Hebel | Belegter Befund (n = 24, ungültiger Lauf) |
| Decke in E-017/E-019 | Die Baseline ist vermessen, und wir wissen *warum* sie leicht ist | "Experiment gescheitert" |

---

## 5. Das große Bild, eine These in drei Sätzen

> **Vertrauen in Agenten-Organisationen skaliert weniger über *mehr Prüfer* als über *bessere Information*.**
> Fehler entstehen dort, wo Information fehlt (Sollwert nicht im Auftrag), sich widerspricht (grüner Status gegen Zahl) oder durch Behauptungen ersetzt wird (Selbstauskunft, Stimme statt Beleg). Aufmerksamkeitsmangel spielt kaum eine Rolle.
> Die wirksamen Harness-Hebel sind deshalb: **Sollwerte explizit machen, Belege der Umwelt statt Selbstauskunft, Unsicherheit eskalieren, Prüfer über Information entkoppeln statt über Modelle.**

Was dafür spricht:
- E-018 (Beleg statt Stimme)
- die Landkarte (Spurtyp, Spezifikation, Konfidenz)
- die Literatur (Information entkoppelt, Selbstauskunft primt, Overclaiming ist normal)
- METR (Signaturen wurden erfunden, aber nicht geprüft)

Was dagegen sprechen könnte:
- Unser Material ist synthetisch und sauber.
- Echte Fehler könnten öfter Wissensfehler sein (Domäne unbekannt), wo mehr Prüfer doch helfen.
- E-020 und ein Abgleich mit echten Wave-Fällen sind die Prüfsteine.

**Brücken:**
- **AAP** ist "Beleg statt Behauptung" als Infrastruktur.
- **Wave** braucht morgen schon: Sollwerte in jedes Ticket, Selbstauskunft vom Prüfer fernhalten, Eskalation nach Konfidenz statt nach Bauchgefühl.
- **Elara** sollte rohe Episoden statt Lehrsätze speichern, und Identität (soul.md) getrennt von Gedächtnis halten.

---

## 6. Woran dein Kopf jetzt arbeiten kann (pro Front eine Denkfrage)

- **A Institutionen:** Wo in Wave wird heute *abgestimmt* oder *behauptet*, wo es einen *Beleg* geben könnte? Jede solche Stelle ist ein E-018-Fall.
- **B Prüfer:** Wo eskaliert Wave heute an dich? Nach welchem Kriterium? Lässt sich das als Konfidenzschwelle denken, und wie viele Minuten würde das sparen?
- **C Korrelation:** Welche Prüfungen in Wave laufen heute doppelt mit *gleicher Information*? Laut Literatur bringen die wenig. Was wäre der "andere Kanal"?
- **D Optimierung:** Welche *Mechanismen* (nicht Prompt-Regeln) würdest du einem Optimierer zur Auswahl geben? Frist, Quorum, Belegpflicht, Rotation, Konfidenzschwelle …
- **E Kontext:** Wer in Wave sieht heute den Bericht des Erzeugers, bevor er prüft? (HK-19-1, E-020 Faktor AUSKUNFT)
- **F AAP:** Welche Wave-Aktion braucht als Erstes eine Umwelt-Quittung statt einer Selbstauskunft?
- **G Elara:** Was soll Elara über dich *wissen* (roh, mit Datum, belegbar) und was *glauben* (abgeleitet, revidierbar)?
- **H Methodik:** Rund zehn Mal haben wir ein Modell "falsch" gewertet, das eigentlich recht hatte, weil unser Generator falsch lag. Das waren 3 Fehler im E-016-Pilot, 3 in E-017, 3 in E-019 L1 und die mehrdeutige `zero_traffic`-Spezifikation. Das ist selbst ein Blog-Thema: *Wer prüft den Prüfer-Prüfer?*

---

## 7. Nächste Schritte (Vorschlag, Reihenfolge)
1. **E-020 freigeben** (`experimente/E-020-realitaet-in-dosen/prereg-entwurf.md`, 3 offene Fragen an dich), Pilot, Hauptlauf (~20 $).
2. **Konfidenz-Eskalation bestätigend testen.** Billig, und viele Daten sind schon da. Das zahlt direkt auf die Kernmetrik ein.
3. **Reasoning gegen Fehlalarme bestätigen.** Kann als Arm in E-020 laufen (offene Frage 3).
4. **Wave-Abgleich:** 10–20 echte Fehlprüfungen aus Wave nach Spurtyp, Spezifikation und Selbstauskunft kodieren. Ist das Laborbild realistisch?
5. **Blogpost 1:** "Wann irrt ein KI-Prüfer?" Die Decke als Befund, die Landkarte, Lehrstück Generatorfehler.
