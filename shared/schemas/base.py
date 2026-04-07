from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    success: bool = True
    message: str = "Request processed successfully"
    data: Any = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: str
    details: Any = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
