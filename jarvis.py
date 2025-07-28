from functions import (
    system_control,
    reminders,
    launcher,
    system_info,
    memory,
    voice,
    wakeword,
)
import re


def handle_jarvis_command(text: str) -> str | None:
    text = text.lower()

    if "remind me" in text:
        return reminders.handle_reminder_command(text)

    if "shut down" in text or "shutdown" in text:
        return system_control.shutdown()
    if "restart" in text or "reboot" in text:
        return system_control.restart()
    if "lock" in text:
        return system_control.lock()
    if "sleep" in text:
        return system_control.sleep()

    if "silent" in text:
        return system_control.mute_volume()
    if "unmute" in text:
        return system_control.unmute_volume()
    if "increase volume" in text:
        return system_control.set_volume(80)
    if "decrease volume" in text:
        return system_control.set_volume(30)
    if "set volume to" in text:
        match = re.search(r"set volume to (\d+)", text)
        if match:
            level = int(match.group(1))
            return system_control.set_volume(level) or f"Volume set to {level}%"
        return "Please specify a volume level."

    if "open" in text:
        app = text.split("open", 1)[-1].strip()
        return system_control.open_app(app)
    if "close" in text:
        app = text.split("close", 1)[-1].strip()
        return system_control.close_app(app)

    if "battery" in text:
        return system_info.get_battery_status()
    if "current time" in text or "what time" in text:
        return system_info.get_current_datetime()
    if "date" in text or "uptime" in text:
        return system_info.get_system_uptime()
    if "cpu" in text:
        return system_info.get_cpu_usage()
    if "memory usage" in text or "ram" in text:
        return system_info.get_ram_usage()

    if "remember that" in text:
        return memory.remember(text)
    if "what do you remember" in text or "recall memory" in text:
        return memory.recall()
    if "forget everything" in text:
        return memory.clear_memory()

    if "speak this" in text:
        content = text.split("speak this", 1)[-1].strip()
        voice.speak(content)
        return f"Speaking: {content}"

    if "activate wake word" in text:
        wakeword.detect_wake_word()
        return "Wake word listening activated."

    return None
