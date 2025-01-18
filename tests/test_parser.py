from pathlib import Path

import tomllib

from bili_album.parser import parse_config


def test_parse_config():
    sample = """\
[[up]]
name = 'abc'
uid = '123'
root = '/path/to'
[[up]]
name = '你-好'
uid = '456'
root = '/目录'
[[up]]
name = 'test-ignore'
uid = '123'
root = 'root'
"""
    sth = tomllib.loads(sample)
    up = parse_config(sth).up

    assert len(up) == 3

    assert up[0].name == "abc"
    assert up[0].uid == "123"
    assert up[0].root == Path("/path/to/abc.db")

    assert up[1].name == "你-好"
    assert up[1].uid == "456"
    assert up[1].root == Path("/目录/你-好.db")

    assert up[2].name == "test-ignore"
    assert up[2].uid == "123"
    assert up[2].root == Path("root/test-ignore.db")
