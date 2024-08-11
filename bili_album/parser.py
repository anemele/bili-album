from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from dataclass_binder import Binder


@dataclass
class Up:
    name: str
    uid: str
    root: Path
    ignore: Optional[bool] = False

    def __post_init__(self):
        self.root = self.root.joinpath(f'{self.name}.db')


@dataclass
class Config:
    up: list[Up]


def parse(config_file: Path) -> Config:
    return Binder(Config).parse_toml(config_file)


def parse_config(s: dict[str, Any]) -> Config:
    return Binder(Config).bind(s)
