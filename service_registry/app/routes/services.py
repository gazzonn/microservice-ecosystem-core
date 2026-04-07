from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from service_registry.app.core.dependencies import get_session
from service_registry.app.repositories.service_repository import ServiceRepository
from service_registry.app.schemas.registry import ServiceRegisterRequest, ServiceStatusUpdateRequest
from service_registry.app.services.service_registry_service import ServiceRegistryService
from shared.schemas.base import SuccessResponse


router = APIRouter(prefix="/services", tags=["service_registry"])


def build_service(session: Session) -> ServiceRegistryService:
    return ServiceRegistryService(ServiceRepository(session))


@router.post("/register", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def register_service(payload: ServiceRegisterRequest, session: Session = Depends(get_session)) -> SuccessResponse:
    service = build_service(session).register_service(payload)
    return SuccessResponse(message="Service registered", data={"id": service.id, "name": service.name})


@router.delete("/{service_id}", response_model=SuccessResponse)
def delete_service(service_id: str, session: Session = Depends(get_session)) -> SuccessResponse:
    build_service(session).remove_service(service_id)
    return SuccessResponse(message="Service removed", data={})


@router.get("", response_model=SuccessResponse)
def list_services(session: Session = Depends(get_session)) -> SuccessResponse:
    services = build_service(session).list_services()
    data = [
        {"id": item.id, "name": item.name, "base_url": item.base_url, "status": item.status, "version": item.version}
        for item in services
    ]
    return SuccessResponse(message="Services retrieved", data=data)


@router.get("/resolve/route", response_model=SuccessResponse)
def resolve_route(
    path: str = Query(...),
    method: str = Query(...),
    session: Session = Depends(get_session),
) -> SuccessResponse:
    service, route = build_service(session).resolve_route(path=path, method=method)
    data = {
        "service_name": service.name,
        "base_url": service.base_url,
        "status": service.status,
        "path": route.path,
        "method": route.method,
        "is_protected": route.is_protected,
        "required_permission": route.required_permission,
    }
    return SuccessResponse(message="Route resolved", data=data)


@router.get("/{name}", response_model=SuccessResponse)
def get_service(name: str, session: Session = Depends(get_session)) -> SuccessResponse:
    service = build_service(session).get_service_by_name(name)
    return SuccessResponse(
        message="Service retrieved",
        data={"id": service.id, "name": service.name, "base_url": service.base_url, "status": service.status},
    )


@router.patch("/{service_id}/status", response_model=SuccessResponse)
def update_status(
    service_id: str, payload: ServiceStatusUpdateRequest, session: Session = Depends(get_session)
) -> SuccessResponse:
    service = build_service(session).update_status(service_id, payload.status)
    return SuccessResponse(message="Service status updated", data={"id": service.id, "status": service.status})
