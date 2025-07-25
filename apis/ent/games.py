import requests
import logging
import re

API_KEY = "4fdeb4f662c24280bdc99d1d7426b1a6"
BASE_URL = "https://api.rawg.io/api"

logging.basicConfig(level=logging.ERROR)

def make_request(endpoint: str, params: dict = {}):
    params["key"] = API_KEY
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


def search_game(query: str):
    return make_request("/games", {"search": query})


def game_details(game_slug: str):
    return make_request(f"/games/{game_slug}")


def game_screenshots(game_slug: str):
    return make_request(f"/games/{game_slug}/screenshots")


def game_trailers(game_slug: str):
    return make_request(f"/games/{game_slug}/movies")


def game_suggestions(game_slug: str):
    return make_request(f"/games/{game_slug}/suggested")


def route_game_query(query: str):
    if not query:
        return None

    query = query.lower()

    if match := re.search(r"game details for (.+)", query):
        game = search_game(match.group(1))
        if game and game.get("results"):
            return game_details(game["results"][0]["slug"])

    if match := re.search(r"screenshots of (.+)", query):
        game = search_game(match.group(1))
        if game and game.get("results"):
            return game_screenshots(game["results"][0]["slug"])

    if match := re.search(r"trailers? (for|of) (.+)", query):
        game = search_game(match.group(2))
        if game and game.get("results"):
            return game_trailers(game["results"][0]["slug"])

    if match := re.search(r"games? (like|similar to) (.+)", query):
        game = search_game(match.group(2))
        if game and game.get("results"):
            return game_suggestions(game["results"][0]["slug"])

    if match := re.search(r"search for (.+)", query):
        return search_game(match.group(1))

    return search_game(query)

def format_game_response(data):
    if not data or "name" not in data:
        return "No game info found."

    name = data.get("name", "Unknown Title")
    description = data.get("description_raw", "No description available.")
    website = data.get("website", "")
    released = data.get("released", "Unknown")

    return f"**{name}** (Released: {released})\n\n{description}\n\n{website if website else ''}"

