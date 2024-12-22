import os

from bili_album.db import Connect
from bili_album.rest import Item, Picture


def new_data(ctime, description, img_src, img_width, img_height, img_size):
    return Item(
        ctime=ctime,
        description=description,
        pictures=[
            Picture(
                img_src=img_src,
                img_width=img_width,
                img_height=img_height,
                img_size=img_size,
            )
        ],
    )


def test_connect():
    path = "local.db"
    conn = Connect(path, IS_TEST=True)
    try:
        conn.insert(new_data(123456, "haha", "https://1", 1980, 1080, 1024))
        conn.insert_all(
            [
                new_data(123, "haihai", "https://2", 1980, 1080, 1024),
                new_data(456, "heihei", "ftps", 512, 512, 8192),
            ]
        )
        assert conn.select_newest() == 123456
        assert conn.select_desc_src() == [
            ("haha", "https://1"),
            ("haihai", "https://2"),
            ("heihei", "ftps"),
        ]
    finally:
        conn.disconnect()
        os.remove(path)
