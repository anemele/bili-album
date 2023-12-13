import tomllib
from pathlib import Path

from .parser import parse_config


def test_parse_config():
    sample = '''\
[abc]
uid = 123
root = '/path/to'
['你-好']
uid = 456
root = '/目录'
[test-ignore]
ignore = 1
'''
    sth = tomllib.loads(sample)
    config = list(parse_config(sth))

    assert len(config) == 2
    assert config[0][0] == '123'
    assert config[0][1] == Path('/path/to/abc')
    assert config[0][2] == Path('/path/to/db_abc.db')
    assert config[1][0] == '456'
    assert config[1][1] == Path('/目录/你-好')
    assert config[1][2] == Path('/目录/db_你-好.db')
