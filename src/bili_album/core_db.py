import asyncio
from pathlib import Path
from typing import AsyncIterable, Iterable

from .api import PAGE_SIZE, api_user_album
from .common import new_session
from .db import Connect
from .log import logger
from .rest import Item, Rest


async def request_data(uid: str) -> AsyncIterable[Iterable[Item]]:
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
            items = Rest.from_json(content).data.items

            # 解析需要的数据（通常一页是 30 个）并返回
            yield items
            logger.info(f"finish page {page_num}")

            # 如果当前页图集数量小于 page size，认为到达最后一页，退出循环
            # 一般只有第一次运行才会遇到
            if len(items) < PAGE_SIZE:
                logger.info("page end")
                break
            page_num += 1


async def update(uid: str, database: Path):
    conn = Connect(database)

    last_ctime = conn.select_newest()

    count = 0
    flag = False
    async for page in request_data(uid):
        tmp = []
        for item in page:
            if item.ctime <= last_ctime:
                flag = True
                break

            tmp.append(item)
            count += len(item.pictures)

        conn.insert_all(tmp)
        if flag:
            break

    logger.info(f"done. {count} update.")


def run(uid: str, database: Path):
    logger.info(f"updating database...   with uid={uid}, db={database}")

    asyncio.run(update(uid, database))
