from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.common.models import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # relationship with farm one tenat may farms
    farms = relationship("Farm", back_populates="tenant")
