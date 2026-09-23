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


@pytest.fixture
def fresh_public_limiters(monkeypatch):
    """Swap in permissive public limiters so a burst of malformed-body cases
    cannot exhaust the shared 3 req/min email limiter and leak 429s into other
    tests (which run against the original limiter after monkeypatch restores)."""
    import api.index as idx
    from api.services.security import RateLimiter

    monkeypatch.setattr(idx, "_mcp_limiter", RateLimiter(60, 1_000_000))
    monkeypatch.setattr(idx, "_chat_limiter", RateLimiter(60, 1_000_000))
    monkeypatch.setattr(idx, "_email_limiter", RateLimiter(60, 1_000_000))


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


# --------------------------------------------------------------------------
# H8 / M2: mSeat input validation
# --------------------------------------------------------------------------

def test_predict_seat_accepts_string_rank():
    from api.mseat_mcp import handle_predict_seat

    assert handle_predict_seat({"state_rank": "3000"}).get("success") is True


def test_predict_seat_rejects_bad_inputs():
    from api.mseat_mcp import handle_predict_seat

    assert handle_predict_seat({"category": None}).get("success") is False
    assert handle_predict_seat({"category": "XX"}).get("success") is False
    assert handle_predict_seat({"state_rank": 0}).get("success") is False
    assert handle_predict_seat({"state_rank": -5}).get("success") is False
    assert handle_predict_seat({"air": "high"}).get("success") is False
    assert handle_predict_seat(None).get("success") is False


def test_predict_seat_consistent_response_shape():
    from api.mseat_mcp import handle_predict_seat

    allocated = handle_predict_seat({"state_rank": 100})
    not_allocated = handle_predict_seat({"state_rank": 9999999})
    for key in ("stateRank", "categoryRank", "category", "allocated", "success"):
        assert key in allocated, key
        assert key in not_allocated, key


def test_college_info_requires_query():
    from api.mseat_mcp import handle_college_info

    assert handle_college_info({"college_code_or_name": ""}).get("success") is False


def test_compare_colleges_requires_both():
    from api.mseat_mcp import handle_compare_colleges

    assert handle_compare_colleges({}).get("success") is False
    assert handle_compare_colleges({"college_a": "Gandhi"}).get("success") is False


def test_sliding_odds_requires_both():
    from api.mseat_mcp import handle_sliding_odds

    assert handle_sliding_odds({}).get("success") is False
    assert handle_sliding_odds({"current_college": "Gandhi"}).get("success") is False


# --------------------------------------------------------------------------
# H9: JSON-RPC validation
# --------------------------------------------------------------------------

def test_jsonrpc_invalid_method_and_params():
    import api.ai_eco_mcp as eco
    import api.mseat_mcp as mseat

    for mod in (eco, mseat):
        resp = mod.process_mcp_request({"jsonrpc": "2.0", "id": 1, "method": None})
        assert resp["error"]["code"] == -32600

        resp = mod.process_mcp_request({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": "x"})
        assert resp["error"]["code"] == -32602

        resp = mod.process_mcp_request({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": [1, 2]})
        assert resp["error"]["code"] == -32602


def test_jsonrpc_notifications_ok():
    import api.ai_eco_mcp as eco

    # JSON-RPC 2.0: notifications must NOT be answered -> None (route maps to 204)
    resp = eco.process_mcp_request({"jsonrpc": "2.0", "method": "notifications/initialized"})
    assert resp is None or "error" not in resp


# --------------------------------------------------------------------------
# M13: malformed JSON bodies -> 400, never 500
# --------------------------------------------------------------------------

def test_malformed_json_bodies_return_400(client, fresh_public_limiters):
    # JSON string / array / object-for-string / string-history must all 400
    assert client.post("/api/chat", data="just-a-string", content_type="application/json").status_code == 400
    assert client.post("/api/chat", json=[1, 2, 3]).status_code == 400
    assert client.post("/api/chat", json={"query": {"a": 1}}).status_code == 400
    assert client.post("/api/chat", json={"query": "hi", "history": "not-a-list"}).status_code == 400
    assert client.post("/api/chat", json={"query": "hi", "history": ["not-a-dict"]}).status_code == 400

    assert client.post("/api/interview", data="[1,2,3]", content_type="application/json").status_code == 400
    assert client.post("/api/interview", json={"message": {"a": 1}}).status_code == 400
    # syntactically invalid JSON must 400, not 500 (get_json silent=True)
    assert client.post("/api/interview", data="just-a-string", content_type="application/json").status_code == 400

    assert client.post("/api/chat_agent", data='"str"', content_type="application/json").status_code == 400
    assert client.post("/api/chat_agent", json={"message": 42}).status_code == 400
    assert client.post("/api/chat_agent", data="just-a-string", content_type="application/json").status_code == 400


# --------------------------------------------------------------------------
# H3: job fallback never blanks when only non-job files exist
# --------------------------------------------------------------------------

def test_job_fallback_skips_non_job_files(tmp_path, monkeypatch):
    """With an empty daily dir, load_job_listings must return monthly jobs,
    not 0 jobs from ecosystem_telemetry.json / recent.json."""
    import api.index as idx

    monthly = {"month": "May 2026", "jobs": [{"title": "AI Engineer", "company": "Acme"}]}
    job_data = tmp_path / "job_data"
    job_data.mkdir()
    (job_data / "ecosystem_telemetry.json").write_text('{"commit_history": 1136}', encoding="utf-8")
    (job_data / "recent.json").write_text('{"month": "Sep 2026", "models_used": {}}', encoding="utf-8")
    (job_data / "may-2026.json").write_text(json.dumps(monthly), encoding="utf-8")
    (job_data / "daily").mkdir()  # empty

    # job_data_dir is derived from index.py's __file__ -> redirect it
    monkeypatch.setattr(idx, "__file__", str(tmp_path / "api" / "index.py"))
    jobs, month, models_used, _report, _trace = idx.load_job_listings()
    assert len(jobs) == 1
    assert month == "May 2026"


def _load_job_server():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "job_server_under_test", os.path.join(ROOT, "scripts", "job_server.py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_verify_jobs_persists_to_source_file(tmp_path, monkeypatch):
    """verify_jobs must persist updates to each job's own source file (audit H5)."""
    try:
        mod = _load_job_server()
    except Exception:
        pytest.skip("job_server.py requires FastMCP extras not installed offline")

    monkeypatch.setattr(mod, "JOB_DATA_DIR", tmp_path)
    (tmp_path / "may-2026.json").write_text(json.dumps({"month": "May 2026", "jobs": [
        {"id": 1, "title": "AI Engineer", "company": "Acme", "apply_url": ""}
    ]}), encoding="utf-8")

    saved = {}
    monkeypatch.setattr(mod, "_save_jobs",
                        lambda jobs, source_file=None: saved.update({"jobs": jobs, "source_file": source_file}))

    mod.verify_jobs([1])
    assert saved["source_file"] == "may-2026.json"


def test_save_jobs_refuses_to_create_empty_month_file(tmp_path, monkeypatch):
    """_save_jobs must not materialize a brand-new (empty) month file (audit H5)."""
    try:
        mod = _load_job_server()
    except Exception:
        pytest.skip("job_server.py requires FastMCP extras not installed offline")

    monkeypatch.setattr(mod, "JOB_DATA_DIR", tmp_path)
    from datetime import datetime

    current_month_file = tmp_path / (datetime.now().strftime("%B-%Y").lower() + ".json")
    # jobs whose real source is a different month -> nothing to persist here
    mod._save_jobs([{"id": 1, "title": "X", "company": "Y", "_source_file": "may-2026.json"}])
    assert not current_month_file.exists()
