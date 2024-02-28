from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional
from uuid import UUID
from datetime import datetime


class ServerResponse(SQLModel, table=True):
    __tablename__ = "server_response"
    timestamp: int = Field(primary_key=True)
    response: dict = Field(sa_column=Column(JSON))


class CarPark(SQLModel, table=True):
    __tablename__ = "carpark"
    id: Optional[UUID] = Field(default=None, primary_key=True)
    name: str
    code: str
    type: str
    low: int  # Number of spaces considered low


class Spaces(SQLModel, table=True):
    __tablename__ = "spaces"
    id: Optional[UUID] = Field(default=None, primary_key=True)
    car_park_id: UUID = Field(foreign_key="carpark.id")
    open: bool
    spaces: int
    unusable_spaces: int
    time: datetime
