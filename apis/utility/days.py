import requests
from datetime import datetime
import re

def get_calendarific_holidays(
    country_code="US",
    year=None,
    month=None,
    day=None,
    type_filter=None,
    location=None,
    language="en",
    rapidapi_key="3fed5ae3acmshb6f4ce20fd17af9p1857a5jsn2ec77070065e"
):
    if year is None:
        year = datetime.now().year

    url = "https://calendarific.p.rapidapi.com/v1/holidays"
    querystring = {
        "country": country_code,
        "year": str(year),
        "language": language
    }

    if month:
        querystring["month"] = month
    if day:
        querystring["day"] = day
    if type_filter:
        querystring["type"] = type_filter
    if location:
        querystring["location"] = location

    headers = {
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "calendarific.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        holidays = response.json().get('response', {}).get('holidays', [])

        if not holidays:
            return " No holidays found for that request."

        results = []
        for h in holidays[:10]:  
            name = h.get('name')
            date = h.get('date', {}).get('iso')
            description = h.get('description')
            holiday_type = ", ".join(h.get('type', []))
            weekday = h.get('date', {}).get('datetime', {}).get('weekday', "")
            results.append(
                f" {name} ({weekday}, {date})\n Type: {holiday_type}\n {description or 'No description.'}\n"
            )

        return "\n".join(results)

    except Exception as e:
        return f"Calendarific API error: {str(e)}"


def route_calendar_query(text: str):
    text = text.lower()
    today = datetime.now()
    country = "US"
    language = "en"
    year = today.year
    month = None
    day = None
    type_filter = None

    country_match = re.search(r"holidays in ([a-zA-Z]{2})", text)
    if country_match:
        country = country_match.group(1).upper()

    year_match = re.search(r"\b(20\d{2})\b", text)
    if year_match:
        year = int(year_match.group(1))

    for i, name in enumerate(["january", "february", "march", "april", "may", "june",
                              "july", "august", "september", "october", "november", "december"], 1):
        if name in text:
            month = i
            break

    day_match = re.search(r"(\d{1,2})(?:st|nd|rd|th)?", text)
    if day_match:
        d = int(day_match.group(1))
        if 1 <= d <= 31:
            day = d

    if "national" in text: type_filter = "national"
    elif "religious" in text: type_filter = "religious"
    elif "observance" in text: type_filter = "observance"

    return get_calendarific_holidays(
        country_code=country,
        year=year,
        month=month,
        day=day,
        type_filter=type_filter,
        language=language
    )

def format_holiday_data(data):
    if not data:
        return "No holidays found."

    if isinstance(data, str):
        return f"```\n{data.strip()}\n```"

    if isinstance(data, list):
        try:
            formatted = []
            for h in data[:10]: 
                name = h.get('name', 'Unnamed')
                date = h.get('date', {}).get('iso', 'Unknown Date')
                weekday = h.get('date', {}).get('datetime', {}).get('weekday', 'Unknown')
                description = h.get('description', 'No description.')
                types = ", ".join(h.get('type', []))

                formatted.append(
                    f"{name}\n"
                    f"{weekday}, {date}\n"
                    f"Type: {types or 'N/A'}\n"
                    f" {description}\n"
                )
            return "\n".join(formatted)
        except Exception as e:
            return f"Error formatting holidays: {str(e)}"

    return "Invalid holiday data format."
