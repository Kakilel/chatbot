import os
import subprocess
import webbrowser
import platform

APP_ALIASES = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "notepad": "notepad.exe",
    "cmd": "cmd.exe",
    "explorer": "explorer.exe",
    "vs code": os.path.expandvars(r"%USERPROFILE%\AppData\Local\Programs\Microsoft VS Code\Code.exe")
}

def launch_app(name_or_path: str) -> str:
    """
    Launch an app by name (alias or path).
    """
    app = APP_ALIASES.get(name_or_path.lower(), name_or_path)
    try:
        if platform.system() == "Windows":
            subprocess.Popen(app, shell=True)
        elif platform.system() == "Linux":
            subprocess.Popen([app])
        elif platform.system() == "Darwin":  
            subprocess.Popen(["open", app])
        else:
            return " Unsupported OS."
        return f"Launched: {name_or_path}"
    except Exception as e:
        return f" Failed to launch: {name_or_path}\n{e}"

def open_website(url: str) -> str:
    """
    Open a website in the default browser.
    """
    if not url.startswith("http"):
        url = "http://" + url
    try:
        webbrowser.open(url)
        return f" Opened website: {url}"
    except Exception as e:
        return f"Failed to open website: {url}\n{e}"

def open_file(path: str) -> str:
    """
    Open a file or folder with the default app.
    """
    try:
        if not os.path.exists(path):
            return " Path not found."
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Linux":
            subprocess.call(["xdg-open", path])
        elif platform.system() == "Darwin":
            subprocess.call(["open", path])
        return f" Opened: {path}"
    except Exception as e:
        return f"Failed to open file/folder:\n{e}"

def search_and_open(app_name: str) -> str:
    """
    Search common drives for an app and try to launch it.
    """
    drives = ['C:\\', 'D:\\'] if platform.system() == "Windows" else ['/']
    for drive in drives:
        for root, _, files in os.walk(drive):
            if app_name.lower() in [f.lower() for f in files]:
                full_path = os.path.join(root, app_name)
                try:
                    subprocess.Popen(full_path)
                    return f" Found and launched: {full_path}"
                except Exception:
                    continue
    return f" Couldn't find '{app_name}' on disk."
