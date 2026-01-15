from fastapi import APIRouter
import os

router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "services": "smart-farm-platform",
        "version": os.getenv("APP_VERSION")
    }
