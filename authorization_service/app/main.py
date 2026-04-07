from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from authorization_service.app.models import Permission, Role, RolePermission, UserRole  # noqa: F401
from authorization_service.app.routes.authorization import router as authorization_router
from shared.database.base import Base
from shared.database.session import engine
from shared.exceptions.api import AppException
from shared.schemas.base import ErrorResponse
from shared.schemas.health import HealthResponse
from shared.utils.logging import configure_logging


configure_logging("authorization_service")
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Authorization Service", version="1.0.0")
app.include_router(authorization_router)


@app.exception_handler(AppException)
async def handle_app_exception(_: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(message=exc.message, error_code=exc.error_code, details=exc.details).model_dump(mode="json"),
    )


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="authorization_service")
