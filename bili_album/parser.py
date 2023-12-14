import tomllib
from pathlib import Path
from typing import Any, Iterable

T_CONFIG = tuple[str, Path]


def parse(config_file: Path) -> Iterable[T_CONFIG]:
    sth = tomllib.load(config_file.open('rb'))
    return parse_config(sth)


def parse_config(sth: dict[str, dict[str, Any]]) -> Iterable[T_CONFIG]:
    for name in sth:
        it = sth[name]
        # 设置一个过滤器
        if it.get('ignore'):
            continue

        uid = it['uid']
        assert isinstance(uid, int) or isinstance(uid, str) and uid.isdigit()

        root = Path(it['root'])
        db = f'{name}.db'

        yield (str(uid), root / db)
