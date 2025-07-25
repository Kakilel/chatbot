import requests

def get_time_info(timezone="Africa/Nairobi"):
    url = f"https://worldtimeapi.org/api/timezone/{timezone}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        time_info = {
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
        return time_info
    except Exception as e:
        return {"error": f"Couldn't fetch time data: {e}"}
