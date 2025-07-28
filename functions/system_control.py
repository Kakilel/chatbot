import os
import subprocess
import ctypes
import psutil
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def set_volume(level: int):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level / 100.0, None)
        return f"Volume set to {level}%"
    except Exception as e:
        return f"Failed to set volume: {e}"


def mute_volume():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(1, None)
        return "Volume muted."
    except Exception as e:
        return f"Failed to mute: {e}"


def unmute_volume():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(0, None)
        return "Volume unmuted."
    except Exception as e:
        return f"Failed to unmute: {e}"


def toggle_mute():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current = volume.GetMute()
        volume.SetMute(0 if current else 1, None)
        return "Toggled mute state."
    except Exception as e:
        return f" Failed to toggle mute: {e}"


def open_app(app_name: str):
    try:
        subprocess.Popen(app_name)
        return f"{app_name} launched."
    except FileNotFoundError:
        return f"App '{app_name}' not found."
    except Exception as e:
        return f" Failed to open '{app_name}': {e}"


def close_app(process_name: str):
    try:
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
                proc.terminate()
                return f"{process_name} closed."
        return f" {process_name} is not running."
    except Exception as e:
        return f"Failed to close {process_name}: {e}"


def shutdown():
    try:
        os.system("shutdown /s /t 1")
        return "Shutting down the system..."
    except Exception as e:
        return f"Failed to shut down: {e}"


def restart():
    try:
        os.system("shutdown /r /t 1")
        return "Restarting the system..."
    except Exception as e:
        return f"Failed to restart: {e}"


def lock():
    try:
        ctypes.windll.user32.LockWorkStation()
        return "System locked."
    except Exception as e:
        return f"Failed to lock system: {e}"


def sleep():
    try:
        ctypes.windll.PowrProf.SetSuspendState(False, True, False)
        return "System going to sleep..."
    except Exception as e:
        return f"Failed to put system to sleep: {e}"
