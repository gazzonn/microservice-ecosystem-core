import time
from collections import defaultdict, deque

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from shared.schemas.base import ErrorResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit: int, window_seconds: int) -> None:
        super().__init__(app)
        self.limit = limit
        self.window_seconds = window_seconds
        self.requests: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        request_window = self.requests[client_ip]
        while request_window and now - request_window[0] > self.window_seconds:
            request_window.popleft()
        if len(request_window) >= self.limit:
            payload = ErrorResponse(message="Too many requests", error_code="GATEWAY_429", details={})
            return JSONResponse(status_code=429, content=payload.model_dump(mode="json"))
        request_window.append(now)
        return await call_next(request)
