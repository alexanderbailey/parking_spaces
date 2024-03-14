from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from datetime import datetime

from parks.schemas import (
    WeatherForecast,
)
from parks.database import session

router = APIRouter()


@router.post(
    "/upload",
    status_code=201,
    include_in_schema=False
)
def weather_upload(
        *,
        current_weather: dict,
        session: Session = Depends(session)
):

    try:
        st_helier_uuid = '1b6cf4b3-a9cf-433c-a3f1-18c1c7bc8d1f'
        time = datetime.fromtimestamp(current_weather['data'][0]['dt'])
        weather_forecast = WeatherForecast(
            weather_location_id=st_helier_uuid,
            time=time,
            data=current_weather
        )
    except Exception as e:
        raise HTTPException(422, f'Bad upload. Error: {e}')

    session.add(weather_forecast)
    session.commit()

    return f'Successfully uploaded'