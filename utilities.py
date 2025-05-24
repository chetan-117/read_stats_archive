# import os
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
