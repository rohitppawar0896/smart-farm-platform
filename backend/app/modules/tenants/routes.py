from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.modules.tenants.schemas import TenantCreate, TenantResponse
from app.modules.tenants.service import create_tenant
from app.common.dependencies import get_db

router = APIRouter(
    prefix="/tenants",
    tags=["Tenants"]
)


@router.post("/", response_model=TenantResponse)
def create_tenat_api(
    tenant: TenantCreate,
    db: Session = Depends(get_db)
):
    return create_tenant(db, tenant)
