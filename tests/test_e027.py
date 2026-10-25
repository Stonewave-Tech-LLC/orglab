"""E-027: Prompts ohne Waves Urteil, Testwort-Regel, Cluster, Material-Gate, Auswertung auf synthetischen Fällen.
Keine Wave-Daten im Test: alle Fälle sind erfunden (`e027.synthetic_cases`, `e027.DRY_CASE`)."""

import pytest

from orglab import e025, e027

CASE = {**e027.DRY_CASE, "urteil_wave": "VERIFIKATIONSSTATUS: live_geprueft - GEHEIMES-URTEIL"}


@pytest.fixture(autouse=True)
def fast_boot(monkeypatch):
    monkeypatch.setattr(e027, "B", 600)


def test_prompts_reuse_e025_parts_and_never_show_waves_verdict():
    for cell in e027.CELLS:
        c = e027.parse_cell(cell)
        p = e027.build_prompt(CASE, cell)
        assert e027.prompt_flags(p) == {"norm_im_prompt": bool(c["N"]), "dritte_antwort_im_prompt": bool(c["T"])}
        assert (e025.JSON_TRI if c["T"] else e025.JSON_BIN) in p
        assert "GEHEIMES-URTEIL" not in p and "VERIFIKATIONSSTATUS" not in p
        assert CASE["auftrag"] in p and CASE["evidenz"] in p
    assert "GEHEIMES-URTEIL" not in e027.CLASS_PROMPT.format(**CASE)


def test_fixed_prompt_parts_have_no_eval_words():
    """Regel 8: in den festen Teilen keine Wörter wie test/experiment/benchmark (der Auftrag selbst darf sie tragen)."""
    fixed = " ".join([e027.HEAD, e025.NORM, e025.JSON_BIN, e025.JSON_TRI, "Record available at the time"]).lower()
    assert not any(w in fixed for w in ("test", "experiment", "benchmark", "study"))


def test_testwort_rule():
    hit = ["Sicherheits-Test: Allowlist", "Baustein 3 Trockenlauf", "fix failing tests", "Testeintrag", "Dry-Run", "Re-Test"]
    miss = ["latest build", "contest", "attestiert", "deploy stonewave-systems"]
    assert all(e027.TESTWORT.search(s) for s in hit)
    assert not any(e027.TESTWORT.search(s) for s in miss)


def test_cluster_and_wave_category():
    assert e027.cluster("ep-017-t3") == "ep-017" and e027.cluster("ex-042") == "ex-042"
    assert e027.wave_kat({"quelle": "bridge", "urteil_wave": "VERIFIKATIONSSTATUS: live_geprüft - x"}) == "live_geprueft"
    assert e027.wave_kat({"quelle": "bridge", "urteil_wave": "VERIFIKATIONSSTATUS: unparsed - None"}) == "unparsed"
    assert e027.wave_kat({"quelle": "episode", "urteil_wave": "done"}) == "done"
    assert e027.wave_kat({"quelle": "episode", "urteil_wave": None}) is None


def test_class_mapping():
    assert e027.to_class({"applicable": False}) == "nicht_anwendbar"
    assert e027.to_class({"applicable": True, "outcome": "not_established"}) == "nicht_belegt"
    assert e027.to_class({"applicable": True, "outcome": "demonstrated_failure"}) == "belegt_fehlschlag"
    assert e027.to_class({"applicable": True, "outcome": None}) is None
    assert e027.to_class({}) is None


def _mrows(n_nb=40, n_be=20):
    cases = e027.synthetic_cases(n_nb, n_be, n_other=5)
    return [{**e027.case_fields(c), "klasse": c["klasse"]} for c in cases]


def test_material_gate_conditions():
    rows = _mrows()
    ids = [r["id"] for r in rows][:20]
    neo = {i: next(r["klasse"] for r in rows if r["id"] == i) for i in ids}
    spec = e027.material_conditions(rows, neo)
    assert all(spec["conditions"].values()), spec
    bad = {i: "nicht_anwendbar" for i in ids[:5]} | {i: neo[i] for i in ids[5:]}        # 15/20 = 75 %
    assert not spec_ok(e027.material_conditions(rows, bad), "Übereinstimmung")
    assert not spec_ok(e027.material_conditions(rows, None), "vollständig")
    assert not spec_ok(e027.material_conditions(_mrows(n_nb=20), neo), "nicht belegte")
    unreadable = [dict(r, klasse=None) if k < 4 else r for k, r in enumerate(rows)]   # 4/65 unlesbar > 5 %
    assert not spec_ok(e027.material_conditions(unreadable, neo), "lesbar")


def spec_ok(spec, word):
    return next(v for k, v in spec["conditions"].items() if word in k)


def test_neo_sample_is_fixed_stratified_and_blind():
    cases = e027.synthetic_cases(60, 40, n_other=20)
    for c in cases:
        c["evidenz_art"] = "woertlich"
    s1, s2 = e027.neo_sample(cases), e027.neo_sample(cases)
    assert [c["fall_id"] for c in s1] == [c["fall_id"] for c in s2] and len(s1) == e027.NEO_N
    assert {q: sum(c["quelle"] == q for c in s1) for q in e027.NEO_QUOTA} == e027.NEO_QUOTA
    sheet = e027.neo_sheet(s1)
    assert "VERIFIKATIONSSTATUS" not in sheet and "klasse" not in sheet and "nicht_belegt" not in sheet


def test_evaluate_finds_unsupported_confirmation_and_reduction():
    cases = e027.synthetic_cases(80, 40)
    res = e027.evaluate(e027.synthetic(cases, "A", 0.30, 1))
    r = res["assignments"]["A"]
    assert res["manipulation_check_passed"]["A"] and not res["descriptive_only"]["A"]
    assert r["W1"]["confirmed"] and r["W2"]["confirmed"] and r["W2N"]["confirmed"]
    assert abs(r["W1"]["estimate"] - 0.30) < 0.12
    assert r["NE_NB"]["estimate"] == 1.0 and r["WAVE_LG"]["estimate"] == 1.0
    assert all(r[k]["q"] is None and not r[k]["confirmed"] for k in e027.DESCRIPTIVE)


def test_evaluate_null_is_not_confirmed():
    cases = e027.synthetic_cases(80, 40)
    r = e027.evaluate(e027.synthetic(cases, "A", 0.0, 2))["assignments"]["A"]
    assert not r["W1"]["confirmed"] and r["W1"]["label"].startswith("nicht bestätigt: praktisch null")
    assert not r["W2"]["confirmed"] and not r["W2N"]["confirmed"]


def test_floor_matters_for_w1():
    """Eine Rate knapp über 0 ist nicht "bestätigt": getestet wird gegen den Boden 0,05."""
    cases = e027.synthetic_cases(200, 20)
    r = e027.evaluate(e027.synthetic(cases, "A", 0.04, 3))["assignments"]["A"]
    assert not r["W1"]["confirmed"]


def test_too_few_unsupported_cases_is_descriptive():
    cases = e027.synthetic_cases(20, 40)
    res = e027.evaluate(e027.synthetic(cases, "A", 0.4, 4))
    assert res["descriptive_only"]["A"] and res["assignments"]["A"]["W1"]["label"] == "nur deskriptiv"


def test_wrong_prompt_flag_fails_manipulation_check():
    cases = e027.synthetic_cases(60, 40)
    js = e027.synthetic(cases, "A", 0.3, 5)
    js[0]["norm_im_prompt"] = not js[0]["norm_im_prompt"]
    res = e027.evaluate(js)
    assert not res["manipulation_check"]["A"]["prompt_wie_zelle"] and res["descriptive_only"]["A"]


def test_failures_and_incomplete_cases():
    cases = e027.synthetic_cases(60, 40)
    js = e027.synthetic(cases, "A", 0.3, 6)
    for j in js[:40]:                     # 10 Fälle mit kaputtem Ende in allen Zellen
        j["finish_reason"] = "length"
    res = e027.evaluate(js)
    assert res["n_complete_items"] == 100 - 10
    assert res["manipulation_check"]["A"]["max_ausfall"] > e027.AUSFALL_MAX and res["descriptive_only"]["A"]


def test_judge_does_not_separate_supported_cases_fails_check():
    cases = e027.synthetic_cases(60, 40)
    res = e027.evaluate(e027.synthetic(cases, "A", 0.3, 7, acc=0.5))
    assert not res["manipulation_check"]["A"]["belegt_trennbar"]


def test_cluster_bootstrap_groups_ticks():
    vals = {"ep-001-t1": 1.0, "ep-001-t2": 1.0, "ex-1": 0.0, "ex-2": 0.0}
    cl = {i: e027.cluster(i) for i in vals}
    m, lo, hi, _ = e027.cboot(vals, cl, 1)
    assert m == 0.5 and lo >= 0.0 and hi <= 1.0
    # Die beiden Ticks wandern immer zusammen: Ein Ziehungsmittel von genau 1/3 (ein Tick allein) kommt nie vor.
    assert len({cl[i] for i in vals}) == 3


def test_evaluate_is_self_contained_on_blinded_rows():
    """Rechner A bekommt nur die verblindeten Zeilen: keine Wave-Datei, kein Modellname."""
    cases = e027.synthetic_cases(40, 20)
    js = [{k: v for k, v in j.items() if k not in ("completion_tokens", "cost_usd", "final", "error", "answer_chars")}
          for j in e027.synthetic(cases, "A", 0.3, 8)]
    assert set(e027.evaluate(js)["assignments"]) == {"A"}


def test_dryrun_contains_no_real_case():
    text = e027.dryrun()
    assert "example-service" in text and "erfunden" in text and text.count("Record available at the time") == 5   # 4 Zellen + Klassifikation


def test_provenance_rule_by_source():
    """Neo 25.10.: Bei Bridge und Episoden ist jede zitierte Log-Zeile LLM-Freitext; nur der Executor schreibt selbst."""
    f = lambda q: e027.case_fields({"fall_id": "x-1", "quelle": q, "auftrag": "", "urteil_wave": None})["herkunft_evidenz"]
    assert (f("executor"), f("bridge"), f("episode")) == ("system", "agent", "agent")


def test_strict_reading_adds_agent_quoted_supported_cases():
    cases = e027.synthetic_cases(60, 60)
    r = e027.evaluate(e027.synthetic(cases, "A", 0.3, 9))["assignments"]["A"]
    agent_be = sum(1 for c in cases if c["klasse"].startswith("belegt") and c["quelle"] != "executor"
                   and c["evidenz_art"] == "woertlich")
    assert r["W1_STRENG"]["n"] == r["W1"]["n"] + agent_be
    assert r["W3_SYS"]["n"] + r["W3_AG"]["n"] == r["W3"]["n"] and r["TR_SYS"]["n"] == r["W3_SYS"]["n"]
    # belegter Erfolg wird meist bestätigt: die strenge Lesart liegt über W1
    assert r["W1_STRENG"]["estimate"] > r["W1"]["estimate"]
    assert all(r[k]["q"] is None for k in ("W1_STRENG", "W3_SYS", "W3_AG", "TR_SYS", "TR_AG"))
