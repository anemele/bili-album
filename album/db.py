""" SQLite 数据库相关操作 """
import sqlite3
from pathlib import Path
from typing import Union

from .utils import hash_str

sql_create_items = """CREATE TABLE IF NOT EXISTS "items" (
"ctime"	INTEGER NOT NULL,
"desc"	TEXT,
"pid"	TEXT NOT NULL
);"""
sql_create_pics = """CREATE TABLE IF NOT EXISTS "pics" (
"pid"	TEXT NOT NULL,
"src"	TEXT NOT NULL,
"width"	INTEGER NOT NULL,
"height"	INTEGER NOT NULL,
"size"	NUMERIC NOT NULL,
"valid"	INTEGER NOT NULL
);"""


class Connect:
    def __init__(self, database: Union[Path, str]):
        self.database = database
        self.connect = sqlite3.connect(database)
        self.cursor = self.connect.cursor()

    def create_tables(self):
        self.cursor.execute(sql_create_items)
        self.cursor.execute(sql_create_pics)

    def insert_item(self, data: dict):
        pid = hash_str(data["ctime"])
        self.cursor.execute(
            "insert into items values(?,?,?)", (data["ctime"], data["description"], pid)
        )
        p = data["pictures"][0]
        self.cursor.execute(
            "insert into pics values(?,?,?,?,?,?)",
            # the valid is of `img_src`, default by 1, update to 0 if it is invalid.
            (pid, p["img_src"], p["img_width"], p["img_height"], p["img_size"], 1),
        )
        self.connect.commit()

    def insert_items(self, data: list):
        for d in data:
            self.insert_item(d)

    def _select_and_fetch_one(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def select_newest(self):
        sql = "select max(ctime) from items"
        res = self._select_and_fetch_one(sql)
        if res is None:
            return 0
        return res[0] or 0

    def select_desc_src(self):
        # 添加有效性过滤器
        self.cursor.execute(
            "select items.desc, pics.src from items "
            "inner join pics "
            "on items.pid=pics.pid and pics.valid=1"
        )
        return self.cursor.fetchall()

    def update_valid(self, pid, valid=0):
        self.cursor.execute("update pics set valid=? where pid=?", (valid, pid))
        self.connect.commit()

    def disconnect(self):
        self.cursor.close()
        self.connect.close()

    def __repr__(self) -> str:
        return f"<{__class__.__name__} {self.database}>"
