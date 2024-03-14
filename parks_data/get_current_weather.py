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

    def current_weather(self) -> dict:
        # Returns current weather data
        # Included in free tier (60 calls/minute, 1,000,000 calls/month)
        return self._call_endpoint('2.5', 'weather')


if __name__ == '__main__':
    ow = OpenWeather(lat=LAT, lon=LON, api_key=API_KEY)
    current_weather = ow.current_weather()
    print(json.dumps(current_weather))

