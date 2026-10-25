# Analyseplan (dritter Prüfer)

Stand: 23.10.2026, geschrieben **vor** der Auswertung der Ergebnisse.

## Was ich vor dem Schreiben gesehen habe (Offenlegung)

Bevor ich diesen Plan geschrieben habe, habe ich nur die Struktur der Daten geprüft:
- Feldnamen, Zahl der Zeilen (je Modell und Seed-Satz 288 Belege × 8 Zellen = 2304), keine Dubletten.
- Verteilung der Belegtypen (Domäne × Art × Fehlerart × Subtilität) in beiden Seed-Sätzen.
- Der vorgelegte Kanal (`presented`) ist je Beleg fest, also in allen ZU-0-Zellen gleich und für beide Modelle gleich.
- Fehlende Urteile: 1 bei Haiku 6000, 8 im Satz 7000. 6 davon betreffen denselben Beleg (`business-fail_moderate-7016`, Timeouts).
- `n_tool_calls` reicht von 0 bis 6, nur 2 Läufe erreichen 6.
- Nebenbei die Randverteilung der GPT-Datei gesehen: `decidable` 229 ja / 59 nein, GPT-Urteil 185 × „kaputt“ / 103 × „funktioniert“ bei 144/144 Wahrheit. Das ist schon ein Ergebnis; ich habe es nicht weiter aufgeschlüsselt.

Keine Trefferquoten der Prüfer, keine Effekte angesehen.

## Grundentscheidungen

- **Einheit:** Beleg (`id`) innerhalb eines Seed-Satzes. Ein Beleg kommt je Modell in 8 Zellen vor, also sind die 8 Urteile nicht unabhängig.
- **Unsicherheit:** Cluster-Bootstrap über Belege (2000 Ziehungen, Perzentil-Intervalle, 95 %). Wird ein Beleg gezogen, kommen alle seine Zellen und beide Modelle mit (gepaarte Vergleiche). Ziehung geschichtet nach Belegtyp `kind` × `domain`, damit das ausgewogene Design erhalten bleibt.
- **Datensätze:** 6000 und 7000 werden **getrennt** ausgewertet und dann verglichen. Ein Befund, der in beiden auftaucht, zählt als repliziert. Gepoolte Zahlen gebe ich zusätzlich an.
- **Zielgröße:** `correct = (verdict == truth)`. Zusätzlich getrennt: Sensitivität (kaputt erkannt, `truth = false`) und Spezifität (intakt bestätigt, `truth = true`) sowie die Neigung zu „funktioniert“ (P(verdict = true)).
- **Fehlende Urteile:** Primär als falsch gezählt (ein Prüfer, der kein Urteil liefert, hat nicht geprüft). Gegenprobe: als fehlend ausgeschlossen.
- **Skala:** Effekte in Prozentpunkten **und** als Log-Odds-Verhältnis (Logit). Aussagen über Wechselwirkungen (Bedingung × Modell, Bedingung × Schwierigkeit) mache ich **auf der Logit-Skala**. Ein konstanter Logit-Effekt erzeugt in Prozent automatisch das Muster „größte Wirkung bei p ≈ 0,5“; das allein werte ich nicht als echte Abhängigkeit. Bei Anteilen von 0 oder 1 nutze ich die Korrektur +0,5 (Haldane), und ich sage dazu, wenn ein Logit-Wert nur von dieser Korrektur lebt (Decke).

## Frage 1: Vorgehen der Modelle

Je Modell, je Seed-Satz:
- Trefferquote, Sensitivität, Spezifität, P(„funktioniert“).
- Konfidenz: Mittel bei richtigen gegen falsche Urteile, Brier-Score, AUROC der Konfidenz für Richtigkeit, Überkonfidenz (mittlere Konfidenz − Trefferquote).
- Nachschlagen: Anteil `looked_up`, `right_section`, Zahl der Themen.
- Kanäle (nur ZU = 1): `n_checks`, `distinct_checks`, Anteil mit allen 3 Kanälen, Anteil mit 0 Kanälen.
- Aufwand: `n_tool_calls`, `completion_tokens`, `cost_usd`.
- Modellunterschied gepaart je Beleg, Bootstrap.

## Frage 2: Wirkung von SP, ZU, AU

- Haupteffekt je Faktor und Modell: Der Plan ist vollständig gekreuzt, also für jeden Beleg Mittel der 4 Zellen mit Stufe 1 minus Mittel der 4 Zellen mit Stufe 0. Dazu Logit-Version (log OR aus den aggregierten Anteilen).
- Zweifach-Wechselwirkungen SP×ZU, SP×AU, ZU×AU je Modell (Logit und pp).
- Modell × Faktor: Differenz der Logit-Effekte zwischen Modellen, Bootstrap.
- Wirkung auf Vorgehen: Wie verändern SP/ZU/AU Nachschlagen, `right_section`, `n_checks`, Konfidenz?
- Moderatoren: Effekt getrennt nach Wahrheit/Art (`kind`), Domäne, `primary`, Subtilität, Fehlerart. **Geplante Hypothesen:**
  - H-SP: SP = 1 schadet vor allem bei `primary = true` (Sollwert nötig) und wirkt über das Nachschlagen. Prüfung: SP-Effekt bei primary gegen nicht-primary; SP-Effekt getrennt nach `right_section`.
  - H-ZU: ZU = 1 hilft bei kaputten Belegen, weil mehr Kanäle zugänglich sind, sofern der Prüfer sie abruft.
  - H-AU: AU = 1 schiebt Urteile Richtung „funktioniert“: Sensitivität sinkt, Spezifität steigt oder bleibt.
- Fehlerart-Aufschlüsselung (12 Fehlerarten × 2 Modelle × 3 Faktoren) gilt als **explorativ**; da sind viele Vergleiche, ich nenne nur, was in beiden Seed-Sätzen in dieselbe Richtung geht.

## Frage 3: Schwierigkeit ohne Zirkelschluss

Schwierigkeit = Fehlerquote eines Belegs bzw. Belegtyps, Logit-Skala.

Schätzer, alle so gebaut, dass die Schwierigkeit nicht aus denselben Urteilen kommt wie der Effekt:
- **S1 extern, vorab festgelegt:** Art (`kind`) und Subtilität aus dem Generator. Keine Antwortdaten.
- **S2 Kreuzanpassung über Seed-Sätze:** Belegtyp = Domäne × Art × Fehlerart (bei intakten Belegen Domäne × Art). Schwierigkeit des Typs aus Satz 6000, Effekt in Satz 7000 gemessen, und umgekehrt. Das ist die Hauptanalyse, weil die Seeds getrennte Datensätze sind.
- **S3 anderes Modell:** Schwierigkeit eines Belegs für Sonnet aus den Haiku-Urteilen (und umgekehrt), im selben Satz. Unabhängiges Rauschen, aber andere „Person“.
- **S4 Kreuzanpassung über Zellen:** Für den Effekt von Faktor F wird die Schwierigkeit aus den Zellen mit G = g (anderer Faktor, beide Stufen von F symmetrisch) geschätzt und der Effekt in den Zellen mit G = 1 − g gemessen; dann Rollen tauschen.
- **Zum Vergleich absichtlich zirkulär:** Schwierigkeit aus der Basisstufe (F = 0) desselben Modells, Effekt F1 − F0. Das soll zeigen, wie groß der Scheineffekt ist.
- **Nullsimulation:** Parametrischer Bootstrap aus einem Modell ohne Wechselwirkung (Beleg-Wahrscheinlichkeit je Modell plus konstanter Logit-Effekt je Faktor). Darauf laufen dieselben Analysen. So sehe ich, welches Muster die Analyse mechanisch erzeugt.

Wechselwirkung Effekt × Schwierigkeit: Steigung δ des Logit-Effekts gegen die (unabhängige) Schwierigkeit, bzw. Effekt in Terzilen der Schwierigkeit, verglichen mit der Nullsimulation.

Ähnlichkeit zwischen Modellen: Korrelation der Typ-Schwierigkeiten (Spearman und Pearson auf Logit) zwischen Sonnet und Haiku, je Satz und kreuzweise über die Sätze. Die Reliabilität jeder Schwierigkeitsschätzung bestimme ich über die Replikation 6000 ↔ 7000 desselben Modells; damit korrigiere ich die Korrelation zwischen Modellen für Messfehler (Attenuation).

## Frage 4: Fehlerkorrelation

Auf Ebene Beleg × Zelle (beide Modelle sahen exakt denselben Beleg in derselben Bedingung):
- Beobachtete gemeinsame Fehlerquote gegen erwartete bei Unabhängigkeit (Double-Fault-Verhältnis).
- Cohens κ der Richtigkeit (Fehlerkonsistenz nach Geirhos), korrigiert für die unterschiedlichen Fehlerraten.
- **Geschichtet:** κ bzw. Double-Fault innerhalb von Belegtyp × Zelle (erwartete Übereinstimmung je Schicht). Das trennt „beide scheitern, weil der Typ schwer ist“ von „beide scheitern am selben Einzelbeleg darüber hinaus“.
- **Referenz:** Übereinstimmung desselben Modells mit sich selbst zwischen AU = 0 und AU = 1 (sonst gleiche Zelle). Das ist keine echte Wiederholung, gibt aber eine grobe Obergrenze, wie konsistent ein Modell mit sich selbst ist.
- Alles mit Bootstrap über Belege. Nur Satz 7000 hat beide Modelle im selben Lauf; 6000 dient als Replikation mit zeitlich getrennten Läufen.

## Frage 5: Einzelkanal (nur Satz 7000)

- Trefferquote bei ZU = 0 je Modell, getrennt nach GPT `decidable` ja/nein, primär in SP = 0 (GPT hatte auch die Sollwerte), dann SP = 1.
- ZU-Effekt (ZU1 − ZU0) getrennt nach `decidable`. Hypothese: Bei nicht entscheidbaren Belegen schadet ZU = 0 mehr bzw. hilft ZU = 1 mehr.
- Zusätzlich GPT-Richtigkeit und vorgelegter Kanal als Schichtung. Vorbehalt: `decidable` ist ein Urteil eines anderen LLM in einem Lauf, keine Wahrheit.

## Frage 6: Gegenproben

- Drift/Lauf-Effekt: Satz 6000 lief Haiku später als Sonnet; Satz 7000 im selben Lauf. Ist der Modellunterschied in beiden Sätzen gleich?
- Decke/Boden und Skala: Wo liegen die Anteile? Logit-Ergebnisse gegenüber pp-Ergebnissen.
- Regression zur Mitte: zirkuläre gegen nicht zirkuläre Schwierigkeit, Nullsimulation.
- Fehlende Urteile, Werkzeugrunden-Kappung.
- Verwechslung von Fehlerart mit Domäne/primary (Research hat 3 von 4 primary-Fehlerarten).
- Viele Vergleiche: explorative Befunde nur, wenn in beiden Sätzen gleichgerichtet.
- Vorgelegter Kanal als Störgröße bei ZU.

## Welche Ergebnisse welche Lesart stützen würden

| Lesart | stützend | dagegen |
|---|---|---|
| **Gemeinsame Schwierigkeitsskala** (Belege sind für beide Modelle aus denselben Gründen schwer) | hohe, attenuationskorrigierte Korrelation der Typ-Schwierigkeit zwischen Modellen; geschichtetes κ ≈ 0 | niedrige Korrelation trotz hoher Reliabilität; Rangvertauschungen bei Typen |
| **Gemeinsame Fehler über Schwierigkeit hinaus** | geschichtetes κ > 0 mit Intervall über 0 in beiden Sätzen | geschichtetes κ ≈ 0, nur ungeschichtetes κ > 0 |
| **Wirkung hängt an der Grenznähe** | Logit-Steigung δ ≠ 0 mit unabhängiger Schwierigkeit, in beiden Sätzen, außerhalb der Nullverteilung | nur der zirkuläre Schätzer zeigt das Muster; Logit-Effekt konstant, nur pp variiert |
| **SP wirkt über fehlende Sollwerte** | SP-Schaden konzentriert auf primary; mit `right_section` kleiner | SP-Schaden gleich bei nicht-primary |
| **AU = Gefälligkeit** | mehr „funktioniert“-Urteile, Sensitivität sinkt | keine Verschiebung |
| **ZU wirkt über Information** | ZU-Nutzen bei nicht entscheidbaren Belegen größer; abhängig von `distinct_checks` | ZU-Nutzen unabhängig von Entscheidbarkeit |
| **Modellunterschied = Lauf-/Drift-Effekt** | Modellabstand in 6000 deutlich anders als in 7000 | gleicher Abstand in beiden Sätzen |

Alles, was nicht in diesem Plan steht, kennzeichne ich im Bericht als **explorativ**.
