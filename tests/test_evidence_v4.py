"""Material v4 (D-018): Lecktests nach Regel 17 und Grok-Gutachten 2.

Geprüft wird, was sich im Code prüfen lässt: keine Konventions-Marker in spec-reinen Spuren, keine Normwerte in den
Kanälen, Normen im langen Auftrag und im passenden Runbook-Abschnitt, aber nicht im Kurzauftrag, eine Spur in jedem
Kanal, balancierte Fehlerarten und überlappende Verteilungen der beobachtbaren Größe (eine Schwellenregel ohne Norm
trennt Ok und Fehler höchstens zu 75 %). Ob ein *Modell* die Spur ohne Norm entscheidet, prüft erst der Leckpilot
(E-020 v3, Stufe 0).
"""

import hashlib
import json
import re
from collections import Counter

import pytest

from orglab import evidence_v4 as v4
from orglab.evidence import as_dict as as_dict_v2, generate_set_v2

SEEDS = range(9000, 9048)          # nur für Tests, nie für Experimente
EVS = v4.generate_set(SEEDS)
BROKEN_PRIMARY = [e for e in EVS if e.primary]

# Marker, die auch ohne Sollwert "kaputt" sagen (Grok-Gutachten 2, Regel 17)
FORBIDDEN = [r"\b0 kB\b", r"\b0 pages\b", r"\(0/\d+", r"\b\d+/\d+ (shards|columns)", r"mean 100\b", r"mean 1\.00\b",
             r"\(last 60s\): 0$", r"✗", r"MISMATCH", r"ERROR", r"SYN-SENT", r"status=bounced", r"over quota",
             r"still pending", r"soft-bounce", r"waiting\": [1-9]"]
# Nicht verboten: Rauschzeilen, die in Ok-Belegen genauso vorkommen (z. B. Greylisting "status=deferred (421 …)").


def test_v31_unchanged():
    """E-021 und E-022 sind auf v3.1 präregistriert: v4 darf daran nichts ändern."""
    s = json.dumps([as_dict_v2(e) for e in generate_set_v2(range(4000, 4004))], ensure_ascii=False, sort_keys=True)
    assert hashlib.sha256(s.encode()).hexdigest() == "c3c54f25eca3bd80baf9a92cc20a8de93f00da47a6e96236e2218a5e0a8c18f1"


def test_deterministic():
    assert v4.as_dict(v4.generate("coding", "fail_subtle", 9001)) == v4.as_dict(v4.generate("coding", "fail_subtle", 9001))


def test_faults_balanced_and_crossed_with_channel():
    for d in v4.FAULTS:
        fails = [e for e in EVS if e.domain == d and not e.works]
        assert set(Counter(e.fault for e in fails).values()) == {len(SEEDS) * 2 // 4}
        combos = Counter((e.fault, int(e.id[-4:]) % 3) for e in fails)
        assert len(combos) == 12 and len(set(combos.values())) == 1     # E-020 ZUGANG=0: Kanal = Seed mod 3


def test_every_fault_leaves_trace_in_every_channel():
    for e in EVS:
        if e.works:
            assert not e.signatures
        else:
            for ch, text in e.channels.items():
                assert e.signatures.get(ch), (e.id, ch)
                assert e.signatures[ch] in text or e.signatures[ch].replace("\n", " ") in text.replace("\n", " ") \
                    or e.fault in ("cache_partial", "low_traffic"), (e.id, ch)


@pytest.mark.parametrize("e", BROKEN_PRIMARY, ids=lambda e: e.id)
def test_primary_has_no_convention_markers(e):
    for ch, text in e.channels.items():
        for line in text.splitlines():
            for pat in FORBIDDEN:
                assert not re.search(pat, line), (e.id, ch, pat, line)


def test_primary_norm_not_in_channels():
    key = {"cache_partial": "shards", "wrong_contact": "contact", "weights_misscaled": "pop",
           "duplicates_partial": "dups", "column_loss": "ncols", "wrong_terms": "terms"}
    for e in BROKEN_PRIMARY:
        if e.fault in key:
            norm = e.norms[key[e.fault]]
            assert all(norm not in t for t in e.channels.values()), (e.id, norm)


def test_norms_in_long_item_and_runbook_not_in_short():
    topics = {"coding": ["normal traffic", "cache cluster"], "business": ["billing contact", "payment terms"],
              "research": ["duplicates", "weights", "schema columns"]}
    for e in EVS:
        looked = "\n".join(v4.lookup(e, t) for t in topics[e.domain])
        for name, norm in e.norms.items():
            assert norm in e.item, (e.id, name)
            assert norm not in e.item_short, (e.id, name)
            assert norm.split()[0] in looked, (e.id, name)


def test_runbook_unknown_topic_reveals_nothing():
    e = EVS[0]
    assert v4.lookup(e, "quarterly roadmap") == "No entry for 'quarterly roadmap'."
    assert "traffic" not in v4.lookup(e, "database") and "shards" not in v4.lookup(e, "traffic")


OBSERVABLE = {
    "low_traffic": r"requests served \(last 60s\): (\d+)",
    "cache_partial": r"cache connected \((\d+) shards\)",
    "weights_misscaled": r"rescaled to total ([\d,]+)",
    "duplicates_partial": r"dropped (\d+) duplicates",
    "column_loss": r"\((\d+) columns\)",
}


def _best_threshold_accuracy(ok: list[float], bad: list[float]) -> float:
    """Beste balancierte Trefferquote (Mittel aus Sensitivität und Spezifität) einer einzelnen Schwelle."""
    best = 0.0
    for t in sorted(set(ok + bad)):
        for sign in (1, -1):
            sens = sum(sign * x <= sign * t for x in bad) / len(bad)
            spec = sum(sign * x > sign * t for x in ok) / len(ok)
            best = max(best, (sens + spec) / 2)
    return best


@pytest.mark.parametrize("fault", sorted(OBSERVABLE))
def test_observable_overlaps_without_norm(fault):
    """Ohne Norm trennt keine Schwelle auf der beobachtbaren Größe Ok und Fehler zu mehr als 75 %."""
    evs = v4.generate_set(range(9000, 9240))
    dom = next(d for d, fs in v4.FAULTS.items() if fault in fs)
    ch = {"coding": "deploy", "research": "joblog"}[dom]
    val = lambda e: float(re.search(OBSERVABLE[fault], e.channels[ch]).group(1).replace(",", ""))
    ok = [val(e) for e in evs if e.domain == dom and e.works]
    bad = [val(e) for e in evs if e.fault == fault]
    assert _best_threshold_accuracy(ok, bad) <= 0.75, fault


def test_research_item_announces_recalibration():
    """v4.1: Die Rescale-Zeile darf dem Auftrag nicht widersprechen (GPT-Fremdkontrolle v4, notizen/29)."""
    for e in EVS:
        if e.domain == "research":
            assert "recalibrate the survey weights" in e.item and "recalibrate the survey weights" in e.item_short
            assert " only " not in e.item


def test_due_date_overlaps_without_norm():
    import datetime
    evs = v4.generate_set(range(9000, 9240))
    days = lambda e: (datetime.date.fromisoformat(re.search(r"due (\d{4}-\d\d-\d\d)", e.channels["ledger"]).group(1))
                      - datetime.date(2026, 10, 23)).days
    ok = [days(e) for e in evs if e.domain == "business" and e.works]
    bad = [days(e) for e in evs if e.fault == "wrong_terms"]
    assert set(ok) == set(bad) == {14, 30, 45, 60}
    assert _best_threshold_accuracy(ok, bad) <= 0.75


def test_page_lookup_by_entity_returns_norm_section():
    """Seitenbasierte Suche (E-020-v3-Pilot 1): Dienst-, Rechnungs- oder Datensatzname liefert die Seite mit der Norm."""
    want = {"low_traffic": "[traffic]", "cache_partial": "[cache]", "wrong_contact": "[contacts]", "wrong_terms": "[payment]",
            "weights_misscaled": "[weights]", "duplicates_partial": "[duplicates]", "column_loss": "[schema]"}
    for e in BROKEN_PRIMARY:
        for name in e.entities:
            assert want[e.fault] in v4.lookup(e, f"runbook {name}"), (e.id, name)
    assert v4.lookup(EVS[0], "quarterly roadmap").startswith("No entry")


# --- v4.2 (Grok-Gutachten 3) ---------------------------------------------------------------------------------------
MAIN = v4.generate_set(range(6000, 6024))


@pytest.mark.parametrize("e", [x for x in MAIN if x.primary], ids=lambda e: e.id)
def test_leak_checks_also_on_main_seeds(e):
    for ch, text in e.channels.items():
        for line in text.splitlines():
            for pat in FORBIDDEN:
                assert not re.search(pat, line), (e.id, ch, pat, line)


def test_norm_text_identical_in_long_item_and_runbook():
    """SPEC=0 und SPEC=1 tragen dieselbe Information: Was zur Norm im Runbook steht, steht auch im langen Auftrag."""
    for e in MAIN:
        rb = e.runbook
        n = e.norms
        phrases = {"coding": lambda: ["single production instance", "steady around the clock", "±20 %", "connects to all shards",
                                      n["rate"].split()[0], n["shards"]],
                   "business": lambda: [n["contact"], n["terms"].split()[0] + " days"],
                   "research": lambda: [n["pop"], n["dups"].split()[0], n["ncols"].split()[0]]}[e.domain]()
        for ph in phrases:
            assert ph in e.item and ph in rb, (e.id, ph)


def test_pages_hide_the_norm_among_similar_values():
    """Die richtige Normzeile steht zwischen mindestens drei gleich aussehenden Werten anderer Einheiten."""
    pat = {"traffic": r"~\d+", "cache": r"\d+ shards", "payment": r"\d+ days", "contacts": r"billing contact",
           "duplicates": r"D\d \d+", "weights": r"D\d [\d,]+", "schema": r"D\d \d+"}
    for e in MAIN:
        for sec, rx in pat.items():
            if sec in e.runbook_sections:
                assert len(re.findall(rx, e.runbook_sections[sec])) >= 4, (e.id, sec)


def test_keyword_lookup_respects_word_start():
    e = next(x for x in MAIN if x.domain == "coding")
    assert "[ports]" not in v4.lookup(e, "report")
    assert "[ports]" in v4.lookup(e, "port")


def test_no_contradicting_distractor_sections():
    for e in MAIN:
        assert "German" not in e.runbook


def test_file_descriptors_unique_per_process():
    """v4.3: Ein Prozess kann denselben Datei-Deskriptor nicht für zwei Sockets nutzen (GPT-Fremdkontrolle v4.2)."""
    for e in MAIN + EVS:
        if e.domain != "coding":
            continue
        pairs = re.findall(r'pid=(\d+),fd=(\d+)', e.channels["sockets"])
        seen = Counter(pairs)
        assert all(c == 1 for c in seen.values()), (e.id, [p for p, c in seen.items() if c > 1])

