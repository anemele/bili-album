""" 存放一些与业务无关的小方法 """
import hashlib

from typing import Union, Optional, List, Dict, Any, Tuple

from .constants import TIME_HASH_METHOD


def hash_str(sth: Union[str, int], encoding: str = 'ascii') -> Optional[str]:
    try:
        bytes_ = bytes(str(sth), encoding=encoding)
    except:
        return
    method = getattr(hashlib, TIME_HASH_METHOD, hashlib.sha1)
    return method(bytes_).hexdigest()


def filter_dict(items: List[Dict[str, Any]], keys: Tuple[str, ...]):
    """输入一个字典列表和一个字符串元组，输出一个迭代器，
    仅保留字典中含关键字的数据。

    例如输入 [ {'a': 1, 'b': 2 ...}, ... ] 和 ('a', 'c', ...) ，
    输出 [ {'a': 1, ...}, ...]

    """
    for item in items:
        yield {key: item[key] for key in keys}
