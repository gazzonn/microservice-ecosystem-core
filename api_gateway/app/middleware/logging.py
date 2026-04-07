import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        started_at = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - started_at
        logger.info("%s %s -> %s in %.4fs", request.method, request.url.path, response.status_code, elapsed)
        return response
