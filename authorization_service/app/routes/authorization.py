from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from authorization_service.app.core.dependencies import get_session
from authorization_service.app.repositories.authorization_repository import AuthorizationRepository
from authorization_service.app.schemas.authorization import (
    AccessCheckRequest,
    AssignPermissionRequest,
    AssignRoleRequest,
    PermissionCreateRequest,
    RoleCreateRequest,
)
from authorization_service.app.services.authorization_service import AuthorizationService
from shared.schemas.base import SuccessResponse


router = APIRouter(prefix="/authorize", tags=["authorization"])


def build_service(session: Session) -> AuthorizationService:
    return AuthorizationService(AuthorizationRepository(session))


@router.post("/check", response_model=SuccessResponse)
def check_access(payload: AccessCheckRequest, session: Session = Depends(get_session)) -> SuccessResponse:
    result = build_service(session).check_access(payload)
    return SuccessResponse(message="Access evaluated", data=result.model_dump())


@router.get("/user/{user_id}/roles", response_model=SuccessResponse)
def get_user_roles(user_id: str, session: Session = Depends(get_session)) -> SuccessResponse:
    roles = build_service(session).get_user_roles(user_id)
    return SuccessResponse(message="Roles retrieved", data=[{"id": item.id, "name": item.name} for item in roles])


@router.get("/user/{user_id}/permissions", response_model=SuccessResponse)
def get_user_permissions(user_id: str, session: Session = Depends(get_session)) -> SuccessResponse:
    permissions = build_service(session).get_user_permissions(user_id)
    data = [{"id": item.id, "name": item.name, "resource": item.resource, "action": item.action} for item in permissions]
    return SuccessResponse(message="Permissions retrieved", data=data)


@router.post("/roles", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def create_role(payload: RoleCreateRequest, session: Session = Depends(get_session)) -> SuccessResponse:
    role = build_service(session).create_role(payload)
    return SuccessResponse(message="Role created", data={"id": role.id, "name": role.name})


@router.post("/permissions", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def create_permission(payload: PermissionCreateRequest, session: Session = Depends(get_session)) -> SuccessResponse:
    permission = build_service(session).create_permission(payload)
    return SuccessResponse(message="Permission created", data={"id": permission.id, "name": permission.name})


@router.post("/assign-role", response_model=SuccessResponse)
def assign_role(payload: AssignRoleRequest, session: Session = Depends(get_session)) -> SuccessResponse:
    build_service(session).assign_role(payload.user_id, payload.role_id)
    return SuccessResponse(message="Role assigned", data={})


@router.post("/assign-permission", response_model=SuccessResponse)
def assign_permission(payload: AssignPermissionRequest, session: Session = Depends(get_session)) -> SuccessResponse:
    build_service(session).assign_permission(payload.role_id, payload.permission_id)
    return SuccessResponse(message="Permission assigned", data={})
