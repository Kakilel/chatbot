import requests

def get_joke(separate=False):
    url = "https://v2.jokeapi.dev/joke/Any?safe-mode"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['type'] == 'single':
            if separate:
                return {'setup': data['joke'], 'delivery': ""}
            return data['joke']
        else:
            if separate:
                return {"setup": data["setup"], "delivery": data["delivery"]}
            return f"{data['setup']} ... {data['delivery']}"
    except Exception as e:
        if separate:
            return {'setup': 'Error getting joke', 'delivery': str(e)}
        return f"Error getting joke: {str(e)}"

# Example usage:
print(get_joke(separate=True)) 
