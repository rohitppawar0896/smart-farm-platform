from app.modules.tenants.models import Tenant


def create_tenant(db, tenant_data):
    tenant = Tenant(
        name=tenant_data.name
    )
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant
