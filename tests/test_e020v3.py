"""E-020 v3: Prompts ohne Anstupser, Faktoren sauber getrennt, Auswertung an synthetischen Daten (Regel 16)."""

import random
from collections import Counter

from orglab import e020v3 as e
from orglab.evidence_v4 import generate_set

EVS = generate_set(range(6000, 6024))
NUDGES = ["Use the available tools", "look up the runbook", "what you can look up", "before you decide", "Base your judgment"]


def test_eight_cells():
    assert len(e.CELLS) == 8 and len(set(e.CELLS)) == 8


def test_prompts_have_no_nudges_and_spec_controls_norms():
    for ev in EVS[:48]:
        for c in e.CELLS:
            p = e.build_prompt(ev, c)
            assert not any(n.lower() in p.lower() for n in NUDGES), (c, p)
            cc = e.parse_cell(c)
            assert (ev.item in p) == (cc["SP"] == 0)
            assert (e.SELF_REPORT in p) == (cc["AU"] == 1)
            assert ("No system output is attached." in p) == (cc["ZU"] == 1)


def test_runbook_tool_in_every_cell_check_tool_only_with_access():
    ev = EVS[0]
    for c in e.CELLS:
        names = [t["function"]["name"] for t in e.tools_for(ev, e.parse_cell(c)["ZU"])]
        assert "lookup_runbook" in names
        assert ("run_check" in names) == (e.parse_cell(c)["ZU"] == 1)


def test_presented_channel_balanced_per_fault():
    combos = Counter((ev.fault, e.presented_channel(ev)) for ev in EVS if not ev.works)
    for f in {ev.fault for ev in EVS if not ev.works}:
        counts = [v for (ff, _), v in combos.items() if ff == f]
        assert len(counts) == 3 and max(counts) - min(counts) <= 1, f


def _synth(sp_effect: float, au_effect: float, seed: int = 1, drop_seed: bool = False):
    rng = random.Random(seed)
    js = []
    for ev in EVS:
        s = int(ev.id[-4:])
        for c in e.CELLS:
            if drop_seed and s == 6000 and c == e.CELLS[0]:
                continue
            cc = e.parse_cell(c)
            if ev.works:
                p_err = 0.03 - (0.01 if cc["AU"] else 0)
            else:
                p_err = 0.05 + (sp_effect if (cc["SP"] and ev.primary) else 0) + (au_effect if cc["AU"] else 0)
            err = rng.random() < p_err
            js.append({"id": ev.id, "seed": s, "cell": c, **cc, "truth": ev.works, "primary": ev.primary, "fault": ev.fault,
                       "verdict": (not ev.works) if err else ev.works, "confidence": rng.uniform(0.6, 1.0),
                       "n_checks": (rng.randint(1, 3) - (1 if cc["AU"] else 0)) if cc["ZU"] else 0,
                       "looked_up": cc["SP"] == 1, "right_section": cc["SP"] == 1 and rng.random() < 0.7,
                       "completion_tokens": 600, "cost_usd": 0.01})
    return js


def test_effects_detected():
    res, text = e.analyze_data(_synth(0.30, 0.15))
    assert res["complete_seeds"] == 24
    assert res["v1"] > 0.15 and res["v1_lo"] > 0
    assert res["v2"] > 0.08 and res["v2_lo"] > 0
    assert res["v3_hi"] < 0
    assert "gestützt" in text


def test_null_not_supported():
    res, text = e.analyze_data(_synth(0.0, 0.0, seed=2))
    assert abs(res["v1"]) < 0.08 and abs(res["v2"]) < 0.05
    assert "V1** SPEC 1 − 0" in text and "gestützt (≥ Vorhersage" not in text.split("V2**")[0]


def test_incomplete_seed_excluded():
    res, _ = e.analyze_data(_synth(0.0, 0.0, seed=3, drop_seed=True))
    assert res["complete_seeds"] == 23


def test_fewer_than_16_seeds_only_descriptive():
    js = [j for j in _synth(0.30, 0.15, seed=4) if j["seed"] < 6010]
    res, text = e.analyze_data(js)
    assert res["complete_seeds"] == 10 and res["descriptive_only"]
    assert "gestützt (" not in text and "nur deskriptiv" in text


def test_sensitivity_drops_only_the_item_not_its_seed():
    js = _synth(0.2, 0.1, seed=5)
    full, _ = e.analyze_data(js)
    sens, _ = e.analyze_data(js, exclude=e.GRENZFAELLE)
    assert sens["complete_seeds"] == full["complete_seeds"] == 24
    assert sens["n"] == full["n"] - len(e.CELLS)



# --- Abweichung 2 (Grok-Gutachten 3): kohärente Entscheidungsregel, Tests genau an den Schwellen ---------------------

def test_classify_boundaries():
    assert e.classify(0.12, 0.05, 0.19, 0.01, 0.10).startswith("Vorhersage gestützt")
    assert e.classify(0.05, 0.02, 0.08, 0.01, 0.10).startswith("Effekt nachgewiesen, aber")
    assert e.classify(0.00, -0.03, 0.015, 0.6, 0.10).startswith("praktisch null")
    assert e.classify(0.03, -0.01, 0.07, 0.2, 0.10).startswith("Vorhersage widerlegt")
    assert e.classify(0.06, -0.01, 0.13, 0.08, 0.10) == "nicht entschieden"
    assert e.classify(0.12, 0.05, 0.19, 0.01, 0.10, descriptive=True) == "nur deskriptiv"
    assert not e.classify(0.12, 0.05, 0.19, 0.20, 0.10).startswith("Vorhersage gestützt")   # q > 0,05 reicht nicht


def test_true_effect_at_prediction_is_supported():
    res, _ = e.analyze_data(e.synthetic_judgments(EVS, 0.10, 0.05, seed=11))
    assert res["v1_label"].startswith("Vorhersage gestützt"), res["v1_label"]
    assert res["v2_label"].startswith("Vorhersage gestützt"), res["v2_label"]


def test_null_effect_is_refuted():
    res, _ = e.analyze_data(e.synthetic_judgments(EVS, 0.0, 0.0, seed=12))
    assert "widerlegt" in res["v1_label"], res["v1_label"]
