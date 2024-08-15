"""API 需要三个参数
uid 是用户的 uid
page_num 是相册分页，从 0 开始
page_size 是相册每页图集数目"""

PAGE_SIZE = 30  # 默认设为 30


def api_user_album(uid: str, page_num: int) -> str:
    return (
        'https://api.bilibili.com/x/dynamic/feed/draw/doc_list'
        f'?uid={uid}&page_num={page_num}&page_size={PAGE_SIZE}'
        '&biz=all&jsonp=jsonp'
    )
