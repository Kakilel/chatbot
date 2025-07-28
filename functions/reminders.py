import threading
import time
import datetime
import re

reminder_list = []

def parse_time(time_text):
    now = datetime.datetime.now()

    match = re.match(r"in (\d+)\s?(second|minute|hour|day)s?", time_text)
    if match:
        value = int(match.group(1))
        unit = match.group(2)
        delta = {
            "second": datetime.timedelta(seconds=value),
            "minute": datetime.timedelta(minutes=value),
            "hour": datetime.timedelta(hours=value),
            "day": datetime.timedelta(days=value)
        }[unit]
        return now + delta

    match = re.match(r"at (\d{1,2})(:(\d{2}))?\s?(am|pm)?", time_text)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(3)) if match.group(3) else 0
        meridian = match.group(4)

        if meridian:
            if meridian.lower() == "pm" and hour < 12:
                hour += 12
            elif meridian.lower() == "am" and hour == 12:
                hour = 0

        reminder_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if reminder_time < now:
            reminder_time += datetime.timedelta(days=1)
        return reminder_time

    return None

def add_reminder(text, time_str):
    remind_time = parse_time(time_str)
    if not remind_time:
        return "I couldn't understand the time."

    reminder = {
        "text": text,
        "time": remind_time
    }
    reminder_list.append(reminder)
    return f"Reminder set: “{text}” at {remind_time.strftime('%H:%M:%S')}"

def reminder_checker(callback=None):
    """Background thread to check reminders. Optional callback for GUI popup/speech."""
    while True:
        now = datetime.datetime.now()
        for reminder in reminder_list[:]:
            if now >= reminder["time"]:
                output = f"Reminder: {reminder['text']}"
                if callback:
                    callback(output)
                else:
                    print(output)
                reminder_list.remove(reminder)
        time.sleep(1)

def start_reminder_thread(callback=None):
    thread = threading.Thread(target=reminder_checker, kwargs={"callback": callback}, daemon=True)
    thread.start()

def handle_reminder_command(text):
    match = re.match(r"remind me to (.+?) (in .+|at .+)", text, re.I)
    if match:
        task = match.group(1).strip()
        time_str = match.group(2).strip()
        return add_reminder(task, time_str)
    return "I didn't understand the reminder command."
