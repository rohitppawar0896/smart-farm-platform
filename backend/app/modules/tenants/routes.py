from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.modules.tenants.schemas import TenantCreate, TenantResponse
from app.modules.tenants.service import create_tenant, get_user_tenants
from app.common.dependencies import get_db
from app.modules.users.models import User
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.dependencies import get_tenant_context
from app.modules.auth.rbac import require_roles
from app.common.roles import TenantRole

router = APIRouter(
    prefix="/tenant",
    tags=["Tenant"]
)


# api to create Tenant
@router.post("/", response_model=TenantResponse)
def create_tenant(
    tenant: TenantCreate,
    # fetch current user to add as owner of tenant
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_tenant(db, tenant, current_user)


# api to get Tenant details
@router.get("/details")
def get_tenant_details(
    # Owener, admin , viewer can view details of tenant
    context: dict = Depends(require_roles(
        TenantRole.OWNER,
        TenantRole.ADMIN,
        TenantRole.VIEWER
    ))
):
    return {
        "tenat_id": context["tenant_id"],
        "user": context["user"].email,
        "role": context["role"]
    }


# api to delete Tenant, Only Owner can perform this
@router.delete("/")
def delete_tenant(
    context=Depends(require_roles(TenantRole.OWNER))
):
    return {
        "Status": "Tenant Deleted"
    }


# api to add a user to Tenant
@router.post("/user")
def add_user_to_tenant(
    context=Depends(require_roles(
        TenantRole.OWNER,
        TenantRole.ADMIN
    ))
):
    return {
        "Status": "User Added"
    }


# list all tenants of user
@router.get("/my/tenants")
def list_my_tenats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_user_tenants(db, current_user.id)
