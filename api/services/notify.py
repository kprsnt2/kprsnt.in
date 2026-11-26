"""Tell Prashanth by email when someone uses the site's chat bots.

The app still sends no email itself. It POSTs the question and the AI answer
to the Cloudflare worker in ``cloudflare/email-worker/`` (its ``/notify``
route), which mails them to the owner from chat@kprsnt.in.

Off unless both ``CHAT_NOTIFY_URL`` and ``CHAT_NOTIFY_SECRET`` are set. The
call is synchronous with a short timeout: Cloud Run throttles CPU once a
response is sent, so a background thread could stall. A failure is logged and
never breaks the chat reply.
"""
import logging
import os

import httpx

logger = logging.getLogger(__name__)

# Requests the email worker makes carry this header; the owner already gets a
# copy of those conversations by email, so they are not notified twice.
EMAIL_WORKER_HEADER = "X-Kprsnt-Source"
EMAIL_WORKER_VALUE = "email-worker"

_TIMEOUT = 4.0


def notify_owner(source, message, answer, request_headers=None):
    """Send one chat exchange to the owner. Returns True if it was delivered."""
    url = os.environ.get("CHAT_NOTIFY_URL", "").strip()
    secret = os.environ.get("CHAT_NOTIFY_SECRET", "").strip()
    if not url or not secret:
        return False
    if request_headers is not None and \
            request_headers.get(EMAIL_WORKER_HEADER, "") == EMAIL_WORKER_VALUE:
        return False
    payload = {
        "source": str(source)[:40],
        "message": str(message or "")[:4000],
        "answer": str(answer or "")[:8000],
    }
    try:
        resp = httpx.post(url, json=payload, headers={"X-Notify-Secret": secret},
                          timeout=_TIMEOUT)
        if resp.status_code != 200:
            logger.warning("chat notify returned HTTP %s", resp.status_code)
            return False
        return True
    except Exception as exc:  # network trouble must never break the chat
        logger.warning("chat notify failed: %s", exc)
        return False
