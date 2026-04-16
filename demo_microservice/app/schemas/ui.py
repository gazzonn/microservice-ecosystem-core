from pydantic import BaseModel, EmailStr


class UserRegisterPayload(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLoginPayload(BaseModel):
    username: str
    password: str


class RolePayload(BaseModel):
    name: str
    description: str | None = None


class PermissionPayload(BaseModel):
    name: str
    resource: str
    action: str
    description: str | None = None


class AssignRolePayload(BaseModel):
    user_id: str
    role_id: str


class AssignPermissionPayload(BaseModel):
    role_id: str
    permission_id: str


class GatewayRequestPayload(BaseModel):
    path: str
    token: str | None = None
