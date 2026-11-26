"""Owner notifications for chat-bot questions (api/services/notify.py).

The app must stay silent unless both settings are present, send the shared
secret to the worker, never notify twice for the email worker's own calls, and
never let a notification failure break the chat answer.
"""
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "api"))

from api.services import notify  # noqa: E402


class _Resp:
    def __init__(self, status):
        self.status_code = status


@pytest.fixture
def calls(monkeypatch):
    sent = []

    def fake_post(url, json=None, headers=None, timeout=None):
        sent.append({"url": url, "json": json, "headers": headers, "timeout": timeout})
        return _Resp(200)

    monkeypatch.setattr(notify.httpx, "post", fake_post)
    return sent


@pytest.fixture
def configured(monkeypatch):
    monkeypatch.setenv("CHAT_NOTIFY_URL", "https://worker.example/notify")
    monkeypatch.setenv("CHAT_NOTIFY_SECRET", "s3cret-value")


@pytest.mark.parametrize("url,secret", [("", ""), ("https://w/notify", ""), ("", "x")])
def test_off_unless_url_and_secret_set(monkeypatch, calls, url, secret):
    monkeypatch.setenv("CHAT_NOTIFY_URL", url)
    monkeypatch.setenv("CHAT_NOTIFY_SECRET", secret)
    assert notify.notify_owner("site", "hi", "hello") is False
    assert calls == []


def test_sends_question_answer_and_secret(configured, calls):
    assert notify.notify_owner("site chat", "What stack?", "Python + BigQuery", {}) is True
    assert len(calls) == 1
    c = calls[0]
    assert c["url"] == "https://worker.example/notify"
    assert c["headers"] == {"X-Notify-Secret": "s3cret-value"}
    assert c["json"] == {"source": "site chat", "message": "What stack?", "answer": "Python + BigQuery"}
    assert c["timeout"] and c["timeout"] <= 5


def test_skips_email_worker_requests(configured, calls):
    headers = {"X-Kprsnt-Source": "email-worker"}
    assert notify.notify_owner("site", "q", "a", headers) is False
    assert calls == []


def test_truncates_long_text(configured, calls):
    notify.notify_owner("s" * 100, "q" * 10000, "a" * 20000, {})
    body = calls[0]["json"]
    assert len(body["source"]) == 40 and len(body["message"]) == 4000 and len(body["answer"]) == 8000


def test_network_error_is_swallowed(configured, monkeypatch):
    def boom(*a, **k):
        raise notify.httpx.ConnectError("down")
    monkeypatch.setattr(notify.httpx, "post", boom)
    assert notify.notify_owner("site", "q", "a", {}) is False


def test_chat_agent_notifies_with_the_real_answer(configured, calls, monkeypatch):
    import api.index as index
    monkeypatch.setattr(index, "get_ai_response", lambda message, **kw: f"answer to {message}")
    index.app.config.update(TESTING=True)
    with index.app.test_client() as client:
        r = client.post("/api/chat_agent", json={"message": "Is he open to remote work?"},
                        headers={"CF-Connecting-IP": "203.0.113.77"})
        assert r.status_code == 200
        r2 = client.post("/api/chat_agent", json={"message": "from email"},
                         headers={"CF-Connecting-IP": "203.0.113.78",
                                  "X-Kprsnt-Source": "email-worker"})
        assert r2.status_code == 200
    assert [c["json"]["message"] for c in calls] == ["Is he open to remote work?"]
    assert calls[0]["json"]["answer"] == "answer to Is he open to remote work?"
