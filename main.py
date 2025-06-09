#! /bin/python3
# this is going to read several files to get the stats related to the system and transform them
# in to a dictionary and then into a json object and transfer that to the master node using the MQTT protocol

import json

import datetime
from time import sleep

import paho.mqtt
import paho.mqtt.enums
import paho.mqtt.client

# my hand made files - ohh yeah
from cpu_related import monitor_cpu_usage, get_cpu_name, cpu_temperatures_core_wise
from memory_related import get_memory_related_info
from network_related import get_network_information, get_dns_info
from packages_releated import detect_installed_packages
from utilities import *


def handle_publisher_on_connect(client_id, userdata, flags, return_code):
    # if return code is 0, then that means connection was successful
    if return_code == 0:
        print(f"Connection successful with Broker!")
    else:
        print(f"Connection with broker failed! Return Code: {return_code}")


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

    # going to run this at every 5 seconds and then sending it to the broker
    mqtt_client = paho.mqtt.client.Client(
        client_id="stats_from_machine",
        callback_api_version=paho.mqtt.enums.CallbackAPIVersion.VERSION1,
    )

    mqtt_client.on_connect = handle_publisher_on_connect
    mqtt_client.connect(host="localhost", port=1883, keepalive=60)

    mqtt_client.loop_start()

    try:
        while True:
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

            mqtt_client.publish(
                topic="machine_stats/current_stats",
                payload=json.dumps(
                    {"stats_time": datetime.datetime.now().__str__(), "stats": stats}
                ),
                qos=0,
            )

            current_time = datetime.datetime.now()
            print(
                f'[{current_time}]: Stats published on topic "machine_stats/current_stats"'
            )

            sleep(10)

    except KeyboardInterrupt:
        print(f"\tPUBLISHER STOPPED!")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

    # print(json.dumps(stats))
