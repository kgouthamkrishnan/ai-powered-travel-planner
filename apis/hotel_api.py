import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEOAPIFY_API_KEY")

# GET COORDINATES

def get_coordinates(place):

    url = "https://api.geoapify.com/v1/geocode/search"

    params = {
        "text": place,
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params).json()

    features = response.get("features")

    if features:
        lon, lat = features[0]["geometry"]["coordinates"]
        return lat, lon

    return None, None


# SEARCH ACCOMMODATIONS


def search_accommodations(destination):

    lat, lon = get_coordinates(destination)

    if not lat:
        return None

    url = "https://api.geoapify.com/v2/places"

    params = {
        "categories": ",".join([
            "accommodation.hotel",
            "accommodation.hostel",
            "accommodation.guest_house",
            "accommodation.apartment"
        ]),
        "filter": f"circle:{lon},{lat},5000",
        "bias": f"proximity:{lon},{lat}",
        "limit": 10,
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)

    return response.json()