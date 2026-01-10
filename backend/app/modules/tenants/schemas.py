from pydantic import BaseModel, EmailStr
from app.common.roles import TenantRole


class TenantCreate(BaseModel):
    name: str


class TenantResponse(BaseModel):
    id: int
    name: str


# inputs required for invite user api
class InviteUserRequest(BaseModel):
    email: EmailStr
    role: TenantRole


# inputs to change role
class ChangeUserRoleRequest(BaseModel):
    user_id: int
    role: TenantRole
