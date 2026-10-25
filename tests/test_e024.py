"""E-024: Bestätigungslauf. Auswertung an synthetischen Daten mit bekannten Effekten (Regel 16)."""

from orglab import e020v3 as base
from orglab import e024 as e
from orglab.evidence_v4 import generate_set

EVS = generate_set(e.SEEDS)


def _both(v1, crowd, fa, s=1):
    return e.synthetic(EVS, e.HAIKU, v1, crowd, fa, seed=s) + e.synthetic(EVS, e.SONNET, 0.0, 0.0, 0.0, seed=s + 100)


def test_fresh_seeds_not_used_before():
    assert e.SEEDS == range(7000, 7024)
    assert not set(e.SEEDS) & set(base.MAIN_SEEDS)


def test_effects_detected():
    arms, seeds = e.prepare(_both(0.15, 0.4, 0.05))
    assert len(seeds) == 24
    res = e.evaluate(arms, e.HAIKU, e.SONNET)
    for k in ("V1", "W1", "C1", "C2"):
        assert res[k]["lo"] > 0, (k, res[k])
    assert res["C1"]["m"] > 0.3 and res["C2"]["m"] > 0.2


def test_null_not_supported(monkeypatch):
    """Echte Null (immer nachgeschlagen, kein Effekt): über 10 Datensätze × 5 Kontraste höchstens 3 Falsch-Positive
    (erwartet etwa 5 %, einzelne Ziehungen dürfen zufällig treffen)."""
    monkeypatch.setattr(base, "B", 1000)
    hits = 0
    for s in range(10):
        js = e.synthetic(EVS, e.HAIKU, 0.0, 0.0, 0.0, seed=s, base_look=1.0) +              e.synthetic(EVS, e.SONNET, 0.0, 0.0, 0.0, seed=500 + s, base_look=1.0)
        arms, _ = e.prepare(js)
        hits += sum(v["label"].startswith("BESTÄTIGT") for v in e.evaluate(arms, e.HAIKU, e.SONNET).values())
    assert hits <= 3, hits


def test_incomplete_seed_dropped_in_both_arms():
    js = [j for j in _both(0.1, 0.2, 0.0, s=5) if not (j["model"] == e.HAIKU and j["seed"] == 7003 and j["cell"] == "SP0-ZU0-AU0")]
    arms, seeds = e.prepare(js)
    assert 7003 not in seeds and len(seeds) == 23
    assert all(j["seed"] != 7003 for v in arms.values() for j in v)


def test_blind_analysis_runs_on_ab_labels():
    js = [dict(j, model={"anthropic/claude-haiku-5.5": "A", "anthropic/claude-sonnet-5.5": "B"}[j["model"]])
          for j in _both(0.15, 0.4, 0.05, s=7)]
    text = e.analyze_blind(js)
    assert "Falls A = Haiku" in text and "Falls B = Haiku" in text
    assert "claude" not in text


def test_few_seeds_only_descriptive():
    js = [j for j in _both(0.15, 0.4, 0.05, s=9) if j["seed"] < 7010]
    arms, seeds = e.prepare(js)
    res = e.evaluate(arms, e.HAIKU, e.SONNET, descriptive=len(seeds) < e.MIN_SEEDS)
    assert all(v["label"] == "nur deskriptiv" for v in res.values())


def test_f1_uses_only_single_channel_decidable_ok_items():
    arms, _ = e.prepare(_both(0.1, 0.2, 0.05, s=11))
    ok_ids = {j["id"] for j in arms[e.HAIKU] if j["truth"]}
    ex = set(sorted(ok_ids)[:40])
    full = e.evaluate(arms, e.HAIKU, e.SONNET)
    restricted = e.evaluate(arms, e.HAIKU, e.SONNET, f1_exclude=ex)
    assert restricted["F1"]["n"] == full["F1"]["n"] - 40
    assert restricted["V1"]["n"] == full["V1"]["n"]          # andere Kontraste unberührt


def test_exclusion_file_matches_prereg():
    ex = e.exclusion()
    assert len(ex) == 62 and "coding-ok_clear-7009" in ex


# --- Grok-Gutachten 5: Etiketten wie prereg, Abbruch ohne Ausschlussdatei, Manipulationscheck verblindet ----------------

def test_labels_follow_prereg():
    assert e.label(0.05, 0.19, 0.01, 0.10, False).startswith("BESTÄTIGT (")
    assert e.label(0.02, 0.08, 0.01, 0.10, False).startswith("BESTÄTIGT, aber kleiner")      # nicht "widerlegt"
    assert "widerlegt" not in e.label(0.02, 0.08, 0.01, 0.10, False)
    assert e.label(-0.03, 0.015, 0.6, 0.10, False).startswith("nicht bestätigt: praktisch null")
    assert e.label(-0.01, 0.07, 0.2, 0.10, False).startswith("nicht bestätigt: Vorhersagewert ausgeschlossen")
    assert e.label(-0.01, 0.015, 0.6, 0.02, False, weak=True) == "nicht bestätigt (schwache Power, kein Widerlegen)"
    assert e.label(0.05, 0.19, 0.01, 0.10, True) == "nur deskriptiv"
    assert e.label(0.05, 0.19, 0.20, 0.10, False).startswith("nicht bestätigt")              # q > 0,05 reicht nicht


def test_missing_exclusion_file_aborts(tmp_path, monkeypatch):
    monkeypatch.setattr(e, "EXPDIR", tmp_path)
    import pytest
    with pytest.raises(FileNotFoundError):
        e.exclusion()


def test_manipulation_check_failure_makes_blind_analysis_descriptive():
    js = _both(0.15, 0.4, 0.05, s=13)
    js = [dict(j, n_checks=0) if j["model"] == e.HAIKU else j for j in js]           # Werkzeuge nicht benutzt
    js = [dict(j, model={e.HAIKU: "A", e.SONNET: "B"}[j["model"]]) for j in js]
    mc = e.manipulation_check(js)
    assert not mc["A"]["ok"] and mc["B"]["ok"]
    text = e.analyze_blind(js)
    assert "GESCHEITERT" in text and "BESTÄTIGT" not in text
