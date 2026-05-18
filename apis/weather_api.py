import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

# GET WEATHER

def get_weather(city):

    try:

        url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"q={city}"
            f"&appid={API_KEY}"
            f"&units=metric"
        )

        response = requests.get(url)

        data = response.json()

        # TEMPERATURE

        temperature = data["main"]["temp"]

        # WEATHER CONDITION

        condition = data["weather"][0]["main"]

        # WIND SPEED

        wind_speed = data["wind"]["speed"]

        # RETURN CLEAN DICTIONARY

        return {
            "temperature": temperature,
            "condition": condition,
            "wind_speed": wind_speed
        }

    except Exception:

        return {
            "temperature": "N/A",
            "condition": "N/A",
            "wind_speed": "N/A"
        }