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
    id: UUID = Field(default=None, primary_key=True,  sa_column_kwargs={'server_default': 'uuid_generate_v4()'})
    name: str
    lat: float
    lon: float
    timezone: str
    timezone_offset: int


class WeatherType(SQLModel, table=True):
    __tablename__ = "weather_type"
    id: UUID = Field(default=None, primary_key=True,  sa_column_kwargs={'server_default': 'uuid_generate_v4()'})
    name: str
    description: str


class Weather(SQLModel, table=True):
    __tablename__ = "weather"
    id: UUID = Field(default=None, primary_key=True,  sa_column_kwargs={'server_default': 'uuid_generate_v4()'})
    location_id: UUID = Field(foreign_key="weather_location.id")
    time: datetime
    data: dict = Field(sa_column=Column(JSON))
    type_id: UUID = Field(foreign_key="weather_type.id")


class CarPark(SQLModel, table=True):
    __tablename__ = "carpark"
    id: UUID = Field(default=None, primary_key=True,  sa_column_kwargs={'server_default': 'uuid_generate_v4()'})
    name: str
    code: str
    type: str
    low: int  # Number of spaces considered low


class SpacesRead(SQLModel):
    spaces: int
    time: datetime


class Spaces(SpacesRead, table=True):
    __tablename__ = "spaces"
    id: UUID = Field(default=None, primary_key=True,  sa_column_kwargs={'server_default': 'uuid_generate_v4()'})
    carpark_id: UUID = Field(foreign_key="carpark.id")
    open: bool
    unusable_spaces: int


