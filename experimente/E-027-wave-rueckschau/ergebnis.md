# E-027: Rückschau auf echte Wave-Fälle – Ergebnis: am Material-Gate gestoppt, zur Seite gelegt

- **Datum:** 2026-10-25
- **Stand:** Kein Hauptlauf. Sonnet hat keinen Fall beurteilt; zu H-043 gibt es **kein Ergebnis**. Neo, 25.10.: "legen wir es zur seite mit kommentar und möglichem späteren zweiten versuch".
- **Harness-Läufe** (Welt `welt-wave/`, lokal): E-027-1 vom Kritiker gestoppt (einmal präzisiert, Antworten in `prereg.md`), E-027-2 Kritik bestanden, **Gate MATERIAL rot**.
- **Kosten:** etwa 2 $ (Klassifikation aller 316 Fälle durch GPT, zwei Kritiken).

## Was passiert ist
- **FESTLEGEN:** bestanden. Code-Tests grün; der Hash des Wave-Exports und der von Neos Stichprobe stimmen.
- **KRITIK (E-027-2):** nichts Blockierendes. Die kleinen Punkte des Kritikers stehen schon unter "Offene Schwächen" (kurze Fälle in Neos Stichprobe, Bridge nicht geclustert, LLM-Text als Beleg, p ohne +1).
- **MATERIAL:**

| Bedingung | Ergebnis | verlangt |
|---|---|---|
| Klassifikation lesbar | 316/316 | ≥ 95 % |
| Neos Stichprobe vollständig | 20/20 | 20 |
| **Übereinstimmung GPT mit Neo** | **13/20 (65 %)** | **≥ 80 %** |
| nicht belegte wörtliche Fälle | 137 | ≥ 30 |

GPTs Klassen (alle 316): nicht anwendbar 92, belegt Erfolg 45, belegt Fehlschlag 19, nicht belegt 160 (davon 137 wörtlich). Das ist eine Beschreibung des Materials, kein Prüfer-Ergebnis.

## Warum die Übereinstimmung zu niedrig war
Die 7 Abweichungen haben genau zwei Ursachen. Bei den übrigen 13 Fällen stimmen Neo und GPT überein.

1. **Abschlussberichte von Agenten** (5 Episoden-Fälle: ep-002-t2, ep-008-t2, ep-017-t2, ep-032-t2, ep-033-t2). Neo: belegt Erfolg. GPT: nicht belegt.
   - Der Worker beschreibt im Abschlusstext sehr konkret, was er getan hat (Zustände, Commit-Hashes, Exit-Code).
   - GPT wertet das als Selbstauskunft, weil keine Ausgabe des Systems selbst wiedergegeben ist. Neo las die konkreten Details als Beleg.
   - Die Definition ließ das offen: "Aussage des Agenten zählt nicht" stand neben "wiedergegebene Ausgabe zählt". Neo hatte genau diese Frage vor dem Start gestellt ("wie aussagekräftig ist es wenn auch eine logzeile aus dem output des agenten eigentlich llm freitext ist"). Die daraufhin ergänzte strenge Lesart lief nur deskriptiv mit und änderte die Klassen nicht.
2. **Sicherheitstests, die eine Ablehnung prüfen** (2 Executor-Fälle: ex-002, ex-009). Neo: belegt Fehlschlag (die Aktion lief nicht). GPT: belegt Erfolg (die beabsichtigte Ablehnung ist protokolliert).
   - Die Definition sagte nicht, ob der beabsichtigte Effekt die Aktion selbst ist oder das, was der Auftrag prüfen wollte.

## Was daraus folgt (Status: Hinweis)
- **Das Gate hat getan, wofür es da ist.** Ohne den Stopp hätte Sonnet auf einer Grundwahrheit gerechnet, bei der Mensch und Klassifikator "belegt" bei Agentenberichten verschieden lesen. Jede Zahl zu W1 hätte an dieser unklaren Grenze gehangen.
- **Für Wave (Hinweis):** Ob der detaillierte Abschlussbericht eines Workers als Beleg gilt, ist schon zwischen einem sorgfältigen Menschen und einem starken Modell strittig. Genau auf diesem Text entscheidet laut Ace der Episoden-Tick (`berichte/2026-10-25-antwort-ace-update-4.md`). Das ist eine Beobachtung an 5 Fällen, kein Befund.
- **Lehre für das Verfahren:** Definitionen der Grundwahrheit vor dem Einfrieren an einigen Fällen mit Neo eichen (eine kurze Eichrunde, deren Fälle danach nicht mehr zur blinden Stichprobe gehören).

## Möglicher zweiter Versuch (nur Vorschlag, braucht neue Präregistrierung und Neos Freigabe)
- **Agentenbericht zählt nie als Beleg**, egal wie detailliert. Als Beleg gilt nur, was das System selbst protokolliert hat. Folge: Bei Bridge und Episoden ist "belegt" praktisch nie möglich. W1 misst dann, wie oft Sonnet auf einen Bericht des Agenten hin Erfolg bestätigt, also die Lage des Episoden-Ticks.
- **Prüft ein Auftrag, dass etwas abgelehnt wird, ist die Ablehnung der Erfolg.**
- GPT stuft alle Fälle neu ein. **Neo stuft 20 andere Fälle blind ein**, denn die bisherigen 20 kennt er jetzt samt GPTs Antwort.
- Vorher eine kurze Eichrunde mit Neo an wenigen Fällen außerhalb der Stichprobe.
- Alles andere (Zellen, Vorhersagen, Auswertung, Harness v1.3) kann bleiben. Material, Code und Welt liegen bereit.

## Grenzen dieses Ergebnisses
- 20 Fälle, eine menschliche Einstufung. Wer bei den 7 Fällen "recht" hat, ist eine Frage der Definition, nicht der Messung.
- Claude hat für diese Diagnose die 4 betroffenen Fälle und GPTs Begründungen gelesen. Prüfer-Urteile gibt es keine.
