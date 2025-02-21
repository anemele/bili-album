import json
from dataclasses import asdict, dataclass

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
class Rest(DataClassORJSONMixin):
    code: int
    message: str
    data: Data


def parse_response(resp: bytes) -> Rest:
    return Rest.from_json(resp)


def dump_item(item: Item) -> str:
    return json.dumps(asdict(item), ensure_ascii=False)
