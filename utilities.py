import os
import sqlite3

# import subprocess


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


# doesn't appear to be of much use, but discuss with people and then decide
""" 
def get_shell() -> str:
    return os.environ["SHELL"]
"""


def bytes_proper_format(memory_value: str, all_KB=True) -> str:
    # by default all the things are in kB, so I only have to
    # convert with a factor of 20 to make them in to GB
    if all_KB:
        gega_factor = 2**20
        mega_factor = 2**10
    else:
        gega_factor = 2**30
        mega_factor = 2**20

    return (
        str(round(memory_value / gega_factor, 3)) + " GB"
        if memory_value >= gega_factor
        else str(round(memory_value / mega_factor)) + " MB"
    )


if __name__ == "__main__":
    pass
