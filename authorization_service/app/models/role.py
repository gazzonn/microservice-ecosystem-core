from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from shared.database.base import Base, UUIDPrimaryKeyMixin


class Role(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
