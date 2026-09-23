"""
Shared security helpers: client IP normalization, in-memory rate limiting,
and email validation.

The rate limiter is intentionally dependency-free. On serverless (Vercel) each
warm instance keeps its own window, so this is best-effort abuse mitigation, not
a hard global quota. For global limits, swap in Vercel KV / Upstash.
"""
import re
import time
import threading

# Pragmatic email shape check (not full RFC 5322). Rejects obvious junk while
# allowing normal addresses.
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")


# Maximum accepted request body for public JSON-RPC endpoints (~1 MB).
MAX_MCP_BODY_BYTES = 1_048_576


def body_exceeds_limit(request, max_bytes: int = MAX_MCP_BODY_BYTES) -> bool:
    """Return True when the request body exceeds ``max_bytes``.

    Relies on Content-Length, which every HTTP client sets. Routes should
    reject before parsing to bound memory/CPU per request.
    """
    length = request.content_length
    return bool(length) and length > max_bytes


def is_valid_email(email) -> bool:
    """Return True for a plausibly valid, non-empty email address."""
    if not email or not isinstance(email, str):
        return False
    email = email.strip()
    if len(email) > 254 or "\n" in email or "\r" in email:
        return False
    return bool(_EMAIL_RE.match(email))


def get_client_ip(request) -> str:
    """Return the best-guess client IP for rate-limit keying.

    Trusts the platform-provided ``X-Real-IP`` first (Vercel sets it), then
    the LAST ``X-Forwarded-For`` hop (appended by the trusted proxy). The
    first XFF hop is client-controlled and can be spoofed to rotate
    rate-limit keys, so it is never used. Falls back to remote_addr.
    """
    real = request.headers.get("X-Real-IP", "").strip()
    if real:
        return real
    xff = request.headers.get("X-Forwarded-For", "")
    if xff:
        last = xff.split(",")[-1].strip()
        if last:
            return last
    return request.remote_addr or "unknown"


class RateLimiter:
    """Thread-safe sliding-window in-memory limiter with TTL pruning and a key cap.

    Allows up to ``max_requests`` hits per ``window_seconds`` (e.g.
    ``RateLimiter(60, 60)`` = 60 requests/minute), instead of enforcing a
    fixed minimum interval between requests. On serverless (Vercel) each
    warm instance keeps its own window, so this is best-effort abuse
    mitigation, not a hard global quota. For global limits, swap in
    Vercel KV / Upstash.
    """

    def __init__(self, window_seconds: float, max_requests: int = 60, max_keys: int = 10000):
        self.window = window_seconds
        self.max_requests = max_requests
        self.max_keys = max_keys
        self._hits = {}  # key -> list of hit timestamps within the window
        self._lock = threading.Lock()

    def _prune(self, now: float) -> None:
        self._hits = {k: [t for t in ts if t > now - self.window]
                      for k, ts in self._hits.items() if ts and max(ts) > now - self.window}
        # Hard cap: evict the oldest entries if still over budget.
        if len(self._hits) > self.max_keys:
            for key in sorted(self._hits, key=lambda k: max(self._hits[k]))[:len(self._hits) - self.max_keys]:
                self._hits.pop(key, None)

    def check(self, key: str):
        """Record a hit for ``key``.

        Returns ``(allowed, retry_after_seconds)``. When ``allowed`` is False the
        caller should respond 429 and may include ``retry_after_seconds``.
        """
        now = time.time()
        with self._lock:
            if len(self._hits) > self.max_keys:
                self._prune(now)
            hits = [t for t in self._hits.get(key, []) if t > now - self.window]
            if len(hits) >= self.max_requests:
                self._hits[key] = hits
                return False, max(0.0, hits[0] + self.window - now)
            hits.append(now)
            self._hits[key] = hits
            return True, 0.0
