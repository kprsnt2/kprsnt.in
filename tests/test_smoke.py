"""
Smoke tests for the kprsnt.in Flask app.

These run offline (no LLM calls) and assert that every public page and data
route renders without a server error, and that basic input validation and the
OAuth open-redirect guard hold.
"""
import os
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


PAGES = [
    "/",
    "/skills",
    "/projects",
    "/resume",
    "/resume/edit",
    "/blog",
    "/aie",
    "/aie/blogs",
    "/ecosystem",
    "/ecosystem/logs",
    "/mcp",
    "/docs",
    "/api/docs",
    "/jobs",
    "/jobs/dashboard",
    "/plotter",
    "/dashboard",
    "/case-studies",
    "/case-study/jobagents",
]

APIS = [
    "/api/blogs",
    "/api/case-studies",
    "/api/hiring-evidence",
    "/api/mseat/openapi.json",
]


@pytest.mark.parametrize("path", PAGES)
def test_pages_render(client, path):
    response = client.get(path)
    assert response.status_code == 200, f"{path} -> {response.status_code}"


@pytest.mark.parametrize("path", APIS)
def test_data_apis(client, path):
    response = client.get(path)
    assert response.status_code == 200, f"{path} -> {response.status_code}"


def test_mseat_predict(client):
    response = client.get("/api/mseat/predict?category=OC&state_rank=3000")
    assert response.status_code == 200
    assert response.get_json().get("success") is True


def test_mseat_colleges(client):
    response = client.get("/api/mseat/colleges?query=Gandhi")
    assert response.status_code == 200


def test_unknown_page_is_404(client):
    assert client.get("/definitely-not-a-page-xyz").status_code == 404


def test_chat_rejects_empty_query(client):
    response = client.post("/api/chat", json={})
    assert response.status_code == 400


def test_interview_rejects_empty_message(client):
    response = client.post("/api/interview", json={})
    assert response.status_code == 400


def test_robots_and_sitemap(client):
    robots = client.get("/robots.txt")
    assert robots.status_code == 200
    assert b"Sitemap:" in robots.data

    sitemap = client.get("/sitemap.xml")
    assert sitemap.status_code == 200
    assert b"<urlset" in sitemap.data


def test_oauth_blocks_open_redirect(client):
    response = client.get(
        "/api/oauth/authorize?redirect_uri=https://evil.example/steal"
    )
    assert response.status_code == 200
    assert "Location" not in response.headers


def test_ecosystem_logs_structure(client):
    from scripts.ecosystem_agents import SWARM_SIZE

    response = client.get("/ecosystem/logs")
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "Swarm Logs &amp; Council" in html or "Swarm Logs & Council" in html
    assert f"{SWARM_SIZE} Registered Agents" in html
    assert html.count("Latest Live Output / Action") == SWARM_SIZE
    assert html.count("col-lg-6") >= SWARM_SIZE


def test_homepage_analytical_and_ai_positioning(client):
    """Home page showcases the interactive System Atlas, Command Palette, and live workbenches without duplicate CTA bugs."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "INTERACTIVE SYSTEM ATLAS" in html
    assert "GCP Cloud Run (asia-south1)" in html
    assert "18-Sector Automated ETL" in html
    assert "rAsh Score" in html
    assert "cmdPaletteBackdrop" in html
    assert html.count("Open Fleet Command Center →") == 1


# ---------------------------------------------------------------------------
# Recruiter-facing guarantees (2026-11 audit)
# ---------------------------------------------------------------------------

def _internal_links(html):
    import re

    links = set()
    for href in re.findall(r'href="(/[^"#?]*)', html):
        if not href.startswith(("/static/", "//")):
            links.add(href)
    return links


@pytest.mark.parametrize("page", ["/", "/projects", "/dashboard", "/case-studies", "/blog", "/resume"])
def test_no_dead_internal_links(client, page):
    """Every internal link on the main pages resolves (the home page once shipped three 404s)."""
    html = client.get(page).data.decode("utf-8")
    dead = sorted(
        link for link in _internal_links(html)
        if client.get(link, follow_redirects=True).status_code >= 400
    )
    assert not dead, f"{page} links to missing pages: {dead}"


def test_home_states_held_title_and_direction(client):
    html = client.get("/").data.decode("utf-8")
    assert "Data Analyst" in html and "AI Engineering" in html
    assert "mailto:interview@kprsnt.in" in html


def test_every_case_study_renders(client):
    from api.data.case_studies import get_all_case_studies

    for study in get_all_case_studies():
        response = client.get(f"/case-study/{study['slug']}")
        assert response.status_code == 200, study["slug"]
    assert client.get("/case-study/not-a-real-study").status_code == 404


def test_blog_lists_articles_not_agent_logs(client):
    html = client.get("/blog").data.decode("utf-8")
    assert "/blog/BLOG_MODEL_VS_CLI" in html
    assert "/blog/github-activity-" not in html
    assert "/aie/blog/github-activity-" not in html
    # Unlisted posts stay reachable by URL.
    assert 'href="/blog/sample"' not in html
    assert client.get("/blog/sample").status_code == 200


def test_agent_log_has_one_url(client):
    from api.index import load_ai_eco_blogs

    slug = load_ai_eco_blogs()[0]["slug"]
    response = client.get(f"/blog/{slug}")
    assert response.status_code == 301
    assert response.headers["Location"].endswith(f"/aie/blog/{slug}")
    assert client.get(f"/aie/blog/{slug}").status_code == 200


@pytest.mark.parametrize("path", ["/jobs", "/jobs/dashboard", "/resume/edit"])
def test_private_pages_are_noindex(client, path):
    assert "noindex" in client.get(path).headers.get("X-Robots-Tag", "")


def test_job_search_output_is_not_public(client):
    """The public dashboard, nav and sitemap must not surface personal job-search data."""
    dashboard = client.get("/dashboard")
    assert "X-Robots-Tag" not in dashboard.headers
    assert "Career Agent Pipeline Analytics" not in dashboard.data.decode("utf-8")
    assert "Career Agent Pipeline Analytics" in client.get("/jobs/dashboard").data.decode("utf-8")

    home = client.get("/").data.decode("utf-8")
    assert 'href="/jobs' not in home

    sitemap = client.get("/sitemap.xml").data.decode("utf-8")
    assert "kprsnt.in/jobs" not in sitemap
    assert "kprsnt.in/case-study/jobagents" in sitemap


def test_unknown_resume_slug_is_404(client):
    assert client.get("/resume/data-ai-engineer").status_code == 200
    assert client.get("/resume/not-a-role").status_code == 404


def test_print_resume_matches_site_data(client):
    """The PDF source renders the same employment data as /resume, with held titles only."""
    from api.data.projects import EXPERIENCES

    response = client.get("/resume/print")
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    for exp in EXPERIENCES:
        assert exp["period"] in html, exp["company"]
    assert "Optum" in html
    assert "Independent Projects" in html
    # Claims the old hand-written PDF carried that the data modules had removed as unsourced.
    for stale in ("AI Systems Engineer", "60%", "Power BI", "ARIMA", "26 tools", "arXiv"):
        assert stale not in html, stale

    legacy = client.get("/static/resume_pdf.html")
    assert legacy.status_code == 301
    assert legacy.headers["Location"].endswith("/resume/print")


def test_swarm_logs_has_a_single_h1(client):
    import re

    html = client.get("/ecosystem/logs").data.decode("utf-8")
    assert len(re.findall(r"<h1[\s>]", html)) == 1


def test_jobs_api_requires_private_token(client, monkeypatch):
    monkeypatch.delenv("PRIVATE_API_TOKEN", raising=False)
    assert client.get("/api/jobs/data").status_code == 404
    # An empty expected token must never match an empty header.
    assert client.get("/api/jobs/data", headers={"X-Private-Token": ""}).status_code == 404

    monkeypatch.setenv("PRIVATE_API_TOKEN", "s3cret")
    assert client.get("/api/jobs/data").status_code == 404
    assert client.get("/api/jobs/data", headers={"X-Private-Token": "wrong"}).status_code == 404
    ok = client.get("/api/jobs/data", headers={"X-Private-Token": "s3cret"})
    assert ok.status_code == 200 and "jobs" in ok.get_json()


def test_bot_only_emails_for_the_trusted_webhook(client, monkeypatch):
    """A public caller cannot make the server email an address of their choosing."""
    import api.index as index

    sent, tool_flags = [], []
    monkeypatch.setattr(index, "send_reply_email", lambda *a, **k: sent.append(a) or True)
    monkeypatch.setattr(index, "notify_owner", lambda *a, **k: None)
    monkeypatch.setattr(
        index, "get_ai_response",
        lambda *a, **k: tool_flags.append(k.get("allow_email_tool")) or "hello",
    )
    monkeypatch.setattr(index, "_email_limiter", index.RateLimiter(60, 100))
    body = {"message": "hi", "from_email": "victim@example.com", "send_email": True}

    for path in ("/api/interview", "/api/chat_agent"):
        monkeypatch.delenv("EMAIL_WEBHOOK_SECRET", raising=False)
        response = client.post(path, json=body)
        assert response.status_code == 200 and response.get_json()["email_sent"] is False
        # Form posts used to force send_email on.
        client.post(path, data={"text": "hi", "from": "victim@example.com"})

        monkeypatch.setenv("EMAIL_WEBHOOK_SECRET", "hook")
        client.post(path, json=body, headers={"X-Email-Webhook-Secret": "nope"})
        assert sent == [] and not any(tool_flags), path

        trusted = client.post(path, json=body, headers={"X-Email-Webhook-Secret": "hook"})
        assert trusted.get_json()["email_sent"] is True
        assert len(sent) == 1 and tool_flags[-1] is True
        sent.clear()
        tool_flags.clear()


def test_public_bots_and_mcp_do_not_leak_private_details(client):
    from api.bot_utils import get_system_prompt

    for agent in ("interview", "chat"):
        prompt = get_system_prompt(agent)
        for private in ("12,70,500", "30L", "70k USD", "LIVE JOB PIPELINE DATA", "jobs applied to"):
            assert private not in prompt, f"{agent}: {private}"

    for tool in ("get_my_profile", "get_my_resume", "get_my_skills"):
        response = client.post("/api/mcp", json={
            "jsonrpc": "2.0", "id": 1, "method": "tools/call",
            "params": {"name": tool, "arguments": {}},
        })
        text = response.get_data(as_text=True)
        assert "phone" not in text and "+91" not in text, tool
        assert "zohomail" not in text and "live.com" not in text, tool
        assert "Expert" not in text, tool


def test_site_uses_role_addresses_not_the_personal_one(client):
    for page in ("/", "/resume", "/projects", "/case-study/jobagents"):
        html = client.get(page).data.decode("utf-8")
        assert "zohomail" not in html and "live.com" not in html, page
    assert "interview@kprsnt.in" in client.get("/resume").data.decode("utf-8")
    # The resume document itself carries the personal address, and no phone
    # number unless RESUME_PHONE is set at build time.
    printable = client.get("/resume/print").data.decode("utf-8")
    assert "kprsnt@zohomail.in" in printable
    assert "+91" not in printable


def test_csp_allows_the_scripts_pages_load(client):
    """Every external script host used by a template must be in script-src."""
    import glob
    import re
    from urllib.parse import urlparse

    csp = client.get("/").headers["Content-Security-Policy"]
    script_src = next(part for part in csp.split(";") if part.strip().startswith("script-src"))
    hosts = set()
    for template in glob.glob(os.path.join(ROOT, "templates", "*.html")):
        with open(template, encoding="utf-8") as fh:
            text = fh.read()
        for url in re.findall(r"<script[^>]+src=\"(https://[^\"]+)\"", text):
            hosts.add(urlparse(url).netloc)
        for url in re.findall(r"import\s+\w+\s+from\s+'(https://[^']+)'", text):
            hosts.add(urlparse(url).netloc)
    missing = sorted(host for host in hosts if f"https://{host}" not in script_src)
    assert not missing, f"script-src is missing: {missing}"


def test_mcp_messages_rejects_oversized_body(client):
    response = client.post(
        "/api/mcp/messages",
        data=b"x" * (1_048_576 + 10),
        content_type="application/json",
    )
    assert response.status_code == 413

