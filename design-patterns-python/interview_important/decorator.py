"""
** Decorator Pattern (Interview Important)
When to use: When you need to add responsibilities to objects dynamically without affecting other objects. Use when extending functionality via subclassing is impractical (too many combinations), or when behavior should be added/removed at runtime.

Real-world examples:
- Django middleware stack (authentication, session, CSRF, GZip)
- Python decorators (@cache, @lru_cache, @property)
- Flask extensions adding behavior to app/routes
- Java I/O streams (BufferedInputStream, GZIPInputStream, etc.)
- Express.js middleware pipeline
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from functools import wraps
from typing import Callable
import gzip
import io
import json
import re
import time
import uuid


class HttpRequest:
    def __init__(self, method: str, path: str, headers: dict | None = None, body: bytes | None = None, remote_ip: str = "127.0.0.1"):
        self.method = method.upper()
        self.path = path
        self.headers = headers or {}
        self.body = body or b""
        self.remote_ip = remote_ip
        self.request_id = str(uuid.uuid4())
        self.timestamp = datetime.now(timezone.utc)
        self.attributes: dict = {}

    @property
    def body_text(self) -> str:
        return self.body.decode("utf-8", errors="replace")

    def __repr__(self) -> str:
        return f"<HttpRequest {self.method} {self.path} [{self.request_id[:8]}]>"


@dataclass
class HttpResponse:
    status_code: int
    body: bytes
    headers: dict = field(default_factory=dict)
    content_type: str = "text/plain"

    @classmethod
    def ok(cls, body: str, content_type: str = "text/plain") -> "HttpResponse":
        return cls(status_code=200, body=body.encode("utf-8"), content_type=content_type)

    @classmethod
    def json(cls, data: dict) -> "HttpResponse":
        body = json.dumps(data, indent=2).encode("utf-8")
        return cls(status_code=200, body=body, content_type="application/json")

    @classmethod
    def error(cls, status_code: int, message: str) -> "HttpResponse":
        return cls(status_code=status_code, body=message.encode("utf-8"), content_type="text/plain")

    def __repr__(self) -> str:
        return f"<HttpResponse {self.status_code} ({len(self.body)} bytes)>"


class HttpHandler(ABC):
    @abstractmethod
    def handle(self, request: HttpRequest) -> HttpResponse:
        pass


class BaseHandler(HttpHandler):
    def __init__(self, inner: HttpHandler | None = None):
        self._inner = inner

    def handle(self, request: HttpRequest) -> HttpResponse:
        if self._inner:
            return self._inner.handle(request)
        return HttpResponse.error(404, "Not Found")


class LoggingMiddleware(BaseHandler):
    def handle(self, request: HttpRequest) -> HttpResponse:
        start = time.perf_counter()
        print(f"[Logging] --> {request.method} {request.path} [{request.request_id[:8]}] from {request.remote_ip}")

        response = super().handle(request)

        elapsed = (time.perf_counter() - start) * 1000
        print(f"[Logging] <-- {response.status_code} ({len(response.body)} bytes, {elapsed:.1f}ms)")
        response.headers["X-Request-Id"] = request.request_id
        response.headers["X-Response-Time-Ms"] = f"{elapsed:.1f}"
        return response


class AuthenticationMiddleware(BaseHandler):
    def __init__(self, inner: HttpHandler, valid_tokens: set[str] | None = None):
        super().__init__(inner)
        self._valid_tokens = valid_tokens or {"admin-token-123", "user-token-456"}

    def handle(self, request: HttpRequest) -> HttpResponse:
        auth_header = request.headers.get("Authorization", "")
        match = re.match(r"Bearer\s+(\S+)", auth_header)

        if not match:
            print(f"[Auth] Missing or malformed Authorization header")
            return HttpResponse.error(401, "Unauthorized: missing or malformed token")

        token = match.group(1)
        if token not in self._valid_tokens:
            print(f"[Auth] Invalid token: {token[:16]}...")
            return HttpResponse.error(403, "Forbidden: invalid token")

        request.attributes["user"] = "admin" if token.startswith("admin") else "user"
        print(f"[Auth] Authenticated as '{request.attributes['user']}'")
        return super().handle(request)


class RateLimitingMiddleware(BaseHandler):
    def __init__(self, inner: HttpHandler, max_requests: int = 5, window_seconds: int = 60):
        super().__init__(inner)
        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._buckets: dict[str, list[float]] = {}

    def handle(self, request: HttpRequest) -> HttpResponse:
        now = time.time()
        window_start = now - self._window_seconds

        bucket = self._buckets.setdefault(request.remote_ip, [])
        bucket[:] = [t for t in bucket if t > window_start]

        if len(bucket) >= self._max_requests:
            retry_after = int(bucket[0] + self._window_seconds - now)
            print(f"[RateLimit] Blocked {request.remote_ip}: {len(bucket)}/{self._max_requests} requests")
            resp = HttpResponse.error(429, f"Rate limit exceeded. Retry after {retry_after}s")
            resp.headers["Retry-After"] = str(retry_after)
            resp.headers["X-RateLimit-Limit"] = str(self._max_requests)
            resp.headers["X-RateLimit-Remaining"] = "0"
            return resp

        bucket.append(now)
        remaining = self._max_requests - len(bucket)
        response = super().handle(request)
        response.headers["X-RateLimit-Limit"] = str(self._max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response


class CompressionMiddleware(BaseHandler):
    MIN_SIZE = 512

    def handle(self, request: HttpRequest) -> HttpResponse:
        accepts_gzip = request.headers.get("Accept-Encoding", "").find("gzip") != -1
        response = super().handle(request)

        if accepts_gzip and len(response.body) > self.MIN_SIZE:
            buf = io.BytesIO()
            with gzip.GzipFile(fileobj=buf, mode="wb") as f:
                f.write(response.body)
            compressed = buf.getvalue()
            ratio = (1 - len(compressed) / len(response.body)) * 100
            print(f"[Compression] Compressed {len(response.body)} -> {len(compressed)} bytes ({ratio:.1f}% reduction)")
            response.body = compressed
            response.headers["Content-Encoding"] = "gzip"

        return response


class CORSMiddleware(BaseHandler):
    def __init__(self, inner: HttpHandler, allowed_origins: set[str] | None = None):
        super().__init__(inner)
        self._allowed_origins = allowed_origins or {"*"}

    def handle(self, request: HttpRequest) -> HttpResponse:
        origin = request.headers.get("Origin", "")
        if request.method == "OPTIONS":
            print(f"[CORS] Preflight for origin: {origin}")
            resp = HttpResponse.ok("")
            resp.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            resp.headers["Access-Control-Max-Age"] = "3600"
        else:
            resp = super().handle(request)

        if "*" in self._allowed_origins or origin in self._allowed_origins:
            resp.headers["Access-Control-Allow-Origin"] = origin if origin else "*"
        return resp


class Router(HttpHandler):
    def __init__(self):
        self._routes: list[tuple[str, str, Callable[[HttpRequest], HttpResponse]]] = []

    def get(self, path: str, handler: Callable[[HttpRequest], HttpResponse]) -> None:
        self._routes.append(("GET", path, handler))

    def post(self, path: str, handler: Callable[[HttpRequest], HttpResponse]) -> None:
        self._routes.append(("POST", path, handler))

    def handle(self, request: HttpRequest) -> HttpResponse:
        for method, path, handler in self._routes:
            if request.method == method and self._match_path(path, request.path):
                print(f"[Router] Matched {request.method} {request.path} -> {handler.__name__}")
                return handler(request)
        return HttpResponse.error(404, f"Not Found: {request.method} {request.path}")

    @staticmethod
    def _match_path(pattern: str, path: str) -> bool:
        pattern_parts = pattern.strip("/").split("/")
        path_parts = path.strip("/").split("/")
        if len(pattern_parts) != len(path_parts):
            return False
        for p, q in zip(pattern_parts, path_parts):
            if p.startswith("{") and p.endswith("}"):
                continue
            if p != q:
                return False
        return True


def build_middleware_stack(inner: HttpHandler) -> HttpHandler:
    stack = inner
    stack = CompressionMiddleware(stack)
    stack = RateLimitingMiddleware(stack, max_requests=10, window_seconds=30)
    stack = AuthenticationMiddleware(stack)
    stack = CORSMiddleware(stack)
    stack = LoggingMiddleware(stack)
    return stack


if __name__ == "__main__":
    router = Router()

    router.get("/api/health", lambda req: HttpResponse.json({"status": "ok", "service": "api"}))
    router.get("/api/users/{id}", lambda req: HttpResponse.json({"user_id": req.path.split("/")[-1], "name": "Alice", "role": "admin"}))
    router.post("/api/data", lambda req: HttpResponse.json({"received": True, "data": req.body_text[:200], "length": len(req.body)}))

    app = build_middleware_stack(router)

    requests = [
        HttpRequest("GET", "/api/health", {"Authorization": "Bearer admin-token-123", "Accept-Encoding": "gzip"}),
        HttpRequest("GET", "/api/users/42", {"Authorization": "Bearer user-token-456", "Accept-Encoding": "gzip"}),
        HttpRequest("POST", "/api/data", {"Authorization": "Bearer admin-token-123", "Content-Type": "application/json"}, json.dumps({"message": "Hello, world!", "nested": {"key": "value"}}).encode(), "10.0.0.1"),
        HttpRequest("GET", "/api/health", {"Authorization": "Bearer bad-token"}, remote_ip="10.0.0.2"),
        HttpRequest("GET", "/api/health", {"Authorization": "Bearer admin-token-123"}, remote_ip="10.0.0.3"),
    ]

    for i, req in enumerate(requests):
        print(f"\n{'='*60}")
        print(f"Request #{i+1}: {req.method} {req.path}")
        print(f"{'='*60}")
        resp = app.handle(req)
        print(f"Result: {resp.status_code} [{resp.content_type}]")
        if resp.headers:
            notable = {k: v for k, v in resp.headers.items() if k.startswith("X-") or k in ("Retry-After", "Content-Encoding")}
            if notable:
                print(f"Headers: {notable}")
        print(f"Body preview: {resp.body[:120].decode('utf-8', errors='replace')}...")

