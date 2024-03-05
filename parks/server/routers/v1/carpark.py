from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from parks.schemas import (
    CarPark
)
from parks.database import session

router = APIRouter()


@router.get(
    "/get-all",
    response_model=list[CarPark],
    include_in_schema=False
)
def get_all_carparks(
        *,
        session: Session = Depends(session)
):
    return session.exec(select(CarPark)).all()
