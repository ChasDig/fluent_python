import asyncio

from httpx import AsyncClient

from chapter_20.flags import main, save_flag, BASE_URL


async def get_flag(client: AsyncClient, cc: str) -> bytes:
    url = f"{BASE_URL}/{cc}/{cc}.gif".lower()
    response = await client.get(url=url, timeout=6, follow_redirects=True)

    return response.read()


async def download_one(client: AsyncClient, cc: str) -> str:
    img = await get_flag(client=client, cc=cc)
    save_flag(img_data=img, filename=f"{cc}.gif")
    print(cc, end=" ", flush=True)

    return cc


async def supervisor(cc_lst: list[str]) -> int:
    async with AsyncClient() as client:
        to_do = [download_one(client=client, cc=cc) for cc in cc_lst]

        res = await asyncio.gather(*to_do)

    return len(res)


def download_many(cc_lst: list[str]) -> int:
    return asyncio.run(main=supervisor(cc_lst=cc_lst))


if __name__ == "__main__":
    main(downloader=download_many)


