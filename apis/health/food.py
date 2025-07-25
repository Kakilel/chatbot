import requests
import logging
import re

API_KEY = "325bb94d1be04451b74d20fb0eb0f7ac"
BASE_URL = "https://api.spoonacular.com"

logging.basicConfig(level=logging.ERROR)

def make_request(endpoint: str, params: dict):
    params["apiKey"] = API_KEY
    try:
        res = requests.get(f"{BASE_URL}{endpoint}", params=params, timeout=10)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error: {e} - {res.text}")
    except requests.exceptions.Timeout:
        logging.error("Request timed out")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request exception: {e}")
    return None

# --- NUTRITION ---
def get_nutrition(food_name: str):
    return make_request("/food/ingredients/search", {"query": food_name, "number": 1})

def get_nutrition_info_by_id(ingredient_id: int):
    return make_request(f"/food/ingredients/{ingredient_id}/information", {"amount": 100, "unit": "g"})

# --- RECIPES ---
def search_recipes(query: str, diet: str = None):
    params = {"query": query, "number": 5}
    if diet:
        params["diet"] = diet
    return make_request("/recipes/complexSearch", params)

def get_recipe_information(recipe_id: int):
    return make_request(f"/recipes/{recipe_id}/information", {})

# --- NATURAL QUERY ROUTING ---
def route_food_query(query: str):
    query = query.lower()

    if match := re.search(r"(nutrition( facts)?|calories|macros|how (many|much) (calories|protein|fat|carbs).*?) (for|of|in) (.+)", query):
        name = match.group(7)
        result = get_nutrition(name)
        if result and result.get("results"):
            return get_nutrition_info_by_id(result["results"][0]["id"])

    if match := re.search(r"(?:find|show|give me|search for)? ?(recipes?|meals|dishes) (with|using|containing)? (.+)", query):
        return search_recipes(match.group(3))

    if match := re.search(r"(keto|vegan|vegetarian|paleo|low[- ]?carb|gluten[- ]?free|high[- ]?protein) (recipes?|meals|foods)", query):
        return search_recipes("", match.group(1))

    if match := re.search(r"(?:recipe|dish|meal) info (for|about)? (.+)", query):
        name = match.group(2)
        recipes = search_recipes(name)
        if recipes and recipes.get("results"):
            return get_recipe_information(recipes["results"][0]["id"])

    if match := re.search(r"what can i cook (with|using)? (.+)", query):
        return search_recipes(match.group(2))

    if match := re.search(r"suggest a meal (with|that includes)? (.+)", query):
        return search_recipes(match.group(2))

    return search_recipes(query)
