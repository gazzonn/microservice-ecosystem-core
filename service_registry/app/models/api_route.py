from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from shared.database.base import Base, UUIDPrimaryKeyMixin


class ApiRoute(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "api_routes"

    service_id: Mapped[str] = mapped_column(ForeignKey("services.id"), nullable=False, index=True)
    path: Mapped[str] = mapped_column(String(255), nullable=False)
    method: Mapped[str] = mapped_column(String(10), nullable=False)
    is_protected: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    required_permission: Mapped[str | None] = mapped_column(String(100), nullable=True)
