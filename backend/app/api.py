from fastapi import APIRouter

from app.modules.tenants.routes import router as tenant_router
from app.modules.users.routes import router as user_router
from app.modules.auth.routes import router as auth_router

router = APIRouter()

# api to check health status of application


@router.get("/health")
def health_check():
    return {"status": "ok"}


# route to access tenat related routs/apis
router.include_router(tenant_router)

# route to access user related routs/apis
router.include_router(user_router)

# route to create jwt token
router.include_router(auth_router)
