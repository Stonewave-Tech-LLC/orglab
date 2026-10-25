# 36 – Zwei Kritiker-Einwände gegen die E-024-Präregistrierung geprüft

- **Datum:** 2026-10-24, 23:08 (aus `date`)
- **Status: EXPLORATIV.** Nachträgliche Analyse auf schon ausgewerteten Daten, keine neue Bestätigung. Sie ändert keine Etiketten in `experimente/E-024-bestaetigung-massstab/ergebnis.md`. Rohdaten, `prereg.md` und `ergebnis.md` sind unverändert.
- **Anlass:** Im Lichttest v1 des research-harness (`research-harness/laeufe/lichttest-v1/auswertung.md`, Abschnitt 3) lief Gemini 4 Argon als Fremdkritiker 52-mal über `prereg.md`. In 18 von 48 Läufen ohne eingeschleusten Fehler meldete er etwas Blockierendes, meist diese zwei Punkte:
  1. Bootstrap über Belege statt über Seed-Cluster (vgl. Regel 13)
  2. ein Widerspruch bei der F1-Primärmenge
- Dass GPT im dritten Prüfer denselben ersten Punkt als "wichtige Sensitivitätsanalyse" vorgeschlagen hat (`notizen/34-dritter-pruefer/gpt/bericht_gpt.md`, Z. 402), ist hier mit erledigt.
- **Skript und Ausgabe:** `notizen/36-kritiker-einwaende-e024/seed_cluster.py` und `ausgabe.txt`
  - Reproduktion: `PYTHONPATH=. .venv/Scripts/python notizen/36-kritiker-einwaende-e024/seed_cluster.py`
  - Laufzeit etwa 2 s

## Kurz
1. **Seed-Cluster:** Mit Cluster-Bootstrap über die 21 vollständigen Seeds bleiben **alle fünf Etiketten gleich** (5 × BESTÄTIGT, alle q < 0,001). Die Intervalle werden **schmaler**, nicht breiter (60–90 % der Breite).
   - Die Belege eines Seeds hängen nicht positiv zusammen. Die ICCs der Je-Beleg-Kontraste sind alle negativ (−0,05 bis −0,12).
   - Grund ist das Design: Jeder Seed enthält jede Kombination Domäne × Art genau einmal, und die Fehlerart wird durch den Seed reihum zugeteilt. Ein Seed ist deshalb eine kleine ausgewogene Schicht.
   - Der präregistrierte Bootstrap über Belege ignoriert diese Ausgewogenheit und ist damit der **vorsichtigere** der beiden.
   - **Der Einwand trifft formal zu, ändert aber nichts.** Die Richtung ist umgekehrt zu der, die der Kritiker befürchtet.
2. **F1-Widerspruch:** Im Wortlaut gibt es ihn wirklich, er ist aber ein Überbleibsel aus dem Entwurf.
   - Der allgemeine Satz "**Primär:** alle Belege" stammt aus dem Entwurf von 18:59. Damals galt F1 noch auf allen Ok-Belegen. Bei der F1-Einschränkung um 19:28 (Commit 50c9698) wurde er nicht angepasst.
   - Vier spätere, F1-spezifische Stellen legen F1 eindeutig auf die einzeln entscheidbaren Ok-Belege fest.
   - Beide Fremd-Nachrechnungen (GPT, Gemini) haben die Stelle so gelesen. GPT hat das ausdrücklich als Auslegung vermerkt.
   - Die Etiketten hängen nicht daran. F1 auf allen Ok-Belegen ergäbe ebenfalls BESTÄTIGT, mit Belege- wie mit Seed-Bootstrap.

## 1. Seed-Cluster-Bootstrap

### Vorgehen
- Die Je-Beleg-Kontraste kommen unverändert aus `orglab.e024.contrasts` (W1 gepaart je Beleg wie in `evaluate`). Getauscht wird **nur die Resampling-Einheit**.
- Ganze Seeds werden mit Zurücklegen gezogen, alle Belege des Seeds kommen mit. Das Mittel wird über die gepoolten Belege gebildet, damit jeder Beleg gleich gewichtet bleibt wie präregistriert.
- B = 5.000, Startwerte 241–245 (KI) und 251–255 (p), Perzentil-Indizes wie präregistriert. BH über die fünf, Etiketten über `e024.label`.
- 21 Seeds. 7010, 7015 und 7016 fallen wie im Primärlauf heraus.
- **ICC(1):** einfaktorielle ANOVA mit Seed als Gruppe, ungleiche Gruppengrößen über n₀. Zusätzlich die ICC der Reste nach Abzug des Mittels je Domäne × Art × Fehlerart × vorgelegtem Kanal. Sie zeigt, was nach der vom Seed bestimmten Zusammensetzung noch am Seed hängt.
- **Empirischer Designeffekt:** (SE Seed-Bootstrap / SE Belege-Bootstrap)², aus eigenen Ziehungen.

### Ergebnis (Haiku, primäre Mengen)

| Nr | n Belege (Seeds) | Mittel | KI Belege (prereg) | KI Seed-Cluster | Breite Cluster / Belege | Etikett Belege | Etikett Cluster |
|---|---|---|---|---|---|---|---|
| V1 | 76 (21) | +0,263 | [+0,207; +0,322] | [+0,213; +0,299] | 0,75 | BESTÄTIGT | BESTÄTIGT |
| W1 | 76 (21) | +0,260 | [+0,204; +0,316] | [+0,211; +0,294] | 0,75 | BESTÄTIGT | BESTÄTIGT |
| C1 | 252 (21) | +0,472 | [+0,417; +0,530] | [+0,437; +0,504] | 0,60 | BESTÄTIGT | BESTÄTIGT |
| C2 | 76 (21) | +0,408 | [+0,309; +0,513] | [+0,314; +0,479] | 0,81 | BESTÄTIGT | BESTÄTIGT |
| F1 | 87 (21) | +0,029 | [+0,014; +0,046] | [+0,015; +0,043] | 0,90 | BESTÄTIGT | BESTÄTIGT |

- Alle q < 0,001, mit beiden Einheiten. Etikett jeweils "Vorhersagewert nicht ausgeschlossen".
- **Sekundär (ohne die 62 einzeln nicht entscheidbaren Belege):** gleiches Bild. Etiketten gleich, Breite 0,60–0,90.
- **F1 deskriptiv auf allen 126 Ok-Belegen:** +0,046, Belege [+0,030; +0,063], Seed-Cluster [+0,028; +0,063], Breite 1,06.

### Zusammenhang innerhalb eines Seeds

| Nr | Belege je Seed (Mittel) | ICC(1) roh | ICC(1) der Reste | Designeffekt |
|---|---|---|---|---|
| V1 | 3,6 | −0,08 | −0,02 | 0,59 |
| W1 | 3,6 | −0,08 | −0,06 | 0,57 |
| C1 | 12,0 | −0,06 | −0,02 | 0,38 |
| C2 | 3,6 | −0,12 | −0,24 | 0,62 |
| F1 | 4,1 | −0,09 | +0,06 | 0,72 |
| F1 (alle Ok) | 6,0 | −0,00 | +0,07 | 0,96 |

### Warum die ICC negativ ist (Erklärung, gestützt durch Code und Gegenrechnung)
- **Der Seed bestimmt die Zusammensetzung, nicht den Inhalt.**
  - Jeder Beleg hat einen eigenen Zufallsstrom (`evidence_v4.generate`: `Random(f"evidence-v4:{domain}:{kind}:{seed}")`).
  - Am Seed hängen nur die Fehlerart (`fault_for`: `(seed + Versatz) % 4`) und der bei ZUGANG = 0 vorgelegte Kanal (`e020v3.presented_channel`: `seed % 3`).
- Jeder Seed enthält alle 12 Kombinationen Domäne × Art. Die Kontraste hängen stark an der Domäne, etwa C1: research ≈ 0, coding und business ≈ 0,5–0,9. Deshalb schwanken Seed-Mittel weniger, als zufällig gezogene Belege es täten.
- **Gegenrechnung:** Ein nach Domäne × Art geschichteter Belege-Bootstrap ist ebenfalls schmaler als der präregistrierte (SE V1 0,014, C1 0,021, C2 0,033, F1 0,008 gegen 0,029 / 0,029 / 0,052 / 0,009).
  - Die präregistrierte Wahl ist also gegenüber beiden Alternativen konservativ.
  - Skript nur im Scratchpad, die Zahlen stehen hier.
- **Spec-reine Belege je Seed sind sehr ungleich verteilt:** 10 Seeds mit 1 Beleg, 11 Seeds mit 6, je nach Seed-Parität. Das Verhältnis-Mittel im Cluster-Bootstrap gleicht das aus.

### Grenzen dieser Prüfung
- 21 Cluster sind wenige. ICC-Schätzungen auf 3–12 Belegen je Seed sind unsicher, und Perzentil-Intervalle mit wenigen Clustern sind eher zu schmal.
  - Das ändert die Aussage nicht: Selbst ein Designeffekt von 1 ließe alle Untergrenzen über 0.
- Die einzige leicht positive Rest-ICC hat F1 (+0,06). Als grobe Überschlagsrechnung mit Designeffekt 1 + (4,1 − 1) · 0,064 ≈ 1,2 läge die SE um etwa 10 % höher und die Untergrenze bei etwa +0,011, also noch über 0.
  - Das ist ein Hinweis, keine gerechnete Analyse.
- **Nicht geprüft:** Abhängigkeit über die Laufzeit. Die Warteschlange lief seedweise, Urteile eines Seeds fielen also zeitlich zusammen (API-Zustand). Die negativen ICCs sprechen nicht für einen solchen Effekt, schließen ihn aber nicht aus.
- **Einordnung zu Regel 13:** Sie verlangt Cluster-Bootstrap, wo Messungen zusammenhängen ("derselbe Beleg in mehreren Kanälen, Urteile im selben Stapel"). Die 8 Zellen und 2 Modelle je Beleg hängen zusammen und werden bereits gemeinsam gezogen.
  - Die Belege eines Seeds teilen keine Inhalte, nur die reihum vergebene Zusammensetzung.
  - Ob Seeds eine Cluster-Einheit im Sinne von Regel 13 sind, ist Auslegung. Empirisch spielt es hier keine Rolle.

## 2. F1-Primärmenge: Widerspruch in `prereg.md`?

### Die beiden Stellen
- **Allgemein**, Auswertungsplan (`prereg.md`, Z. 134):
  > "**Primär:** alle Belege. **Sekundär (vorab festgelegt):** ohne die einzeln nicht entscheidbaren Belege laut `einzelkanal-ausschluss.json`."
- **F1-spezifisch**, Vorhersagetabelle (Z. 42):
  > "Fehlalarm AUSKUNFT 1 − 0, **nur Ok-Belege, die auch mit einem Kanal entscheidbar sind** (101 von 144, laut `einzelkanal-ausschluss.json`)"
- **F1-spezifisch**, Entscheidungen nach der Materialprüfung, Punkt 2 (Z. 97):
  > "F1 nur auf einzeln entscheidbaren Ok-Belegen. … F1 auf allen Ok-Belegen (wie in E-023) wird nur deskriptiv berichtet."
- Dazu Z. 59 (Teststärke): "F1 auf den 101 einzeln entscheidbaren Ok-Belegen (**endgültige Definition**)".
- Und Z. 110 (nach Grok-Gutachten 5): "Fehlt `einzelkanal-ausschluss.json`, bricht die Auswertung ab, statt F1 still über alle Ok-Belege zu rechnen."

### Befund
- **Wörtlich gelesen widerspricht sich die Präregistrierung.** Z. 134 sagt ohne Ausnahme "Primär: alle Belege", die F1-Stellen sagen "primär nur die einzeln entscheidbaren". Der Kritiker liest richtig, dass die Datei hier nicht in sich geschlossen ist.
- **Herkunft laut Git:**
  - Z. 134 steht schon im Entwurf 2cd76b6 (23.10., 18:59). Dort lautet F1 noch "Ok-Belege" ohne Einschränkung, der Satz war also stimmig.
  - Die F1-Einschränkung kam in 50c9698 (19:28) hinzu, Z. 134 blieb unverändert.
  - Beides lag vor dem Hauptlauf vor, eingefroren in d3f6d31 (19:41).
- **Auslegung:** Die spezifischen und späteren Stellen gehen der allgemeinen vor. Z. 134 meint für V1, W1, C1 und C2: Der Einzelkanal-Ausschluss ist dort nur sekundär.
  - Das Skript setzt genau das um (`e024.contrasts`, `f1_exclude`).
  - GPT hat dieselbe Auslegung aus der Präregistrierung allein gewählt und als Entscheidung vermerkt: "The latest pre-start amendments control: F1 uses only non-excluded true items" (`daten/E-024-bestaetigung-massstab/nachrechnung/gpt-6.1-sol-ergebnis.json`).
  - Gemini kam ohne Vermerk auf dieselbe Menge (F1 = +0,029, n = 87).
- **Folge für das Ergebnis: keine.** F1 auf allen Ok-Belegen ist +0,046 [+0,030; +0,063] und wäre ebenfalls BESTÄTIGT, mit Seed-Cluster [+0,028; +0,063] auch.
  - Ein Forscher-Freiheitsgrad, der das Etikett bewegt, liegt also nicht vor.
  - Die Wahl der eingeschränkten Menge ist zudem die strengere: kleinerer Effekt, weniger Power.
- **Nebenbefund:** Für F1 ist die Sekundäranalyse "ohne die 62" identisch mit der Primäranalyse, denn F1 schließt sie ja schon aus. In `ergebnis.md` sieht das wie eine zweite Prüfung aus, ist aber keine.

## Braucht `ergebnis.md` einen Nachtrag? (Neo hat am 24.10. zugestimmt, angehängt um 23:32)
- **Inhaltlich nötig ist keiner.** Kein Etikett und kein Status ändert sich.
- **Sinnvoll wäre ein kurzer Nachtrag**, aus drei Gründen:
  1. Der Checklistenpunkt "Kritiker hat versucht, den Befund zu brechen" bekommt einen echten Versuch auf den Ergebnisdaten.
  2. Die Formulierungslücke in `prereg.md` Z. 134 wird offen benannt, statt nur hier zu stehen. `prereg.md` selbst bleibt unverändert.
  3. Der F1-Nebenbefund (Sekundär = Primär) wird klargestellt.
- **Möglicher Wortlaut:**
  > **Nachtrag 24.10.2026: Kritiker-Einwände aus dem Lichttest geprüft (`notizen/36`, explorativ).**
  > - Cluster-Bootstrap über die 21 Seeds statt über Belege: alle fünf Etiketten unverändert, Intervalle schmaler (60–90 %), ICC innerhalb der Seeds negativ, weil jeder Seed eine ausgewogene Schicht Domäne × Art ist. Der präregistrierte Bootstrap über Belege ist der vorsichtigere.
  > - `prereg.md` Z. 134 ("Primär: alle Belege") ist ein Überbleibsel aus dem Entwurf vor der F1-Einschränkung. Gemeint und umgesetzt ist F1 auf den einzeln entscheidbaren Ok-Belegen (Z. 42, 59, 97, 110), von beiden Nachrechnungen so gelesen. F1 auf allen Ok-Belegen wäre ebenfalls bestätigt. Für F1 ist die Sekundäranalyse "ohne die 62" mit der primären identisch.
- **Für den research-harness (Hinweis):** Beide Einwände sind berechtigt formuliert, aber nicht blockierend. Ein Kritiker, der sie in 18 von 48 sauberen Läufen als blockierend meldet, ist auf dieser Präregistrierung zu streng kalibriert.
  - Besser wäre die Frage "Ändert sich ein Etikett?" statt "Ist das formal sauber?". Das gehört in die Lichttest-Auswertung, nicht hierher.
