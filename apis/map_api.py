import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEOAPIFY_API_KEY")

# GET PLACE COORDINATES

def get_place_coordinates(place):

    try:

        url = (
            f"https://api.geoapify.com/v1/geocode/search?"
            f"text={place}"
            f"&apiKey={API_KEY}"
        )

        response = requests.get(url)

        data = response.json()

        # SAFE CHECK

        if "features" not in data:
            return None, None

        if not data["features"]:
            return None, None

        lon = data["features"][0]["properties"]["lon"]
        lat = data["features"][0]["properties"]["lat"]

        return lat, lon

    except Exception:

        return None, None