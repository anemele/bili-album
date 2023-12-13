import json
from itertools import chain
from pathlib import Path

from .constants import ITEM_KEYS, PAGE_SIZE, api_user_album
from .db import Connect
from .log import logger
from .request import get
from .utils import filter_dict


def _request_data(uid: str):
    # 从最新的一页（0）开始爬取数据。
    page_num = 0
    while True:
        url = api_user_album(uid=uid, page_num=page_num)
        response = get(url)
        if response is None:
            # 如果响应为空，则退出循环。
            # TODO（此处应有处理方法）
            break
        # 返回结果是 json 形式
        json_ = json.loads(response.content)
        # 取出目标数据
        items = json_['data']['items']
        # 解析需要的数据（通常一页是 30 个）并返回
        yield filter_dict(items, ITEM_KEYS)
        logger.info(f'finish page {page_num}')

        # 如果当前页图集数量小于 page size，认为到达最后一页，退出循环
        # 一般只有第一次运行才会遇到
        if len(items) < PAGE_SIZE:
            logger.info('page end')
            break
        page_num += 1


def _save_data(uid: str, conn: Connect):
    last_ctime = conn.select_newest()
    pages_data = chain.from_iterable(_request_data(uid))
    for data in pages_data:
        if data['ctime'] <= last_ctime:
            logger.info('last end')
            break
        conn.insert_item(data)
        # 这里将新添加的数据 url 返回给下载器下载
        for picture in data['pictures']:
            yield picture['img_src']


def _run(uid: str, save_path: Path, conn: Connect):
    count = 0
    count_saved = 0
    for url in _save_data(uid, conn):
        count += 1
        save_name = save_path / Path(url).name
        if save_name.exists():
            logger.debug(f'exists {save_name}')
            continue

        response = get(url)
        if response is None:
            # 返回 None 应将数据库 valid 设为 0
            # 但可能链接有效，因其它原因返回 None
            # TODO How?
            continue

        save_name.write_bytes(response.content)
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
    _run(uid, save_path, conn)
