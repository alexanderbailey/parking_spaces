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
    try:
        # Load the JSON data from the file
        json_data = json.load(server_response.file)
        # TODO: Replace hard-coded UUID with a lookup from the database
        st_helier_uuid = '1b6cf4b3-a9cf-433c-a3f1-18c1c7bc8d1f'
        # Convert the timestamp to a datetime object
        time = datetime.fromtimestamp(json_data['dt'])
        # Get the weather type id from the database
        type_id = session.execute(f"SELECT id FROM weather_type WHERE name = 'current'").fetchone()[0]
        # Create a new weather object
        weather = Weather(
            location_id=st_helier_uuid,
            time=time,
            data=json_data,
            type_id=type_id
        )
    except Exception as e:
        raise HTTPException(422, f'Bad upload weather. Error: {e}')

    # Add the new weather object to the database and commit the changes
    session.add(weather)
    session.commit()

    return f'Successfully uploaded weather'


@router.post(
    "/submit",
    status_code=201,
    include_in_schema=False
)
def weather_submit(
        *,
        data: dict,
        type: str,
        session: Session = Depends(session)
):
    try:
        # TODO: Replace hard-coded UUID with a lookup from the database
        st_helier_uuid = '1b6cf4b3-a9cf-433c-a3f1-18c1c7bc8d1f'
        # Convert the timestamp to a datetime object
        time = datetime.fromtimestamp(data['data'][0]['dt'])
        # Get the weather type id from the database
        type_id = session.execute(f"SELECT id FROM weather_type WHERE name = '{type}'").fetchone()[0]
        # Create a new weather object
        weather = Weather(
            location_id=st_helier_uuid,
            time=time,
            data=data,
            type_id=type_id
        )
    except Exception as e:
        raise HTTPException(422, f'Bad submission for {type} weather. Error: {e}')

    # Add the new weather object to the database and commit the changes
    session.add(weather)
    session.commit()

    return f'Successfully submitted {type} weather at {time}'