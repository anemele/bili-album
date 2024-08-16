from dataclasses import dataclass

from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass
class Picture:
    img_src: str
    img_width: str
    img_height: str
    img_size: str


@dataclass
class Item:
    ctime: int
    description: str
    pictures: list[Picture]


@dataclass
class Data:
    items: list[Item]


@dataclass
class REST(DataClassORJSONMixin):
    code: int
    message: str
    data: Data
