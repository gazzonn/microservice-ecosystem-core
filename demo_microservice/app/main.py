from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from demo_microservice.app.routes.demo import router as demo_router
from demo_microservice.app.routes.ui import router as ui_router
from shared.exceptions.api import AppException
from shared.schemas.base import ErrorResponse
from shared.schemas.health import HealthResponse
from shared.utils.logging import configure_logging


configure_logging("demo_microservice")

app = FastAPI(title="Demo Microservice", version="1.0.0")
app.include_router(ui_router)
app.include_router(demo_router)


@app.exception_handler(AppException)
async def handle_app_exception(_: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(message=exc.message, error_code=exc.error_code, details=exc.details).model_dump(mode="json"),
    )


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="demo_microservice")
