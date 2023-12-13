import asyncio
import json
from pathlib import Path

import aiofiles
import aiohttp
from aiohttp.client_exceptions import ClientPayloadError
from fake_useragent import FakeUserAgent

from .constants import ITEM_KEYS, PAGE_SIZE, api_user_album
from .db import Connect
from .log import logger
from .utils import filter_dict


def new_session():
    return aiohttp.ClientSession(
        headers={'user-agent': FakeUserAgent().random},
        timeout=aiohttp.ClientTimeout(total=600),  # 将超时时间设置为600秒
        connector=aiohttp.TCPConnector(limit=50),  # 将并发数量降低
    )


async def _request_data(uid: str):
    async with new_session() as session:
        # 从最新的一页（0）开始爬取数据。
        page_num = 0
        while True:
            url = api_user_album(uid=uid, page_num=page_num)
            async with session.get(url) as response:
                if response.status != 200:
                    # 如果响应为空，则退出循环。
                    # TODO（此处应有处理方法）
                    break
                try:
                    content = await response.read()
                except ClientPayloadError as e:
                    logger.warning(e)
                    continue

            # 返回结果是 json 形式，取出目标数据
            items = json.loads(content)['data']['items']

            # 解析需要的数据（通常一页是 30 个）并返回
            yield filter_dict(items, ITEM_KEYS)
            logger.info(f'finish page {page_num}')

            # 如果当前页图集数量小于 page size，认为到达最后一页，退出循环
            # 一般只有第一次运行才会遇到
            if len(items) < PAGE_SIZE:
                logger.info('page end')
                break
            page_num += 1


async def _save_data(uid: str, conn: Connect):
    last_ctime = conn.select_newest()
    pages_data = _request_data(uid)

    async for tmp in pages_data:
        for data in tmp:
            if data['ctime'] <= last_ctime:
                logger.info('last end')
                return
            conn.insert_item(data)
            # 这里将新添加的数据 url 返回给下载器下载
            for picture in data['pictures']:
                yield picture['img_src']


async def _run(uid: str, save_path: Path, conn: Connect):
    count = 0
    count_saved = 0

    async with new_session() as session:
        async for url in _save_data(uid, conn):
            count += 1

            save_name = save_path / Path(url).name
            if save_name.exists():
                logger.debug(f'exists {save_name}')
                continue

            async with session.get(url) as response:
                if response is None:
                    # 返回 None 应将数据库 valid 设为 0
                    # 但可能链接有效，因其它原因返回 None
                    # TODO How?
                    continue

                try:
                    content = await response.read()
                except ClientPayloadError as e:
                    logger.warning(e)
                    continue

            async with aiofiles.open(save_name, 'wb') as fp:
                await fp.write(content)

            count_saved += 1
            logger.debug(f'saved {count} {save_name}')

    logger.info(f'all done.  {count} update, {count_saved} saved.')


def run(uid: str, save_path: Path | str, database: Path | str):
    if isinstance(save_path, str):
        save_path = Path(save_path)
    if not save_path.exists():
        save_path.mkdir(parents=True)

    conn = Connect(database)
    conn.create_tables()

    logger.info(f'start {uid} at {save_path}')
    asyncio.run(_run(uid, save_path, conn))
