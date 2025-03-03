import asyncio
from pathlib import Path
from typing import Any, Coroutine, Iterable

import aiofiles
from aiohttp import ClientSession

from .api import PAGE_SIZE, api_user_album
from .log import logger
from .parser import Config, Up
from .rest import Item, dump_item, load_item, parse_response
from .utils import new_session, new_session_a

BATCH_SIZE = 100

INFO_JSON = "info.json"


CHUNK_SIZE = 1024


async def _download_image(session: ClientSession, url: str, path: Path | str):
    async with session.get(url) as resp, aiofiles.open(path, "wb") as fp:
        chunks = resp.content.iter_chunked(CHUNK_SIZE)
        async for chunk in chunks:
            await fp.write(chunk)


async def download_image(session: ClientSession, urls: Iterable[str], savepath: Path):
    def filter_exists(urls: Iterable[str]) -> Iterable[tuple[str, Path]]:
        for url in urls:
            logger.debug(f"{url=}")
            name = url.rsplit("/", 1)[1].rsplit("?", 1)[0]
            path = savepath / name
            if not path.exists():
                yield url, path

    tasks = (_download_image(session, url, path) for url, path in filter_exists(urls))
    await asyncio.gather(*tasks)
    return savepath


async def fetch_image(savepath: Path):
    async with new_session_a() as session:
        tasks = list[Coroutine[Any, Any, Path]]()
        for item_path in savepath.iterdir():
            json_str = (item_path / INFO_JSON).read_text(encoding="utf-8")
            urls = [pic.img_src for pic in load_item(json_str).pictures]
            tasks.append(download_image(session, urls, item_path))

        futs = asyncio.as_completed(tasks)
        num_task = len(tasks)
        for i, fut in enumerate(futs, start=1):
            try:
                savepath = await fut
                logger.info(f"{i}/{num_task} {savepath} done")
            except Exception as e:
                logger.error(f"{i}/{num_task} {savepath} failed: {e}")


def get_items(uid: str) -> Iterable[Item]:
    sess = new_session()
    # 从最新的一页（0）开始爬取数据。
    page_num = 0
    while True:
        url = api_user_album(uid, page_num)
        logger.debug(f"{url=}")
        resp = sess.get(url)
        if resp.status_code != 200:
            logger.error(f"error: {resp.status_code} {url}")
            break
        items = parse_response(resp.content).data.items
        yield from items

        # 如果当前页图集数量小于 page size，认为到达最后一页，退出循环
        # 一般只有第一次运行才会遇到
        if len(items) < PAGE_SIZE:
            logger.info("page end")
            break
        page_num += 1


async def fetch_info(up: Up, savepath: Path):
    logger.info(f"downloading {up.name}...")

    # 读取最新 item ctime ，用于判断是否需要更新
    ctimes = [int(path.name) for path in savepath.iterdir()]
    ctimes.append(0)
    last_ctime = max(ctimes)

    for item in get_items(up.uid):
        if item.ctime <= last_ctime:
            break
        item_path = savepath / f"{item.ctime}"
        item_path.mkdir(exist_ok=True)
        (item_path / INFO_JSON).write_text(dump_item(item), encoding="utf-8")


async def _run(config: Config):
    config.root.mkdir(exist_ok=True)
    tasks = list[Coroutine[Any, Any, None]]()
    for up in config.up:
        savepath = config.root / up.name
        savepath.mkdir(exist_ok=True)
        tasks.append(fetch_info(up, savepath))
        tasks.append(fetch_image(savepath))
    await asyncio.gather(*tasks)


def run(config: Config):
    asyncio.run(_run(config))
