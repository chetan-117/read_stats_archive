#! /bin/python3
# this is going to read several files to get the stats related to the system and transform them
# in to a dictionary and then into a json object and transfer that to the master node using the MQTT protocol

import json

# my hand made files - ohh yeah
from cpu_related import monitor_cpu_usage, get_cpu_name, cpu_temperatures_core_wise
from memory_related import get_memory_related_info
from network_related import get_network_information, get_dns_info
from packages_releated import detect_installed_packages
from utilities import *


if __name__ == "__main__":
    # methods to read the files separately

    """
    OS
    host
    uptime
    kernel
    number of installed packages
    shell being used
    """

    stats: dict = {
        "memory_related": get_memory_related_info(),
        "networks": {
            "host": get_network_information(),
            "dns_resolve_file": get_dns_info(),
        },
        "OS": get_os_name(),
        "hostname": get_hostname(),
        "uptime_seconds": get_uptime_seconds(),
        "uptime_pretty": get_uptime_pretty(get_uptime_seconds()),
        "kernel": get_kernel_version(),
        "number of installed packages": detect_installed_packages(),
        # "shell": get_shell(),
        "cpu usage": monitor_cpu_usage(continuous=False),
        "cpu info": get_cpu_name(),
        "thermals_information": {
            "fan": "NA",
            "cpu temperatures(°C)": cpu_temperatures_core_wise(),
        },
    }

    print(json.dumps(stats))
