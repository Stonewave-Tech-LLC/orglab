# Reflexionsprotokoll: der Forschungsprozess als Beobachtungsgegenstand

**Angelegt:** 23.10.2026, 09:21, auf Neos Wunsch. Fortsetzung von `notizen/25` (rückblickende Fehlerzählung) und `notizen/24` (neutrale Gegenprobe).
**Status von allem, was hier steht:** Erfahrungsbericht, n = 1 Forschungsteam (Neo und Claude). **Kein Beleg.** Methodisch ist das reflexive Praxis bzw. Autoethnographie, und so wird es auch gekennzeichnet.

## Warum
Neos zwei Lesarten (23.10. vormittags):
1. **"Bug in der Matrix":** Hinter den Mustern steckt etwas, das wir noch gar nicht auf dem Schirm haben.
2. **Schleichende Konvergenz:** Claude baut sich die Welt so, dass sie zu den gewünschten Ergebnissen konvergiert, nicht durch große Fehler, sondern durch viele kleine Deutungen, die sich in dieselbe Richtung neigen.

Lesart 2 ist **widerlegbar**. Dieses Protokoll soll sie prüfen, statt sie im Rückblick zu erzählen. Lesart 1 bleibt auf dem Parkplatz, bis die langweiligen Erklärungen ausgeschöpft sind (gemeinsame Trainingsdaten, auf Zustimmung trainierte Modelle, Prompt-Konventionen).

## Was als Fehler zählt (vorab festgelegt)
Etwas, das **unkorrigiert** ein Dokument, Daten, eine Auswertung oder eine Aussage an Neo, Ace oder den Blog verändert hätte. Code-Fehler, die schon beim ersten Ausführen auffallen (Syntaxfehler, Absturz), zählen **nicht**, weil sie nie etwas erreicht hätten.

## Kategorien je Eintrag (vorab festgelegt, nicht nachträglich ändern)

| Feld | Werte |
|---|---|
| **Wann** | Datum, Uhrzeit |
| **Was** | ein Satz |
| **Wer machte den Fehler** | Claude · Neo · GPT · Ace · Grok · Code/Generator (von Claude gebaut) |
| **Gefunden durch** | selbst (ohne Anstoß) · Regel (Nr.) · anderes Modell (welches) · Neo · Realität (Lauf, Daten) · noch nicht |
| **Ohne diese Regel/Prüfung aufgefallen?** | ja · nein · unklar |
| **Hätte das Ergebnis verändert?** | ja · nein · unklar |
| **Richtung (Claude)** | pro These · contra These · neutral · unklar, dazu welche These |
| **Richtung (blind)** | dieselben Werte, kodiert von GPT oder Neo **ohne** Claudes Einschätzung. **Nur diese Spalte zählt für die Auswertung**, weil Claude bei der eigenen Richtung befangen wäre. |
| **Verweis** | Laborbuch-Eintrag, Datei, Commit |

## Vorab festgelegte Auswertung (Lesart 2)
- **Zeitpunkt:** nach 20 *vorausschauenden* Einträgen mit Fehlerquelle Claude oder Code/Generator, spätestens am 23.11.2026.
- **Vorhersage, falls Lesart 2 zutrifft:**
  - (a) Unter den Einträgen mit Richtung pro oder contra (blind kodiert) überwiegen **pro These mindestens 2:1**, bei mindestens 10 gerichteten Einträgen.
  - (b) Fehler pro These werden **seltener selbst** gefunden als Fehler contra These.
- **Gegenteil:** Etwa symmetrische Richtung (zwischen 1:2 und 2:1) gilt als kein Hinweis auf schleichende Konvergenz.
- **Zu wenig Einträge:** Unter 10 gerichteten Einträgen wird nur beschrieben.
- **Außenblick:** Danach liest ein Kritiker aus anderer Familie (Grok) oder eine Fachperson aus `notizen/16` Protokoll und Auswertung.
- **Bekannte Schwächen:**
  - Claude trägt ein und kann dabei auswählen. Gegenmittel: Jeder Fehler, der im Laborbuch als Korrektur auftaucht, muss auch hier stehen. Eine spätere Session kann das gegen das Laborbuch prüfen.
  - "These" ist nicht immer eindeutig. Gegenmittel: Die These wird je Eintrag benannt.

## Version 2 (23.10., ~13:45, Neo: "Gute idee"): zusätzliches Feld Fehlerquelle
Die Kategorien oben bleiben unverändert. Neu ist ein Feld je **vorausschauendem** Eintrag, in einer eigenen Tabelle unten, damit die bisherigen Zeilen unangetastet bleiben. Herleitung: `notizen/32` §10.

| Wert | Bedeutung |
|---|---|
| **Z** Zufall / Ausrutscher | Unaufmerksamkeit, Zählfehler, Tippfehler |
| **I** Informationsmangel | Dem Fehlermacher fehlte eine Tatsache über die Welt (Anbieterverhalten, Daten, Doku) |
| **K** Kontext-Bias | Was der Fehlermacher gerade im Kopf hatte (Hypothese, eigener Plan), hat das Urteil gefärbt |
| **M** Modell-Bias | Blinder Fleck, den auch andere Instanzen desselben Modells oder derselben Familie teilen würden |
| **S** Spezifikationslücke | Regel oder Plan sagt etwas, die Umsetzung tut es nicht |
| **U** unklar | |

- **Kodierung:** Claude trägt eine eigene Einschätzung ein (Spalte "Quelle (Claude)"). **Für die Auswertung zählt nur die blinde Kodierung** durch GPT oder Neo, die Claudes Spalte nicht sieht.
- **Zusätzliche Vorhersage (These aus `notizen/32` §10):** Fehler werden überwiegend von der Plattenart gefunden, die zu ihrer Quelle passt: Z durch Nachprüfen, I durch Messung oder Realität, K durch Verblindung oder kontextfreie Prüfer, M durch andere Familie oder Mensch, S durch Neuimplementierung. **Widerlegt**, wenn bei mindestens 10 blind kodierten Einträgen weniger als die Hälfte von der passenden Plattenart gefunden wurde.

## Einträge

### Rückblickend (23.10., vor Anlage des Protokolls): zählen **nicht** für die Auswertung
Sie stehen hier, damit das Format geübt ist und nichts verloren geht. Rückblickend weiß man schon, wie es ausging, deshalb sind sie für den Test wertlos.

| Wann | Was | Wer | Gefunden durch | Ohne Regel? | Ergebnis verändert? | Richtung (Claude) | Richtung (blind) | Verweis |
|---|---|---|---|---|---|---|---|---|
| 23.10. 05:53 | Morgenzusammenfassung nennt H-037 "belegt" statt "gestützt" | Claude | selbst (neue Session, Abgleich mit Statustabelle) | unklar | ja (an Neo) | pro (H-037) | | Laborbuch 07:05 |
| 23.10. nachts | E-020-Entwurf v2 behält REASONING "low gegen aus", obwohl "aus" nicht existiert | Claude | selbst (neue Session) | unklar | ja (Design) | neutral | | Laborbuch 07:05 |
| 23.10. ~07:40 | Generator v4: Last- und Duplikatzahlen verraten den Fehler ohne Norm | Code/Generator | Regel 17 (Code-Lecktest) | nein | ja | contra (SPEC, H-033) | | Laborbuch 07:26 |
| 23.10. ~07:45 | Lecktest misst einfache statt balancierte Trefferquote | Claude | selbst (Testfehlschlag analysiert) | ja | ja (Test wäre zu lasch gewesen) | neutral | | Laborbuch 07:26 |
| 23.10. ~07:50 | Kodierbogen-Beispiel enthielt echte Werte für Fall 1 (Ankereffekt) | Claude | selbst | ja | ja (Neos Kodierung) | unklar | | Chat |
| 23.10. ~00:55 | Wave-Kodierung: K1 6× "nein" (GPT, Ace 0×), K5 6× "ja" (GPT, Ace 4×) | Claude | anderes Modell (GPT, Ace; D-019) | nein | ja | pro (H-033, Spurtyp) | | `notizen/28…/05-vergleich.md` |
| 23.10. ~08:00 | v4: Rescale-Zeile widerspricht dem Research-Auftrag "only" | Code/Generator | anderes Modell (GPT, Regel 12) | nein | ja | neutral | | `notizen/29` |
| 23.10. ~08:00 | v4: Portal-Auftrag "no attachment", aber Logo angehängt | Code/Generator | anderes Modell (GPT, Regel 12) | nein | ja | neutral | | `notizen/29` |
| 23.10. ~08:00 | v4: "Rechnung ohne PDF" ist Konventionsleck | Code/Generator | anderes Modell (GPT, Regel 17) | nein | ja | contra (SPEC) | | `notizen/29` |
| 23.10. ~08:00 | v4: `low_traffic` auch mit Norm mehrdeutig | Code/Generator | anderes Modell (GPT, Regel 12) | nein | ja | unklar | | `notizen/29` |
| 23.10. 07:26 | Laborbuch-Uhrzeit "~08:00" geschätzt statt gemessen | Claude | selbst | ja | nein | neutral | | Laborbuch |
| 23.10. ~09:00 | Annahme: GPT-Fremdkontrolle mit `effort: high` = gründlich (tatsächlich ~120 Denk-Tokens) | Claude | Neo (Frage nach dem Preis) | nein | unklar | neutral | | `notizen/29` §5 |
| 23.10. ~08:50 | Design-Annahme: `effort: medium` liegt zwischen low und high (tatsächlich = low) | Claude | Regel 10 (Manipulationscheck) | nein | ja (Scheinbestätigung einer Dosis) | pro (H-037) | | E-022 `ergebnis.md` |

Erste Beobachtung (rückblickend, zählt nicht): Von 13 Einträgen hat Claude **5 selbst** gefunden. Alle 5 sind formal oder zeitlich (Status, Uhrzeit, Testmaß, Anker, Design-Rest). **Kein einziger** inhaltlicher Material- oder Deutungsfehler wurde selbst gefunden. Alle inhaltlichen Fehler kamen über Regeln, andere Modelle oder Neo ans Licht. Das deckt sich mit `notizen/25`.

### Vorausschauend (ab 23.10., 09:21): diese zählen
| Wann | Was | Wer | Gefunden durch | Ohne Regel? | Ergebnis verändert? | Richtung (Claude) | Richtung (blind) | Verweis |
|---|---|---|---|---|---|---|---|---|
| 23.10. ~10:50 | `orglab/e022.py` setzt die präregistrierte Regel "unter 16 vollständigen Stapeln nur deskriptiv" nicht um | Claude | anderes Modell (GPT und Gemini, doppelte Buchführung) | nein | nein (24 Stapel), bei Abbruch ja | pro (H-037: lascher als geplant) | unklar (GPT) | E-022 `ergebnis.md`, Nachtrag |
| 23.10. ~11:45 | Vorschlag "sichere Verblindung: Neo würfelt die Zahl" versprach mehr Schutz, als er auf einem gemeinsamen Rechner bietet (die Zahl wäre wieder durch Claudes Hände gegangen) | Claude | Neo ("wofür braucht das einen Menschen?") | nein | ja (Regel-Entwurf) | neutral | **pro** (GPT) | Chat, D-021 |
| 23.10. ~13:15 | Ace-Antwort zu den Monolith-Bruchstellen: Summenzeile ("14 Einträge, I 7, S 6, Z 3, K 2") passt nicht zur eigenen Tabelle (24 Zeilen, I 9, S 4, Z 2, K 1) | Ace | Claude (Nachzählung) | nein | nein (Richtung gleich), ja für Zahlen | neutral | unklar (GPT) | `notizen/33` Nachtrag |
| 23.10. 12:24 (aus `date`) | Laborbuch- und Entscheidungs-Uhrzeiten seit ~11:50 geschätzt statt gemessen, bis zu 2 h zu spät (gegen die Vorlage "aus `date`, nicht schätzen") | Claude | Claude selbst, beim `date`-Aufruf für den Dry-Run | ja | nein (Inhalte), ja (Chronik) | neutral | | Laborbuch-Korrektur |
| 23.10. 12:40 | Präregistrierung E-020 v3 versprach eine Sensitivitätsanalyse ohne Grenzfall 6021, das Skript konnte sie nicht. Der erste Reparaturentwurf hätte den ganzen Seed (12 Belege) entfernt statt einem | Claude | Claude selbst, beim Vermerken der Freigabe vor dem Pilot | ja | nein (vor jedem Lauf behoben) | neutral | | `orglab/e020v3.py`, Test |

### Fehlerquelle je vorausschauendem Eintrag (Version 2)
| Wann | Quelle (Claude) | Quelle (blind) | passende Platte hat gefunden? (nach blinder Kodierung) |
|---|---|---|---|
| 23.10. ~10:50 | S | S (GPT) | ja (Neuimplementierung) |
| 23.10. ~11:45 | I | **K** (GPT) | ja (kontextfreier Mensch) |
| 23.10. ~13:15 | Z | Z (GPT) | ja (Nachzählen) |
| 23.10. 12:24 | Z | | |
| 23.10. 12:40 | S | | |

Blinde Kodierung: `openai/gpt-6.1-sol` (`effort: high`), sah nur Was, Wer, Gefunden durch und den Thesen-Wortlaut (`orglab/protokoll_blind.py`, Rohdaten `daten/protokoll-blind/`). Abweichungen zu Claudes Einschätzung: Beim Verblindungs-Vorschlag hatte Claude "Informationsmangel, neutral" eingeschätzt, GPT kodiert **"Kontext-Bias, pro"**, also die eigene Idee habe die Sicherheitsbewertung gefärbt. Beim Skriptfehler kodiert GPT die Richtung "unklar" statt "pro".
