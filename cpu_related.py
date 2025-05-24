from functools import reduce
from time import sleep


def get_cpu_name() -> str:
    return (
        list(
            filter(
                lambda row: row.startswith("model name"),
                open("/proc/cpuinfo").readlines(),
            )
        )[0]
        .split(":")[-1]
        .strip()
    )


# user , nice , system
def get_total_avg_percore() -> dict:
    info = list(
        filter(lambda line: line.startswith("cpu"), open("/proc/stat").readlines())
    )

    avg = reduce(lambda x, y: x + int(y), info[0].split(" ")[2:5], 0)

    # per core
    #     (user + nice + system) || (SUMMATION)
    cores = list(
        map(
            lambda row: (
                reduce(lambda x, y: x + int(y), row.split(" ")[1:4], 0),
                reduce(lambda x, y: x + int(y), row.split(" ")[1:], 0),
            ),
            info[1:],
        )
    )

    total = reduce(lambda x, y: x + int(y), info[0].split(" ")[2:], 0)

    return {"total": total, "avg": avg, "cores": cores}


def monitor_cpu_usage(continuous: bool):

    prev = get_total_avg_percore()

    # doing a wait for 2 seconds to refresh the file to the new parameters
    sleep(1)

    while True:
        curr = get_total_avg_percore()

        delta_total = abs(curr["total"] - prev["total"])
        delta_avg = abs(curr["avg"] - prev["avg"])
        usage_per_core = [
            round(
                (
                    abs(item[1][0] - item[0][0]) * 100 / abs(item[1][1] - item[0][1])
                    if (item[1][1] - item[0][1]) != 0
                    else 1
                ),
                2,
            )
            for item in zip(curr["cores"], prev["cores"])
        ]
        usage_avg = round(delta_avg * 100 / delta_total if delta_total != 0 else 1, 2)

        if continuous == False:
            return {"usage_avg(%)": usage_avg, "usage_per_core(%)": usage_per_core}

        print("=" * 80)
        print(f"{usage_per_core=}")
        print(f"{usage_avg=}\n\n")

        prev = curr

        sleep(1)


if __name__ == "__main__":
    # monitor_cpu_usage()

    print(get_cpu_name())
