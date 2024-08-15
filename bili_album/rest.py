from dataclasses import dataclass

from dataclasses_json import dataclass_json


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


@dataclass_json
@dataclass
class REST:
    code: int
    message: str
    data: Data
