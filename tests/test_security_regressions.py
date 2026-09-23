"""
Regression tests for Phase 1 security & startup fixes (audit_merged.md).

Covers:
  * SEC-1 — unauthenticated path traversal in the swarm MCP tools
  * SEC-2 — client IP spoofing via X-Forwarded-For
  * SEC-3 — raw exception detail leaked to MCP callers
  * SEC-4 — no request-body size cap on the public MCP endpoint
  * H7   — mseat_rest importing mseat_mcp (boot fragility)

All tests run offline.
"""
import json
import os
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "api"))


@pytest.fixture(scope="session")
def client():
    from api.index import app

    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def fresh_mcp_limiter(monkeypatch):
    """Swap in a permissive limiter so H2 (min-interval limiter) doesn't
    contaminate these Phase 1 tests; H2 is fixed separately in Phase 2."""
    import api.index as idx
    from api.services.security import RateLimiter

    monkeypatch.setattr(idx, "_mcp_limiter", RateLimiter(60, 1_000_000))


# --------------------------------------------------------------------------
# SEC-1: path traversal
# --------------------------------------------------------------------------

def test_daily_views_rejects_traversal():
    from api.ai_eco_mcp import handle_get_swarm_daily_views

    for bad in ["../../README", "../../../etc/passwd", "/etc/passwd", "..\\..\\README", "not-a-date"]:
        res = handle_get_swarm_daily_views({"date": bad})
        blob = json.dumps(res)
        assert "error" in res, f"{bad!r} must be rejected with an error"
        assert res.get("count", 0) == 0
        assert "kprsnt" not in blob and "Repository" not in blob, "repo content must never leak"


def test_weekly_meeting_rejects_traversal():
    from api.ai_eco_mcp import handle_get_swarm_weekly_meeting

    for bad in ["../../README", "../../../etc/passwd", "/etc/passwd", "2026-W99x"]:
        res = handle_get_swarm_weekly_meeting({"week": bad})
        assert "error" in res, f"{bad!r} must be rejected with an error"
        assert "minutes" not in res


def test_daily_views_valid_date_still_works():
    from api.ai_eco_mcp import SWARM_DAILY_DIR, handle_get_swarm_daily_views

    files = sorted(SWARM_DAILY_DIR.glob("*.md"), reverse=True)
    if not files:
        pytest.skip("no daily views present")
    res = handle_get_swarm_daily_views({"date": files[0].stem})
    assert res.get("count") == 1
    assert res["daily_views"][0]["date"] == files[0].stem


def test_weekly_valid_week_still_works():
    from api.ai_eco_mcp import SWARM_WEEKLY_DIR, handle_get_swarm_weekly_meeting

    files = sorted(SWARM_WEEKLY_DIR.glob("*.md"), reverse=True)
    if not files:
        pytest.skip("no weekly meetings present")
    res = handle_get_swarm_weekly_meeting({"week": files[0].stem})
    assert "error" not in res
    assert res.get("file") == files[0].name


# --------------------------------------------------------------------------
# SEC-2: client IP normalization
# --------------------------------------------------------------------------

def test_client_ip_prefers_x_real_ip():
    from flask import request

    from api.index import app
    from api.services.security import get_client_ip

    with app.test_request_context(
        "/",
        headers={"X-Real-IP": "10.1.1.1", "X-Forwarded-For": "9.9.9.9, 10.0.0.7"},
        environ_base={"REMOTE_ADDR": "203.0.113.9"},
    ):
        assert get_client_ip(request) == "10.1.1.1"


def test_client_ip_uses_last_xff_hop_not_first():
    from flask import request

    from api.index import app
    from api.services.security import get_client_ip

    with app.test_request_context(
        "/",
        headers={"X-Forwarded-For": "9.9.9.9, 10.0.0.7"},
        environ_base={"REMOTE_ADDR": "203.0.113.9"},
    ):
        # The first hop is client-controlled; the last hop is proxy-appended.
        assert get_client_ip(request) == "10.0.0.7"


def test_client_ip_falls_back_to_remote_addr():
    from flask import request

    from api.index import app
    from api.services.security import get_client_ip

    with app.test_request_context("/", environ_base={"REMOTE_ADDR": "203.0.113.9"}):
        assert get_client_ip(request) == "203.0.113.9"


# --------------------------------------------------------------------------
# SEC-3: exception-detail disclosure
# --------------------------------------------------------------------------

def test_eco_mcp_error_hides_internals(monkeypatch):
    import api.ai_eco_mcp as eco

    def boom(_args):
        raise RuntimeError("SECRET-INTERNAL-DETAIL-XYZ")

    monkeypatch.setattr(eco, "handle_site_overview", boom)
    resp = eco.process_mcp_request({
        "jsonrpc": "2.0", "id": 1, "method": "tools/call",
        "params": {"name": "get_site_overview", "arguments": {}},
    })
    blob = json.dumps(resp)
    assert "SECRET-INTERNAL-DETAIL-XYZ" not in blob
    assert resp["result"]["isError"] is True


def test_mseat_mcp_error_hides_internals(monkeypatch):
    import api.mseat_mcp as mseat

    def boom(_args):
        raise RuntimeError("SECRET-MSEAT-DETAIL-XYZ")

    monkeypatch.setattr(mseat, "handle_predict_seat", boom)
    resp = mseat.process_mcp_request({
        "jsonrpc": "2.0", "id": 1, "method": "tools/call",
        "params": {"name": "predict_mbbs_seat", "arguments": {}},
    })
    blob = json.dumps(resp)
    assert "SECRET-MSEAT-DETAIL-XYZ" not in blob
    assert resp["result"]["isError"] is True


# --------------------------------------------------------------------------
# SEC-4: request-size cap
# --------------------------------------------------------------------------

def test_mcp_rejects_oversized_body(client):
    resp = client.post(
        "/api/mcp",
        json={"jsonrpc": "2.0", "id": 1, "method": "tools/list", "padding": "a" * 1_100_000},
    )
    assert resp.status_code == 413


def test_mcp_normal_body_still_ok(client):
    resp = client.post("/api/mcp", json={"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    assert resp.status_code == 200


# --------------------------------------------------------------------------
# H7: boot-fragile imports
# --------------------------------------------------------------------------

def test_mseat_rest_does_not_import_mseat_mcp():
    code = (
        "import sys; sys.path.insert(0, %r); "
        "import api.mseat_rest; "
        "bad = [m for m in sys.modules if m.split('.')[-1] == 'mseat_mcp']; "
        "assert not bad, bad" % ROOT
    )
    subprocess.run([sys.executable, "-c", code], check=True, cwd=ROOT)


def test_app_boots():
    from api.index import app

    assert app is not None


# --------------------------------------------------------------------------
# H2: rate limiter burst behaviour
# --------------------------------------------------------------------------

@pytest.fixture
def prod_config_limiter(monkeypatch):
    """The production MCP limiter config (60/min, 120/min), fresh state."""
    import api.index as idx
    from api.services.security import RateLimiter

    monkeypatch.setattr(idx, "_mcp_limiter", RateLimiter(60, 120))


def test_rate_limiter_allows_burst_up_to_max():
    from api.services.security import RateLimiter

    rl = RateLimiter(60, 3)
    assert all(rl.check("1.2.3.4")[0] for _ in range(3))
    allowed, retry_after = rl.check("1.2.3.4")
    assert allowed is False and retry_after > 0


def test_rate_limiter_window_expiry():
    import time

    from api.services.security import RateLimiter

    rl = RateLimiter(0.05, 1)
    assert rl.check("1.2.3.4")[0] is True
    assert rl.check("1.2.3.4")[0] is False
    time.sleep(0.06)
    assert rl.check("1.2.3.4")[0] is True


def test_mcp_handshake_burst_all_succeeds(client, prod_config_limiter):
    """H2 regression: a real MCP client's initialize -> notifications/initialized
    -> tools/list sequence must not be throttled."""
    r1 = client.post("/api/mcp", json={"jsonrpc": "2.0", "id": 1, "method": "initialize"})
    assert r1.status_code == 200

    r2 = client.post("/api/mcp", json={"jsonrpc": "2.0", "method": "notifications/initialized"})
    assert r2.status_code in (200, 204)

    r3 = client.post("/api/mcp", json={"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    assert r3.status_code == 200

    r4 = client.post(
        "/api/mcp",
        json={"jsonrpc": "2.0", "id": 3, "method": "tools/call",
              "params": {"name": "get_site_overview", "arguments": {}}},
    )
    assert r4.status_code == 200
