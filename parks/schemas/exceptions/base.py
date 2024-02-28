from pydantic import BaseModel


class ExceptionModel(BaseModel):
    message: str = ""
    detail: str = ""
    error: str = "BaseError"


class PGExceptionModel(BaseModel):
    pgcode: int
    pgerror: str
