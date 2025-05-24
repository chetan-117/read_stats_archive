#! /bin/python3
# this is going to read several files to get the stats related to the system and transform them
# in to a dictionary and then into a json object and transfer that to the master node using the MQTT protocol

import json

# my hand made files - ohh yeah
from cpu_usage import monitor_cpu_usage
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
        "memory_related": get_memory_related_info_via_command(),
        "networks": {
            "interface_name": {
                "ip": "ip address",
                "tx_packets": "some number",
                "rx_packets": "some number",
                "tx_bytes": "number in bytes",
                "rx_bytes": "number in bytes",
            },
            "another_interface_name": {
                "ip": "ip address",
                "tx_packets": "some number",
                "rx_packets": "some number",
                "tx_bytes": "number in bytes",
                "rx_bytes": "number in bytes",
            },
            "dns_resolve_file": {},
        },
        "OS": get_os_name(),
        "hostname": get_hostname(),
        "uptime_seconds": get_uptime_seconds(),
        "uptime_pretty": get_uptime_pretty(get_uptime_seconds()),
        "kernel": get_kernel_version(),
        "number of installed packages": "value to get",
        "shell": get_shell(),
        "cpu usage": monitor_cpu_usage(continuous=False),
        "cpu info": "everything related to the CPU",
        "thermals_information": {
            "fan": "rpm speed",
            "cpu temperatures": [
                # multiple values for the multiple cores of the CPU
            ],
        },
    }

    print(json.dumps(stats))
