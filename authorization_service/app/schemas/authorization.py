from pydantic import BaseModel


class RoleCreateRequest(BaseModel):
    name: str
    description: str | None = None


class PermissionCreateRequest(BaseModel):
    name: str
    resource: str
    action: str
    description: str | None = None


class AssignRoleRequest(BaseModel):
    user_id: str
    role_id: str


class AssignPermissionRequest(BaseModel):
    role_id: str
    permission_id: str


class AccessCheckRequest(BaseModel):
    user_id: str
    resource: str
    action: str


class AccessCheckResponse(BaseModel):
    allowed: bool
    roles: list[str]
    permissions: list[str]
