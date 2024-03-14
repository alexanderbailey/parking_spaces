from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlmodel import Session
from datetime import datetime

from parks.schemas import (
    Weather,
)
from parks.database import session
import json

router = APIRouter()


@router.post(
    "/upload",
    status_code=201,
    include_in_schema=False
)
def weather_upload(
        *,
        server_response: UploadFile = File(...),
        session: Session = Depends(session)
):
    file_name = server_response.filename
    try:
        json_data = json.load(server_response.file)
        # TODO: Replace hard-coded UUID with a lookup from the database
        st_helier_uuid = '1b6cf4b3-a9cf-433c-a3f1-18c1c7bc8d1f'
        time = datetime.fromtimestamp(json_data['data'][0]['dt'])
        weather = Weather(
            weather_location_id=st_helier_uuid,
            time=time,
            data=json_data
        )
    except Exception as e:
        raise HTTPException(422, f'Bad upload weather. Error: {e}')

    session.add(weather)
    session.commit()

    return f'Successfully uploaded weather'
