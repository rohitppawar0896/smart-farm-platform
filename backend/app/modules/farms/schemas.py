from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FarmBase(BaseModel):
    name: str = Field(..., example="Saffron Farm")
    location: Optional[str] = Field(None, example="Solapur, Maharashtra")
    area: Optional[int] = Field(None, example=2000)
    farming_type: str = Field(..., example="indoor")


class FarmCreate(FarmBase):
    pass


class FarmResponse(FarmBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
