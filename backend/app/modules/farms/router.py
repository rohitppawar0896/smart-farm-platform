from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.dependencies import get_db
from app.modules.farms.schemas import FarmCreate, FarmResponse
from app.modules.farms import service
from app.modules.auth.rbac import require_roles
from app.common.roles import TenantRole


router = APIRouter(
    prefix="/farms",
    tags=["Farms"]
)


@router.post("/", response_model=FarmResponse)
def create_farm(
    farm_data: FarmCreate,
    db: Session = Depends(get_db),
    context=Depends(require_roles(TenantRole.OWNER, TenantRole.ADMIN)),
):
    return service.create_farm(
        db=db,
        farm_data=farm_data,
        tenant_id=context["tenant_id"],
    )


@router.get("/", response_model=list[FarmResponse])
def list_farms(
    db: Session = Depends(get_db),
    context=Depends(require_roles(TenantRole.OWNER,
                    TenantRole.ADMIN, TenantRole.VIEWER)),
):
    return service.get_farms(
        db=db,
        tenant_id=context["tenant_id"],
    )
