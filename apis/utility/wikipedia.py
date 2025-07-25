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

        if "extract" not in data or not data.get("extract"):
            return {"error": "No summary found."}

        return {
            "title": data.get("title"),
            "extract": data.get("extract"),
            "url": data.get("content_urls", {}).get("desktop", {}).get("page")
        }
    except requests.exceptions.RequestException as e:
        logging.error(f"Wikipedia request failed: {e}")
        return {"error": "Could not fetch information."}


def route_wikipedia_query(text: str):
    text = text.lower().strip()

    if not re.search(r"(who|what|when|where|how|history|tell me|explain|information|define|summary|about|was|were|did|discovery|origin)", text):
        return None

    patterns = [
        r"who (is|was) (.+)",
        r"what (is|was) (.+)",
        r"tell me about (.+)",
        r"give me info(?:rmation)? on (.+)",
        r"explain (.+)",
        r"define (.+)",
        r"history of (.+)",
        r"when (did|was) (.+)",
        r"where (is|was) (.+)",
        r"origin of (.+)",
        r"(.+)",  
    ]

    for pattern in patterns:
        if match := re.match(pattern, text):
            subject = match.groups()[-1].strip()
            return get_wikipedia_summary(subject)

    return get_wikipedia_summary(text)


def format_wikipedia_result(result):
    if not result:
        return "No information available."

    if "error" in result:
        return f" {result['error']}"

    return (
        f"**{result['title']}**\n\n"
        f"{result['extract']}\n\n"
        f"[Read more]({result['url']})"
    )
