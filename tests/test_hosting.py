"""
Hosting behaviour for the Cloud Run + Cloudflare deployment: static asset
caching, the favicon, the PWA manifest icons, canonical-host redirects, and
keeping the OpenAI SDK off the cold-start import path.
"""
import os
import re
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "api"))


@pytest.fixture(scope="module")
def client():
    from api.index import app

    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_pages_link_content_hashed_assets(client):
    html = client.get("/").get_data(as_text=True)
    assets = re.findall(r'(?:href|src)="(/static/(?:css|js)/[^"]+)"', html)
    assert assets, "expected the layout to link CSS/JS from /static"
    for url in assets:
        assert re.search(r"\?v=[0-9a-f]{10}$", url), url


def test_versioned_static_is_cached_for_a_year(client):
    html = client.get("/").get_data(as_text=True)
    url = re.search(r'href="(/static/css/custom\.css\?v=[0-9a-f]+)"', html).group(1)
    resp = client.get(url)
    assert resp.status_code == 200
    assert resp.headers["Cache-Control"] == "public, max-age=31536000, immutable"


def test_unversioned_static_gets_a_day(client):
    resp = client.get("/static/css/custom.css")
    assert resp.status_code == 200
    assert "max-age=86400" in resp.headers["Cache-Control"]
    assert "no-cache" not in resp.headers["Cache-Control"]


def test_html_still_revalidates(client):
    assert client.get("/").headers["Cache-Control"] == "no-cache"


def test_favicon_ico_is_served(client):
    resp = client.get("/favicon.ico")
    assert resp.status_code == 200
    assert resp.data[:4] == b"\x00\x00\x01\x00"  # ICO magic


def test_manifest_icons_exist(client):
    icons = client.get("/manifest.webmanifest").get_json()["icons"]
    sizes = {i["sizes"] for i in icons}
    assert {"192x192", "512x512"} <= sizes
    for icon in icons:
        assert client.get(icon["src"]).status_code == 200, icon["src"]


@pytest.mark.parametrize("host", ["www.kprsnt.in", "kprsnt-in-abc123-el.a.run.app"])
def test_off_canonical_hosts_redirect(client, host):
    resp = client.get("/blog?page=2", headers={"Host": host})
    assert resp.status_code == 308
    assert resp.headers["Location"] == "https://kprsnt.in/blog?page=2"


def test_api_posts_keep_method_on_redirect(client):
    resp = client.post("/api/chat", json={}, headers={"Host": "www.kprsnt.in"})
    assert resp.status_code == 308


def test_run_app_via_cloudflare_is_not_redirected(client):
    # Cloudflare may send the run.app Host header to reach Cloud Run; those
    # requests must be served, or the site would redirect-loop.
    resp = client.get("/", headers={"Host": "kprsnt-in-abc123-el.a.run.app", "CF-Ray": "abc-IAD"})
    assert resp.status_code == 200


def test_health_is_never_redirected(client):
    resp = client.get("/health", headers={"Host": "kprsnt-in-abc123-el.a.run.app"})
    assert resp.status_code == 200


def test_canonical_host_is_served(client):
    assert client.get("/", headers={"Host": "kprsnt.in"}).status_code == 200


def test_openai_sdk_not_imported_at_startup():
    code = "import sys; import api.index; print('openai' in sys.modules)"
    out = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True,
                         text=True, check=True).stdout.strip()
    assert out == "False"
