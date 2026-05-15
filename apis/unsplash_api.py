
import requests
import os

ACCESS_KEY = os.getenv("UNSPLASH_API_KEY")

def get_destination_image(query):
    try:
        url = f"https://api.unsplash.com/search/photos?query={query}&client_id={ACCESS_KEY}"
        response = requests.get(url).json()
        return response["results"][0]["urls"]["regular"]
    except:
        return None
