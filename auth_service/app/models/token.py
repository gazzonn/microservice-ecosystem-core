from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from shared.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Token(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "tokens"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    token_value: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    token_type: Mapped[str] = mapped_column(String(20), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def is_expired(self) -> bool:
        return self.expires_at <= datetime.now(timezone.utc)

    def revoke(self) -> None:
        self.revoked = True
