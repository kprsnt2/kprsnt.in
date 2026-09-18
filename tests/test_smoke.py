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
]

APIS = [
    "/api/blogs",
    "/api/case-studies",
    "/api/hiring-evidence",
    "/api/jobs/data",
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
