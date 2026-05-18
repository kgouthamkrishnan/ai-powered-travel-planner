import requests
import os
from dotenv import load_dotenv
from apis.map_api import get_place_coordinates

load_dotenv()

API_KEY = os.getenv("GEOAPIFY_API_KEY")

# =====================================================
# GET RESTAURANTS & CAFES
# =====================================================

def get_restaurants(destination):

    lat, lon = get_place_coordinates(destination)

    if not lat or not lon:
        return []

    url = (
        f"https://api.geoapify.com/v2/places?"
        f"categories=catering.restaurant,catering.cafe"
        f"&filter=circle:{lon},{lat},15000"
        f"&bias=proximity:{lon},{lat}"
        f"&limit=20"
        f"&apiKey={API_KEY}"
    )

    response = requests.get(url)

    data = response.json()

    restaurants = []

    added_names = set()

    if "features" in data:

        for place in data["features"]:

            props = place["properties"]

            name = props.get("name")

            if not name:
                continue

            # REMOVE DUPLICATES

            if name.lower() in added_names:
                continue

            added_names.add(name.lower())

            restaurants.append({

                "name": name,

                "lat": props.get("lat"),

                "lon": props.get("lon"),

                "address": props.get(
                    "formatted",
                    "No address available"
                ),

                "rating": props.get(
                    "rank",
                    {}
                ).get(
                    "importance",
                    0
                )
            })

    restaurants = sorted(
        restaurants,
        key=lambda x: x["rating"],
        reverse=True
    )

    return restaurants[:15]