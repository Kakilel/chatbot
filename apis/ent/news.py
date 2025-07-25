import requests
import re
import logging

API_KEY = "788c98dcf5e2485d850ad301d918d448"
BASE_URL = "https://newsapi.org/v2"

logging.basicConfig(level=logging.ERROR)

COUNTRY_LANG_MAP = {
    "united states": ("us", "en"),
    "usa": ("us", "en"),
    "canada": ("ca", "en"),
    "uk": ("gb", "en"),
    "united kingdom": ("gb", "en"),
    "germany": ("de", "de"),
    "france": ("fr", "fr"),
    "spain": ("es", "es"),
    "italy": ("it", "it"),
    "india": ("in", "en"),
    "china": ("cn", "zh"),
    "japan": ("jp", "ja"),
    "russia": ("ru", "ru"),
    "australia": ("au", "en"),
    "brazil": ("br", "pt"),
    "mexico": ("mx", "es"),
    "kenya": ("ke", "en"),
    "nigeria": ("ng", "en"),
    "south africa": ("za", "en"),
}

def infer_country_language(location: str):
    location = location.strip().lower()
    return COUNTRY_LANG_MAP.get(location, ("us", "en"))

def make_request(endpoint: str, params: dict):
    params["apiKey"] = API_KEY
    try:
        res = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=10)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        return {"error": str(e)}

def get_top_headlines(country: str = "us", category: str = None):
    params = {"country": country}
    if category:
        params["category"] = category
    return make_request("top-headlines", params)

def search_news(query: str, language: str = "en", from_param: str = None):
    params = {"q": query, "language": language}
    if from_param:
        params["from"] = from_param
    return make_request("everything", params)

def format_news_response(data):
    if not data or not data.get("articles"):
        return "No news found for your query."

    articles = data["articles"][:5]
    result = []
    for article in articles:
        title = article.get("title", "No title")
        description = article.get("description", "")
        url = article.get("url", "")
        date = article.get("publishedAt", "").split("T")[0]
        result.append(f"📰 *{title}* ({date})\n{description}\n🔗 {url}")
    return "\n\n".join(result)

def route_news_query(query: str):
    query = query.lower()

    if match := re.search(r"(top|latest|breaking)? ?(news|headlines)( in)? ([a-z]{2})\b", query):
        country = match.group(4)
        return get_top_headlines(country)

    if match := re.search(r"\b(tech|sports|business|entertainment|health|science)\b( news)?", query):
        return get_top_headlines(category=match.group(1))

    if match := re.search(r"(news|headlines)( about| on| regarding)? (.+?) (from|since|after) (\d{4}-\d{2}-\d{2})", query):
        topic = match.group(3).strip()
        date = match.group(5)
        return search_news(topic, from_param=date)

    if match := re.search(r"(news|headlines)( about| on| regarding)? (.+)", query):
        return search_news(match.group(3).strip())

    if match := re.search(r"what'?s happening (in|at|around) ([a-zA-Z ]+)", query):
        location = match.group(2).strip()
        country, lang = infer_country_language(location)
        return get_top_headlines(country)

    if match := re.search(r"show me (top|latest)? news (from|in) ([a-zA-Z ]+)", query):
        location = match.group(3).strip()
        country, lang = infer_country_language(location)
        return get_top_headlines(country)

    return search_news(query)
