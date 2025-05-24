import os
import subprocess
from functools import reduce
from json import dumps


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


def memory_proper_format(memory_value) -> str:
    # by default all the things are in kB, so I only have to
    # convert with a factor of 20 to make them in to GB
    gega_factor = 2**20
    mega_factor = 2**10

    return (
        str(round(memory_value / gega_factor, 3)) + " GB"
        if memory_value >= gega_factor
        else str(round(memory_value / mega_factor)) + " MB"
    )


def get_memory_related_info() -> dict:

    # memory related information here
    meminfo_file: list = open("/proc/meminfo").readlines()
    mem_total = int(meminfo_file[0].split(" ")[-2])
    mem_free = int(meminfo_file[1].split(" ")[-2])
    mem_available = int(meminfo_file[2].split(" ")[-2])
    mem_used = mem_total - mem_available
    buffer_cache = reduce(
        lambda x, y: x + int(y.split(" ")[-2]),
        list(
            filter(
                lambda row: row.startswith("Buffers")
                or row.startswith("Cached")
                or row.startswith("SReclaimable"),
                meminfo_file,
            )
        ),
        0,
    )

    # swap related information here
    swap_total = int(
        list(filter(lambda row: row.startswith("SwapTotal"), meminfo_file))[0].split(
            " "
        )[-2]
    )

    swap_free = int(
        list(filter(lambda row: row.startswith("SwapFree"), meminfo_file))[0].split(
            " "
        )[-2]
    )

    swap_used = swap_total - swap_free

    return {
        "memory": {
            "mem_total": memory_proper_format(mem_total),
            "mem_free": memory_proper_format(mem_free),
            "mem_available": memory_proper_format(mem_available),
            "mem_used": memory_proper_format(mem_used),
            "buffer_cache": memory_proper_format(buffer_cache),
        },
        "swap": {
            "swap_total": memory_proper_format(swap_total),
            "swap_used": memory_proper_format(swap_used),
            "swap_free": memory_proper_format(swap_free),
        },
    }


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


if __name__ == "__main__":
    print(dumps(get_memory_related_info()))
