from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from shared.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from shared.utils.enums import ServiceStatus


class ServiceEntity(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "services"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    base_url: Mapped[str] = mapped_column(String(255), nullable=False)
    health_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=ServiceStatus.ACTIVE.value)
    version: Mapped[str | None] = mapped_column(String(20), nullable=True)

    def is_available(self) -> bool:
        return self.status == ServiceStatus.ACTIVE.value
