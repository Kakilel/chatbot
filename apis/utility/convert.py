import math
import re

class UnitConverter:
    def __init__(self):
        self.units = {
            "length": {
                "m": 1.0, "meter": 1.0, "meters": 1.0,
                "km": 1000.0, "kilometer": 1000.0, "kilometers": 1000.0,
                "cm": 0.01, "centimeter": 0.01, "centimeters": 0.01,
                "mm": 0.001, "millimeter": 0.001, "millimeters": 0.001,
                "mi": 1609.34, "mile": 1609.34, "miles": 1609.34,
                "yd": 0.9144, "yard": 0.9144, "yards": 0.9144,
                "ft": 0.3048, "foot": 0.3048, "feet": 0.3048,
                "in": 0.0254, "inch": 0.0254, "inches": 0.0254,
            },
            "mass": {
                "g": 1.0, "gram": 1.0, "grams": 1.0,
                "kg": 1000.0, "kilogram": 1000.0, "kilograms": 1000.0,
                "mg": 0.001, "milligram": 0.001, "milligrams": 0.001,
                "lb": 453.592, "pound": 453.592, "pounds": 453.592,
                "oz": 28.3495, "ounce": 28.3495, "ounces": 28.3495,
            },
            "volume": {
                "l": 1.0, "liter": 1.0, "liters": 1.0,
                "ml": 0.001, "milliliter": 0.001, "milliliters": 0.001,
                "gal": 3.78541, "gallon": 3.78541, "gallons": 3.78541,
                "pt": 0.473176, "pint": 0.473176, "pints": 0.473176,
                "cup": 0.24, "cups": 0.24,
                "floz": 0.0295735, "fluid ounce": 0.0295735, "fluid ounces": 0.0295735,
            },
            "temperature": {
                "celsius": "c", "fahrenheit": "f", "kelvin": "k",
            },
            "time": {
                "second": 1, "seconds": 1,
                "minute": 60, "minutes": 60,
                "hour": 3600, "hours": 3600,
                "day": 86400, "days": 86400,
                "week": 604800, "weeks": 604800,
            },
            "speed": {
                "m/s": 1, "meter/second": 1, "meters/second": 1,
                "km/h": 0.277778, "kph": 0.277778,
                "mph": 0.44704, "mile/hour": 0.44704, "miles per hour": 0.44704,
                "knot": 0.514444, "knots": 0.514444,
            },
            "area": {
                "m2": 1, "square meter": 1, "square meters": 1,
                "km2": 1e6, "square kilometer": 1e6, "square kilometers": 1e6,
                "acre": 4046.86, "acres": 4046.86,
                "hectare": 10000, "hectares": 10000,
                "ft2": 0.092903, "square foot": 0.092903, "square feet": 0.092903,
            },
            "energy": {
                "joule": 1, "joules": 1,
                "calorie": 4.184, "calories": 4.184,
                "kwh": 3.6e6, "kilowatt hour": 3.6e6,
            },
            "pressure": {
                "pa": 1, "pascal": 1, "pascals": 1,
                "atm": 101325, "atmosphere": 101325, "atmospheres": 101325,
                "bar": 100000, "bars": 100000,
                "mmhg": 133.322, "millimeters of mercury": 133.322,
                "psi": 6894.76,
            },
            "power": {
                "watt": 1, "watts": 1,
                "kw": 1000, "kilowatt": 1000, "kilowatts": 1000,
                "hp": 745.7, "horsepower": 745.7,
            },
            "storage": {
                "byte": 1, "bytes": 1,
                "kilobyte": 1024, "kilobytes": 1024,
                "megabyte": 1024**2, "megabytes": 1024**2,
                "gigabyte": 1024**3, "gigabytes": 1024**3,
                "terabyte": 1024**4, "terabytes": 1024**4,
                "kb": 1000, "mb": 1e6, "gb": 1e9, "tb": 1e12,
            },
            "currency": {
                "usd": 1.0,         
                "eur": 0.92,         
                "kes": 145.0,        
                "gbp": 0.78,
                "jpy": 140.0,
                "inr": 83.0,
                "cny": 7.1,
            }
        }

    def convert(self, amount, from_unit, to_unit):
        from_unit = from_unit.lower().strip()
        to_unit = to_unit.lower().strip()

        for category, unit_dict in self.units.items():
            if from_unit in unit_dict and to_unit in unit_dict:
                if category == "temperature":
                    return self.convert_temperature(amount, from_unit, to_unit)
                base = amount * unit_dict[from_unit]
                return base / unit_dict[to_unit]

        raise ValueError(f"Cannot convert from '{from_unit}' to '{to_unit}'")

    def convert_temperature(self, amount, from_unit, to_unit):
        if from_unit == to_unit:
            return amount
        if from_unit == "celsius":
            if to_unit == "fahrenheit":
                return amount * 9 / 5 + 32
            elif to_unit == "kelvin":
                return amount + 273.15
        elif from_unit == "fahrenheit":
            if to_unit == "celsius":
                return (amount - 32) * 5 / 9
            elif to_unit == "kelvin":
                return (amount - 32) * 5 / 9 + 273.15
        elif from_unit == "kelvin":
            if to_unit == "celsius":
                return amount - 273.15
            elif to_unit == "fahrenheit":
                return (amount - 273.15) * 9 / 5 + 32
        raise ValueError(f"Invalid temperature conversion: {from_unit} to {to_unit}")

if __name__ == "__main__":
    converter = UnitConverter()
    examples = [
        (10, "km", "mi"),
        (5, "kg", "lb"),
        (100, "celsius", "fahrenheit"),
        (2, "liter", "ml"),
        (5000, "g", "kg"),
        (60, "second", "minute"),
        (1000, "byte", "megabyte"),
        (100, "usd", "kes"),
        (50, "eur", "usd"),
    ]

    for amount, from_u, to_u in examples:
        try:
            result = converter.convert(amount, from_u, to_u)
            print(f"{amount} {from_u} = {result:.4f} {to_u}")
        except Exception as e:
            print(f"Error converting {amount} {from_u} to {to_u}: {e}")

    while True:
        print("\nType 'exit' to quit.")
        amt_input = input("Enter amount: ")
        if amt_input.lower() == "exit":
            break
        from_unit = input("From unit: ")
        if from_unit.lower() == "exit":
            break
        to_unit = input("To unit: ")
        if to_unit.lower() == "exit":
            break

        try:
            amt = float(amt_input)
            converted = converter.convert(amt, from_unit, to_unit)
            print(f"{amt} {from_unit} = {converted:.4f} {to_unit}")
        except Exception as ex:
            print("Error:", ex)
def format_unit_conversion(amount, from_unit, to_unit, result):
    return f"{amount} {from_unit} = {result:.4f} {to_unit}"



def route_unit_query(text: str):
    pattern = r"(?:convert|change|how many|what(?:'s| is) the) (\d+(?:\.\d+)?)\s*(\w+)\s*(?:to|in|into)\s*(\w+)"
    match = re.search(pattern, text.lower())
    if match:
        try:
            amount = float(match.group(1))
            from_unit = match.group(2)
            to_unit = match.group(3)
            converter = UnitConverter()
            result = converter.convert(amount, from_unit, to_unit)
            return format_unit_conversion(amount, from_unit, to_unit, result)
        except Exception as e:
            return f"Error converting units: {str(e)}"
    return None
