"""E-023: nur das Modell wechselt; Wechselwirkung Modell × Faktor an synthetischen Daten (Regel 16)."""

from orglab import e020v3 as base
from orglab import e023 as e
from orglab.evidence_v4 import generate_set

EVS = generate_set(base.MAIN_SEEDS)


def test_same_design_as_e020():
    assert e.HAIKU == "anthropic/claude-haiku-5.5"
    assert e.DATA != base.DATA
    assert base.MAIN_SEEDS == range(6000, 6024) and len(base.CELLS) == 8


def test_undecidable_rule_matches_e020_finding():
    ids = e.undecidable_ids(EVS)
    assert len(ids) == 8
    assert "coding-fail_moderate-6006" in ids and "coding-fail_moderate-6005" in ids


def test_interaction_detects_model_difference():
    haiku = base.synthetic_judgments(EVS, 0.20, 0.0, seed=21)
    sonnet = base.synthetic_judgments(EVS, 0.0, 0.0, seed=22)
    res = e.interaction(haiku, sonnet)
    mh, ms, m, lo, hi, n = res["V1 SPEC (spec-rein)"]
    assert n == 84 and lo > 0 and m > 0.1


def test_interaction_null_when_models_equal():
    haiku = base.synthetic_judgments(EVS, 0.10, 0.0, seed=23)
    sonnet = base.synthetic_judgments(EVS, 0.10, 0.0, seed=24)
    _, _, m, lo, hi, _ = e.interaction(haiku, sonnet)["V1 SPEC (spec-rein)"]
    assert lo < 0 < hi


def test_exclusion_drops_items_from_pairing():
    js = base.synthetic_judgments(EVS, 0.1, 0.05, seed=25)
    full = e.interaction(js, js)
    ex = e.interaction(js, js, e.undecidable_ids(EVS))
    assert ex["V2 AUSKUNFT"][5] == full["V2 AUSKUNFT"][5] - 8
    assert ex["V1 SPEC (spec-rein)"][5] == full["V1 SPEC (spec-rein)"][5] - 4
