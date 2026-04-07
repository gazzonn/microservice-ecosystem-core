from pydantic import BaseModel, Field


class ApiRouteCreateRequest(BaseModel):
    path: str
    method: str
    is_protected: bool
    required_permission: str | None = None


class ServiceRegisterRequest(BaseModel):
    name: str
    base_url: str
    health_url: str | None = None
    status: str = "ACTIVE"
    version: str | None = None
    routes: list[ApiRouteCreateRequest] = Field(default_factory=list)


class ServiceStatusUpdateRequest(BaseModel):
    status: str
