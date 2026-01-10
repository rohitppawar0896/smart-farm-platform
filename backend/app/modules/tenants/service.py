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


# Function reuturns all tenants in user belong
def get_user_tenants(db: Session, user_id: int):
    # fetch all tenant maps to a user
    results = (
        db.query(UserTenant, Tenant)
        .join(Tenant, Tenant.id == UserTenant.tenant_id)
        .filter(UserTenant.user_id == user_id)
        .all()
    )

# reulsts looks like
# [
#  (UserTenant(...), Tenant(...)),
#  (UserTenant(...), Tenant(...)),
# ]
# so we will append requred details in response and return it
    response = []
    for user_tenant, tenant in results:
        response.append({
            "tenant_id": tenant.id,
            "tenant_name": tenant.name,
            "role": user_tenant.role,
        })

    return response
