from concurrent import futures

from chapter_20.flags import save_flag, get_flag, main

COUNT_WORKERS = None


def download_one(cc: str) -> str:

    cc_img = get_flag(cc=cc)
    save_flag(img_data=cc_img, filename=f"{cc}.gif")

    print(cc, end=" ", flush=True)

    return cc


def download_many_on_thread(cc_lst: list[str]) -> int:  # 1.44 sec.

    executor = futures.ThreadPoolExecutor(max_workers=COUNT_WORKERS)
    print(f"Workers count: {executor._max_workers}")

    with executor:
        result = executor.map(download_one, cc_lst)

    return len(list(result))


def download_many_with_future_objects(cc_lst: list[str]) -> int:  # 1.66 sec.

    with futures.ThreadPoolExecutor(max_workers=COUNT_WORKERS) as executor:
        to_do: list[futures.Future] = list()

        for cc in cc_lst:
            future_object = executor.submit(download_one, cc)
            to_do.append(future_object)

            print(f"Scheduler {future_object} for {cc}")

        for num, future_object in enumerate(iterable=futures.as_completed(fs=to_do), start=1):  # without block
            result = future_object.result()

            print(f"{future_object} result {result!r}")

        return num


def download_many_on_process(cc_lst: list[str]) -> int:  # 0.68 sec.

    with futures.ProcessPoolExecutor(max_workers=COUNT_WORKERS) as executor:
        result = executor.map(download_one, cc_lst)

    return len(list(result))


if __name__ == "__main__":
    # main(downloader=download_many_on_thread)
    main(downloader=download_many_with_future_objects)
    # main(downloader=download_many_on_process)
