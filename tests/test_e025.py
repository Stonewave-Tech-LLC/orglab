"""E-025 (H-041): Auszug ohne Fehlerspur, Prompts je Zelle, Parser, Fehlerspur-Zählung, Auswertung auf synthetischen Daten."""

import re
from collections import defaultdict

import pytest

from orglab import e025
from orglab.evidence_v4 import generate_set

EVS = generate_set(e025.SEEDS)


def test_excerpt_carries_no_fault_signature():
    """Keine Fehlerspur des eigenen Fehlers steht im Auszug (Kanal des Auszugs)."""
    for ev in EVS:
        if ev.works:
            continue
        sig = ev.signatures.get(e025.EXCERPT_CHANNEL[ev.domain])
        assert sig, ev.id                                   # v4: jede Fehlerart hat eine Spur in jedem Kanal
        for part in sig.split("\n"):
            assert part.strip() not in e025.excerpt(ev), (ev.id, ev.fault, part)


def _shape(line: str) -> str:
    """Zeilenart: Zahlen, Hex-IDs, Namen und Adressen normalisiert."""
    line = re.sub(r"<[^>]+>|\S+@\S+", "<A>", line)
    line = re.sub(r"\b[0-9A-F]{7,10}\b|\b[0-9a-f]{7,8}\b", "<H>", line)
    line = re.sub(r"\d[\d,.]*", "<N>", line)
    line = re.sub(r"(auth-service|billing-api|search-indexer|notify-worker|portal-frontend|d\d|D\d)", "<S>", line)
    line = re.sub(r"INV-<N>|K-<N>", "<ID>", line)
    return line.strip()


def test_excerpt_line_types_do_not_depend_on_truth():
    """Was im Auszug bei kaputten Belegen vorkommt, kommt auch bei Ok-Belegen derselben Domäne vor."""
    shapes = defaultdict(lambda: {True: set(), False: set()})
    for ev in EVS:
        shapes[ev.domain][ev.works] |= {_shape(l) for l in e025.excerpt(ev).splitlines()}
    for dom, s in shapes.items():
        assert s[False] <= s[True], (dom, sorted(s[False] - s[True])[:5])


def test_excerpt_is_shorter_and_from_one_channel():
    for ev in EVS[:30]:
        ex = e025.excerpt(ev)
        assert ex and len(ex) < len(ev.channels[e025.EXCERPT_CHANNEL[ev.domain]])


def test_prompts_per_cell():
    ev = EVS[0]
    for c in e025.CELLS:
        cc = e025.parse_cell(c)
        p = e025.build_prompt(ev, c)
        assert ev.item in p and e025.SELF_REPORT in p
        assert (e025.NORM in p) == bool(cc["N"])
        assert ('"not established"' in p) == bool(cc["T"])
        assert p.count("System output") == (1 if cc["D"] else 3)
        assert not re.search(r"\b(benchmark|experiment|test)\b", p, re.I)


@pytest.mark.parametrize("text,expected", [
    ('blah {"works": true, "confidence": 0.9, "reason": "x"}', (True, 0.9)),
    ('{"works": "not established", "confidence": 0.4, "reason": "x"}', (e025.NE, 0.4)),
    ('{"works": "Not_Established", "confidence": 0.4}', (e025.NE, 0.4)),
    ('{"works": false} trailing {"x": 1}', (False, None)),
    ("kein json", (None, None)),
])
def test_parse_verdict(text, expected):
    assert e025.parse_verdict(text) == expected


def test_counted_needs_regular_finish():
    row = {"verdict": True, "parse_ok": True, "finish_reason": "stop"}
    assert e025.counted(row)
    assert not e025.counted(dict(row, finish_reason="length"))
    assert not e025.counted(dict(row, parse_ok=False))


def _two_arms(k0, r1, r2, seed=1):
    evs = generate_set(range(8000, 8012))
    return (e025.synthetic(evs, "A", k0, r1, r2, seed) + e025.synthetic(evs, "B", k0 / 2, 0.0, 0.0, seed + 1))


def test_effects_found_and_null_not_supported():
    old = e025.B
    e025.B = 1000
    try:
        res = e025.evaluate(_two_arms(0.7, 0.3, 0.3))
    finally:
        e025.B = old
    a, b = res["assignments"]["A"], res["assignments"]["B"]
    assert res["n_complete_seeds"] == 12 and res["n_complete_items"] == 144 and not res["descriptive_only"]
    assert a["R1"]["confirmed"] and a["R2"]["confirmed"]
    assert not b["R1"]["confirmed"] and not b["R2"]["confirmed"]
    assert abs(a["K0"]["estimate"] - 0.7) < 0.12


def test_failed_rows_remove_seed_and_trace_counts():
    js = _two_arms(0.6, 0.2, 0.2)
    js[0] = dict(js[0], finish_reason="length")           # abgeschnittene Antwort zählt nicht
    old = e025.B
    e025.B = 200
    try:
        res = e025.evaluate(js)
    finally:
        e025.B = old
    assert res["n_complete_seeds"] == 11 and res["n_complete_items"] == 143   # nur der eine Beleg fällt weg


def test_leaky_excerpt_makes_everything_descriptive():
    evs = generate_set(range(8000, 8012))
    js = []
    for arm in ("A", "B"):
        rows = e025.synthetic(evs, arm, 0.5, 0.0, 0.0, 3)
        for r in rows:
            if r["D"] == 1:
                r["verdict"] = r["truth"]                  # Auszug verrät die Wahrheit
        js += rows
    old = e025.B
    e025.B = 200
    try:
        res = e025.evaluate(js)
    finally:
        e025.B = old
    assert res["descriptive_only"] and not any(m["ok"] for m in res["manipulation_check"].values())
