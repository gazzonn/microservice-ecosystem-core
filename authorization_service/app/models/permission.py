from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from shared.database.base import Base, UUIDPrimaryKeyMixin


class Permission(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    resource: Mapped[str] = mapped_column(String(100), nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
