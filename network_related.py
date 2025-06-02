import os
import subprocess
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

    interface_ip_addresses = parse_fib_trie_for_ip_addr()

    full_interface_information = {
        interface: {
            "ip_addr": interface_ip_addresses[interface],
            "mac_addr": interface_mac_addresses[interface],
            "data_flow": interface_flow_info[interface],
        }
        for interface in interfaces
    }

    # print(f"{interface_mac_addresses}")
    # print(f"{interface_flow_info}")

    return full_interface_information


"""
 ================================== cancelled ==================================
    get only the Local section --> then get the ip with "/32 host LOCAL" as its value
        this is the device IP

    the network IP with the address of the last octet as 1 should be the gateway

    now since i have the IP address and its index, i have to move upwards the ladder to
    find the line starting with +-- because that contains information about the nw and the subnet etc.

    gateway is either the first usable address or the last usable address in the ip range

# to parse the fib_trie file
def parse_fib_trie():

    fib_trie_file = open("/proc/net/fib_trie").readlines()
    fib_trie_file = fib_trie_file[: fib_trie_file.__len__() // 2]

    valid_ips_match = []
    for i in range(fib_trie_file.__len__()):
        if "/32 host LOCAL" in fib_trie_file[i]:
            valid_ips_match.append(i)

    # there is some confusion that I am still facing and it is about the (not the netmask) but about the
    # gateway information and I need it to be present in that file but I can't seem to find that one

    return list(map(lambda index: fib_trie_file[index - 1].strip(), valid_ips_match))
"""


def parse_fib_trie_for_ip_addr():
    ip_ifname = subprocess.run(
        "bash ./find_ifname_by_ip.sh", shell=True, text=True, capture_output=True
    ).stdout

    return {
        row.split(":")[0].strip(): row.split(":")[1].strip()
        for row in ip_ifname.strip().split("\n")
    }


# dns related information to be retrieved from the file /run/systemd/resolve/resolv.conf
# for debian only systems -> /run/systemd/netif/leases
def get_dns_info():
    debian_netif_location = "/run/systemd/netif/leases"
    if (
        os.path.exists(debian_netif_location)
        and os.listdir(debian_netif_location).__len__() != 0
    ):
        domain_info = {
            row.split("=")[0]: row.split("=")[1].strip()
            for row in list(
                filter(
                    lambda line: line.startswith("DNS")
                    or line.startswith("DOMAINNAME"),
                    open(os.listdir(debian_netif_location)[0]).readlines(),
                )
            )
        }

        return domain_info

    return None


"""
    this thing is in work in progress, still don't have much idea on how to implement this thing 
"""
"""
def parse_ip_from_hex(ip: str) -> str:
    result: list = []

    for i in range(0, len(ip), 2):
        result.append(str(int("0x" + ip[i : i + 2], 16)))

    result.reverse()
    return ".".join(result)


def get_ip_info():
    route_table = open("/proc/net/route").readlines()[1:]

    iname_gateway_map = {}
    for row in route_table:
        cleaned_row = re.sub(r"\s+", " ", row)
        iname, _, gateway, *_ = cleaned_row.split(" ")

        if gateway != "00000000":
            iname_gateway_map[iname] = parse_ip_from_hex(gateway)
"""

if __name__ == "__main__":
    # print(dumps(get_network_information()))
    # print(parse_fib_trie())

    # ip_ifname = parse_fib_trie_for_ip_addr()
    # print(f"{ip_ifname=}")

    print(f"{get_dns_info()=}")
