from datetime import datetime
from dotenv import find_dotenv, load_dotenv
from os import getenv
import requests
import json

load_dotenv(find_dotenv())
API_KEY = getenv("OPEN_WEATHER_API_KEY")
LAT = float(getenv("LAT"))
LON = float(getenv("LON"))


class OpenWeather:

    api_key: str
    session: requests.Session
    lat: float
    lon: float

    def __init__(self, lat: float, lon: float, api_key: str):
        # Get API key from .env file
        self.api_key = api_key
        # Set coords
        self.lat, self.lon = lat, lon
        # Initialise requests session
        self.session = requests.session()

    def _call_endpoint(self, version: str, endpoint: str, params: dict = {}) -> dict:
        url = f'https://api.openweathermap.org/data/{version}/{endpoint}'
        params = {
            **params,
            'units': 'metric',
            'lat': self.lat,
            'lon': self.lon,
            'appid': self.api_key
        }
        resp = self.session.get(url, params=params)
        return resp.json()

    def weather_for_timestamp(self, dt: datetime) -> dict:
        # Returns weather data for a specific timestamp
        # Included in One Call (1000 calls/day)
        return self._call_endpoint('3.0', 'onecall/timemachine', {'dt': int(dt.timestamp())})


if __name__ == '__main__':
    ow = OpenWeather(lat=LAT, lon=LON, api_key=API_KEY)
    for hour in range(12, 13):
        for min in range(10):
            weather = ow.weather_for_timestamp(datetime(2024, 3, 1, hour, min))
            historic_weather = {
                'data': weather,
                'type': 'historic'
            }
            resp = requests.post('http://localhost:8000/v1/weather/submit', json=historic_weather)
            print(resp.text)

