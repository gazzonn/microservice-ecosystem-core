from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from shared.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from shared.security.hash import hash_password, verify_password
from shared.utils.enums import UserStatus


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=UserStatus.ACTIVE.value)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    def verify_password(self, password: str) -> bool:
        return verify_password(password, self.password_hash)

    def set_password(self, password: str) -> None:
        self.password_hash = hash_password(password)

    def is_active(self) -> bool:
        return self.status == UserStatus.ACTIVE.value
