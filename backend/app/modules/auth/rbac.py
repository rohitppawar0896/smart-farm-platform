from fastapi import Depends, HTTPException, status

from app.common.roles import TenantRole
from app.modules.auth.dependencies import get_tenant_context


# function for requied roles
def require_roles(*allowed_roles: TenantRole):
    # Inner fuction used to check role of the user for that tenant based on tent context containing tenant user and role
    def role_checker(context=Depends(get_tenant_context)):
        user_role = TenantRole(context["role"])

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )

        return context

    return role_checker
