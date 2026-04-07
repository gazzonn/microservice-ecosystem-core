from authorization_service.app.models.permission import Permission
from authorization_service.app.models.role import Role
from authorization_service.app.repositories.authorization_repository import AuthorizationRepository
from authorization_service.app.schemas.authorization import (
    AccessCheckRequest,
    AccessCheckResponse,
    PermissionCreateRequest,
    RoleCreateRequest,
)
from shared.exceptions.api import NotFoundException


class AuthorizationService:
    """Role and permission management."""

    def __init__(self, repository: AuthorizationRepository) -> None:
        self.repository = repository

    def create_role(self, data: RoleCreateRequest) -> Role:
        return self.repository.create_role(Role(name=data.name, description=data.description))

    def create_permission(self, data: PermissionCreateRequest) -> Permission:
        return self.repository.create_permission(
            Permission(name=data.name, resource=data.resource, action=data.action, description=data.description)
        )

    def assign_role(self, user_id: str, role_id: str) -> None:
        if not self.repository.get_role(role_id):
            raise NotFoundException("Role not found")
        self.repository.assign_role(user_id, role_id)

    def assign_permission(self, role_id: str, permission_id: str) -> None:
        if not self.repository.get_role(role_id):
            raise NotFoundException("Role not found")
        if not self.repository.get_permission(permission_id):
            raise NotFoundException("Permission not found")
        self.repository.assign_permission(role_id, permission_id)

    def get_user_roles(self, user_id: str) -> list[Role]:
        return self.repository.get_user_roles(user_id)

    def get_user_permissions(self, user_id: str) -> list[Permission]:
        return self.repository.get_user_permissions(user_id)

    def check_access(self, data: AccessCheckRequest) -> AccessCheckResponse:
        roles = self.repository.get_user_roles(data.user_id)
        permissions = self.repository.get_user_permissions(data.user_id)
        permission_keys = [f"{item.resource}:{item.action}" for item in permissions]
        allowed = any(item.resource == data.resource and item.action == data.action for item in permissions)
        return AccessCheckResponse(allowed=allowed, roles=[item.name for item in roles], permissions=permission_keys)
