from fastapi import FastAPI

from demo_microservice.app.routes.demo import router as demo_router
from shared.schemas.health import HealthResponse
from shared.utils.logging import configure_logging


configure_logging("demo_microservice")

app = FastAPI(title="Demo Microservice", version="1.0.0")
app.include_router(demo_router)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="demo_microservice")
