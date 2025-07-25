import requests
import re

TRANSLATE_URL = "https://libretranslate.com/translate"
DETECT_URL = "https://libretranslate.com/detect"
LANGUAGES_URL = "https://libretranslate.com/languages"

def get_supported_languages():
    try:
        response = requests.get(LANGUAGES_URL)
        response.raise_for_status()
        return response.json()
    except:
        return []

def name_to_lang_code(name: str) -> str:
    try:
        name = name.strip().lower()
        languages = get_supported_languages()
        for lang in languages:
            if lang["code"].lower() == name or lang["name"].lower() == name:
                return lang["code"]
    except:
        pass
    return "en"

def detect_language(text: str) -> str:
    try:
        response = requests.post(DETECT_URL, json={"q": text})
        response.raise_for_status()
        detections = response.json()
        return detections[0]["language"] if detections else "en"
    except:
        return "en"

def translate_text(text: str, target: str = "en", source: str = None) -> str:
    try:
        target = name_to_lang_code(target)
        source = name_to_lang_code(source) if source else detect_language(text)
        payload = {
            "q": text,
            "source": source,
            "target": target,
            "format": "text"
        }
        response = requests.post(TRANSLATE_URL, json=payload, timeout=10)
        response.raise_for_status()
        translated = response.json().get("translatedText", "")
        return f"**Translated ({source} → {target})**:\n{translated}"
    except:
        return "Error: Translation failed."

def format_detect_result(text: str):
    lang = detect_language(text)
    return f"**Detected language**: {lang}"

def route_translation_query(text: str):
   
    if "detect language of" in text or "what language is" in text:
        match = re.search(r"(?:detect language of|what language is) (.+)", text)
        if match:
            return format_detect_result(match.group(1))

    match = re.search(r"translate (.+) from (\w+) to (\w+)", text)
    if match:
        phrase, source, target = match.groups()
        return translate_text(phrase, target=target, source=source)

    match = re.search(r"translate (.+) to (\w+)", text)
    if match:
        phrase, target = match.groups()
        return translate_text(phrase, target=target)

    match = re.search(r"translate (.+)", text)
    if match:
        return translate_text(match.group(1))

    return None
