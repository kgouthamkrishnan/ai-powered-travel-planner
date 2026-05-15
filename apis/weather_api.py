import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city):

    try:

        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(url, params=params)

        data = response.json()

        if data.get("cod") != 200:
            return "Weather data not found"

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]

        weather_report = f"""
🌡 Temperature: {temp}°C

💧 Humidity: {humidity}%

☁ Condition: {description}
"""

        return weather_report

    except Exception as e:

        return f"Weather Error: {e}"