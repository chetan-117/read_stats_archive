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

# packages
#   snap => /snap or /var/lib/snap and count the directories only

#  dnf system checking => /etc/fedora|redhat|centos-release
#   dnf => search /var/lib/rpm and look for the count(*) entries in sqlite file


# apt system checking => /etc/debian_release
#   apt => look for /var/lib/dpkg/status file and do something there to know packages count
# I am going to get support for dpkg | rpm based systems only right now
def detect_installed_packages() -> str:
    distribution_type: str = None
    result_string: str = ""

    if os.path.exists("/etc/debian_version"):
        # debian based system
        distribution_type = "debian"

    for os_type in (
        "/etc/redhat-release",
        "/etc/fedora-release",
        "/etc/centos-release",
    ):
        if os.path.exists(os_type):
            distribution_type = "redhat"
            break

    if distribution_type == "redhat":
        # have to read the sqlite file for the count of installed packages
        with sqlite3.connect("/var/lib/rpm/rpmdb.sqlite") as conn:
            count_of_rpm_packges = conn.execute(
                "Select count(*) from Packages"
            ).fetchall()[0][0]
            result_string += str(count_of_rpm_packges) + " (rpm)"

    if distribution_type == "debian":
        # {Status: install ok installed) written for the package name in /var/lib/dpkg/status
        with open("/var/lib/dpkg/status") as dpkg_status_file:
            count_of_dpkg_packages = list(
                filter(
                    lambda line: line.startswith("Status: install ok insatlled"),
                    dpkg_status_file.readlines(),
                )
            ).__len__()
            result_string += str(count_of_dpkg_packages) + " (dpkg)"

    # checking for snap packages if installed
    if os.path.isdir("/snap"):
        # then there are snap packages
        count_of_snap_packages = list(
            filter(
                lambda dirname: os.path.isdir(dirname) and dirname != "bin",
                os.listdir("/snap"),
            )
        ).__len__()

        result_string += ", " + str(count_of_snap_packages) + " (snap)"

    return result_string


if __name__ == "__main__":
    print(detect_installed_packages())
