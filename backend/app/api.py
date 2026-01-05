from fastapi import APIRouter

from app.modules.tenants.routes import router as tenant_router


router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


router.include_router(tenant_router)
