"""E-026: gleiche Prompts wie E-025, Prompt-Flags aus dem gesendeten Text, Bestätigungs-Auswertung je Zuordnung."""

import pytest

from orglab import e025, e026
from orglab.evidence_v4 import generate_set

EVS = generate_set(range(9000, 9012))


def test_same_prompts_as_e025_and_fresh_seeds():
    ev = generate_set(range(9000, 9001))[0]
    assert all(e026.build_prompt(ev, c) == e025.build_prompt(ev, c) for c in e026.CELLS)
    assert not set(e026.SEEDS) & set(e025.SEEDS) and not set(e026.PILOT_SEEDS) & set(e025.PILOT_SEEDS)


def test_prompt_flags_follow_the_sent_text():
    ev = EVS[0]
    for c in e026.CELLS:
        cc = e026.parse_cell(c)
        f = e026.prompt_flags(e026.build_prompt(ev, c))
        assert f == {"norm_im_prompt": bool(cc["N"]), "dritte_antwort_im_prompt": bool(cc["T"])}


def _data(k0_s=0.23, k0_h=0.02, ne_s=0.06, ne_h=0.22):
    return e026.synthetic(EVS, "A", k0_s, ne_s, 1) + e026.synthetic(EVS, "B", k0_h, ne_h, 2)


@pytest.fixture(autouse=True)
def fast_boot():
    old = e025.B
    e025.B = 800
    yield
    e025.B = old


def test_effects_confirmed_for_right_assignment_only():
    res = e026.evaluate(_data())
    a, b = res["assignments"]["A"], res["assignments"]["B"]
    assert not res["descriptive_only"] and res["n_complete_items"] == 144
    assert a["B1"]["confirmed"] and a["B2"]["confirmed"] and a["B3"]["confirmed"] and a["B4"]["confirmed"]
    assert not b["B1"]["confirmed"]                         # falsche Zuordnung: Vorzeichen umgekehrt
    assert abs(a["K0Z"]["estimate"] - 0.23) < 0.08


def test_null_not_confirmed():
    """Ohne Rauschen (Trefferquote 1,0), damit "null" exakt null ist und nicht nur im Mittel."""
    js = e026.synthetic(EVS, "A", 0.02, 0.0, 1, acc=1.0) + e026.synthetic(EVS, "B", 0.02, 0.0, 2, acc=1.0)
    res = e026.evaluate(js)
    a = res["assignments"]["A"]
    assert not a["B1"]["confirmed"] and not a["B4"]["confirmed"]


def test_prompt_mismatch_fails_manipulation_check():
    js = _data()
    js[3] = dict(js[3], norm_im_prompt=not js[3]["norm_im_prompt"])   # Zelle sagt N, Prompt nicht
    res = e026.evaluate(js)
    assert res["descriptive_only"] and not all(res["manipulation_check_passed"].values())


def test_missing_flags_fail_manipulation_check():
    js = _data()
    js[0].pop("norm_im_prompt")
    assert e026.evaluate(js)["descriptive_only"]
