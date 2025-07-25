import requests

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

