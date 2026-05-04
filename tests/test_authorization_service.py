from uuid import uuid4

import pytest

from authorization_service.app.models.permission import Permission
from authorization_service.app.models.role import Role
from authorization_service.app.schemas.authorization import AccessCheckRequest, PermissionCreateRequest, RoleCreateRequest
from authorization_service.app.services.authorization_service import AuthorizationService
from shared.exceptions.api import AppException, NotFoundException


class FakeAuthorizationRepository:
    def __init__(self) -> None:
        self.roles: dict[str, Role] = {}
        self.permissions: dict[str, Permission] = {}
        self.user_roles: list[tuple[str, str]] = []
        self.role_permissions: list[tuple[str, str]] = []

    def create_role(self, role: Role) -> Role:
        if not role.id:
            role.id = str(uuid4())
        self.roles[role.id] = role
        return role

    def create_permission(self, permission: Permission) -> Permission:
        if not permission.id:
            permission.id = str(uuid4())
        self.permissions[permission.id] = permission
        return permission

    def get_role(self, role_id: str) -> Role | None:
        return self.roles.get(role_id)

    def get_role_by_name(self, name: str) -> Role | None:
        return next((role for role in self.roles.values() if role.name == name), None)

    def get_permission(self, permission_id: str) -> Permission | None:
        return self.permissions.get(permission_id)

    def get_permission_by_signature(self, resource: str, action: str) -> Permission | None:
        return next(
            (
                permission
                for permission in self.permissions.values()
                if permission.resource == resource and permission.action == action
            ),
            None,
        )

    def assign_role(self, user_id: str, role_id: str) -> None:
        pair = (user_id, role_id)
        if pair not in self.user_roles:
            self.user_roles.append(pair)

    def assign_permission(self, role_id: str, permission_id: str) -> None:
        pair = (role_id, permission_id)
        if pair not in self.role_permissions:
            self.role_permissions.append(pair)

    def get_user_roles(self, user_id: str) -> list[Role]:
        role_ids = [role_id for uid, role_id in self.user_roles if uid == user_id]
        return [self.roles[role_id] for role_id in role_ids if role_id in self.roles]

    def get_user_permissions(self, user_id: str) -> list[Permission]:
        permissions: list[Permission] = []
        for uid, role_id in self.user_roles:
            if uid != user_id:
                continue
            for assigned_role_id, permission_id in self.role_permissions:
                if assigned_role_id == role_id and permission_id in self.permissions:
                    permissions.append(self.permissions[permission_id])
        return permissions


@pytest.fixture
def authorization_service() -> AuthorizationService:
    return AuthorizationService(FakeAuthorizationRepository())


def test_create_role_returns_existing_role_if_name_already_exists(authorization_service: AuthorizationService) -> None:
    payload = RoleCreateRequest(name="ADMIN", description="Administrator")

    first_role = authorization_service.create_role(payload)
    second_role = authorization_service.create_role(payload)

    assert first_role.id == second_role.id


def test_create_permission_returns_existing_permission_if_signature_already_exists(
    authorization_service: AuthorizationService,
) -> None:
    payload = PermissionCreateRequest(
        name="Read admin endpoint",
        resource="demo",
        action="read_admin",
        description="Access to admin route",
    )

    first_permission = authorization_service.create_permission(payload)
    second_permission = authorization_service.create_permission(payload)

    assert first_permission.id == second_permission.id


def test_assign_role_without_role_id_raises_bad_request(authorization_service: AuthorizationService) -> None:
    with pytest.raises(AppException):
        authorization_service.assign_role(user_id="user-1", role_id="")


def test_assign_permission_without_permission_id_raises_bad_request(authorization_service: AuthorizationService) -> None:
    role = authorization_service.create_role(RoleCreateRequest(name="ADMIN", description="Administrator"))

    with pytest.raises(AppException):
        authorization_service.assign_permission(role_id=role.id, permission_id="")


def test_check_access_returns_allowed_when_permission_present(authorization_service: AuthorizationService) -> None:
    role = authorization_service.create_role(RoleCreateRequest(name="ADMIN", description="Administrator"))
    permission = authorization_service.create_permission(
        PermissionCreateRequest(
            name="Read admin endpoint",
            resource="demo",
            action="read_admin",
            description="Access to admin route",
        )
    )
    authorization_service.assign_role(user_id="user-1", role_id=role.id)
    authorization_service.assign_permission(role_id=role.id, permission_id=permission.id)

    result = authorization_service.check_access(
        AccessCheckRequest(user_id="user-1", resource="demo", action="read_admin")
    )

    assert result.allowed is True
    assert "ADMIN" in result.roles
    assert "demo:read_admin" in result.permissions


def test_assign_role_for_missing_role_raises_not_found(authorization_service: AuthorizationService) -> None:
    with pytest.raises(NotFoundException):
        authorization_service.assign_role(user_id="user-1", role_id="missing-role")
