import asyncio
import json
from pathlib import Path

import aiohttp
from fake_useragent import FakeUserAgent

from .api import PAGE_SIZE, api_user_album
from .db import Connect
from .log import logger
from .utils import filter_dict

# 过滤数据所需的 key
ITEM_KEYS = ('ctime', 'description', 'pictures')


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

                content = await response.read()

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


async def _update(uid: str, conn: Connect):
    last_ctime = conn.select_newest()
    count = 0
    flag = False
    async for page in _request_data(uid):
        tmp = []
        for item in page:
            if item['ctime'] <= last_ctime:
                flag = True
                break

            tmp.append(item)
            count += 1
        conn.insert_all(tmp)
        if flag:
            return count


async def _run(uid: str, conn: Connect):
    count = await _update(uid, conn)

    logger.info(f'done. {count} update.')


def run(uid: str, database: Path | str):
    conn = Connect(database)

    logger.info(f'start. uid={uid}, db={database}')
    asyncio.run(_run(uid, conn))
