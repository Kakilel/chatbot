import requests
import re
import logging

API_KEY = "788c98dcf5e2485d850ad301d918d448"
BASE_URL = "https://newsapi.org/v2"

logging.basicConfig(level=logging.ERROR)

def make_request(endpoint: str, params: dict):
    params["apiKey"] = API_KEY
    try:
        res = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=10)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        return {"error": str(e)}

# --- NEWS FUNCTIONS ---
def get_top_headlines(country: str = "us", category: str = None):
    params = {"country": country}
    if category:
        params["category"] = category
    return make_request("top-headlines", params)

def search_news(query: str, language: str = "en"): 
    return make_request("everything", {"q": query, "language": language})

# --- NATURAL PHRASE ROUTER ---
def route_news_query(query: str):
    query = query.lower()

    if match := re.search(r"(top|latest|breaking) (news|headlines)( in)? ([a-z]{2})?", query):
        country = match.group(4) if match.group(4) else "us"
        return get_top_headlines(country)

    if match := re.search(r"(news|headlines) (about|on|regarding) (.+)", query):
        return search_news(match.group(3))

    if match := re.search(r"(tech|sports|business|entertainment|health|science) (news)?", query):
        return get_top_headlines(category=match.group(1))

    if match := re.search(r"what's happening in ([a-zA-Z ]+)", query):
        return search_news(match.group(1))

    return search_news(query)
