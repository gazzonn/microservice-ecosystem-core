from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreateRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserUpdateRequest(BaseModel):
    email: EmailStr | None = None
    status: str | None = None


class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    status: str
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None = None

    class Config:
        from_attributes = True
