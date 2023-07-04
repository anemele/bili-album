from pathlib import Path
from typing import Tuple

import tomli


def parse_toml(toml_file: Path) -> Tuple[str, Path, Path]:
    config = tomli.load(toml_file.open('rb'))
    uid = config.get('uid')
    assert isinstance(uid, int) or isinstance(uid, str) and uid.isdigit()
    root = config.get('root')
    assert isinstance(root, str)
    root = Path(root)
    name = config.get('name')
    assert isinstance(name, str)
    db = f'db_{name}.db'

    return (str(uid), root / name, root / db)
