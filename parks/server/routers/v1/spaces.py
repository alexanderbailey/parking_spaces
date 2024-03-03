from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from parks.schemas import (
    SpacesRead,
    Spaces,
    CarPark
)
from parks.database import session
from datetime import datetime

router = APIRouter()


@router.get(
    "/get",
    response_model=list[SpacesRead]
)
def get_spaces(
        *,
        carpark_code: str,
        range_start: datetime,
        range_end: datetime,
        session: Session = Depends(session)
):
    return session.exec(
        select(Spaces)
        .join(CarPark)
        .filter(CarPark.code == carpark_code)
        .filter(Spaces.time >= range_start)
        .filter(Spaces.time <= range_end)
        .order_by(Spaces.time.asc())
    ).all()