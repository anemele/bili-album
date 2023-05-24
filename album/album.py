"""下载B站用户的相册，并建立本地数据库，方便相册更新后继续下载。

API（来自浏览器调试）:
https://api.bilibili.com/x/dynamic/feed/draw/doc_list
?uid={uid}&page_num={page_num}&page_size=30&biz=all&jsonp=jsonp"""
import json
import os
import os.path
import random
import time
from itertools import chain

from .db import Connect
from .request import request


""" API 需要三个参数
uid 是用户的 uid
page_num 是相册分页
page_size 是相册每页图集数目 """
api = (
    'https://api.bilibili.com/x/dynamic/feed/draw/doc_list'
    '?uid={uid}&page_num={page_num}&page_size={page_size}'
    '&biz=all&jsonp=jsonp'
)
page_size = 30  # 默认设为 30


class Download:
    """下载数据，更新数据库，并下载最新的图片，保存到指定位置。"""

    def __init__(self, uid: int, save_path: str, database: str):
        self._uid = uid
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        self._save_path = save_path

        assert isinstance(database, str), f'str expected, got {type(database)}'
        self._conn = Connect(database)
        self._conn.create_tables()

    @staticmethod
    def _parse_items(items):
        """
        筛选需要的数据 property
        :param items: list
        :return:
        """
        # 需要的属性
        prop = ('ctime', 'description', 'pictures')
        # 此处过滤器不是必要的，当前需求多于 1 的图集一般都是广告，滤除
        # items = filter(lambda x: x.get('count', 0) == 1, items)
        return (dict((key, item[key]) for key in prop) for item in items)

    def _request_data(self):
        # 从最新的一页（0）开始爬取数据。
        page_num = 0
        while True:
            url = api.format(uid=self._uid, page_num=page_num, page_size=page_size)
            response = request(url)
            if response is None:
                # 如果响应为空，则退出循环。（此处应有处理方法）
                break
            #     返回结果是 json 形式
            json_ = json.loads(response.content)
            # 取出目标数据
            items = json_['data']['items']
            # 解析需要的数据
            data = self._parse_items(items)
            yield data
            # 如果当前页图集数量小于 page size，认为到达最后一页，退出循环
            # 一般只有第一次运行才会遇到
            if len(items) < page_size:
                print('[INFO] Page end')
                break
            page_num += 1
            print(f'[INFO] request page {page_num}')

    def save_data(self):
        last_ctime = self._conn.select_newest()
        for data in chain.from_iterable(self._request_data()):
            if data['ctime'] <= last_ctime:
                print('[INFO] Last end')
                return
            self._conn.insert_item(data)

    def download(self):
        count_all = 0
        count_exist = 0
        count_fail = 0
        for _, url in self._conn.select_desc_src():
            count_all += 1
            save_name = os.path.join(self._save_path, os.path.basename(url))
            if os.path.exists(save_name):
                count_exist += 1
                continue
            response = request(url)
            if response is None:
                # 返回 None 应将数据库 valid 设为 0
                # 但可能链接有效，因其它原因返回 None
                # How to do
                count_fail += 1
                continue
            with open(save_name, 'wb') as fp:
                fp.write(response.content)
            print(f'[INFO] Save  {count_all:4d}  {save_name}')

            time.sleep(random.random())
        print(
            f'[INFO] Done. {count_all} items, {count_exist} exists, {count_fail} failed.'
        )

    def run(self):
        self.save_data()
        self.download()
