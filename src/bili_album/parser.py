from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

from mashumaro.mixins.toml import DataClassTOMLMixin


@dataclass
class Up:
    name: str
    uid: str


@dataclass
class Config(DataClassTOMLMixin):
    root: Path = field(default_factory=Path.cwd)
    up: Sequence[Up] = field(default_factory=list)


def parse_config(config_toml: Path | str) -> Config:
    if isinstance(config_toml, str):
        return Config.from_toml(config_toml)

    return Config.from_toml(config_toml.read_text(encoding="utf-8"))
