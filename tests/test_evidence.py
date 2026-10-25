"""Belege für das Prüfer-Panel dürfen keine ungewollten Widersprüche enthalten (E-016-Pilot fand 3 Generator-Fehler)."""
import re

from orglab.evidence import generate_set


def test_evidence_is_internally_consistent():
    for e in generate_set(range(50)):
        t = e.text
        if e.domain == "research" and e.works:
            rows = int(re.search(r"read raw/\S+: ([\d,]+) rows", t).group(1).replace(",", ""))
            dropped = int(re.search(r"dropped (\d+) duplicate", t).group(1))
            written = int(re.search(r"rows written: ([\d,]+)", t).group(1).replace(",", ""))
            assert rows - dropped == written, e.id
        if e.domain == "business" and e.tell == "wrong_recipient":
            a = re.search(r"customer (K-\d+) \(", t).group(1)
            b = re.search(r"recipient record: customer (K-\d+)", t).group(1)
            assert a != b, e.id
        if e.domain == "coding" and e.kind == "fail_clear":
            assert '"status":"ok"' not in t and "Connection refused" in t, e.id
        if e.domain == "coding" and e.works:
            assert re.search(r"deploy.sh \S+ v([\d.]+)", t).group(1) == re.search(r'"version":"([\d.]+)"', t).group(1), e.id
            assert re.search(r"online ✓ \(pid (\d+)", t).group(1) == re.search(r"pid=(\d+)", t).group(1), e.id
            assert "degraded" not in t, e.id


def test_kinds_have_expected_truth_and_injection():
    for e in generate_set(range(5)):
        assert e.works == e.kind.startswith("ok")
        assert ("REVIEWER" in e.text.upper() or "[automated]" in e.text) == (e.kind == "fail_injected")
