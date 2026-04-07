from sqlalchemy import select
from sqlalchemy.orm import Session

from authorization_service.app.models.permission import Permission
from authorization_service.app.models.role import Role
from authorization_service.app.models.user_role import RolePermission, UserRole


class AuthorizationRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_role(self, role: Role) -> Role:
        self.session.add(role)
        self.session.commit()
        self.session.refresh(role)
        return role

    def create_permission(self, permission: Permission) -> Permission:
        self.session.add(permission)
        self.session.commit()
        self.session.refresh(permission)
        return permission

    def get_role(self, role_id: str) -> Role | None:
        return self.session.get(Role, role_id)

    def get_permission(self, permission_id: str) -> Permission | None:
        return self.session.get(Permission, permission_id)

    def assign_role(self, user_id: str, role_id: str) -> None:
        if not self.session.get(UserRole, {"user_id": user_id, "role_id": role_id}):
            self.session.add(UserRole(user_id=user_id, role_id=role_id))
            self.session.commit()

    def assign_permission(self, role_id: str, permission_id: str) -> None:
        if not self.session.get(RolePermission, {"role_id": role_id, "permission_id": permission_id}):
            self.session.add(RolePermission(role_id=role_id, permission_id=permission_id))
            self.session.commit()

    def get_user_roles(self, user_id: str) -> list[Role]:
        stmt = select(Role).join(UserRole, UserRole.role_id == Role.id).where(UserRole.user_id == user_id)
        return list(self.session.execute(stmt).scalars().all())

    def get_user_permissions(self, user_id: str) -> list[Permission]:
        stmt = (
            select(Permission)
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .join(Role, Role.id == RolePermission.role_id)
            .join(UserRole, UserRole.role_id == Role.id)
            .where(UserRole.user_id == user_id)
        )
        return list(self.session.execute(stmt).scalars().all())
