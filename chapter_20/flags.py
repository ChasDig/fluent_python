import time
from pathlib import Path
from typing import Callable

import httpx


BASE_URL = "https://www.fluentpython.com/data/flags"
BASE_TIMEOUT = 6.0

DOWNLOAD_DIR = Path("download")
POP10_CC = "CN IN US ID BR PK NG BD RU JP".split()
POP10_CC_INCORRECT = "CN IN US ID BR PK NG BD1 RU JP".split()  # Showing how we take future objects with errors


def get_flag(cc: str) -> bytes:
    url = f"{BASE_URL}/{cc}/{cc}.gif".lower()

    resp_ = httpx.get(url=url, timeout=BASE_TIMEOUT, follow_redirects=True)
    resp_.raise_for_status()

    return resp_.content


def save_flag(img_data: bytes, filename: str) -> None:
    (DOWNLOAD_DIR / filename).write_bytes(data=img_data)


def main(downloader: Callable[[list[str]], int]) -> None:
    DOWNLOAD_DIR.mkdir(exist_ok=True)

    t0 = time.perf_counter()
    count_flags = downloader(POP10_CC)
    elapsed = time.perf_counter() - t0

    print(f"Downloaded {count_flags} flags per {elapsed:.2f} sec.")
