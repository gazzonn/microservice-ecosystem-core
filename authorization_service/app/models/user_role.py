from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from shared.database.base import Base


class UserRole(Base):
    __tablename__ = "user_roles"
    __table_args__ = (PrimaryKeyConstraint("user_id", "role_id"),)

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    role_id: Mapped[str] = mapped_column(ForeignKey("roles.id"), nullable=False)


class RolePermission(Base):
    __tablename__ = "role_permissions"
    __table_args__ = (PrimaryKeyConstraint("role_id", "permission_id"),)

    role_id: Mapped[str] = mapped_column(ForeignKey("roles.id"), nullable=False)
    permission_id: Mapped[str] = mapped_column(ForeignKey("permissions.id"), nullable=False)
