import asyncio
import os
from itertools import batched
from pathlib import Path
from typing import Iterable

import aiofiles
from aiohttp import ClientSession

from .common import LAST_TIME, new_session
from .db import Connect
from .log import logger

BATCH_SIZE = 100


async def download_image(session: ClientSession, url: str, path: Path | str):
    async with session.get(url) as resp:
        content = await resp.read()
    async with aiofiles.open(path, 'wb') as fp:
        await fp.write(content)


async def manager(urls: Iterable[str], savepath: Path):
    def filter_exists(urls) -> Iterable[tuple[str, Path]]:
        for url in urls:
            logger.debug(f'{url=}')
            path = savepath / os.path.basename(url)
            if not path.exists():
                yield url, path

    count = 0
    for batch in batched(urls, BATCH_SIZE):
        async with new_session() as session:
            status = await asyncio.gather(
                *(
                    download_image(session, url, path)
                    for url, path in filter_exists(batch)
                )
            )
            count += len(status)
            logger.info(f'done {count}')

    logger.info(f'all done. {count} update.')


def run(database: Path, savepath: Path | None = None):
    if savepath is None:
        savepath = database.with_suffix('')
        if not savepath.exists():
            savepath.mkdir()

    conn = Connect(database)
    lt = database.with_suffix(LAST_TIME)
    if not lt.exists():
        last_ctime = 0
    else:
        last_ctime = lt.read_text().strip()

    urls = conn.select_newer_than(int(last_ctime))

    logger.info(f'start. db={database}')
    asyncio.run(manager(urls, savepath))

    last_ctime = conn.select_newest()
    lt.write_text(str(last_ctime))
