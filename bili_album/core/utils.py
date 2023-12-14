""" 存放一些与业务无关的小方法 """

from typing import Any, Iterable


def filter_dict(items: list[dict[str, Any]], keys: tuple[str, ...]):
    """输入一个字典列表和一个字符串元组，输出一个迭代器，
    仅保留字典中含关键字的数据。

    例如输入 [ {'a': 1, 'b': 2 ...}, ... ] 和 ('a', 'c', ...) ，
    输出 [ {'a': 1, ...}, ...]

    """
    for item in items:
        yield {key: item[key] for key in keys}


# v3.12+ builtin:itertools
def batched(it: Iterable, n: int):
    tmp = []
    count = 0
    for i in it:
        tmp.append(i)
        count += 1
        if count == n:
            yield tuple(tmp)
            tmp.clear()
            count = 0
    if len(tmp) > 0:
        yield tuple(tmp)
