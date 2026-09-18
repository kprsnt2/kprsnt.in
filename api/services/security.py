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


def is_valid_email(email) -> bool:
    """Return True for a plausibly valid, non-empty email address."""
    if not email or not isinstance(email, str):
        return False
    email = email.strip()
    if len(email) > 254 or "\n" in email or "\r" in email:
        return False
    return bool(_EMAIL_RE.match(email))


def get_client_ip(request) -> str:
    """Return the best-guess client IP, honoring the first X-Forwarded-For hop.

    Falls back to remote_addr when no forwarding header is present.
    """
    xff = request.headers.get("X-Forwarded-For", "")
    if xff:
        first = xff.split(",")[0].strip()
        if first:
            return first
    return request.remote_addr or "unknown"


class RateLimiter:
    """Thread-safe fixed-window in-memory limiter with TTL pruning and a key cap."""

    def __init__(self, window_seconds: float, max_keys: int = 10000):
        self.window = window_seconds
        self.max_keys = max_keys
        self._hits = {}
        self._lock = threading.Lock()

    def _prune(self, now: float) -> None:
        cutoff = now - self.window
        self._hits = {k: t for k, t in self._hits.items() if t > cutoff}
        # Hard cap: evict the oldest entries if still over budget.
        if len(self._hits) > self.max_keys:
            for key in sorted(self._hits, key=lambda k: self._hits[k])[: len(self._hits) - self.max_keys]:
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
            last = self._hits.get(key)
            if last is not None and now - last < self.window:
                return False, max(0.0, self.window - (now - last))
            self._hits[key] = now
            return True, 0.0
