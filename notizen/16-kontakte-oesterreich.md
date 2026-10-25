# Mögliche Ansprechpersonen in Österreich (Recherche 21./22.10.2026)

Die Angaben stammen aus öffentlichen Uni- und Institutsseiten bzw. Suchergebnissen. **Vor einer Anfrage jeweils die aktuelle Teamseite prüfen.** Die Sicherheit der Zuordnung ist pro Eintrag angegeben.

## JKU Linz
| Person / Gruppe | Thema | Passung | Sicherheit |
|---|---|---|---|
| **Werner Zellinger**, Robust AI (LIT AI Lab / Institute for Machine Learning) | Verlässlichkeit unter Verteilungsverschiebung, **Konfidenzmaße** für das Verhalten lernender Systeme. Eine (inzwischen offline) Stellenausschreibung der Gruppe nannte "agentic AI: agent harnesses, memory, tool use, LLM-based agents". | hoch, falls der Agentic-Schwerpunkt stimmt. Kalibrierung und Verifikation passen auf jeden Fall | Leitung laut Teamseite bestätigt; Agentic-Schwerpunkt **unbestätigt** |
| **Bernhard Aichernig**, Institut für Formale Modelle und Verifikation (FMV) | vertrauenswürdige Systeme, lernbasiertes Testen, Falsifikation | hoch für Methodik, Verifikation und das Testbed als Prüfstand | gut (Profilseiten, Antrittsvorlesung) |
| **Sepp Hochreiter**, Leitung Institute for ML / LIT AI Lab | Deep Learning, LLM-Alternativen | indirekt. Prominent und schwer erreichbar, besser über die Gruppenleitungen | gut |
| **LIT Robopsychology Lab** (Projekt "DEMYSTIFY AI") | Mensch-KI-Interaktion, Vertrauen in KI | passt zu Leitfrage 3 und zur menschlichen Aufsicht | Lab bestätigt, **Leitung zu prüfen** |
| **Alois Ferscha**, Institut für Pervasive Computing | Koordinationsarchitekturen, sozio-technische Systeme | mittel | gut |

## Außeruniversitär (für den Innovationsscheck zulässig, industrienah)
| Einrichtung | Thema | Passung |
|---|---|---|
| **SCCH Hagenberg** + **Trustifai** (Joint Venture mit TÜV Austria, "AI testing and qualification hub") | Qualität und Prüfung von KI-Systemen, vertrauenswürdige KI | hoch für den praktischen Weg. Ein Verifier-Benchmark ist im Kern ein Prüfverfahren |

## Andere österreichische Unis
| Person | Thema | Passung |
|---|---|---|
| **Bettina Könighofer**, TU Graz | Shielding, Durchsetzung von Sicherheitseigenschaften zur Laufzeit für autonome Agenten | hoch für "Regeln, die durchgesetzt statt nur behauptet werden" (Frist/Veto, AAP) |
| **Krishnendu Chatterjee**, ISTA | Spieltheorie, quantitative Verifikation | Theorie zu BFT- und Governance-Befunden. Eher Grundlagen |
| **Tatjana Chavdarova**, TU Wien (ML Unit) | Multi-Player AI, Multi-Agent-RL, "socially conscious agents" | passt zu Leitfrage 2 (einfache Lerner statt LLMs). Aktualität ungeprüft |

## International (Autoren unserer Bezugsarbeiten)
- MAST (Berkeley)
- Dochkina
- Goel et al. ("Great Models Think Alike")
- METR (Analyse Hugging-Face-Incident)

## FFG Innovationsscheck mit Selbstbehalt (2026, laut FFG-Seiten)
- **Förderhöhe:** bis 10.000 €, max. 80 %. Für die volle Förderung braucht es 12.500 € Projektkosten, also 2.500 € Eigenanteil.
- **Wer und was:** KMU mit Sitz in Österreich, einmal pro 12 Monate, Einreichung jederzeit. Partner können Unis, FHs oder außeruniversitäre Forschungseinrichtungen sein.
- **Passende Leistungen:** forschungsbasierte Ideenstudien, Vorarbeiten für F&E-Projekte, Prototypen.
- **Quelle:** ffg.at/ausschreibung/innovationsscheck-mit-selbstbehalt-2026 (vor dem Antrag die aktuellen Richtlinien prüfen)

## Denkweise und wahrscheinliche Fragen an uns (aus öffentlichen Arbeiten, 22.10.)
| Person | Kernfrage ihrer Forschung | Bezug zu uns | Wahrscheinliche Frage an uns |
|---|---|---|---|
| **Zellinger** | Funktioniert ein Modell noch, wenn sich die Welt verschiebt, und wie stellt man es ohne Zielwahrheit ein? (Domain Adaptation; ICLR 2023 Top-5 % zur Parameterwahl ohne Ziel-Labels) | Holdout-Domänen, Verbessern ohne Verifier (Harness²) | "Halten eure Befunde bei anderem Szenario oder Modell?" |
| **Aichernig** | Falsifikation statt Beweis: aus Beobachtung Modelle von Black-Box-Systemen lernen und daraus Tests ableiten (lernbasiertes Testen) | Agenten-Teams als Black Boxes; unsere Haltung "Befunde brechen wollen" | "Was ist eure Spezifikation, was heißt 'funktioniert' formal?" |
| **Könighofer** | Shields: nur eingreifen, wenn eine kritische Eigenschaft verletzt würde, dann mit Garantie | minimale Regeln, Frist/Veto, AAP-Verifier als Shield | "Welche Eigenschaft garantiert ihr, und ist sie formal fassbar?" |
| **Mara** | Wann und warum vertrauen Menschen Maschinen (Vorhersagbarkeit → Kontrollgefühl), partizipative Studien, "AI Forest" | Spiegel-Frage; **Lücke:** Wirkung niedriger Audit-Raten auf das Vertrauen des Menschen (Automation Complacency) | "Was macht euer System mit dem Menschen, der es beaufsichtigt?" |
| **SCCH/Trustifai (Nessler)** | statistisch valides Testen von ML für Zertifizierung (EU AI Act); seit 2020 Kooperation mit dem JKU-ML-Institut | A/A, Positivkontrolle, Teststärke = unsere Methodik | "Könnt ihr eine Fehlerrate < X für ein Agenten-Setup nachweisen?" (Produktidee) |

**Empfehlung:** Zuerst Mara (Neos Menschenkenntnis als Beitrag) und SCCH/Trustifai (industrienah, Innovationsscheck). Danach Aichernig und Könighofer als technische Kritiker.
