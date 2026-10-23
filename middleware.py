import time
from collections import Counter
from threading import Lock
from uuid import uuid4
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

_counts: Counter[str] = Counter()
_lock = Lock()

class RequestMetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid4())
        started = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - started
        with _lock:
            _counts["requests_total"] += 1
            _counts[f"status_{response.status_code}"] += 1
            _counts["duration_ms_total"] += elapsed * 1000
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time-ms"] = f"{elapsed * 1000:.2f}"
        return response

def get_metrics():
    with _lock:
        total = _counts["requests_total"]
        return {
            "requests_total": total,
            "average_response_time_ms": round(_counts["duration_ms_total"] / total, 2) if total else 0,
            "responses_5xx": sum(v for k, v in _counts.items() if k.startswith("status_5") and k[7:].isdigit()),
        }
