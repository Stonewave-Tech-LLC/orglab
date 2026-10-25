# Problemstellung: Neos Erfahrung, zugespitzt

**Stand:** 20.10.2026

## Neos Beobachtung (sinngemäß)

- Mit dem Design kommt man nicht hinterher, weil das System so dynamisch sein muss.
- Je größer das Multi-Agent-Setup, desto mehr verbindliche Verträge muss man vorausdenken.
- Es fühlt sich an, als würde man immer mehr Fäden verbinden, damit der Loop tiefer läuft: wenn A, dann B, überprüfen, rückmelden, neu evaluieren.
- Es bleibt Zeug liegen. Dann baut man etwas Neues darauf, damit es besser funktioniert. Beim nächsten Mal läuft es ein paar Schritte weiter, dann hakt es wieder. **Man gewinnt kein Land.**
- Vermutung, noch nicht empirisch geprüft: Andere Modelle bevorzugen andere Verhaltensweisen. Verträge, die für ein Modell passen, passen dann für ein anderes nicht.
- Wunsch: Ein System, das sich robust selbst reguliert und dessen Regeln bewusst nach optimierten Maßstäben entstehen, statt von Hand vorgedacht zu werden.

## Zuspitzung

**Das Problem ist nicht ein fehlender Social Skill, sondern das Regulationsregime.** Handgeschriebene Verträge sind eine Steuerung von außen. Damit sie funktionieren, müssen sie so viel Varianz abdecken wie das System erzeugt (Ashby: Law of Requisite Variety). Bei wachsender Agentenzahl, mehr Interaktionstypen und wechselnden Modellen gelingt das nicht.

Jeder Patch schiebt die Fehlerfront ein paar Schritte weiter, ändert aber das Regime nicht. Fixes sind lokal und komponieren nicht.

**Daraus folgt die verschobene Forschungsfrage:** Welche Regulationsmechanismen machen eine Agenten-Organisation selbstkorrigierend, sodass Verbesserungen kumulieren statt verpuffen? Und halten sie auch dann, wenn man das Modell tauscht?

Social Skills sind dann die Mikroverhalten, die Regulation umsetzen: Rückfragen, Eskalieren, Widersprechen, liegengebliebene Arbeit aufgreifen.

## Zwei Ebenen von "selbst regulieren"

1. **Zur Laufzeit (online):** Die Organisation korrigiert sich *während* eines Runs. Beispiele sind Stigmergie bzw. Pressure Fields, Selbstwahl der Rollen und Normen, die Agenten selbst vorschlagen.
2. **Zwischen Runs (offline):** Ein Optimierer schreibt die Org-Konfiguration auf Basis von Evidenz um. Das ist der Propose-Probe-Compose-Loop à la Harness², über eine Org-Konfiguration statt über einen einzelnen Agenten.

"Bewusst nach optimierten Maßstäben entstehen lassen" ist Ebene 2, die Ebene-1-Mechanismen erzeugt und auswählt.

## Kandidaten-Regime für den Vergleich

| Regime | Idee | Bezug |
|---|---|---|
| A: Explizite Verträge | Status quo: Rollen und Wenn-dann-Protokolle von Hand | Wave heute |
| B: Minimales Gerüst | Feste Reihenfolge, Rollen wählen die Agenten selbst | Dochkina |
| C: Stigmergie | Geteiltes Board, Claims verfallen, offene Arbeit erzeugt "Druck" | Pressure Fields, SwarmWorld |
| D: Selbstverfassung | Agenten dürfen Regeln vorschlagen und ändern, mit einer Meta-Regel | Ostrom-Designprinzipien |
| E: Optimierer | Ein Loop zwischen den Runs schreibt die Org-Konfiguration für A–D um | Harness²-Prinzip |

## Metriken, die Neos Symptome direkt messen (Entwurf)

- **Liegengebliebenes:** Anteil offener Commitments am Ende (begonnen, übergeben oder zugesagt, aber nie geschlossen), dazu die Lebensdauer verwaister Arbeit.
- **Land gewinnen:** Wirkt ein Fix aus Runde *n* in Runde *n+k* noch? Komponieren zwei Fixes, oder heben sie sich auf? Steigt die Kurve über die Runden, oder sägt sie?
- **Robustheit:** Gezielte Störungen einspielen (Agent fällt aus, Maulwurf, unklare Spec, Modelltausch mitten im Betrieb) und dann Erholungszeit und Erholungsgrad messen.
- **Modell-Transfer:** Dasselbe Regime auf mehreren Modellen laufen lassen. Ist ein Regime über Modelle hinweg stabil, oder braucht jedes Modell eigene Verträge? Damit wird Neos Vermutung testbar.
- **Design-Kosten:** Wie viele explizite Regeln bzw. Tokens Regeltext braucht ein Regime für ein gegebenes Leistungsniveau?
