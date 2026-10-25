# Externes Gutachten 4: Grok-Nachgutachten zu E-020 v3 (Material v4.3, vor dem Hauptlauf)

- **Datum:** 2026-10-23 14:18, ein einziger Aufruf, angefordert von Neo ("Mach das Nachgutachten")
- **Aufruf:** Grok Build CLI 1.0.62, `-m grok-4.7` (Debug-Log: grok-4.7)
  - Plan-Modus, `--disable-web-search`, `--no-subagents`, Shell/Schreiben/Web/Subagenten gesperrt
  - leerer Kopie-Ordner ohne Secrets und Rohdaten, `GROK_FOLDER_TRUST=0`; Prüfsummen vorher/nachher gleich
- **Material:** prereg-v3, dryrun-v3, pilot-v3-bericht, lecktest, fremdkontrolle, notizen/23c und 29, `e020v3.py`, `evidence_v4.py`, `evidence.py`, Tests, Diff seit Gutachten 3. Fehlerraten der Piloten nicht enthalten.

## Einordnung durch Claude

| Punkt | Einordnung | Konsequenz (Abweichung 3, vor dem Start) |
|---|---|---|
| Alle Punkte aus Gutachten 3 behoben oder teilweise behoben, Empfehlung **"Hauptlauf jetzt starten"** | – | Hauptlauf startet |
| **Erste Zeile:** Die Zielzeile steht auf der Runbook-Seite zuerst und namensgleich. V1 misst also "Langauftrag gegen eine Seite mit Zielzeile oben" | berechtigt, Deutungsgrenze | Wird in ergebnis.md als Grenze von V1 genannt. Ein kleines V1 heißt nicht "Auffindbarkeit egal" |
| **V4:** Die ganze Seite enthält jeden Abschnittskopf, `right_section` ist dann automatisch wahr. Es misst "Kopf/Seite zurück", nicht "Normwert gelesen" | berechtigt, mein Fehler (Abweichung 2 Punkt 4 versprach den Normwert) | V4 wird als "Seite zurück" berichtet. Zusätzlich, **als explorativ markiert**: ob der Normwert-String in einer Werkzeugantwort stand, aus den Transkripten |
| **"Widerlegt" bei V1** heißt obere Grenze < +0,10. Das schließt einen kleinen relevanten Effekt (+0,05) nicht aus. Power-Simulation mit 1000 statt 5000 Bootstrap-Ziehungen und unabhängigen Fehlern | berechtigt | Formulierung im Ergebnis: "+0,10 ausgeschlossen", nicht "kein Effekt". Power-Werte gelten als Näherung |
| "Praktisch null" auch bei klar negativem Intervall | berechtigt, klein | Richtung wird mit Mittel und Intervall immer mitberichtet (steht in derselben Zeile) |
| Veralteter Fließtext (47/48, alter Grenzfall) im Hauptteil | berechtigt, klein | Abweichung 2 gilt, Hauptteil bleibt unverändert (nur anhängen) |
| Wortende fehlt: "port" trifft "portal" | berechtigt, niedrig | Kein Eingriff, das Material ist eingefroren. Wirkt nur, wenn Sonnet "port" sucht und dann einen Portal-Abschnitt zusätzlich bekommt |
| Pilot 3: fünftes Transkript nur im Sammelsatz | berechtigt, stand schon so im Bericht | – |

## Das Gutachten (wörtlich)

Ich lese zuerst `AUFTRAG.md` und arbeite den Auftrag danach genau ab.Der Auftrag ist ein reines Lesegutachten. Ich lese Gutachten 3, die Abweichung, den Pilotbericht und das Diff.Die früheren Punkte sind klar. Als Nächstes prüfe ich Diff, Auswerteskript und Generator dagegen.**Empfehlung: Hauptlauf jetzt starten.** Die Änderungen aus Gutachten 3 sind umgesetzt; was offen bleibt, engt die Deutung ein und lässt V1–V3 gültig.

## 1. Punkte aus Gutachten 3

- Seite als Antwortschlüssel: **teilweise.** Jede Norm steht zwischen mindestens drei weiteren Werten (`evidence_v4.py` 280–286, 388–398, 479–483; `tests/test_evidence_v4.py` 180–187). Der Zieleintrag steht immer zuerst und bleibt über den Namen im Kurzauftrag eindeutig (`prereg-v3.md` 117).
- Entscheidungsregel: **behoben.** `classify` setzt nachgewiesen, gestützt, widerlegt, praktisch null und nicht entschieden (`e020v3.py` 268–281; `prereg-v3.md` 122–127; `tests/test_e020v3.py` 103–111). Die Tabelle „Widerlegt, wenn obere Grenze < +0,02“ (`prereg-v3.md` 52) gilt durch diese Abweichung als ersetzt.
- Power: **behoben.** `power` bewertet diese Etiketten (`e020v3.py` 304–317); die Zahlen stehen in der Abweichung (`prereg-v3.md` 137–140).
- V2 und Fehlalarm: **behoben.** Primär-V2 bleibt über alle kaputten Belege; spec-rein ist sekundär ohne Etikett; der Fehlalarm ist ein eigener Satz (`e020v3.py` 353–359; `prereg-v3.md` 129).
- V4, zwei Felder: **teilweise.** Gespeichert werden `page_returned` und `right_section` (`e020v3.py` 153–154). `right_section` wird wahr, sobald `[{Abschnitt}]` in der Werkzeugantwort steht (`prereg-v3.md` 130 verlangt den Normwert).
- `low_traffic`: **behoben.** Uptime 300–900 s, übliche Last ab 100/min, kaputte Last 10–30 % und mindestens 10 (`evidence_v4.py` 147–158). Fremdkontrolle v4.3: 48/48, 6021 eindeutig (`notizen/29` 44; `prereg-v3.md` 146). Die Sensitivität ohne 6021 bleibt (`pilot-v3-bericht.md` 60).
- Normtext: **behoben.** „±20 %“, „steady around the clock“, „connects to all shards“ und „single production instance“ stehen im langen Auftrag und im Runbook (`evidence_v4.py` 152–153, 280–286; `tests/test_evidence_v4.py` 167–177).
- Wortgrenzen: **teilweise.** Es gilt ein Wortanfang, dadurch trifft „port“ „report“ nicht mehr (`evidence_v4.py` 120–121; `tests/test_evidence_v4.py` 190–193). Ein Wortende fehlt, „port“ trifft weiter „portal“.
- Fünf Transkripte: **behoben** (`pilot-v3-bericht.md` 39–42, 51–56). In Pilot 3 steht das fünfte nur im Sammelsatz (56).
- Analyse-Einheit: **behoben.** Die Abweichung stellt den Beleg klar (`prereg-v3.md` 141); das Skript bootstrapt Belege (`e020v3.py` 233–249).
- Voreilige SPEC-Lesart: **behoben**, ohne Gewicht für den Hauptlauf (`pilot-v3-bericht.md` 37–38; `prereg-v3.md` 131).
- Pilot auf frischen Seeds: **behoben.** Pilot 3, Seeds 1400–1401, Material v4.3, technische Kriterien erfüllt (`pilot-v3-bericht.md` 45–57; `prereg-v3.md` 133–134, 147).

## 2. Neue Probleme

- **Mittel — erste Zeile.** In Verkehr, Cache, Zahlung, Kontakten, Duplikaten, Gewichten und Spaltenzahl ist der Zieleintrag der erste namensgleiche Wert (`evidence_v4.py` 282, 388–391, 395, 480–483). V1 vergleicht den Langauftrag mit dieser Liste. Ein kleines oder als widerlegt etikettiertes V1 heißt: dieser erste Eintrag hat das Übersehen gegenüber dem Langauftrag um weniger als den Vorhersagewert verschoben.
- **Mittel — V4.** Der Einheitennamen-Aufruf liefert die ganze Seite, und die enthält jeden Header (`evidence_v4.py` 118–119). Dann sind `page_returned` und `right_section` zugleich wahr. Der Satz „davon ganze Seite erhalten“ zählt alle SPEC=1-Primärprüfungen mit Seite (`e020v3.py` 373–376); „davon“ hängt sprachlich am unmittelbar davor genannten Teil. Für H-033 ist das Feld „Header kam zurück“.
- **Mittel — „widerlegt“ nach Ersatz der Teststärke.** „Widerlegt“ heißt „obere Grenze < Vorhersagewert“ (`e020v3.py` 279–280; `prereg-v3.md` 125). Die neue Power nennt „gestützt bei +0,10“ und „widerlegt bei Effekt 0“ (`prereg-v3.md` 138–140) und ersetzt den Abschnitt, in dem Effekte um +0,05 offen bleiben (`prereg-v3.md` 62–66). Der kleinste relevante Effekt ist weiter +0,05 (`prereg-v3.md` 62). Die Simulation nutzt innen Bootstrap 1000 statt 5000 (`e020v3.py` 309, 46) und unabhängige Fehler (`prereg-v3.md` 137); der Hinweis auf Abhängigkeit steht im ersetzten Abschnitt (67).
- **Niedrig — negative Intervalle.** Liegt die Obergrenze unter +0,02, lautet das Etikett „praktisch null“, auch bei klar negativem Intervall (`e020v3.py` 277–278). Mittel und Intervall stehen in derselben Zeile (351–354).
- **Niedrig — veralteter Fließtext.** Der Hauptteil nennt noch 47/48 und den alten Grenzfall (`prereg-v3.md` 41–42). Gültig ist Abweichung 2: v4.3, 48/48 (144–146).
- **v4.3:** keine entwertende Verzerrung. Eine Instanz und eindeutige Datei-Deskriptoren sind auf den Hauptlauf-Seeds geprüft (`prereg-v3.md` 145–146; `notizen/29` 43–45; `tests/test_evidence_v4.py` 201–208). Staging steht als eigene Umgebung hinter der Produktionszeile (`evidence_v4.py` 283, 286).

## 3. Empfehlung

Hauptlauf jetzt starten. Vor dem Lesen der Auswertung festziehen: V1 vergleicht den Langauftrag mit einer Seite, deren Zielzeile zuerst und namensgleich steht. „Vorhersage widerlegt“ schließt +0,10 (V1) bzw. +0,05 (V2) aus. V4 gilt als „Header bzw. Seite zurück“, bis `right_section` den Normstring prüft. Die Transkripte enthalten die Werkzeugantworten (`e020v3.py` 137, 156); das ist eine Zeile vor `analyze`, kein neues Material und kein neuer Pilot.
