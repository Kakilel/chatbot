import requests
import logging
import re

API_KEY = "765411659770168493c8c050f709ccd6"
BASE_URL = "https://api.themoviedb.org/3"

logging.basicConfig(level=logging.ERROR)

def make_request(endpoint: str, params: dict = {}):
    url = f"{BASE_URL}{endpoint}"
    params["api_key"] = API_KEY
    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error: {e} - {res.text}")
    except requests.exceptions.Timeout:
        logging.error("Request timed out")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request exception: {e}")
    return None


def route_movie_query(query: str):
    if not query:
        return None

    query = query.lower()

    if any(phrase in query for phrase in ["trending", "what's hot", "what's popular now"]):
        return trending_movies()

    if any(phrase in query for phrase in ["popular shows", "tv trending", "tv hot", "top tv shows"]):
        return popular_tv()

    if any(phrase in query for phrase in ["popular movies", "famous movies", "hit movies", "hot movies"]):
        return popular_movies()

    if any(phrase in query for phrase in ["top rated", "best movies", "top list", "critically acclaimed"]):
        return top_rated_movies()

    if any(phrase in query for phrase in ["upcoming movies", "what's coming", "new releases"]):
        return upcoming_movies()

    if any(phrase in query for phrase in ["now playing", "in theatres", "in cinemas", "currently showing"]):
        return now_playing()

    if match := re.search(r"details (for|about) (.+)", query):
        movie = search_movie(match.group(2))
        if movie and movie.get("results"):
            return movie_details(movie["results"][0]["id"])

    if match := re.search(r"recommend( me)? (a )?(movie|film|show) (like|similar to) (.+)", query):
        movie = search_movie(match.group(5))
        if movie and movie.get("results"):
            return movie_recommendations(movie["results"][0]["id"])

    if match := re.search(r"(movies|films|tv shows|shows) (with|featuring|starring|by) (.+)", query):
        person = search_person(match.group(3))
        if person and person.get("results"):
            return person_movie_credits(person["results"][0]["id"])

    if match := re.search(r"who (acted|stars|is in) (.+)", query):
        movie = search_movie(match.group(2))
        if movie and movie.get("results"):
            return movie_credits(movie["results"][0]["id"])

    if match := re.search(r"where can i watch (.+)", query):
        movie = search_movie(match.group(1))
        if movie and movie.get("results"):
            return movie_watch_providers(movie["results"][0]["id"])

    if match := re.search(r"(trailer|video) (of|for) (.+)", query):
        movie = search_movie(match.group(3))
        if movie and movie.get("results"):
            return movie_videos(movie["results"][0]["id"])

    if match := re.search(r"(posters?|images?|pictures?) (of|for) (.+)", query):
        movie = search_movie(match.group(3))
        if movie and movie.get("results"):
            return movie_images(movie["results"][0]["id"])

    if match := re.search(r"(reviews?|ratings?) (for|of) (.+)", query):
        movie = search_movie(match.group(3))
        if movie and movie.get("results"):
            return movie_reviews(movie["results"][0]["id"])

    if match := re.search(r"(external ids|social links|imdb|facebook|twitter|instagram) for (.+)", query):
        movie = search_movie(match.group(2))
        if movie and movie.get("results"):
            return movie_external_ids(movie["results"][0]["id"])

    return search_multi(query)





def search_movie(query: str):
    if not query:
        return None
    return make_request("/search/movie", {"query": query})

def search_tv(query: str):
    if not query:
        return None
    return make_request("/search/tv", {"query": query})

def search_person(query: str):
    if not query:
        return None
    return make_request("/search/person", {"query": query})

def search_multi(query: str):
    if not query:
        return None
    return make_request("/search/multi", {"query": query})


def trending_movies(period: str = "week"):
    if period not in ["day", "week"]:
        period = "week"
    return make_request(f"/trending/movie/{period}")

def popular_movies():
    return make_request("/movie/popular")

def top_rated_movies():
    return make_request("/movie/top_rated")

def upcoming_movies():
    return make_request("/movie/upcoming")

def now_playing():
    return make_request("/movie/now_playing")

def popular_tv():
    return make_request("/tv/popular")

def top_rated_tv():
    return make_request("/tv/top_rated")

def airing_today():
    return make_request("/tv/airing_today")


def movie_details(movie_id: int):
    if not movie_id:
        return None
    return make_request(f"/movie/{movie_id}")

def tv_details(tv_id: int):
    if not tv_id:
        return None
    return make_request(f"/tv/{tv_id}")

def movie_credits(movie_id: int):
    if not movie_id:
        return None
    return make_request(f"/movie/{movie_id}/credits")

def tv_credits(tv_id: int):
    if not tv_id:
        return None
    return make_request(f"/tv/{tv_id}/credits")

def movie_recommendations(movie_id: int):
    if not movie_id:
        return None
    return make_request(f"/movie/{movie_id}/recommendations")

def movie_similar(movie_id: int):
    if not movie_id:
        return None
    return make_request(f"/movie/{movie_id}/similar")

def movie_keywords(movie_id: int):
    if not movie_id:
        return None
    return make_request(f"/movie/{movie_id}/keywords")

def movie_reviews(movie_id: int):
    if not movie_id:
        return None
    return make_request(f"/movie/{movie_id}/reviews")

def movie_external_ids(movie_id: int):
    if not movie_id:
        return None
    return make_request(f"/movie/{movie_id}/external_ids")


def person_details(person_id: int):
    if not person_id:
        return None
    return make_request(f"/person/{person_id}")

def person_movie_credits(person_id: int):
    if not person_id:
        return None
    return make_request(f"/person/{person_id}/movie_credits")

def person_tv_credits(person_id: int):
    if not person_id:
        return None
    return make_request(f"/person/{person_id}/tv_credits")

def popular_people():
    return make_request("/person/popular")


def genre_movie_list():
    return make_request("/genre/movie/list")

def genre_tv_list():
    return make_request("/genre/tv/list")

def discover_movies(filters: dict = {}):
    return make_request("/discover/movie", filters)

def discover_tv(filters: dict = {}):
    return make_request("/discover/tv", filters)


def watch_providers():
    return make_request("/watch/providers/movie")

def movie_watch_providers(movie_id: int):
    if not movie_id:
        return None
    return make_request(f"/movie/{movie_id}/watch/providers")

def tv_watch_providers(tv_id: int):
    if not tv_id:
        return None
    return make_request(f"/tv/{tv_id}/watch/providers")


def movie_images(movie_id: int):
    if not movie_id:
        return None
    return make_request(f"/movie/{movie_id}/images")

def movie_videos(movie_id: int):
    if not movie_id:
        return None
    return make_request(f"/movie/{movie_id}/videos")

def tv_images(tv_id: int):
    if not tv_id:
        return None
    return make_request(f"/tv/{tv_id}/images")

def tv_videos(tv_id: int):
    if not tv_id:
        return None
    return make_request(f"/tv/{tv_id}/videos")



def tmdb_configuration():
    return make_request("/configuration")


def format_movie_response(data):
    if not data:
        return "No movie information found."

    if 'results' in data:
        results = data['results']
        if not results:
            return "No results found."
        summary = []
        for item in results[:5]:
            title = item.get("title") or item.get("name")
            overview = item.get("overview", "No description available.")
            release = item.get("release_date") or item.get("first_air_date", "N/A")
            summary.append(f"🎬 {title} ({release})\n{overview[:180]}...")
        return "\n\n".join(summary)

    if 'title' in data or 'name' in data:
        title = data.get("title") or data.get("name")
        overview = data.get("overview", "No description available.")
        release = data.get("release_date") or data.get("first_air_date", "N/A")
        return f"🎬 {title} ({release})\n{overview}"

    return str(data)
