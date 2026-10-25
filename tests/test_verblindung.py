"""Verblindung (Regel 20): Roundtrip, keine Armnamen und Leckfelder in der Kopie, Hash-Commitment, Gate."""

import json
import random

import pytest

from orglab import verblindung as v

ARMS = ["low", "medium", "high", "none"]


def _setup(tmp_path):
    root, keys = tmp_path / "repo", tmp_path / "keys"
    data = root / "daten" / "E-T"
    data.mkdir(parents=True)
    calls = [{"batch": "b0", "effort": e, "completion_tokens": t, "raw": "x"} for e, t in
             [("low", 257), ("medium", 257), ("high", 900), (None, 910)]]
    (data / "calls.jsonl").write_text("\n".join(json.dumps(c) for c in calls), encoding="utf-8")
    (data / "andere.jsonl").write_text(json.dumps({"ohne_feld": 1}), encoding="utf-8")
    return root, keys


def test_blinded_copy_has_no_arm_names_or_leak_fields(tmp_path):
    root, keys = _setup(tmp_path)
    out = v.verblinden("E-T", "effort", ARMS, ["completion_tokens", "raw"], keys, root, random.Random(1))
    text = (out / "calls.jsonl").read_text(encoding="utf-8")
    for arm in ("low", "medium", "high", "null"):
        assert arm not in text
    assert "completion_tokens" not in text and "raw" not in text
    assert sorted(json.loads(l)["effort"] for l in text.splitlines()) == ["A", "B", "C", "D"]
    assert not (out / "andere.jsonl").exists()          # Dateien ohne Armfeld werden nicht kopiert
    assert not list(root.rglob("*.json"))               # Schlüssel liegt nicht im Repo


def test_never_reroll(tmp_path):
    root, keys = _setup(tmp_path)
    v.verblinden("E-T", "effort", ARMS, [], keys, root)
    with pytest.raises(FileExistsError):
        v.verblinden("E-T", "effort", ARMS, [], keys, root)


def test_gate_and_roundtrip(tmp_path):
    root, keys = _setup(tmp_path)
    v.verblinden("E-T", "effort", ARMS, [], keys, root, random.Random(2))
    with pytest.raises(PermissionError):
        v.entblinden("E-T", keys, root, gate=lambda p, r: True)        # Auswertung fehlt
    (root / "experimente" / "E-T" / "auswertung-verblindet.md").write_text("A > C", encoding="utf-8")
    with pytest.raises(PermissionError):
        v.entblinden("E-T", keys, root, gate=lambda p, r: False)       # nicht committet
    mapping = v.entblinden("E-T", keys, root, gate=lambda p, r: True)
    blinded = [json.loads(l) for l in (root / "daten" / "E-T" / "verblindet" / "calls.jsonl").read_text().splitlines()]
    original = [json.loads(l) for l in (root / "daten" / "E-T" / "calls.jsonl").read_text().splitlines()]
    for b, o in zip(blinded, original):
        assert mapping["none" if o["effort"] is None else o["effort"]] == b["effort"]


def test_tampered_key_detected(tmp_path):
    root, keys = _setup(tmp_path)
    v.verblinden("E-T", "effort", ARMS, [], keys, root, random.Random(3))
    (root / "experimente" / "E-T" / "auswertung-verblindet.md").write_text("x", encoding="utf-8")
    k = json.loads((keys / "E-T.json").read_text())
    k["mapping"]["low"], k["mapping"]["high"] = k["mapping"]["high"], k["mapping"]["low"]
    (keys / "E-T.json").write_text(json.dumps(k, sort_keys=True))
    with pytest.raises(ValueError):
        v.entblinden("E-T", keys, root, gate=lambda p, r: True)
