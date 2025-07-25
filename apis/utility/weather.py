import requests
import re

WEATHER_API_KEY = "e46bf30d0a6d485ab59222845252307"

def get_weather_emoji(condition):
    condition = condition.lower()
    if "sun" in condition or "clear" in condition:
        return "☀️"
    elif "cloud" in condition:
        return "☁️"
    elif "rain" in condition:
        return "🌧️"
    elif "snow" in condition:
        return "❄️"
    elif "storm" in condition or "thunder" in condition:
        return "⛈️"
    elif "fog" in condition or "mist" in condition:
        return "🌫️"
    return "🌡️"

def describe_feels_like(temp, feels_like):
    try:
        diff = float(temp) - float(feels_like)
        if abs(diff) >= 2:
            direction = "colder" if diff > 0 else "warmer"
            return f"It feels slightly {direction} than the actual temperature."
        else:
            return "Feels just like the temperature."
    except:
        return ""

def get_weather(city):
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": WEATHER_API_KEY,
        "q": city,
        "aqi": "no"
    }

    try:
        response = requests.get(base_url, params=params, timeout=5)
        data = response.json()

        if 'error' in data:
            return f"Error: {data['error'].get('message', 'Unknown error')}"

        location = data["location"].get("name", "Unknown")
        country = data["location"].get("country", "")
        local_time = data["location"].get("localtime", "N/A")

        temp_c = data["current"].get("temp_c", "?")
        feels_like = data["current"].get("feelslike_c", "?")
        condition = data["current"]["condition"].get("text", "Unknown")
        humidity = data["current"].get("humidity", "?")
        wind_kph = data["current"].get("wind_kph", "?")
        wind_dir = data["current"].get("wind_dir", "?")

        emoji = get_weather_emoji(condition)
        feel_note = describe_feels_like(temp_c, feels_like)

        return (
            f"{emoji} Weather in {location}, {country}:\n"
            f"  • Condition: {condition}\n"
            f"  • Temperature: {temp_c}°C (feels like {feels_like}°C)\n"
            f"  • {feel_note}\n"
            f"  • Humidity: {humidity}%\n"
            f"  • Wind: {wind_kph} kph {wind_dir}\n"
            f"  • Local Time: {local_time}"
        )

    except requests.RequestException as e:
        return f"Network Error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def route_weather_query(query: str):
    query = query.lower()

    if match := re.search(r"(is it |feel(s)? )?(hot|cold) in ([a-zA-Z\s]+)", query):
        temp_type = match.group(3)
        city = match.group(4).strip()
        response = get_weather(city)

        if isinstance(response, str):
            temp_match = re.search(r"Temperature: ([\d.]+)°C", response)
            if temp_match:
                temp = float(temp_match.group(1))
                if temp_type == "hot":
                    return f"It is {'hot' if temp >= 28 else 'not hot'} in {city.title()} ({temp}°C)"
                else:
                    return f"It is {'cold' if temp <= 12 else 'not cold'} in {city.title()} ({temp}°C)"
            return response

    patterns = [
        r"(what'?s|how'?s|tell me|give me).*(weather|forecast|temperature).* in ([a-zA-Z\s]+)",
        r"(weather|forecast|temperature) in ([a-zA-Z\s]+)",
        r"(raining|rain|sunny|cloudy|snow|snowing|windy).* in ([a-zA-Z\s]+)",
        r"in ([a-zA-Z\s]+).*(weather|forecast|like)",
        r"(current weather|today'?s weather|weather report).* ([a-zA-Z\s]+)",
        r"(how's it|what's it like) in ([a-zA-Z\s]+)",
        r"([a-zA-Z\s]+)\?*$"  
    ]

    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            groups = match.groups()
            city = next((g for g in reversed(groups) if g and g.strip()), None)
            if city:
                return get_weather(city.strip())

    return "Sorry, I couldn't understand the weather request."

def format_weather_data(weather):
    if isinstance(weather, str):
        return f"```\n{weather.strip()}\n```"

    if isinstance(weather, dict):
        if "error" in weather:
            return f"{weather['error']}"
        try:
            return (
                f"{weather.get('Time Zone', 'Unknown')}\n"
                f"Local Time: {weather.get('Local Time', '?')}\n"
                f"Temperature: {weather.get('Temperature', '?')}°C\n"
                f"Feels Like:{weather.get('Feels Like', '?')}°C\n"
                f"Condition: {weather.get('Condition', '?')}\n"
                f"Humidity:{weather.get('Humidity', '?')}%\n"
                f"Wind:{weather.get('Wind Speed', '?')} kph {weather.get('Wind Dir', '?')}\n"
                f"Day of Week:{weather.get('Day of Week', '?')}  |   Day {weather.get('Day of Year', '?')} of the year\n"
                f"UTC Offset:{weather.get('UTC Offset', '?')} | DST: {weather.get('DST', '?')}"
            )
        except Exception as e:
            return f"Could not format weather data: {e}"

    return "Invalid weather response format."


