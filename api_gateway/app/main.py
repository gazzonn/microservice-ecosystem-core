from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api_gateway.app.core.config import settings
from api_gateway.app.middleware.logging import LoggingMiddleware
from api_gateway.app.middleware.rate_limit import RateLimitMiddleware
from api_gateway.app.routes.gateway import router as gateway_router
from shared.exceptions.api import AppException
from shared.schemas.base import ErrorResponse
from shared.schemas.health import HealthResponse
from shared.utils.logging import configure_logging


configure_logging("api_gateway")

app = FastAPI(title="API Gateway", version="1.0.0")
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    RateLimitMiddleware,
    limit=settings.rate_limit_requests,
    window_seconds=settings.rate_limit_window_seconds,
)
app.include_router(gateway_router)


@app.exception_handler(AppException)
async def handle_app_exception(_: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(message=exc.message, error_code=exc.error_code, details=exc.details).model_dump(mode="json"),
    )


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="api_gateway")
