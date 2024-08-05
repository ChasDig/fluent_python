import socket
import time
import asyncio
from keyword import kwlist

MAX_KEYWORD_LEN = 4


async def domain_checker(domain: str) -> tuple[str, bool]:
    loop = asyncio.get_running_loop()
    domain_is_free = True

    try:
        await loop.getaddrinfo(host=domain, port=None)

    except socket.gaierror as _:
        domain_is_free = False

    return domain, domain_is_free


async def main() -> None:
    t0 = time.perf_counter()

    names = (kw for kw in kwlist if len(kw) < MAX_KEYWORD_LEN)
    domains = (f"{name}.def".lower() for name in names)
    coros = [domain_checker(domain=domain) for domain in domains]

    for coro in asyncio.as_completed(coros):
        domain, domain_is_free = await coro
        mark = '+' if domain_is_free else "-"

        print(f"{mark} {domain}")

    elapsed = time.perf_counter() - t0
    print(f"Checked all domains for {elapsed:.2f} sec.")


if __name__ == "__main__":
    asyncio.run(main=main())
