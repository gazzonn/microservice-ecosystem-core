from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from auth_service.app.models import Token, User  # noqa: F401
from auth_service.app.routes.auth import router as auth_router
from shared.database.base import Base
from shared.database.session import engine
from shared.exceptions.api import AppException
from shared.schemas.base import ErrorResponse
from shared.schemas.health import HealthResponse
from shared.utils.logging import configure_logging


configure_logging("auth_service")
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service", version="1.0.0")
app.include_router(auth_router)


@app.exception_handler(AppException)
async def handle_app_exception(_: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(message=exc.message, error_code=exc.error_code, details=exc.details).model_dump(mode="json"),
    )


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="auth_service")
