from dataclasses import dataclass
from typing import Sequence

from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass
class Picture:
    img_src: str
    img_width: str
    img_height: str
    img_size: str


@dataclass
class Item(DataClassORJSONMixin):
    ctime: int
    description: str
    pictures: Sequence[Picture]


@dataclass
class Data:
    items: Sequence[Item]


@dataclass
class Rest(DataClassORJSONMixin):
    code: int
    message: str
    data: Data


def parse_response(resp: bytes) -> Rest:
    return Rest.from_json(resp)


def dump_item(item: Item) -> str:
    return item.to_json()


def load_item(json_str: str) -> Item:
    return Item.from_json(json_str)
