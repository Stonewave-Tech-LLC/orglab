# Leitfragen 2 und 3 (Neo, mit Claude und Gemini, 21.10. abends)

Leitfrage 1 ist "Vertrauen skalieren", siehe `notizen/14`.

## Leitfrage 2: Ist "Gesellschaft" ein Naturgesetz komplexer Informationsnetze?
*Entsteht Kooperation, Hierarchie und Regelbildung zwangsläufig, sobald man genug Intelligenz zusammenbringt?*

**Was unsere Daten sagen (Entdeckung, ein Modell):**
- Kontrolle entsteht **funktional und dosisabhängig**. Mehr Saboteure führen zu mehr Fremdprüfung, Eskalation und Umverteilung (E-007).
- Rollen differenzieren sich nach Knappheit (Prüfer unter Zeitdruck, E-003).
- Formale Regelsetzung ("RULE:/ENDORSE:") entsteht dagegen **nicht** spontan (E-001), und angebotene Mechanismen werden sofort genutzt (E-008).
- Das sieht eher nach *Anpassung an Bedarf* aus als nach *Ritual*.

**Die große Konfundierung (Teil 2 §2, "Erfinden oder Erinnern"):** LLMs sind auf menschlichen Texten trainiert und per RLHF auf Ehrlichkeit und Hilfsbereitschaft getrimmt. Dass sie Bürokratie, Eskalation und Geständnisse zeigen, kann heißen, dass das die logische Lösung ist. Es kann aber genauso heißen, dass sie es aus unseren Texten kennen. **Mit LLMs allein ist das nicht zu trennen.**

**Wie man es trennen könnte:**
1. **Agenten ohne menschliche Vorprägung:** einfache lernende Agenten (RL, evolutionäre Policies) in derselben Welt. Entwickeln *die* auch dosisabhängige Kontrolle, ist sie strukturell. Zeigen nur LLMs sie, ist sie geerbt.
2. **Fremdartige Umwelten,** in denen menschliche Strukturen nachweislich schlecht sind (Teil 2 §2). Bauen LLMs dort trotzdem Hierarchie und Bürokratie, ist es Erinnerung.
3. **Vergleich über Modellfamilien:** Was alle Familien gleich tun, ist eher Struktur oder gemeinsame Daten. Was sich unterscheidet, ist Training. Das braucht API-Keys.

**Teilbare Hypothese H-027:** Dosisabhängige Kontrolle (Prüfen und Umverteilen proportional zum Misstrauen) entsteht auch bei Agenten ohne Sprachvortraining, wenn sie aus Erfahrung lernen. Sie ist dann eine strukturelle Lösung und kein kulturelles Erbe. Testbar mit Baustein "einfache Lerner" (neu, mittlerer Aufwand).

## Leitfrage 3: Was lernen wir über uns selbst?
*Wie nah ist die Logik von Sprachmodellen an unserer sozialen Programmierung?*

**Vorsicht vor dem "Beschleuniger menschlichen Verhaltens":** LLMs spiegeln nicht den *Durchschnitt* menschlichen Verhaltens, sondern **unsere Texte plus unsere Trainingsziele**. Die Ehrlichkeit der Maulwürfe (E-006) ist sehr wahrscheinlich ein Produkt von RLHF, also ein Spiegel dessen, was Menschen von einer KI *wollen*. Es ist kein Spiegel dessen, was Menschen *tun*.

**Wo der Spiegel trotzdem interessant ist:**
- **Normgehorsam gegen verdeckte Täuschung** (E-005 gegen E-006) hat menschliche Parallelen. Menschen befolgen offen gesetzte Regeln oft auch dann, wenn sie schaden (Milgram, Bürokratie-Kritik). Aktiv zu lügen ist für die meisten unangenehmer, als passiv mitzumachen. Ob der Mechanismus derselbe ist, ist offen.
- **Ehrliche Überbehauptung** (H-023, `notizen/13`) ist bei Menschen ein Kernproblem jeder Organisation: Der Mitarbeiter glaubt, es sei erledigt. Die Ursachen-Taxonomie ist eine *menschliche* Taxonomie, die Agenten zeigen sie nur messbar.
- **Neos Menschenkenntnis als Messinstrument** (Teil 3 §8): Welche der 8 Ursachen der Überbehauptung kennt Neo aus dem Verkauf?

**Methodisch:** Für Leitfrage 3 wäre ein Mensch-Agent-Vergleich nötig, also dieselben Szenarien mit menschlichen Teams. Teil 1 nennt gemischte Mensch-Agent-Organisationen als Forschungslücke. Das ist aufwendig, aber für ein Paper oder einen Blog ein starker Haken.

## Einordnung für Blog oder Paper
Die drei Leitfragen ergeben eine natürliche Erzählung:
1. **Ingenieursfrage:** Wie skaliert man Vertrauen? Messbar, praktisch, für Wave relevant.
2. **Systemfrage:** Entsteht Gesellschaft zwangsläufig? Braucht die Trennung von Erinnern und Erfinden.
3. **Spiegelfrage:** Was zeigt uns das über uns? Braucht den Vergleich mit Menschen.

Nur Leitfrage 1 ist mit dem jetzigen Testbed direkt angehbar. 2 und 3 brauchen neue Bausteine: einfache Lerner, Fremdmodelle, menschliche Teilnehmer.
