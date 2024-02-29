from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlmodel import Session

from parks.schemas import (
    ServerResponse,
)
from parks.database import session
import json

router = APIRouter()


@router.post(
    "/upload",
    status_code=201
)
def data_upload(
        *,
        server_response: UploadFile = File(...),
        session: Session = Depends(session)
):
    file_name = server_response.filename
    try:
        timestamp = int(file_name.split('.')[0])
        json_data = json.load(server_response.file)
        server_response = ServerResponse(
            timestamp=timestamp,
            response=json_data
        )
    except Exception as e:
        raise HTTPException(422, f'Bad upload file. Error: {e}')

    session.add(server_response)
    session.commit()

    return f'{file_name} successfully uploaded'