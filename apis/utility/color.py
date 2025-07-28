import requests
import logging
import re

BASE_URL = "https://www.thecolorapi.com"
logging.basicConfig(level=logging.ERROR)

def get_color_info(color_input: str):
    color_input = color_input.strip().lower()

    if re.match(r"^#?[0-9a-f]{6}$", color_input):
        hex_value = color_input.replace("#", "")
        url = f"{BASE_URL}/id?hex={hex_value}"
    elif re.match(r"^(rgb|rgba)\((\d{1,3},\s*){2,3}\d{1,3}\)$", color_input):
        rgb_clean = color_input.replace(" ", "").replace("rgba", "rgb")
        url = f"{BASE_URL}/id?rgb={rgb_clean}"
    elif color_input.isalpha():
        url = f"{BASE_URL}/id?named=true&name={color_input}"
    else:
        return {"error": "Invalid color format. Use hex, rgb(), or color name."}

    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        return {
            "type": "info",
            "name": data.get("name", {}).get("value"),
            "hex": data.get("hex", {}).get("value"),
            "rgb": data.get("rgb", {}).get("value"),
            "hsl": data.get("hsl", {}).get("value"),
            "contrast": data.get("contrast", {}).get("value"),
            "image": data.get("image", {}).get("bare")
        }
    except requests.exceptions.RequestException as e:
        logging.error(e)
        return {"error": "Failed to fetch color info."}


def generate_color_scheme(base_color: str, mode: str = "monochrome", count: int = 5):
    hex_value = base_color.replace("#", "").lower()
    url = f"{BASE_URL}/scheme?hex={hex_value}&mode={mode}&count={count}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        return {
            "type": "scheme",
            "mode": mode,
            "colors": [color["hex"]["value"] for color in data.get("colors", [])],
            "image": data.get("image", {}).get("bare")
        }
    except requests.exceptions.RequestException as e:
        logging.error(e)
        return {"error": "Failed to generate color scheme."}


def generate_random_colors(mode: str = "random", count: int = 5):
    url = f"{BASE_URL}/scheme?mode={mode}&count={count}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        return {
            "type": "random",
            "mode": mode,
            "colors": [color["hex"]["value"] for color in data.get("colors", [])],
            "image": data.get("image", {}).get("bare")
        }
    except requests.exceptions.RequestException as e:
        logging.error(e)
        return {"error": "Failed to generate random colors."}


def get_named_colors():
    url = f"{BASE_URL}/named"
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        logging.error(e)
        return {"error": "Failed to fetch named colors."}


def route_color_query(text: str):
    text = text.lower().strip()

  
    if match := re.search(r"(palette|color scheme|colors?)\s+(for|of|from)?\s*(#[0-9a-fA-F]{6}|rgb\([^)]+\)|[a-zA-Z]+)", text):
        base = match.group(3)
        return generate_color_scheme(base)

    if match := re.search(r"(hex|rgb|hsl)\s+(code\s+)?(for|of)?\s*(#[0-9a-fA-F]{6}|rgb\([^)]+\)|[a-zA-Z]+)", text):
        return get_color_info(match.group(4))

    if match := re.search(r"(what\s+color\s+is|info\s+on|tell\s+me\s+about|details\s+about|color\s+info\s+for)\s*(#[0-9a-fA-F]{6}|rgb\([^)]+\)|[a-zA-Z]+)", text):
        return get_color_info(match.group(2))

    if match := re.search(r"(#[0-9a-fA-F]{6}|rgb\([^)]+\)|[a-zA-Z]{3,})", text):
        return get_color_info(match.group(1))

    if "random color" in text:
        return generate_random_colors()

    if "list named colors" in text or "named colors" in text:
        return get_named_colors()

    return {"error": "No valid color-related input found."}


def format_color_response(data):
    if "error" in data:
        return f"Error: {data['error']}"

    if data["type"] == "info":
        return (
            f"**Color Info: {data['name']}**\n"
            f"- HEX: `{data['hex']}`\n"
            f"- RGB: `{data['rgb']}`\n"
            f"- HSL: `{data['hsl']}`\n"
            f"- Contrast: {data['contrast']}\n"
            f"[Preview Image]({data['image']})"
        )

    elif data["type"] in ["scheme", "random"]:
        hexes = "\n".join(f"• `{color}`" for color in data["colors"])
        return (
            f"**Color Scheme** *(Mode: {data['mode'].capitalize()})*\n{hexes}\n"
            f"[Preview Image]({data['image']})"
        )

    return "Unknown color data format."
