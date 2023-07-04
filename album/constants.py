""" 存放 API 、默认设置等常量 """

from faker import Faker

""" API 需要三个参数
uid 是用户的 uid
page_num 是相册分页，从 0 开始
page_size 是相册每页图集数目 """
PAGE_SIZE = 30  # 默认设为 30
USER_ALBUM_API = (
    'https://api.bilibili.com/x/dynamic/feed/draw/doc_list'
    f'?uid={{uid}}&page_num={{page_num}}&page_size={PAGE_SIZE}'
    '&biz=all&jsonp=jsonp'
)

TIME_HASH_METHOD = 'sha1'

_faker = Faker()
UA_LIST = [_faker.user_agent() for _ in range(10)]
REQ_BOUND = 10  # 请求 10 次更换 UA

# 过滤数据所需的 key
ITEM_KEYS = ('ctime', 'description', 'pictures')
