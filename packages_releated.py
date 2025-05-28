import os


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
        import sqlite3

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
                lambda dirname: os.path.isdir("/snap/" + dirname) and dirname != "bin",
                os.listdir("/snap"),
            )
        ).__len__()

        result_string += ", " + str(count_of_snap_packages) + " (snap)"

    # checking for flatpak packages
    if os.path.isdir("/var/lib/flatpak"):
        # then i have to count the dirs in <base_dir>/app directory
        # and directories in <base_dir>/runtime , but ignoring the .Locale and .Debug
        flatpak_apps = set(os.listdir("/var/lib/flatpak/app"))
        flatpak_runtimes = len(
            list(
                filter(
                    lambda x: ".".join(x.split(".")[:-1]) not in flatpak_apps,
                    os.listdir("/var/lib/flatpak/runtime"),
                )
            )
        )

        count_of_flatpak_packages = flatpak_apps.__len__() + flatpak_runtimes

        result_string += ", " + str(count_of_flatpak_packages) + " (flatpak)"

    return result_string


if __name__ == "__main__":
    print(detect_installed_packages())
