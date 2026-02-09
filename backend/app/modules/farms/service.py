from sqlalchemy.orm import Session

from app.modules.farms.models import Farm
from app.modules.farms.schemas import FarmCreate


def create_farm(
        db: Session,
        farm_data: FarmCreate,
        tenant_id: int
) -> Farm:
    farm = Farm(
        tenant_id=tenant_id,
        name=farm_data.name,
        location=farm_data.location,
        area=farm_data.area,
        farming_type=farm_data.farming_type
    )

    db.add(farm)
    db.commit()
    db.refresh(farm)

    return farm


def get_farms(
    db: Session,
    tenant_id: int,
) -> list[Farm]:
    return (
        db.query(Farm)
        .filter(
            Farm.tenant_id == tenant_id,
            Farm.is_deleted == False,
        )
        .all()
    )
