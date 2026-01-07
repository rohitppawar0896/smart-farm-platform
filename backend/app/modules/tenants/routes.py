from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.modules.tenants.schemas import TenantCreate, TenantResponse
from app.modules.tenants.service import create_tenant
from app.common.dependencies import get_db
from app.modules.users.models import User
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.dependencies import get_tenant_context

router = APIRouter(
    prefix="/tenants",
    tags=["Tenants"]
)


@router.post("/", response_model=TenantResponse)
def create_tenant_api(
    tenant: TenantCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_tenant(db, tenant, current_user)


@router.get("/details")
def get_tenat_details(
    context: dict = Depends(get_tenant_context)
):
    return {
        "tenat_id": context["tenant_id"],
        "user": context["user"].email,
        "role": context["role"]
    }
