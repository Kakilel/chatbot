import requests
import logging
import re

BASE_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/"

logging.basicConfig(level=logging.ERROR)

def get_wikipedia_summary(query: str):
    query = query.strip().replace(" ", "_")
    try:
        res = requests.get(BASE_URL + query, timeout=10)
        res.raise_for_status()
        data = res.json()
        return {
            "title": data.get("title"),
            "extract": data.get("extract"),
            "url": data.get("content_urls", {}).get("desktop", {}).get("page")
        }
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
    return {"error": "Could not fetch information."}

def route_wikipedia_query(text: str):
    text = text.lower()

    if match := re.search(r"who is (.+)", text):
        return get_wikipedia_summary(match.group(1))

    if match := re.search(r"what is (.+)", text):
        return get_wikipedia_summary(match.group(1))

    if match := re.search(r"tell me about (.+)", text):
        return get_wikipedia_summary(match.group(1))

    if match := re.search(r"info(?:rmation)? on (.+)", text):
        return get_wikipedia_summary(match.group(1))

    return get_wikipedia_summary(text)
