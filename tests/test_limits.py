import json
import time
from types import SimpleNamespace

from orglab import limits


def _setup(tmp_path, monkeypatch):
    monkeypatch.setattr(limits, "STATE", tmp_path / "limits.json")
    monkeypatch.setattr(limits, "POLICY", tmp_path / "limit_policy.json")
    monkeypatch.setattr(limits, "PAUSE", tmp_path / "PAUSE")


def _info(kind, status, util, reset):
    return SimpleNamespace(rate_limit_type=kind, status=status, utilization=util, resets_at=reset)


def test_free_when_nothing_known(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    assert limits.blocked_until() == (0, "")


def test_five_hour_rejected_blocks_until_reset(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    reset = time.time() + 3600
    limits.record(_info("five_hour", "rejected", None, reset))
    until, why = limits.blocked_until()
    assert until == reset + 120 and "five_hour" in why


def test_weekly_cap_and_policy_override(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    limits.record(_info("seven_day", "allowed_warning", 0.8, time.time() + 86400))
    assert limits.blocked_until()[0] > 0
    (tmp_path / "limit_policy.json").write_text(json.dumps({"weekly_max": 0.9}))
    assert limits.blocked_until() == (0, "")


def test_expired_window_ignored_and_pause_file(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    limits.record(_info("five_hour", "rejected", 1.0, time.time() - 10))
    assert limits.blocked_until() == (0, "")
    (tmp_path / "PAUSE").write_text("")
    assert "PAUSE" in limits.blocked_until()[1]
