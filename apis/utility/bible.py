import requests
import logging
import re

logging.basicConfig(level=logging.ERROR)
BASE_URL = "https://bible-api.com"

TRANSLATION_CODES = {
    "swahili": "swh",
    "english": "kjv",
    "king james": "kjv",
    "niv": "niv",
    "esv": "esv",
    "nlt": "nlt"
}


def get_bible_verse(reference: str, translation_code: str = ""):
    reference = reference.strip().replace(" ", "%20")
    url = f"{BASE_URL}/{reference}"
    if translation_code:
        url += f"?translation={translation_code}"

    try:
        res = requests.get(url, timeout=10)
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


def extract_translation(text: str):
    """Returns a translation code (e.g., 'swh') if text mentions a supported language."""
    for lang, code in TRANSLATION_CODES.items():
        if lang in text:
            return code
    return ""


def route_bible_query(text: str):
    text = text.lower().strip()
    translation_code = extract_translation(text)

    patterns = [
        r"(?:bible|verse|scripture)(?: for| from)? (.+)",      
        r"\b(\d?\s?[a-z]+\s\d+:\d+)",                          
        r"\b([a-z]+\s\d+:\d+)",                                
        r"\b([a-z]+\s\d+)",                                    
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            verse = match.group(1).strip()
            return get_bible_verse(verse, translation_code)

    return None


def format_bible_response(data):
    if "error" in data:
        return f"Error: {data['error']}"

    return (
        f"*{data['reference']}*\n"
        f"{data['text'].strip()}\n\n"
        f"_({data['translation']})_"
    )
