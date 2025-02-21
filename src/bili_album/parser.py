from dataclasses import dataclass
from pathlib import Path

from mashumaro.mixins.toml import DataClassTOMLMixin


@dataclass
class Up:
    name: str
    uid: str


@dataclass
class Config(DataClassTOMLMixin):
    root: Path
    up: list[Up]


def parse_config(config_toml: Path | str) -> Config:
    if isinstance(config_toml, str):
        return Config.from_toml(config_toml)
    return Config.from_toml(config_toml.read_text())
