import requests
import logging
import re

BASE_URL = "https://api.jikan.moe/v4"
logging.basicConfig(level=logging.ERROR)

def make_request(endpoint: str, params: dict = {}):
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

# --- SEARCH ---

def search_anime(query: str):
    return make_request("/anime", {"q": query})

def search_manga(query: str):
    return make_request("/manga", {"q": query})

def search_character(query: str):
    return make_request("/characters", {"q": query})

def search_person(query: str):
    return make_request("/people", {"q": query})

# --- DETAILS ---

def anime_details(anime_id: int):
    return make_request(f"/anime/{anime_id}/full")

def manga_details(manga_id: int):
    return make_request(f"/manga/{manga_id}/full")

def character_details(character_id: int):
    return make_request(f"/characters/{character_id}/full")

def person_details(person_id: int):
    return make_request(f"/people/{person_id}/full")

# --- AIRING / SCHEDULE ---

def todays_schedule():
    return make_request("/schedules")

def schedule_by_day(day: str):
    return make_request(f"/schedules/{day.lower()}")

# --- RANKINGS ---

def top_anime(type_filter="airing", limit=10):
    return make_request("/top/anime", {"type": type_filter, "limit": limit})

def top_manga(type_filter="manga", limit=10):
    return make_request("/top/manga", {"type": type_filter, "limit": limit})

# --- SEASONAL ---

def current_season():
    return make_request("/seasons/now")

def upcoming_season():
    return make_request("/seasons/upcoming")

def seasonal_anime(year: int, season: str):
    return make_request(f"/seasons/{year}/{season.lower()}")

# --- RECOMMENDATIONS ---

def anime_recommendations(anime_id: int):
    return make_request(f"/anime/{anime_id}/recommendations")

def manga_recommendations(manga_id: int):
    return make_request(f"/manga/{manga_id}/recommendations")

# --- EPISODES ---

def anime_episodes(anime_id: int):
    return make_request(f"/anime/{anime_id}/episodes")

# --- NATURAL LANGUAGE ROUTING ---

def route_anime_query(query: str):
    if not query:
        return None

    query = query.lower()

    if any(kw in query for kw in ["top anime", "best anime", "popular anime"]):
        return top_anime()
    if any(kw in query for kw in ["top manga", "best manga"]):
        return top_manga()
    if "today's schedule" in query or "airing today" in query:
        return todays_schedule()
    if match := re.search(r"anime schedule on (\w+)", query):
        return schedule_by_day(match.group(1))
    if match := re.search(r"anime like (.+)", query):
        anime = search_anime(match.group(1))
        if anime and anime.get("data"):
            return anime_recommendations(anime["data"][0]["mal_id"])
    if match := re.search(r"anime details for (.+)", query):
        anime = search_anime(match.group(1))
        if anime and anime.get("data"):
            return anime_details(anime["data"][0]["mal_id"])
    if match := re.search(r"manga details for (.+)", query):
        manga = search_manga(match.group(1))
        if manga and manga.get("data"):
            return manga_details(manga["data"][0]["mal_id"])
    if match := re.search(r"episodes of (.+)", query):
        anime = search_anime(match.group(1))
        if anime and anime.get("data"):
            return anime_episodes(anime["data"][0]["mal_id"])
    if "season now" in query:
        return current_season()
    if "upcoming anime" in query:
        return upcoming_season()
    return search_anime(query)
