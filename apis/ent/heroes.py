import requests
import logging
import re

ACCESS_TOKEN = "87206999864c3c89663d2d91143e0be3"  
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



def search_hero(name: str):
    return make_request(f"search/{name}")



def get_hero_by_id(hero_id: str):
    return make_request(hero_id)



def get_stats(hero_id: str):
    return make_request(f"{hero_id}/powerstats")



def get_bio(hero_id: str):
    return make_request(f"{hero_id}/biography")



def get_appearance(hero_id: str):
    return make_request(f"{hero_id}/appearance")



def get_work(hero_id: str):
    return make_request(f"{hero_id}/work")


def get_connections(hero_id: str):
    return make_request(f"{hero_id}/connections")



def route_hero_query(query: str):
    query = query.lower().strip()

    if not query:
        return None
 
    if match := re.search(r"(?:powerstats|stats) for (.+)", query):
        hero = search_hero(match.group(1))
        if hero and hero.get("response") == "success":
            return get_stats(hero["results"][0]["id"])

    if match := re.search(r"(?:biography|bio) of (.+)", query):
        hero = search_hero(match.group(1))
        if hero and hero.get("response") == "success":
            return get_bio(hero["results"][0]["id"])

    if match := re.search(r"(?:appearance|looks) of (.+)", query):
        hero = search_hero(match.group(1))
        if hero and hero.get("response") == "success":
            return get_appearance(hero["results"][0]["id"])

    if match := re.search(r"(?:connections|relatives) of (.+)", query):
        hero = search_hero(match.group(1))
        if hero and hero.get("response") == "success":
            return get_connections(hero["results"][0]["id"])

    if match := re.search(r"(?:work|job) of (.+)", query):
        hero = search_hero(match.group(1))
        if hero and hero.get("response") == "success":
            return get_work(hero["results"][0]["id"])

    if match := re.search(r"(?:search hero|get info on|show me superhero|details for|who is|tell me about) (.+)", query):
        return search_hero(match.group(1))

    return search_hero(query)

def format_hero_response(data):
    if not data or data.get("response") != "success":
        return "Hero not found."

    if isinstance(data.get("results"), list):
        hero = data["results"][0]
    else:
        hero = data

    name = hero.get("name", "Unknown")
    bio = hero.get("biography", {})
    stats = hero.get("powerstats", {})
    appearance = hero.get("appearance", {})

    return (
        f" **{name}**\n\n"
        f"Full Name: {bio.get('full-name', 'N/A')}\n"
        f"Power Stats: {', '.join(f'{k}: {v}' for k, v in stats.items())}\n"
        f"Appearance: Height: {appearance.get('height', ['N/A'])[0]}, Weight: {appearance.get('weight', ['N/A'])[0]}\n"
        f"Alignment: {bio.get('alignment', 'N/A')}\n"
        f"Place of Birth: {bio.get('place-of-birth', 'N/A')}"
    )