from time import sleep, strftime
from concurrent import futures

COUNT_WORKERS = 5
COUNT_TASKS = 20
CONCAT = 10


def display(*args) -> None:
    print(strftime("[%H:%M:%S]"), end=" ")
    print(*args)


def loiter(num) -> int:
    msg_template_await = "{} loiter({}): doing nothing for {} sec."
    display(msg_template_await.format("\t" * num, num, num))

    sleep(num)

    msg_template_create = "{} loiter: {} done."
    display(msg_template_create.format("\t" * num, num))

    return num * CONCAT


def main() -> None:
    display("Start")

    executor = futures.ThreadPoolExecutor(max_workers=COUNT_WORKERS)
    results = executor.map(loiter, range(COUNT_TASKS))

    display("Results: ", results)
    display("Waiting for individual result")
    for num, result in enumerate(iterable=results, start=0):
        display(f"Result {num}: {result}")


if __name__ == "__main__":
    main()
