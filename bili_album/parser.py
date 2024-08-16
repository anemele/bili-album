import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from mashumaro.mixins.toml import DataClassTOMLMixin


@dataclass
class Up:
    name: str
    uid: str
    root: Path
    ignore: Optional[bool] = False

    def __post_init__(self):
        self.root = self.root.joinpath(f'{self.name}.db')


@dataclass
class Config(DataClassTOMLMixin):
    up: list[Up]


def parse(config_file: Path) -> Config:
    with open(config_file, 'rb') as fp:
        content = tomllib.load(fp)
    return parse_config(content)


def parse_config(s: dict[str, Any]) -> Config:
    return Config.from_dict(s)
