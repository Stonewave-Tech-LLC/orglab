"""Belege v2 (E-017): Jeder Kanal muss allein entscheidbar sein, sonst misst "verschiedene Kanäle" Blindheit (D-014)."""
import re

from orglab.evidence import CHANNELS, FINDINGS, KINDS_V2, generate_set_v2, generate_v2

SEEDS = range(60)


def test_every_fail_channel_carries_its_trace():
    for e in generate_set_v2(SEEDS):
        assert set(e.channels) == set(CHANNELS[e.domain]), e.id
        if e.works:
            assert e.signatures == {} and e.fault == "none", e.id
            continue
        assert set(e.signatures) == set(e.channels), e.id
        for ch, s in e.signatures.items():
            assert s and s in e.channels[ch], (e.id, ch, s)


def test_ok_items_are_consistent_with_the_work_item():
    for e in generate_set_v2(SEEDS):
        if not e.works:
            continue
        c = e.channels
        if e.domain == "coding":
            ver, sha = re.search(r"v([\d.]+) \(commit (\w+)\)", e.item).groups()
            assert sha in c["probe"] and f'"{ver}"' in c["probe"], e.id
            listen = re.search(r"LISTEN .*pid=(\d+)", c["sockets"]).group(1)
            assert re.search(rf"^\s*{listen} .*releases/{re.escape(ver)}-{sha}/", c["sockets"], re.M), e.id
            assert "ESTAB" in c["sockets"] and "degraded" not in c["probe"] and "unreachable" not in c["probe"], e.id
            assert "EADDRINUSE" not in c["deploy"] and f"listening on :" in c["deploy"] and "(20/20)" in c["deploy"], e.id
            port = re.search(r"PORT=(\d+)", c["deploy"]).group(1)
            assert f"listening on :{port}" in c["deploy"] and '"active": 0' not in c["probe"], e.id
        if e.domain == "business":
            contact = e.item.rsplit(" ", 1)[1]
            assert f"<{contact}>" in c["smtp"] and f"<{contact}>" in c["delivery"], e.id
            for bad in ("bounced", "expired", "5.1.1", "soft-bounce", "still pending", "EMAIL_BOUNCED"):
                assert all(bad not in t for t in c.values()), (e.id, bad)
        if e.domain == "research":
            raw = int(re.search(r"raw file: ([\d,]+) rows", e.item).group(1).replace(",", ""))
            dups = int(re.search(r"dropped (\d+) duplicates", c["joblog"]).group(1))
            assert f"{raw - dups:,} rows" in c["output"] and "weight float64" in c["joblog"], e.id
            assert "1.00" in c["validation"] and "MISMATCH" not in c["validation"], e.id


def test_fail_items_contradict_the_work_item():
    for e in generate_set_v2(SEEDS):
        if e.works:
            continue
        if e.fault == "wrong_recipient":
            contact = e.item.rsplit(" ", 1)[1]
            assert f"<{contact}>" not in e.channels["smtp"], e.id
        if e.fault == "stale_process":
            sha = re.search(r"commit (\w+)\)", e.item).group(1)
            assert sha not in e.channels["probe"], e.id
            port = re.search(r"PORT=(\d+)", e.channels["deploy"]).group(1)
            assert not re.search(rf"listening on :{port}$", e.channels["deploy"], re.M), e.id
        if e.fault == "row_loss":
            raw = int(re.search(r"raw file: ([\d,]+) rows", e.item).group(1).replace(",", ""))
            out = int(re.search(r"([\d,]+) rows x", e.channels["output"]).group(1).replace(",", ""))
            assert out < 0.25 * raw, e.id


def test_subtlety_and_kinds():
    es = generate_set_v2(SEEDS)
    for e in es:
        assert e.works == e.kind.startswith("ok")
        assert e.subtlety == 1 if e.kind in ("ok_clear", "fail_moderate") else e.subtlety in (2, 3)
    faults = {e.fault for e in es}
    assert faults == set(FINDINGS)
    assert len(es) == 3 * len(KINDS_V2) * len(SEEDS)


def test_deterministic():
    assert generate_v2("coding", "fail_subtle", 7) == generate_v2("coding", "fail_subtle", 7)


def test_research_chunks_sum_to_raw_rows():
    import re as _re
    for e in generate_set_v2(SEEDS, domains=("research",)):
        chunks = [int(x.replace(",", "")) for x in _re.findall(r"read chunk \d+/\d+: ([\d,]+) rows", e.channels["joblog"])]
        if chunks:
            raw = int(_re.search(r"raw file: ([\d,]+) rows", e.item).group(1).replace(",", ""))
            assert sum(chunks) == raw, e.id


def test_padding_is_internally_consistent():
    """Kalibrierung E-019 L1, Kriterium 5: Routinezeilen dürfen sich nicht widersprechen."""
    import re as _re
    for e in generate_set_v2(SEEDS):
        c = e.channels
        if e.domain == "coding":
            listen = set(_re.findall(r'LISTEN .*\("node",pid=(\d+)', c["sockets"]))
            ps = set(_re.findall(r"^\s*(\d+) ", c["sockets"].split("$ ps")[1].split("$ ss")[0], _re.M))
            assert listen <= ps, e.id
            for cmd in ("/api/v1/config/public", "grep -c ^http_"):
                outs = set(_re.findall(_re.escape(cmd) + r"\n(.+)", c["probe"]))
                assert len(outs) <= 1, (e.id, cmd, outs)
        if e.domain == "business":
            sent = {q: m for m, q in _re.findall(r"10:(\d\d):\d\d (\w+): relay=", c["smtp"])}
            for m, q in _re.findall(r"10:(\d\d):\d\d (\w+): from=", c["smtp"]):
                if q in sent:
                    assert int(sent[q]) >= int(m), (e.id, q)


def test_v3_faults_contradict_and_ok_items_agree():
    """Material v3 (D-016): Status grün, aber ein quantitatives Detail widerspricht – in jedem Kanal."""
    import re as _re
    for e in generate_set_v2(SEEDS):
        c = e.channels
        if e.domain == "coding":
            clients = int(_re.search(r"wc -l\n(\d+)", c["sockets"]).group(1))
            assert (clients == 0) == (e.fault == "zero_traffic"), e.id
            assert ("(4/4 shards)" in c["deploy"]) == (e.fault != "cache_down"), e.id
            assert ('"cache_shards": {"up": 4' in c["probe"]) == (e.fault != "cache_down"), e.id
        if e.domain == "business":
            amount = _re.search(r"\((€ [\d,.]+), PDF", e.item).group(1)
            assert (f"({amount})'" in c["smtp"] and f"posted, customer" in c["ledger"]
                    and f"{amount}, status SENT" in c["ledger"]) == (e.fault != "amount_mismatch"), e.id
            assert ("pdf, 0 kB)" in c["delivery"]) == (e.fault == "empty_attachment"), e.id
            assert ("(0 pages)" in c["ledger"]) == (e.fault == "empty_attachment"), e.id
        if e.domain == "research":
            assert ("dropped 0 duplicates" in c["joblog"]) == (e.fault == "duplicates_kept"), e.id
            assert ("parquet (47 columns)" in c["joblog"]) == (e.fault != "column_loss"), e.id
            assert ("schema: 47/47" in c["validation"]) == (e.fault != "column_loss"), e.id


def test_short_item_and_runbook_split_the_background_spec():
    """E-020 SPEC=1: Hintergrund-Sollwerte stehen nur im Runbook, der Kurzauftrag enthält weiter den Auftrag selbst."""
    for e in generate_set_v2(SEEDS):
        assert e.item_short and e.runbook and e.item_short != e.item, e.id
        if e.domain == "coding":
            assert "requests/min" not in e.item_short and "requests/min" in e.runbook and "commit" in e.item_short, e.id
        if e.domain == "business":
            assert "PDF" not in e.item_short and "PDF" in e.runbook and "€" in e.item_short, e.id
        if e.domain == "research":
            assert "47 columns" not in e.item_short and "47 columns" in e.runbook and "mean 1" in e.runbook, e.id
            assert "raw file:" in e.item_short, e.id
