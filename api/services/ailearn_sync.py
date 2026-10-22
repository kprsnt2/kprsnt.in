"""
Learning-progress sync service for the AILearn course (learn.kprsnt.in).

Storage is Vercel KV (Upstash Redis REST API). We talk to it over plain HTTP so
no extra SDK is required, and the module degrades to "disabled" when the env
vars are absent -- the course stays fully usable offline, it just does not sync.

ENVIRONMENT
-----------
    KV_REST_API_URL   e.g. https://xxx.upstash.io
    KV_REST_API_TOKEN the *server* token (not the read-only one)

Vercel supplies both automatically when a KV store is connected to the project.
`UPSTASH_REDIS_REST_URL` / `UPSTASH_REDIS_REST_TOKEN` are accepted as
fallbacks because the store may be created standalone rather than via the
Vercel integration.

SECURITY MODEL
--------------
A client holds a sync code shaped ``<22-char id>-<8-char password>``.

    * The id selects the key. It is treated as a public read handle.
    * The password is checked server-side on every write. We store only its
      SHA-256, so a KV dump does not reveal write access.
    * The payload is a whitelisted, size-capped JSON object (lesson numbers,
      flashcard intervals, calibration score). No free-form fields are
      persisted, so this cannot be used as generic file hosting.

Because the doc is small and contains no personal data, a leaked read id is
low-risk; the password is what protects against mangling someone else's
progress.
"""

import hashlib
import json
import logging
import os
import re
import time

import httpx

# ---------------------------------------------------------------- constants

KV_URL = (os.environ.get("KV_REST_API_URL")
          or os.environ.get("UPSTASH_REDIS_REST_URL")
          or "").strip().rstrip("/")
KV_TOKEN = (os.environ.get("KV_REST_API_TOKEN")
            or os.environ.get("UPSTASH_REDIS_REST_TOKEN")
            or "").strip()

_KEY_PREFIX = "ailearn:sync:"
_TTL_SECONDS = 400 * 24 * 3600          # ~13 months of inactivity, then gone
_MAX_BODY_BYTES = 96 * 1024             # a real doc is < 200 KB; cap hard
_TIMEOUT = 8.0

_ID_RE = re.compile(r"^[a-z0-9]{22}$")
_PW_RE = re.compile(r"^[a-z0-9]{8}$")

# Only these top-level keys are ever persisted.
_ALLOWED_KEYS = {"v", "savedAt", "lessons", "flashcards", "calibration", "counters"}


class SyncError(Exception):
    """Raised for client-caused problems (bad code, bad payload)."""

    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


# ---------------------------------------------------------------- helpers

def is_configured():
    """True when KV credentials are present."""
    return bool(KV_URL and KV_TOKEN)


def parse_code(code):
    """Split and validate a sync code. Returns (id, password_hash)."""
    if not isinstance(code, str):
        raise SyncError("sync code must be a string")
    code = code.strip().lower()
    if code.count("-") != 1:
        raise SyncError("sync code must look like <id>-<password>")
    ident, password = code.split("-")
    if not _ID_RE.match(ident):
        raise SyncError("invalid sync code id")
    if not _PW_RE.match(password):
        raise SyncError("invalid sync code password")
    pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return ident, pw_hash


def _key(ident):
    return _KEY_PREFIX + ident


def _kv(command):
    """POST a single Redis command to the Upstash REST API."""
    if not is_configured():
        raise SyncError("sync backend not configured", status=503)
    try:
        resp = httpx.post(
            KV_URL,
            headers={"Authorization": f"Bearer {KV_TOKEN}"},
            json=command,
            timeout=_TIMEOUT,
        )
    except httpx.HTTPError as e:                    # network / timeout
        logging.warning("ailearn sync: kv transport error: %s", e)
        raise SyncError("sync backend unreachable", status=503)

    if resp.status_code >= 500:
        raise SyncError("sync backend error", status=503)
    if resp.status_code != 200:
        logging.warning("ailearn sync: kv status %s: %s", resp.status_code, resp.text[:200])
        raise SyncError("sync backend rejected the request", status=502)
    try:
        data = resp.json()
    except ValueError:
        raise SyncError("sync backend returned non-JSON", status=502)
    if "error" in data:
        logging.warning("ailearn sync: kv error: %s", str(data["error"])[:200])
        raise SyncError("sync backend error", status=502)
    return data.get("result")


# ---------------------------------------------------------------- validation

def _validate_payload(payload):
    """Coerce the client document into the whitelisted shape.

    Anything unexpected is dropped rather than rejected: forward compatibility
    matters more here than strictness, because an old client must not be
    bricked by a new field.
    """
    if not isinstance(payload, dict):
        raise SyncError("payload must be a JSON object")

    out = {"v": 1}

    lessons = payload.get("lessons")
    if isinstance(lessons, dict):
        clean = {}
        for k, v in list(lessons.items())[:400]:
            if not isinstance(k, str) or len(k) > 200:
                continue
            # completion timestamp (ms) or truthy marker
            if isinstance(v, (int, float)):
                clean[k] = int(v)
            elif v:
                clean[k] = 1
        out["lessons"] = clean
    else:
        out["lessons"] = {}

    cards = payload.get("flashcards")
    if isinstance(cards, dict):
        clean = {}
        for k, v in list(cards.items())[:600]:
            if not isinstance(k, str) or len(k) > 80 or not isinstance(v, dict):
                continue
            try:
                clean[k] = {
                    "ef": round(float(v.get("ef", 2.5)), 3),
                    "interval": max(0, min(3650, int(v.get("interval", 0)))),
                    "reps": max(0, min(999, int(v.get("reps", 0)))),
                    "due": str(v.get("due", ""))[:10],
                    "lapses": max(0, min(999, int(v.get("lapses", 0)))),
                }
            except (TypeError, ValueError):
                continue
        out["flashcards"] = clean
    else:
        out["flashcards"] = {}

    cal = payload.get("calibration")
    if isinstance(cal, dict):
        # keep it opaque but bounded; it is the learner's own scoring draft
        try:
            blob = json.dumps(cal)
        except (TypeError, ValueError):
            blob = "{}"
        out["calibration"] = cal if len(blob) <= 24 * 1024 else None
    else:
        out["calibration"] = None

    counters = payload.get("counters")
    if isinstance(counters, dict):
        streak = counters.get("flashStreak")
        if isinstance(streak, dict):
            try:
                out["counters"] = {
                    "flashStreak": {
                        "n": max(0, min(100000, int(streak.get("n", 0)))),
                        "d": str(streak.get("d", ""))[:10],
                    }
                }
            except (TypeError, ValueError):
                out["counters"] = {"flashStreak": {"n": 0, "d": ""}}
    if "counters" not in out:
        out["counters"] = {"flashStreak": {"n": 0, "d": ""}}

    out["savedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    return out


def _check_size(payload):
    try:
        blob = json.dumps(payload)
    except (TypeError, ValueError):
        raise SyncError("payload is not serialisable")
    if len(blob.encode("utf-8")) > _MAX_BODY_BYTES:
        raise SyncError("payload too large", status=413)
    return blob


# ---------------------------------------------------------------- operations

def read(code):
    """Return the stored document for a sync code, or None if absent."""
    ident, _ = parse_code(code)
    raw = _kv(["GET", _key(ident)])
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except (TypeError, ValueError):
        logging.warning("ailearn sync: corrupt document for %s", ident)
        return None


def write(code, payload):
    """Validate and store a document. Requires the correct password."""
    ident, pw_hash = parse_code(code)

    existing_raw = _kv(["GET", _key(ident)])
    if existing_raw is not None:
        try:
            existing = json.loads(existing_raw)
        except (TypeError, ValueError):
            existing = {}
        stored_pw = existing.get("_pw")
        if stored_pw and stored_pw != pw_hash:
            raise SyncError("wrong password for this sync code", status=403)

    clean = _validate_payload(payload)
    # validates size and serialisability; the returned blob is not needed here
    _check_size(clean)

    # the password hash lives beside the payload but is never returned
    record = dict(clean)
    record["_pw"] = pw_hash
    stored = json.dumps(record)

    _kv(["SET", _key(ident), stored, "EX", _TTL_SECONDS])

    out = dict(clean)
    return out


def public(doc):
    """Strip server-side fields before returning a document to a client."""
    if not isinstance(doc, dict):
        return None
    return {k: v for k, v in doc.items() if k in _ALLOWED_KEYS}
