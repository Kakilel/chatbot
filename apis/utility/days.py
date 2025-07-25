import requests
from datetime import datetime
import calendar

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
            return "No holidays found for that request."

        results = []
        for h in holidays:
            name = h.get('name')
            date = h.get('date', {}).get('iso')
            description = h.get('description')
            holiday_type = ", ".join(h.get('type', []))
            weekday = h.get('date', {}).get('datetime', {}).get('weekday', "")
            results.append(
                f"{name} ({weekday}, {date})\nType: {holiday_type}\n {description}\n"
            )

        return "\n".join(results)

    except Exception as e:
        return f"Calendar error: {str(e)}"
