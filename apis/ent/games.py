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
    if not data:
        return "No game info found."

    if isinstance(data, dict) and "results" in data:
        results = data["results"]
        if not isinstance(results, list) or not results:
            return "No matching games found."

        output = ""
        for game in results[:5]:
            name = game.get("name", "Unknown Title")
            released = game.get("released", "Unknown")
            rating = game.get("rating", "N/A")
            output += f"🎮 **{name}** (Released: {released}, {rating})\n"
        return output.strip()

    if "results" in data and all("image" in item for item in data["results"]):
        images = [item["image"] for item in data["results"][:5]]
        return " Screenshots:\n" + "\n".join(images)

    if "results" in data and all("data" in item and "480" in item["data"] for item in data["results"]):
        trailers = [item["data"]["480"] for item in data["results"][:3]]
        return "🎬 Trailers:\n" + "\n".join(trailers)

    name = data.get("name", "Unknown Title")
    description = data.get("description_raw", "No description available.")
    website = data.get("website", "")
    released = data.get("released", "Unknown")
    rating = data.get("rating", "N/A")
    genres = ", ".join(g["name"] for g in data.get("genres", []))
    platforms = ", ".join(p["platform"]["name"] for p in data.get("platforms", []))

    return (
        f"**{name}**\n"
        f"Released: {released} |Rating: {rating}\n"
        f"Platforms: {platforms}\n"
        f"Genres: {genres}\n\n"
        f"{description[:500]}...\n"
        f"{website if website else ''}"
    )
