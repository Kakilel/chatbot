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

    print("[MOVIE DEBUG] User input →", query) 
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

    if match := re.search(r"(about|on|is)\s+(.*)", query):
        fallback_query = match.group(2)
        movie = search_movie(fallback_query)
        if movie and movie.get("results"):
            return movie

    movie = search_movie(query)
    if movie and movie.get("results"):
        return movie

    return {"results": []}

def search_movie(query: str):
    if not query:
        return None
    response = make_request("/search/movie", {"query": query})
    results = response.get("results", [])
    
    for result in results:
        if result.get("title", "").lower() == query.lower():
            return {"results": [result]}

    return response

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
    return make_request(f"/movie/{movie_id}")

def movie_credits(movie_id: int):
    return make_request(f"/movie/{movie_id}/credits")

def movie_recommendations(movie_id: int):
    return make_request(f"/movie/{movie_id}/recommendations")

def movie_reviews(movie_id: int):
    return make_request(f"/movie/{movie_id}/reviews")

def movie_external_ids(movie_id: int):
    return make_request(f"/movie/{movie_id}/external_ids")

def movie_watch_providers(movie_id: int):
    return make_request(f"/movie/{movie_id}/watch/providers")

def movie_images(movie_id: int):
    return make_request(f"/movie/{movie_id}/images")

def movie_videos(movie_id: int):
    return make_request(f"/movie/{movie_id}/videos")

def person_details(person_id: int):
    return make_request(f"/person/{person_id}")

def person_movie_credits(person_id: int):
    return make_request(f"/person/{person_id}/movie_credits")

def format_movie_response(data):
    if not data:
        return "No movie information found."

    if "results" in data and isinstance(data["results"], dict):
        country = "KE"  
        country_data = data["results"].get(country)
        if not country_data:
            return f"No streaming information available for {country}."
        
        lines = [f"🎬 Available in {country.upper()}:\n"]
        if link := country_data.get("link"):
            lines.append(f"🔗 More info: {link}")
        for method in ["flatrate", "buy", "rent"]:
            if method in country_data:
                platform_list = [provider["provider_name"] for provider in country_data[method]]
                method_name = {
                    "flatrate": "Streaming",
                    "buy": "Buy",
                    "rent": "Rent"
                }[method]
                lines.append(f"📺 {method_name}: {', '.join(platform_list)}")
        return "\n".join(lines)

    if 'results' in data and isinstance(data['results'], list):
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



if __name__ == "__main__":
    print("=== Testing Movies API ===")
    test_queries = [

        "Where can I watch Avatar?",
        "Give me the trailer of Oppenheimer",
    ]
    for q in test_queries:
        print(f"\n--- Test: {q}")
        result = route_movie_query(q)
        print(format_movie_response(result))
