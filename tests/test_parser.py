from pathlib import Path

from bili_album.parser import Config, Up, parse_config


def test_parse_config():
    sample = """
root = 'root'
[[up]]
name = 'abc'
uid = '123'
[[up]]
name = '你-好'
uid = '456'
[[up]]
name = 'test-ignore'
uid = '123'
"""
    expected = Config(
        root=Path("root"),
        up=[
            Up(name="abc", uid="123"),
            Up(name="你-好", uid="456"),
            Up(name="test-ignore", uid="123"),
        ],
    )
    result = parse_config(sample)
    assert result == expected

    sample = ""
    expected = Config(root=Path.cwd(), up=[])
    result = parse_config(sample)
    assert result == expected
