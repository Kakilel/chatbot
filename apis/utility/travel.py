import requests
import logging
import re

API_KEY = "5ae2e3f221c38a28845f05b6b485e35d0c24a87a57b7fcf789be3e37"
BASE_URL = "https://api.opentripmap.com/0.1/en/places"

logging.basicConfig(level=logging.ERROR)

def make_request(endpoint: str, params: dict):
    params["apikey"] = API_KEY
    try:
        res = requests.get(f"{BASE_URL}{endpoint}", params=params, timeout=10)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error: {e} - {res.text}")
    except requests.exceptions.Timeout:
        logging.error("Request timed out")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request exception: {e}")
    return None

# --- COORDINATES ---
def get_coords(city: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city, "format": "json"}
    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception as e:
        logging.error(f"Geolocation error: {e}")
    return None, None

# --- PLACES NEARBY ---
def nearby_places(city: str, radius_km: int = 5, limit: int = 10):
    lat, lon = get_coords(city)
    if lat is None or lon is None:
        return {"error": "Could not find coordinates for that city."}
    return make_request("/radius", {
        "radius": radius_km * 1000,
        "lon": lon,
        "lat": lat,
        "limit": limit,
        "rate": 2,
        "format": "json"
    })

# --- PLACE DETAILS ---
def place_details(xid: str):
    return make_request(f"/xid/{xid}", {})

# --- NATURAL PHRASE ROUTING ---
def route_tourist_query(query: str):
    query = query.lower()

    if match := re.search(r"(what are|show) (some )?(attractions|places|things to do) in (.+)", query):
        return nearby_places(match.group(4))

    if match := re.search(r"places near (.+)", query):
        return nearby_places(match.group(1))

    if match := re.search(r"tourist spots in (.+)", query):
        return nearby_places(match.group(1))

    return nearby_places(query)
