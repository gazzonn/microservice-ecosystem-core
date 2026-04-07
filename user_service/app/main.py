from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from shared.database.base import Base
from shared.database.session import engine
from shared.exceptions.api import AppException
from shared.schemas.base import ErrorResponse
from shared.schemas.health import HealthResponse
from shared.utils.logging import configure_logging
from user_service.app.models import User  # noqa: F401
from user_service.app.routes.users import router as user_router


configure_logging("user_service")
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service", version="1.0.0")
app.include_router(user_router)


@app.exception_handler(AppException)
async def handle_app_exception(_: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(message=exc.message, error_code=exc.error_code, details=exc.details).model_dump(mode="json"),
    )


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="user_service")
