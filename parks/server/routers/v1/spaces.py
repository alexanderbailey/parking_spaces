from fastapi import APIRouter, Depends
from sqlmodel import Session, select, extract

from parks.schemas import (
    SpacesRead,
    Spaces,
    CarPark
)
from parks.database import session
from datetime import datetime

router = APIRouter()


@router.get(
    "/get-in-range",
    response_model=list[SpacesRead],
    include_in_schema=False
)
def get_spaces_in_range(
        *,
        carpark_code: str,
        range_start: datetime,
        range_end: datetime,
        session: Session = Depends(session)
):
    return session.exec(
        select(Spaces.spaces, Spaces.time)
        .join(CarPark)
        .filter(CarPark.code == carpark_code)
        .filter(Spaces.time >= range_start)
        .filter(Spaces.time < range_end)
        .order_by(Spaces.time.asc())
    ).all()


@router.get(
    "/get-day-in-range",
    response_model=list[SpacesRead],
    include_in_schema=False
)
def get_spaces_from_day_in_range(
        *,
        carpark_code: str,
        day: int,
        start_date: datetime,
        end_date: datetime,
        session: Session = Depends(session)
):
    return session.exec(
        select(Spaces.time, Spaces.spaces)
        .join(CarPark)
        .filter(CarPark.code == carpark_code)
        .filter(extract('dow', Spaces.time) == day)
        .filter(Spaces.time >= start_date)
        .filter(Spaces.time < end_date)
        .order_by(Spaces.time.asc())
    ).all()


@router.get(
    "/get-model",
    response_model=list[SpacesRead]
)
def get_model(
        *,
        carpark_code: str,
        day: int,
        session: Session = Depends(session)
):
    return session.exec(
        select(Spaces.time, Spaces.spaces)
        .join(CarPark)
        .filter(CarPark.code == carpark_code)
        .filter(extract('dow', Spaces.time) == day)
        .filter(Spaces.time >= '2024-03-03')
        .filter(Spaces.time < '2024-03-09')
        .order_by(Spaces.time.asc())
    ).all()