from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.modules.users.schemas import UserCreate, UserResponse
from app.modules.users.service import create_user
from app.common.dependencies import get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse)
def create_user_api(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(db, user)
