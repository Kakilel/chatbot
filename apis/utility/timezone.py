import requests
import re

def get_time_info(timezone="Africa/Nairobi"):
    url = f"https://worldtimeapi.org/api/timezone/{timezone}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        return {
            "Local Time": data["datetime"].split("T")[1].split(".")[0],
            "UTC Offset": data["utc_offset"],
            "Time Zone": data["timezone"],
            "Abbreviation": data["abbreviation"],
            "Day of Week": data["day_of_week"],
            "Day of Year": data["day_of_year"],
            "Week Number": data["week_number"],
            "DST": "Yes" if data["dst"] else "No",
            "Unix Time": data["unixtime"]
        }
    except Exception as e:
        return {"error": f"Couldn't fetch time data: {e}"}

def format_time_info(info):
    if "error" in info:
        return info["error"]
    return "\n".join(f"**{k}**: {v}" for k, v in info.items())

def route_time_query(text: str):
    match = re.search(r"(?:time(?:zone)? (?:in|for)|what(?:'s| is) the time(?:zone)? (?:in|for)) ([\w/\-_]+)", text.lower())
    if match:
        timezone = match.group(1).replace(" ", "_")
        return format_time_info(get_time_info(timezone))
    
    if "current time" in text or "local time" in text:
        return format_time_info(get_time_info()) 
    
    return None
