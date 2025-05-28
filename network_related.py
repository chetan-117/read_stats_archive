import os
import re
from json import dumps
from utilities import bytes_proper_format


# have to first get the interface names
# then based on those interface names --> their IP addresses
# then based on those interface names ==> their tx, rx packets and bytes
def get_network_information() -> dict:

    # interface names at /sys/class/net
    # mac address at their corresponding directories
    net_dir = "/sys/class/net"
    interfaces = os.listdir(net_dir)
    interface_mac_addresses = {
        interface_name: open(net_dir + "/" + interface_name + "/address").read().strip()
        for interface_name in interfaces
    }

    # tx and rx packets in /proc/net/dev file
    packets_info_dir = "/proc/net/dev"

    # 1:3 => received bytes and packets
    # 9:11 => sent values
    # 0 => name of the interface
    filtered_info = map(
        lambda dev: re.sub(r"\s+", " ", dev.strip()).split(" "),
        open(packets_info_dir).readlines()[2:],
    )
    interface_flow_info = {
        info[0][:-1]: {
            "recvd_bytes": bytes_proper_format(int(info[1]), all_KB=False),
            "recvd_packets": f"{int(info[2]):,}",
            "sent_bytes": bytes_proper_format(int(info[9]), all_KB=False),
            "sent_packets": f"{int(info[10]):,}",
        }
        for info in filtered_info
    }

    full_interface_information = {
        interface: {
            # "ip_addr": interface_ip_addresses[interface],
            "mac_addr": interface_mac_addresses[interface],
            "data_flow": interface_flow_info[interface],
        }
        for interface in interfaces
    }

    # print(f"{interface_mac_addresses}")
    # print(f"{interface_flow_info}")

    return full_interface_information


if __name__ == "__main__":
    print(dumps(get_network_information()))
