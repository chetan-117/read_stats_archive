import os
import subprocess


def get_hostname() -> str:
    return open("/etc/hostname").read().strip()


def get_os_name() -> str:
    return (
        list(
            filter(
                lambda line: line.startswith("PRETTY_NAME"),
                open("/etc/os-release").readlines(),
            )
        )[0]
        .strip()
        .split("=")[1][1:-1]
    )


def get_kernel_version() -> str:
    return open("/proc/version").read().split(" ")[2]


def get_uptime_pretty(uptime: float) -> str:
    updays = round(uptime // 86400)
    uphours = round(uptime % 86400 // 3600)
    upmins = round(uptime % 86400 % 3600 // 60)

    return f"{updays} {"days" if updays>1 else "day"}, {uphours} {"hours" if uphours>1 else "hour"}, {upmins} {"mins" if upmins>1 else "min"}"


def get_uptime_seconds() -> float:
    return float(open("/proc/uptime").read().split(" ")[0])


def get_shell() -> str:
    return os.environ["SHELL"]


""" 
    total = memtotal + swap total + reserved bits and kernel binary code
    used = total - available 
    buff/cache = sum(buffer, cache)
"""


def get_memory_related_info_via_command():

    ram_info = subprocess.run(
        "free -h | awk '/^Mem:/ {print $2, $3, $4, $7}'",
        text=True,
        capture_output=True,
        shell=True,
    ).stdout

    memory_total, memory_used, memory_free, memory_available = ram_info.strip().split(
        " "
    )

    swap_info = subprocess.run(
        "free -h | awk '/^Swap:/ {print $2, $3, $4}'",
        text=True,
        capture_output=True,
        shell=True,
    ).stdout
    swap_total, swap_used, swap_free = swap_info.strip().split(" ")

    return {
        "memory_used": memory_used,
        "memory_free": memory_free,
        "memory_total": memory_total,
        "memory_available": memory_available,
        "swap_used": swap_used,
        "swap_total": swap_total,
        "swap_free": swap_free,
    }
