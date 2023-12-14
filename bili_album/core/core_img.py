import asyncio
import os
from pathlib import Path
from typing import Iterable
from venv import logger

import aiofiles
from aiohttp import ClientSession

from ..db import Connect
from .common import LAST_TIME, new_session
from .utils import batched

BATCH_SIZE = 100


async def download_image(session: ClientSession, url: str, path: Path | str):
    async with session.get(url) as resp:
        content = await resp.read()
    async with aiofiles.open(path, 'wb') as fp:
        await fp.write(content)


async def manager(urls: Iterable[str], savepath: Path):
    count = 0
    for batch in batched(urls, BATCH_SIZE):
        async with new_session() as session:
            for url in batch:
                logger.debug(f'{url=}')
                path = savepath / os.path.basename(url)
                if path.exists():
                    continue
                await download_image(session, url, path)
                count += 1
    logger.info(f'done. {count} update.')


def run(database: Path, savepath: Path | None = None):
    if savepath is None:
        savepath = database.with_suffix('')
        if not savepath.exists():
            savepath.mkdir()

    conn = Connect(database)
    last_ctime = database.with_suffix(LAST_TIME).read_text().strip()
    urls = conn.select_newer_than(int(last_ctime))

    logger.info(f'start. db={database}')
    asyncio.run(manager(urls, savepath))
