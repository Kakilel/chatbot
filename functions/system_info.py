import psutil
import platform
import datetime
import shutil
import os
import socket
import getpass
import GPUtil

def get_cpu_usage():
    return f" CPU Usage: {psutil.cpu_percent(interval=1)}%"
def get_current_datetime():
    now = datetime.datetime.now()
    formatted = now.strftime("%A, %d %B %Y — %I:%M:%S %p")
    return f" Date & Time: {formatted}"

def get_ram_usage():
    mem = psutil.virtual_memory()
    used = round(mem.used / (1024 ** 3), 2)
    total = round(mem.total / (1024 ** 3), 2)
    return f"RAM Usage: {used} GB / {total} GB ({mem.percent}%)"

def get_disk_usage():
    total, used, _ = shutil.disk_usage(os.getcwd())
    used_gb = round(used / (1024 ** 3), 2)
    total_gb = round(total / (1024 ** 3), 2)
    return f" Disk Usage: {used_gb} GB / {total_gb} GB"

def get_battery_status():
    battery = psutil.sensors_battery()
    if battery:
        return f"Battery: {battery.percent}% {'(Plugged In)' if battery.power_plugged else '(On Battery)'}"
    return " Battery status not available."

def get_system_uptime():
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot_time
    total_seconds = int(uptime.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"⏱ Uptime: {days}d {hours}h {minutes}m"

def get_device_info():
    uname = platform.uname()
    processor = uname.processor or f"{platform.machine()} @ {psutil.cpu_freq().max:.0f}MHz"
    return f"""🖥 System Info:
- OS: {uname.system} {uname.release}
- Version: {uname.version}
- Machine: {uname.machine}
- Processor: {processor}
- Python: {platform.python_version()}
- Logged in as: {getpass.getuser()}
"""

def get_gpu_info():
    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            return " GPU: Not detected"
        gpu = gpus[0]
        return f" GPU: {gpu.name} | Load: {gpu.load * 100:.1f}% | Temp: {gpu.temperature}°C"
    except Exception:
        return " GPU: Info unavailable"

def get_network_info():
    hostname = socket.gethostname()
    try:
        ip = socket.gethostbyname(hostname)
    except socket.error:
        ip = "Unavailable"

    net_if_addrs = psutil.net_if_addrs()
    mac_address = "Unavailable"
    for iface in net_if_addrs.values():
        for addr in iface:
            if addr.family == psutil.AF_LINK:
                mac_address = addr.address
                break
    return f""" Network Info:
- Hostname: {hostname}
- IP Address: {ip}
- MAC Address: {mac_address}
"""

def get_temperature_info():
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return "🌡 Temperature: No sensor data"
        output = ["🌡 Temperatures:"]
        for name, entries in temps.items():
            for entry in entries:
                label = entry.label or name
                output.append(f"- {label}: {entry.current}°C")
        return "\n".join(output)
    except Exception:
        return "🌡 Temperature: Sensor access error"

def get_system_info_summary():
    return "\n".join([
        get_cpu_usage(),
        get_ram_usage(),
        get_disk_usage(),
        get_current_datetime(),
        get_battery_status(),
        get_system_uptime(),
        get_gpu_info(),
        get_temperature_info(),
        get_network_info(),
        get_device_info()
    ])
