"""E-022-Auswertung an synthetischen Daten (Regel 16): erkennt einen eingebauten Effekt, meldet keinen, wo keiner ist,
und lässt H-037 bei gescheitertem Manipulationscheck nicht als bestätigt durch."""

import random

from orglab import e022

TOKENS = {"low": 250, "medium": 420, "high": 560, "ohne": 570}


def synth(fa: dict[str, float], miss: dict[str, float], tokens: dict[str, int] = TOKENS, seed: int = 1,
          drop_batch: bool = False):
    rng = random.Random(seed)
    calls, js = [], []
    for b in range(24):
        bid = f"e022-b{b:02d}"
        items = [(f"x-{b}-{i}", i % 2 == 0) for i in range(12)]
        for arm, effort in e022.ARMS.items():
            for p in range(3):
                if drop_batch and b == 0 and arm == "high" and p == 2:
                    continue
                calls.append({"batch": bid, "position": p, "effort": effort, "size": 12, "parsed": 12,
                              "completion_tokens": tokens[arm] + rng.randint(-20, 20), "cost_usd": 0.02})
                for iid, ok in items:
                    err = rng.random() < (fa[arm] if ok else miss[arm])
                    js.append({"id": iid, "batch": bid, "position": p, "effort": effort, "truth": ok,
                               "verdict": (not ok) if err else ok, "confidence": 0.9, "domain": "coding", "channel": "x"})
    return calls, js


def test_effect_detected():
    res, _ = e022.analyze_data(*synth({"low": 0.12, "medium": 0.06, "high": 0.03, "ohne": 0.03},
                                      {a: 0.05 for a in e022.ARMS}))
    assert res["mc_ok"] and res["p1_ok"] and res["p1_relevant"] and res["p2_ok"] and res["h037"]


def test_null_not_confirmed():
    res, _ = e022.analyze_data(*synth({a: 0.05 for a in e022.ARMS}, {a: 0.05 for a in e022.ARMS}))
    assert not res["p1_relevant"] and not res["h037"]


def test_more_misses_with_high_fails_p2():
    res, _ = e022.analyze_data(*synth({"low": 0.12, "medium": 0.06, "high": 0.03, "ohne": 0.03},
                                      {"low": 0.03, "medium": 0.08, "high": 0.15, "ohne": 0.15}))
    assert res["p1_ok"] and not res["p2_ok"] and not res["h037"]


def test_failed_manipulation_blocks_confirmation():
    flat = {"low": 300, "medium": 300, "high": 310, "ohne": 600}
    res, text = e022.analyze_data(*synth({"low": 0.12, "medium": 0.06, "high": 0.03, "ohne": 0.03},
                                         {a: 0.05 for a in e022.ARMS}, tokens=flat))
    assert res["p1_ok"] and not res["mc_ok"] and not res["h037"]
    assert "Manipulationscheck gescheitert" in text


def test_incomplete_batch_excluded():
    res, _ = e022.analyze_data(*synth({a: 0.05 for a in e022.ARMS}, {a: 0.05 for a in e022.ARMS}, drop_batch=True))
    assert res["complete_batches"] == 23
