import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import re
import requests
import os
from mpl_toolkits.mplot3d import Axes3D


# === Symbolic Math === #

def evaluate_expression(expr: str):
    try:
        result = sp.sympify(expr)
        return str(result.evalf())
    except Exception:
        return "Could not evaluate expression."

def simplify_expression(expr: str):
    try:
        return str(sp.simplify(expr))
    except Exception:
        return "Could not simplify expression."

def solve_equation(expr: str):
    try:
        x = sp.symbols('x')
        lhs, rhs = expr.split('=')
        solution = sp.solve(sp.sympify(lhs) - sp.sympify(rhs), x)
        return str(solution)
    except Exception:
        return "Could not solve the equation."

def differentiate_expression(expr: str):
    try:
        x = sp.symbols('x')
        return str(sp.diff(expr, x))
    except Exception:
        return "Could not differentiate expression."

def integrate_expression(expr: str):
    try:
        x = sp.symbols('x')
        return str(sp.integrate(expr, x))
    except Exception:
        return "Could not integrate expression."

def limit_expression(expr: str, variable='x', to=0, direction='+'):
    try:
        x = sp.symbols(variable)
        parsed = sp.sympify(expr)
        return str(sp.limit(parsed, x, to, dir=direction))
    except Exception:
        return "Could not compute the limit."


# === Step-by-Step (WolframAlpha) === #

def query_wolframalpha_step_by_step(query: str):
    app_id = os.getenv("T2QKGJYAUA")  
    if not app_id:
        return "Error: WolframAlpha App ID not set."
    
    url = "https://api.wolframalpha.com/v1/result"
    params = {"i": query, "appid": app_id}
    
    try:
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            return r.text
        else:
            return f"Error: WolframAlpha responded with {r.status_code}"
    except:
        return "WolframAlpha request failed."

def solve_math_step_by_step(query: str):
    result = query_wolframalpha_step_by_step(query)
    if "Wolfram|Alpha did not understand" in result or result.startswith("Error"):
        return evaluate_expression(query)
    return result


# === Statistics === #

def compute_statistics(numbers: list):
    try:
        arr = np.array(numbers)
        return {
            "mean": np.mean(arr),
            "median": np.median(arr),
            "mode": float(sp.stats.Mode(arr).doit()),
            "variance": np.var(arr),
            "std_dev": np.std(arr)
        }
    except Exception:
        return "Invalid list of numbers."


# === Graphs (2D, 3D, Parametric, Implicit) === #

def generate_2d_graph(expr):
    try:
        x = sp.symbols('x')
        f = sp.lambdify(x, sp.sympify(expr), modules=['numpy'])
        xs = np.linspace(-10, 10, 400)
        ys = f(xs)
        fig, ax = plt.subplots()
        ax.plot(xs, ys)
        ax.set_title(f"Graph of {expr}")
        return encode_plot(fig)
    except Exception:
        return "Failed to generate 2D graph."

def generate_3d_graph(expr):
    try:
        x, y = sp.symbols('x y')
        f = sp.lambdify((x, y), sp.sympify(expr), modules=['numpy'])
        X = np.linspace(-5, 5, 100)
        Y = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(X, Y)
        Z = f(X, Y)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis')
        return encode_plot(fig)
    except Exception:
        return "Failed to generate 3D graph."

def generate_parametric_plot(expr_x, expr_y, t_min=0, t_max=10):
    try:
        t = sp.symbols('t')
        fx = sp.lambdify(t, sp.sympify(expr_x), modules=['numpy'])
        fy = sp.lambdify(t, sp.sympify(expr_y), modules=['numpy'])
        ts = np.linspace(t_min, t_max, 400)
        xs = fx(ts)
        ys = fy(ts)
        fig, ax = plt.subplots()
        ax.plot(xs, ys)
        ax.set_title(f"Parametric plot: x(t)={expr_x}, y(t)={expr_y}")
        return encode_plot(fig)
    except Exception:
        return "Failed to generate parametric plot."

def generate_implicit_plot(equation):
    try:
        x, y = sp.symbols('x y')
        expr = sp.sympify(equation)
        fig, ax = sp.plot_implicit(sp.Eq(expr, 0), show=False)
        return encode_plot(fig._backend.fig)
    except Exception:
        return "Failed to generate implicit plot."

def encode_plot(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return image_base64


# === Geometry (GeoGebra basic API example) === #

def create_geogebra_diagram(construction_str: str):
    try:
        url = "https://www.geogebra.org/api/json.php"
        payload = {
            "cmd": "newMaterial",
            "title": "Auto Diagram",
            "ggbBase64": construction_str,
            "visibility": "O"
        }
        headers = {"Content-Type": "application/json"}
        r = requests.post(url, json=payload, headers=headers)
        if r.status_code == 200:
            return r.json().get('material_id')
        return "Error generating geometry."
    except:
        return "GeoGebra API error."


# === Router === #

def route_math_query(text: str):
    text = text.lower().strip()

    # Stats
    if "mean" in text or "average" in text:
        nums = extract_numbers(text)
        return f"Mean: {np.mean(nums)}"
    if "median" in text:
        nums = extract_numbers(text)
        return f"Median: {np.median(nums)}"
    if "mode" in text:
        nums = extract_numbers(text)
        return f"Mode: {float(sp.stats.Mode(nums).doit())}"
    if "standard deviation" in text:
        nums = extract_numbers(text)
        return f"Standard Deviation: {np.std(nums)}"

    # Step-by-step fallback
    if "solve" in text or "differentiate" in text or "integrate" in text or "limit" in text:
        return solve_math_step_by_step(text)

    # Graphs
    if "graph" in text or "plot" in text:
        if "3d" in text:
            return generate_3d_graph(extract_expression(text))
        if "parametric" in text:
            return generate_parametric_plot("cos(t)", "sin(t)")
        if "implicit" in text or "circle" in text:
            return generate_implicit_plot("x**2 + y**2 - 25")
        return generate_2d_graph(extract_expression(text))

    # Algebra
    if "simplify" in text:
        return simplify_expression(extract_expression(text))
    if "=" in text:
        return solve_equation(text)

    return evaluate_expression(text)

def extract_expression(text: str):
    return re.sub(r"[^0-9x\+\-\*/\^\.\(\) ]", "", text)

def extract_numbers(text: str):
    return [float(x) for x in re.findall(r"[-+]?\d*\.\d+|\d+", text)]


# === MAIN (for CLI test) === #

if __name__ == "__main__":
    while True:
        query = input("Math input: ")
        if query.lower() in ("exit", "quit"):
            break
        result = route_math_query(query)
        print(result)
