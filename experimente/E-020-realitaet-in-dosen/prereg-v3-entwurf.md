# E-020 v3 – Entwurf nach D-018 (Generator v4 gebaut)

> **Entwurf, nicht freigegeben.** Die gültige Präregistrierung bleibt `prereg.md`, der Hauptlauf ist weiter **ausgesetzt**. Dieser Entwurf ersetzt `prereg-v2-entwurf.md` dort, wo er etwas anderes sagt. Neo gibt frei, dann wird daraus eine neue `prereg.md`-Fassung mit Datum, und vor dem Pilot wird committet.

**Stand:** 23.10.2026, vormittags. Grundlage: D-018 (Neos fünf Entscheidungen), Grok-Gutachten 1 und 2 (`notizen/23`, `23b`), E-021-Manipulationscheck.

## 1. Was schon erledigt ist

### Material v4 (`orglab/evidence_v4.py`, Tests `tests/test_evidence_v4.py`)
- **7 spec-reine Fehlerarten** als Primärmenge, je Domäne 2–3. Ihre Spur ist nur mit dem Sollwert als Fehler erkennbar:

| Domäne | spec-rein (primär) | Sollwert, der bei SPEC=1 nur im Runbook steht | weiter mitlaufend (sekundär) |
|---|---|---|---|
| coding | `low_traffic` (4–15 % der üblichen Last) · `cache_partial` (nur ein Teil der Shards verbunden, ohne "k/N") | übliche Last (10–10.000 req/min, je Dienst) · Shard-Zahl (3/4/6/8) | `stale_process`, `db_down` |
| business | `wrong_contact` (an echten Vertriebskontakt derselben Firma) · `wrong_terms` (falsches Zahlungsziel; v4.1 ersetzt `attachment_missing`, das ein Konventionsleck hatte) | Rechnungskontakt · Zahlungsziel 14/30/45/60 Tage | `bounced`, `amount_mismatch` |
| research | `weights_misscaled` (Summe ≠ Zielpopulation, ±8–28 %) · `duplicates_partial` (nur 20–50 % der bekannten Duplikate entfernt) · `column_loss` (ohne "/N") | Zielpopulation (0,8–9 Mio.) · Duplikatzahl (15–1.500) · Spaltenzahl (30–80) | `row_loss` |

- **Lecks aus Gutachten 2 entfernt:** keine `0 kB`, `0 pages`, `mean 100`, `requests: 0`, `0/4`, `/47`, keine Häkchen-Regel, die nur Ok-Belege bekommen. Die Normen sind je Vorgang verschieden, damit kein fester Wert lernbar ist.
- **Lecktest im Code** (Regel 17), auf Test-Seeds 9000–9239:
  - verbotene Konventions-Marker in spec-reinen Spuren
  - Normwert taucht in keinem Kanal auf
  - Norm steht im langen Auftrag und im passenden Runbook-Abschnitt, aber nicht im Kurzauftrag
  - **Schwellenregel ohne Norm:** beste balancierte Trefferquote ≤ 0,75. Ergebnis: `low_traffic` 0,71 · `cache_partial` 0,73 · `weights_misscaled` 0,57 · `duplicates_partial` 0,64 · `column_loss` 0,61. Der erste Entwurf lag bei `low_traffic` (0,84) und `duplicates_partial` (0,81) darüber, der Test hat das gefangen.
- **Runbook abschnittsweise** (`evidence_v4.lookup(ev, topic)`): liefert nur passende Abschnitte, dazu harmlose Distraktor-Abschnitte (logging, on-call, dunning, codes …). Ein unbekanntes Topic liefert "No entry for '…'", **keine Themenliste** (Gutachten 2).
- **Fehlerarten balanciert und mit dem Kanal gekreuzt:** Die Fehlerart wird je Seed deterministisch zugewiesen. Mit Kanal = Seed mod 3 kommt jede Kombination Fehlerart × vorgelegter Kanal alle 12 Seeds gleich oft vor (Gutachten 1 Punkt 9, Gutachten 2 "Primärarten nur zufällig").
- **Power:** 24 Seeds ergeben **84 spec-reine kaputte Belege** (7 × 12) statt ~36 (Gutachten 2).
- **v3.1 unverändert:** v4 ist ein eigenes Modul, ein Hash-Test sichert v3.1 für E-021 und E-022.

### Fremdkontrolle und Lecktest per GPT (`orglab/fremdkontrolle.py`, D-018 Punkt 2)
- `python -m orglab.fremdkontrolle E-020v4`: Wahrheitsprüfung. `openai/gpt-6.1-sol`, `effort: high`, je Beleg einzeln, langer Auftrag und alle drei Kanäle. Geschichtet sind es 48 Belege: je Fehlerart 3 kaputte, je Domäne und Ok-Art 2 Ok-Belege. Neo klärt die Abweichungen.
- `python -m orglab.fremdkontrolle E-020v4 --leck`: **Lecktest durch ein Nicht-Claude-Modell.** Nur der Kurzauftrag, kein Runbook, 6 Belege je spec-reiner Fehlerart plus 12 Ok-Belege. **Kriterium (vorab): Höchstens 25 % je Fehlerart werden ohne Sollwert sicher als kaputt erkannt.** Liegt eine Fehlerart darüber, fällt sie aus der Primärmenge, oder der Generator wird nachgebessert und neu getestet.
- **Gelaufen (23.10., `notizen/29`):** v4.0 zeigte 3 Generatorfehler und ein Konventionsleck. **v4.1 besteht: Lecktest 0/42, Fremdkontrolle 47/48** (ein Grenzfall `low_traffic` bei sehr kleiner Last).

## 2. Neue Designentscheidungen (Vorschlag, Neo entscheidet)

| # | Vorschlag | Begründung |
|---|---|---|
| A | **REASONING-Faktor streichen.** Sonnet läuft in allen Zellen ohne `reasoning`-Parameter (adaptiv, die realistische Standardeinstellung), Manipulationscheck: Tokens werden nur berichtet. Damit bleiben 2³ = **8 Zellen**. | "aus" gibt es über OpenRouter nicht (E-021). Die Reasoning-Frage bearbeitet jetzt E-022 sauber, mit gemessener Dosis. Halbe Kosten, ein Konfundierungsrisiko weniger. H-036 fällt aus E-020 heraus, V6 entfällt. |
| B | Frische Seeds **6000–6023** auf Material v4 (statt 3000–3023 auf v3.1) | anderes Material, saubere Trennung |
| C | Primärmetrik: Übersehensrate auf den **84 spec-reinen kaputten Belegen**, Kontrast SPEC=1 − SPEC=0. Alle anderen Fehlerarten sekundär. | Regel 17: nur dort misst SPEC etwas |

## 3. Was am Prüfer-Code noch fehlt (vor dem Pilot, ohne API-Kosten)
1. `orglab/realitaet.py` auf v4 umstellen:
   - `lookup_runbook(topic)` → `evidence_v4.lookup`, und zwar **in beiden SPEC-Stufen** (v2-Entwurf Punkt 2)
   - die drei Anstupser streichen (v2 Punkt 1)
   - REASONING je nach Entscheidung A
2. **Seedweiser Executor:** Ein Seed läuft vollständig durch alle Zellen, bevor der nächste beginnt. Bei Abbruch werden nur vollständige Seeds ausgewertet (Gutachten 2).
3. **Dry-Run aller Zellen** wörtlich als Anhang einfrieren (Regel 16).
4. **Auswerteskript** `orglab/realitaet_auswertung.py`:
   - Primärmenge, Cluster-Bootstrap über Belege
   - vollständige Blöcke, BH-FDR
   - Prävalenz 5 % (PPV, nicht "Fangquote", Gutachten 2)
   - "richtiger Runbook-Abschnitt nachgeschlagen" als deskriptive Größe (V4 bleibt Selbstselektion)
   - V5-Schwelle 0,80
   - mit synthetischen Daten getestet und committet
5. **Externe Kritik (Regel 18):** Der Hauptlauf liegt über 10 $, deshalb liest Grok vorher Präregistrierung und Code (ein Aufruf, sicher konfiguriert nach `grok-cli-safe-usage`).

## 4. Reihenfolge bis zum Hauptlauf
Lecktest (GPT) → ggf. Generator nachbessern → Fremdkontrolle (GPT, Neo klärt Abweichungen) → Code 1–4 → `prereg.md` v3 mit Neos Freigabe committen → Pilot (Technik, Seeds 1300–1301 auf v4) → Grok-Gutachten → Hauptlauf.

## 5. Offene Fragen an Neo
1. Vorschlag A (REASONING streichen): ja oder nein?
2. Dürfen Lecktest und Fremdkontrolle laufen (2–4 $ OpenRouter)?
3. Anstupser-Arm ("do it better" gegen Affordanz): weiter auf dem Parkplatz? Grok schlug einen Nebenarm nur bei SPEC=1 vor.
