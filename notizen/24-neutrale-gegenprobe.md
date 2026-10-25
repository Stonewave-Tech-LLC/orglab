# Neutrale Gegenprobe: Kommt ein frischer Kritiker von selbst auf unseren Rahmen?

**Stand:** 22.10.2026, spät
**Anlass:** Neo bemerkte, dass sich das "Inception"-Gefühl ("unser Projekt ist selbst ein Fall der These") verdächtig gut anfühlt. Vielleicht ist der Rahmen nur ein Produkt unseres langen Gesprächs.

## Vorab festgelegt (geschrieben, bevor die Antwort vorlag)

**Kritiker:**
- Grok Build CLI, **frische Sitzung**, in einem **leeren Ordner** (keine Projektdateien), ohne Websuche, Nur-Lese-Modus
- Kein Wissen über unser Projekt, die These oder unsere Begriffe

**Frage:** Sie meidet unsere Schlüsselwörter (Beleg, Prüfer, Vertrauen, Verifikation, Selbstauskunft, Quittung, Eskalation). Wortlaut siehe unten.

**Was als Signal zählt:**

| Ergebnis | Kriterium | Deutung |
|---|---|---|
| **Konvergenz** | Unter den **Top 3** der Faktoren für Verlässlichkeit steht ungefragt "Ergebnisse unabhängig gegen den echten Zustand prüfen" bzw. "nicht auf die eigenen Erfolgsmeldungen der Agenten verlassen", **und** die Leistungsfähigkeit des Modells steht nicht auf Platz 1 | Der Rahmen ist kein reines Artefakt unseres Gesprächs. **Aber:** Dann ist er womöglich auch Mainstream und weniger neu, als er sich anfühlt. |
| **Divergenz** | Überprüfung gegen den echten Zustand fehlt in den Top 5, oder Modellleistung bzw. Prompt-Qualität dominieren | Entweder ist unser Rahmen eigen (neu oder schief), oder er ist ein Gesprächsartefakt. Das ist mit dieser Probe nicht zu trennen, aber ein Warnsignal. |
| **Gemischt** | Prüfung in den Top 5, aber nicht in den Top 3 | Rahmen plausibel, aber nicht zwingend. Unsere Gewichtung könnte überzogen sein. |

**Grenze der Probe:** Ein LLM gibt den verbreiteten Diskurs wieder, keine Empirie. Konvergenz heißt "andere denken auch so", nicht "es stimmt". Und Grok ist ein Sprachmodell wie ich. Ähnliche Trainingsdaten können zu ähnlichen Rahmen führen (H-026 lässt grüßen).

## Frage (Wortlaut)

Siehe `FRAGE` unten, unverändert an Grok übergeben.

FRAGE:
Ein mittelgroßes Unternehmen lässt mehrere KI-Agenten zusammenarbeiten. Sie erledigen echte Arbeit: Software ausrollen, Rechnungen an Kunden verschicken, Datensätze aufbereiten. Die Agenten teilen sich die Arbeit untereinander auf.

1. Was bestimmt am stärksten, ob die Ergebnisse am Ende tatsächlich stimmen? Nenne die 5 wichtigsten Faktoren, geordnet nach erwartetem Einfluss, mit je 1–2 Sätzen Begründung.
2. Welcher Faktor wird in der Praxis am häufigsten überschätzt, welcher unterschätzt?
3. Das Unternehmen möchte, dass möglichst wenig menschliche Arbeitszeit dafür nötig ist. Was würdest du konkret raten?

Sag, wo du unsicher bist. Antworte auf Deutsch.

## Antwort

Grok Build CLI 1.0.62 (`-m grok-4.7`), frische Sitzung, leerer Ordner, ohne Websuche, 22.10. ~23:50. Der Wortlaut folgt unverändert, als Zitat eingerückt.

> Am stärksten entscheidet, ob das Ergebnis **unabhängig vom Agenten prüfbar** ist. Modellwahl und „die Agenten kontrollieren sich gegenseitig“ ändern daran wenig.
>
> ## 1. Die fünf Faktoren, nach erwartetem Einfluss
>
> **1. Deterministische Prüfung gegen eine unabhängige Quelle**  
> Ob am Ende ein Abgleich existiert, den kein Sprachmodell auslegen kann: Tests und Canary beim Deploy, Summe = Auftragspositionen + Steuer − Gutschriften bei der Rechnung, Schema, Zeilenzahl, Schlüssel und Verteilungsgrenzen bei Datensätzen. Fängt diese Prüfung den Fehler, ist das Ergebnis belastbar. Fehlt sie, bleibt auch ein plausibler Output unbelegt.
>
> **2. Vollständigkeit der Definition von „richtig“**  
> Regeln, Grenzfälle und Verbote müssen vor dem Lauf festliegen: Teillieferung, Skonto, Storno, Dublette, Feature-Flag, Migration, leere Datei, nachgezogene Korrektur. Agenten erfüllen den Auftrag wörtlich. Was in den Regeln fehlt, wird selbstbewusst falsch erledigt.
>
> **3. Eindeutigkeit und Aktualität der führenden Daten**  
> Kundenstamm, Preise, Steuerkennzeichen, Auftragsstatus, Repo-Stand, Quelldateien. Die Agenten erzeugen keine Ground Truth. Ein veralteter Preis oder ein mehrdeutiges Ticket wird in Rechnung, Deploy und Datensatz weitergereicht.
>
> **4. Seiteneffekte: Rechte, Idempotenz, Staging, Rücknahme**  
> Deploy und Rechnungsversand sind schwer zurückzuholen. Enge Rechte, Entwurf vor Versand, Canary, automatisches Rollback und Idempotenzschlüssel entscheiden, ob ein Fehler eine Vorschau bleibt oder beim Kunden ankommt. Ein zweiter Lauf darf keine zweite Rechnung und kein zweites Deploy erzeugen.
>
> **5. Verträge an den Übergaben**  
> Typisierte Artefakte mit Schema: Diff, Testbericht, Rechnungsentwurf, Prüfsumme. Freitext wie „der andere Agent macht den Rest“ verliert Annahmen, doppelt Arbeit und markiert Teilstände als fertig. Die Aufteilung selbst ist selten die Fehlerquelle. Die Übergabe ist es.
>
> Die Reihenfolge von 3 bis 5 ist ein Urteil, kein Messwert. Bei Rechnungen wiegen Daten und Abgleich schwerer, beim Deploy Tests und Rollback, bei der Datenaufbereitung Schema und Goldmengen. Faktor 1 bleibt in allen drei Fällen vorn.
>
> ## 2. Überschätzt und unterschätzt
>
> **Überschätzt wird die Modellstärke und die gegenseitige Agentenprüfung.** Mehr Agenten, ein Planungsagent oder „ein zweites Modell reviewed das“ erzeugen im Alltag oft denselben Fehler in höflichem Ton. Ein Prüfer ohne unabhängige Quelle bestätigt den Entwurf, er widerlegt ihn nicht. Orchestrierung steht bewusst nicht in den fünf Faktoren.
>
> **Unterschätzt wird Faktor 1, die mechanische Prüfung.** Teams investieren in Prompts und Rollen und behandeln Tests, Abgleich und Invarianten als Nacharbeit. Dort entscheidet sich, ob das Ergebnis stimmt.
>
> ## 3. Wenig menschliche Zeit: konkret
>
> Menschliche Stunden gehören in die Regeln und in die Ausnahme, nicht in die Durchsicht jedes Laufs.
>
> - **Workflows fest verdrahten.** Wer deployt, wer eine Rechnung baut, wer Daten schreibt, legt Code fest. Agenten handeln das in der Produktion nicht untereinander aus. Dynamische Aufteilung ist der Teil, den später Menschen debuggen.
> - **Jede Aktion in drei Klassen schneiden.** Lesen und Entwurf laufen frei. Versenden, Mergen, Prod-Deploy und Schreiben ins führende System nur, wenn die Checks grün sind. Alles andere geht in eine kurze Queue.
> - **Invarianten als Code, nicht als Prompt.** Beispiele: Rechnungssumme gleich Auftrag, keine Dublette auf Auftragsnummer plus Zeitraum, Deploy nur bei grüner CI, Datensatz nur wenn Pflichtfelder, Schlüssel und Zeilenzahl in der erwarteten Spanne liegen. Jede neue Fehlerklasse aus der Queue wird ein Check, kein neuer Agent.
> - **Zuerst Schattenbetrieb.** Die Agenten erzeugen Diff, Rechnungsentwurf und Datensatz. Menschen führen noch aus. Automatisieren Sie nur die Scheibe, auf der über ein paar Wochen keine Abweichung auftrat. Den Rest lassen Sie in der Queue.
> - **Rechnungen.** Automatisch senden nur bei bekanntem Kunden, passendem Auftrag, plausibler Steuer, keiner offenen Gutschrift und keiner zweiten Rechnung auf denselben Schlüssel. Grenzfälle sieht ein Mensch. Bei Umsatzsteuer, GoBD und E-Rechnung ist eine nachweisbare Kontrolle oft nötig. Wie weit der Versand ohne Person rechtssicher ist, kann ich von hier nicht beurteilen.
> - **Deploys.** Agent öffnet die Änderung. Merge und Rollout folgen der Pipeline: Tests, Canary, automatisches Rollback. Ein Mensch kommt bei rot, bei Migration und bei Änderungen an Berechtigungen oder Abrechnung.
> - **Datensätze.** Schema, Summen, Nullanteile, Goldset. Der Mensch sieht die Abweichungsliste, nicht die Tabelle.
> - **Rechte trennen.** Der Rechnungsagent deployt nicht. Der Deploy-Agent versendet keine Kundenmail. Der Datenagent schreibt nicht ins Buchhaltungssystem.
> - **Eine feste, kleine Review.** Ein bis zwei Stunden pro Woche auf die Queue und das Audit-Log. Stichprobe statt Vollprüfung. Das senkt die Menschenzeit über die Monate, weil jede Wiederholung ein Check wird.
>
> Ein durchgängiger Verzicht auf Menschen ist bei Deploy und Rechnung der teure Weg: Der erste nicht erkannte Fehler kostet mehr Zeit, als die Queue je gespart hat. Der sparsame Weg ist, die langweilige Wiederholung maschinell zu prüfen und Menschen nur auf Irreversibles und auf Fälle ohne klares „richtig“ zu setzen.
>
> **Unsicher bin ich hier:** Die Rangfolge 3–5 hängt am Mischungsverhältnis der drei Arbeiten, und ich kenne Ihre Fehlerquoten, Systeme und Freigaberegeln nicht. Wie stark ein zweites Modell hilft, wenn es echte Tools zum Abgleich hat und nicht nur den Text liest, ist eine Grauzone. Ich bin sicher, dass diese Hilfe den Abgleich nicht ersetzt.

## Auswertung gegen die Kriterien

**Ergebnis: Konvergenz** (Kriterium erfüllt)
- Platz 1: "Deterministische Prüfung gegen eine unabhängige Quelle"
- Modellstärke steht ausdrücklich unter "überschätzt", nicht auf Platz 1
- Ebenfalls "überschätzt": "Ein Prüfer ohne unabhängige Quelle bestätigt den Entwurf"

**Weitere Überschneidungen, nicht vorab als Kriterium festgelegt, deshalb nur beschreibend:**

| Grok, ungefragt | Unser Projekt |
|---|---|
| Platz 2: "Vollständigkeit der Definition von richtig" | H-033 (Sollwerte im Auftrag), E-020 Faktor SPEC |
| "Ein Prüfer ohne unabhängige Quelle bestätigt den Entwurf" | H-018, H-029, Literatur zu korrelierten Fehlern |
| "Menschliche Stunden in die Regeln und in die Ausnahme", Stichprobe, Queue | `notizen/14` (Verlässlichkeit pro Mensch-Minute), Eskalation |
| Platz 5: Übergabeverträge statt Freitext | H-007 (gemeinsamer Zustandsträger) |
| "Workflows fest verdrahten, Agenten handeln das nicht aus" | **Widerspruch** zu H-003 (Selbstorganisation robuster) und zu Dochkina. Passt aber zu Mieczkowski (Vorab-Zuweisung schlägt Selbst-Claimen bei Abhängigkeiten, HK-D7) |

**Deutung (wie vorab festgelegt):**
1. Der Kern des Rahmens ist **kein Artefakt unseres Gesprächs**. Ein frischer Kritiker ohne unsere Begriffe kommt von selbst darauf.
2. **Der Kern ist damit aber auch nicht neu.** Das ist verbreitetes Praktikerwissen (Tests, Invarianten, Idempotenz, Schattenbetrieb, Ausnahme-Queue). Das "Inception"-Gefühl kam eher daher, dass ein bekanntes, gutes Prinzip auf uns selbst passt, nicht von einer neuen Entdeckung.
3. **Wo unser Beitrag liegen kann:** nicht in der Idee, sondern in **Messung und Grenzen**.
   - Wie viel bringt welcher Hebel?
   - Wann gilt das Prinzip *nicht*?
   - Konkrete, belegte Mechanismen: Beleg-Regel gegen Abstimmung (E-018), Reasoning und Fehlalarme (H-036), Information gegen Stil (H-029/H-030).
   - Was Grok als Urteil formuliert ("Reihenfolge 3–5 ist ein Urteil, kein Messwert"), ist genau das, was wir messen können.
4. **Ein echter Widerspruch** zu unseren Annahmen: feste Verdrahtung statt Selbstorganisation. Er verdient eine eigene Prüfung (HK-D7, Abhängigkeitsstruktur als Moderator).

**Grenzen:**
- Die Frage enthält "tatsächlich stimmen". Das könnte leicht in Richtung Prüfung lenken.
- Grok ist ein Sprachmodell mit ähnlichen Trainingsdaten. Konvergenz zweier LLMs kann auch geteilter Diskurs sein, gemeinsame Fehler eingeschlossen (H-026 auf Ebene der Weltbilder).
- Eine einzige Antwort, keine Wiederholung.
- Grok hat eine globale Gedächtnisfunktion (`/remember`). Wir haben dort nichts gespeichert, und die Sitzung lief in einem leeren Ordner. Ganz ausschließen lässt sich ein Übertrag aus der Gutachten-Sitzung nicht. Die Wortwahl enthält aber keine unserer Projektbegriffe.
