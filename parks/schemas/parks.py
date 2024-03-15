from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional
from uuid import UUID
from datetime import datetime


class ServerResponse(SQLModel, table=True):
    __tablename__ = "server_response"
    timestamp: int = Field(primary_key=True)
    response: dict = Field(sa_column=Column(JSON))


class WeatherLocation(SQLModel, table=True):
    __tablename__ = "weather_location"
    id: Optional[UUID] = Field(default=None, primary_key=True)
    name: str
    lat: float
    lon: float
    timezone: str
    timezone_offset: int


class Weather(SQLModel, table=True):
    __tablename__ = "weather"
    weather_location_id: UUID = Field(primary_key=True, foreign_key="weather_location.id")
    time: datetime = Field(primary_key=True)
    data: dict = Field(sa_column=Column(JSON))
    historic: bool | None


class CarPark(SQLModel, table=True):
    __tablename__ = "carpark"
    id: Optional[UUID] = Field(default=None, primary_key=True)
    name: str
    code: str
    type: str
    low: int  # Number of spaces considered low


class SpacesRead(SQLModel):
    spaces: int
    time: datetime


class Spaces(SpacesRead, table=True):
    __tablename__ = "spaces"
    id: Optional[UUID] = Field(default=None, primary_key=True)
    carpark_id: UUID = Field(foreign_key="carpark.id")
    open: bool
    unusable_spaces: int


