import requests
import re

CATEGORIES = ["programming", "misc", "dark", "pun", "spooky", "christmas", "any"]

def get_joke(category="any", separate=False):
    category = category.lower()
    if category not in CATEGORIES:
        category = "any"

    url = f"https://v2.jokeapi.dev/joke/{category}?safe-mode"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['type'] == 'single':
            if separate:
                return {'setup': data['joke'], 'delivery': ""}
            return data['joke']
        else:
            if separate:
                return {"setup": data["setup"], "delivery": data["delivery"]}
            return f"{data['setup']} ... {data['delivery']}"
    except Exception as e:
        if separate:
            return {'setup': 'Error getting joke', 'delivery': str(e)}
        return f"Error getting joke: {str(e)}"


def format_joke(joke_data):
    if isinstance(joke_data, str):
        return f" {joke_data}"
    if isinstance(joke_data, dict):
        setup = joke_data.get("setup", "")
        delivery = joke_data.get("delivery", "")
        if delivery:
            return f" {setup}\n {delivery}"
        return f" {setup}"
    return " Invalid joke format."

def route_joke_query(query: str):
    query = query.lower().strip()
    if not query:
        return None

    joke_keywords = [
        "tell me a joke", "make me laugh", "something funny", "joke please",
        "say a joke", "give me a joke", "any jokes", "funny joke", "make a joke"
    ]

    for category in CATEGORIES:
        if category in query:
            joke = get_joke(category=category, separate=True)
            return format_joke(joke)

    if any(kw in query for kw in joke_keywords):
        return format_joke(get_joke(separate=True))

    return None
