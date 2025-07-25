import requests
import logging
import re

ACCESS_TOKEN = "87206999864c3c89663d2d91143e0be3"  # Get from https://superheroapi.com/
BASE_URL = f"https://superheroapi.com/api/{ACCESS_TOKEN}"

logging.basicConfig(level=logging.ERROR)

def make_request(endpoint: str):
    try:
        res = requests.get(f"{BASE_URL}/{endpoint}", timeout=10)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error: {e} - {res.text}")
    except requests.exceptions.Timeout:
        logging.error("Request timed out")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request exception: {e}")
    return None

# --- SEARCH ---

def search_hero(name: str):
    return make_request(f"search/{name}")

# --- GET HERO BY ID ---

def get_hero_by_id(hero_id: str):
    return make_request(hero_id)

# --- POWERSTATS ---

def get_stats(hero_id: str):
    return make_request(f"{hero_id}/powerstats")

# --- BIOGRAPHY ---

def get_bio(hero_id: str):
    return make_request(f"{hero_id}/biography")

# --- APPEARANCE ---

def get_appearance(hero_id: str):
    return make_request(f"{hero_id}/appearance")

# --- WORK & CONNECTIONS ---

def get_work(hero_id: str):
    return make_request(f"{hero_id}/work")

def get_connections(hero_id: str):
    return make_request(f"{hero_id}/connections")

# --- ROUTE NATURAL QUERY ---

def route_hero_query(query: str):
    query = query.lower()

    if match := re.search(r"powerstats for (.+)", query):
        hero = search_hero(match.group(1))
        if hero and hero.get("response") == "success":
            return get_stats(hero["results"][0]["id"])

    if match := re.search(r"biography of (.+)", query):
        hero = search_hero(match.group(1))
        if hero and hero.get("response") == "success":
            return get_bio(hero["results"][0]["id"])

    if match := re.search(r"appearance of (.+)", query):
        hero = search_hero(match.group(1))
        if hero and hero.get("response") == "success":
            return get_appearance(hero["results"][0]["id"])

    if match := re.search(r"connections of (.+)", query):
        hero = search_hero(match.group(1))
        if hero and hero.get("response") == "success":
            return get_connections(hero["results"][0]["id"])

    if match := re.search(r"work of (.+)", query):
        hero = search_hero(match.group(1))
        if hero and hero.get("response") == "success":
            return get_work(hero["results"][0]["id"])

    if match := re.search(r"search hero (.+)", query):
        return search_hero(match.group(1))

    return search_hero(query)
