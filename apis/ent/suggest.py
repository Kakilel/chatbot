import requests
import re

def get_activity():
    url = 'https://www.boredapi.com/api/activity'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return data
    except Exception as e:
        return {"error": str(e)}

def format_activity(data):
    if not data or "error" in data:
        return f"Couldn't fetch a boredom-buster. {data.get('error', '')}"

    activity = data['activity']
    type = data.get('type', 'random').capitalize()
    participants = data.get('participants', 1)
    price = data.get('price', 0)
    accessibility = data.get('accessibility', 0)
    link = data.get('link', '')

    emojis = {
        "Education": "📚",
        "Recreational": "🎨",
        "Social": "🗣️",
        "Diy": "🛠️",
        "Charity": "❤️",
        "Cooking": "👩‍🍳",
        "Relaxation": "🧘",
        "Music": "🎵",
        "Busywork": "📋",
        "Random": "🎲"
    }

    emoji = emojis.get(type, "")

    if price == 0:
        price_label = 'Free'
    elif price < 0.3:
        price_label = 'Cheap'
    elif price < 0.6:
        price_label = 'Moderate'
    else:
        price_label = 'Pricey'

    if accessibility <= 0.2:
        difficulty = 'Easy'
    elif accessibility <= 0.5:
        difficulty = 'Moderate'
    else:
        difficulty = 'Hard'

    result = f"{emoji} **{activity}**\n"
    result += f"Participants: {participants}\n"
    result += f"{price_label} | {difficulty}\n"
    if link:
        result += f"More info: {link}"

    return result

def route_activity_query(query: str):
    query = query.lower()
    patterns = [
        r"\bbored\b",
        r"\bi'?m bored\b",
        r"\bgot any ideas\b",
        r"\bsomething to do\b",
        r"\bsuggest (an )?activity\b",
        r"\bactivity idea\b",
        r"\bwhat should i do\b",
        r"\bdo for fun\b",
        r"\bboredom buster\b"
    ]

    for pattern in patterns:
        if re.search(pattern, query):
            return get_activity()

    return None
