from app.modules.tenants.models import Tenant
from app.modules.tenants.schemas import TenantCreate
from app.modules.users.models import User, UserTenant
from app.common.roles import TenantRole

from sqlalchemy.orm import Session
from fastapi import HTTPException, status


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


# add user to a tenant
# currenly we are adding user directly.In future we can invite a user via email.
def invite_user_to_tenant(
    db: Session,
    tenant_id: int,
    email: str,
    role: TenantRole,
    invited_by_role: TenantRole
):
    # Only owner can assign OWNER role
    if role == TenantRole.OWNER and invited_by_role != TenantRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only OWNER can assign OWNER role"
        )

    user = db.query(User).filter(User.email == email).first()

# check if user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

# check if user is already part of tenant
    existing = (
        db.query(UserTenant).filter(
            UserTenant.user_id == user.id,
            UserTenant.tenant_id == tenant_id
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already part of Tenant"
        )

# add mappings to add in user_tenant table
    mapping = UserTenant(
        user_id=user.id,
        tenant_id=tenant_id,
        role=role.value
    )

    db.add(mapping)
    db.commit()

    return {
        "message": "User Invited"
    }


# function to change user role
def change_user_role(
        db: Session,
        tenant_id: int,
        target_user_id: int,
        new_role: TenantRole,
        current_user_id: int,
        current_user_role: TenantRole
):
    # only owner can change role
    if current_user_role != TenantRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Owner can change role"
        )

    # owner cannot change own role
    if current_user_id == target_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Owener cannot change own role"
        )

    mapping = (
        db.query(UserTenant)
        .filter(
            UserTenant.tenant_id == tenant_id,
            UserTenant.user_id == target_user_id
        )
        .first()
    )

    if not mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is not part of tenant"
        )

    mapping.role = new_role
    db.commit()

    return {
        "message": "User Role Updated successfully"
    }


# Function to remove user
def remove_user_from_tenant(
    db: Session,
    tenant_id: int,
    target_user_id: int,
    current_user_id: int,
    current_user_role: TenantRole

):
    # only owner can remove user
    if current_user_role != TenantRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Owener can remove users from tenant"
        )

    # Owener cananot remove Themselves
    if current_user_id == target_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Owner cannot remove themselves"
        )

    mapping = (
        db.query(UserTenant)
        .filter(
            UserTenant.user_id == target_user_id,
            UserTenant.tenant_id == tenant_id
        )
        .first()
    )

    if not mapping:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not part of tenant"
        )

    # prevents removing last owner
    if mapping.role == TenantRole.OWNER:
        owner_count = (
            db.query(UserTenant)
            .filter(
                UserTenant.role == TenantRole.OWNER.value,
                UserTenant.tenant_id == mapping.tenant_id
            )
            .count()
        )

        if owner_count <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot remove last Owner"
            )

    db.delete(mapping)
    db.commit()

    return {
        "message": "User removed from Tenant"
    }


# fuction to transfer owenership
def transfer_tenant_ownership(
        db: Session,
        tenant_id: int,
        current_user_id: int,
        new_owner_user_id: int,
        current_user_role: TenantRole
):
    if current_user_id == new_owner_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot transfer ownership to yourself"
        )

    current_user = (
        db.query(UserTenant)
        .filter(
            UserTenant.tenant_id == tenant_id,
            UserTenant.user_id == current_user_id,
            UserTenant.role == TenantRole.OWNER.value
        )
        .first()
    )

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Owner Can Transfer Ownership"
        )

    new_owner = (
        db.query(UserTenant)
        .filter(
            UserTenant.tenant_id == tenant_id,
            UserTenant.user_id == new_owner_user_id
        )
        .first()
    )

    if not new_owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target user is not part of tenant"
        )

    current_user.role = TenantRole.ADMIN.value
    new_owner.role = TenantRole.OWNER.value

    db.commit()

    return {
        "Message": "Tenant Ownership Transferred successfully"
    }


# function to list all users present in tenant
def list_users_in_tenants(
        db: Session,
        tenant_id: int
):
    results = (
        db.query(User, UserTenant)
        .join(UserTenant, User.id == UserTenant.user_id)
        .filter(UserTenant.tenant_id == tenant_id)
        .all()
    )

    response = []

    for user, user_tenant in results:
        response.append({
            "user_id": user.id,
            "email": user.email,
            "role": user_tenant.role
        })

    return response
