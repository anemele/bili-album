import json
import random
import time
from itertools import chain
from pathlib import Path
from typing import Union

from .constants import USER_ALBUM_API as API, PAGE_SIZE, ITEM_KEYS
from .db import Connect
from .request import request
from .utils import filter_dict


class Download:
    """下载数据，更新数据库，并下载最新的图片，保存到指定位置。"""

    def __init__(
        self,
        uid: str,
        save_path: Union[Path, str],
        database: Union[Path, str],
    ):
        self._uid = uid

        assert isinstance(save_path, (Path, str))
        if isinstance(save_path, str):
            save_path = Path(save_path)
        if not save_path.exists():
            save_path.mkdir()
        self._save_path = save_path

        assert isinstance(database, (Path, str))
        self._conn = Connect(database)
        self._conn.create_tables()

    def _request_data(self):
        # 从最新的一页（0）开始爬取数据。
        page_num = 0
        while True:
            url = API.format(uid=self._uid, page_num=page_num)
            response = request(url)
            if response is None:
                # 如果响应为空，则退出循环。（此处应有处理方法）
                break
            # 返回结果是 json 形式
            json_ = json.loads(response.content)
            # 取出目标数据
            items = json_['data']['items']
            # 解析需要的数据（通常一页是 30 个）并返回
            yield filter_dict(items, ITEM_KEYS)

            # 如果当前页图集数量小于 page size，认为到达最后一页，退出循环
            # 一般只有第一次运行才会遇到
            if len(items) < PAGE_SIZE:
                print('[INFO] Page end')
                break
            page_num += 1
            print(f'[INFO] get page {page_num}')

    def save_data(self):
        last_ctime = self._conn.select_newest()
        pages_data = chain.from_iterable(self._request_data())
        for data in pages_data:
            if data['ctime'] <= last_ctime:
                print('[INFO] Last end')
                break
            self._conn.insert_item(data)
            # 这里将新添加的数据 url 返回给下载器下载
            yield data['pictures'][0]['img_src']

    def run(self):
        count = 0
        count_saved = 0
        for count, url in enumerate(self.save_data()):
            save_name = self._save_path / Path(url).name
            if save_name.exists():
                print(f'[WARNING] Exists  {save_name}')
                continue
            response = request(url)
            if response is None:
                # 返回 None 应将数据库 valid 设为 0
                # 但可能链接有效，因其它原因返回 None
                # How to do
                continue

            save_name.write_bytes(response.content)
            print(f'[INFO] Saved  {count:4d}  {save_name}')

            time.sleep(random.random())
        print(f'[INFO] Done. {count} update, {count_saved} saved.')
