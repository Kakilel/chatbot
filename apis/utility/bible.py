import requests
import logging
import re

BASE_URL = "https://bible-api.com/"

logging.basicConfig(level=logging.ERROR)

def get_bible_verse(reference: str):
    reference = reference.strip()
    try:
        res = requests.get(BASE_URL + reference, timeout=10)
        res.raise_for_status()
        data = res.json()
        if "text" in data:
            return {
                "reference": data.get("reference"),
                "text": data.get("text"),
                "translation": data.get("translation_name")
            }
        else:
            return {"error": "Verse not found or invalid reference."}
    except requests.exceptions.RequestException as e:
        logging.error(e)
        return {"error": "Could not fetch verse."}

def route_bible_query(text: str):
    text = text.lower().strip()

    patterns = [
        r"(?:bible|verse|scripture)(?: for| from)? (.+)",     
        r"(john \d+:\d+)",                                   
        r"(psalm \d+)",                                       
        r"(genesis \d+:\d+)"                                  
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return get_bible_verse(match.group(1))

    return get_bible_verse(text)


def format_bible_response(data):
    if "error" in data:
        return f"Error: {data['error']}"
    return (
        f"{data['reference']}\n"
        f"{data['text'].strip()}\n\n"
        f"_({data['translation']})_"
    )
