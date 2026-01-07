from app.modules.tenants.models import Tenant
from app.modules.tenants.schemas import TenantCreate
from app.modules.users.models import User, UserTenant

from sqlalchemy.orm import Session


def create_tenant(db: Session, tenant_data: TenantCreate, current_user: User):
    new_tenant = Tenant(
        name=tenant_data.name
    )
    db.add(new_tenant)
    db.flush()  # get tenant.id WITHOUT commit

    # assign owner
    owner_mapping = UserTenant(
        user_id=current_user.id,
        tenant_id=new_tenant.id,
        role="OWNER"
    )
    db.add(owner_mapping)

    # commit all changes
    db.commit()
    db.refresh(new_tenant)
    return new_tenant
