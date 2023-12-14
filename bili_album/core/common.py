import aiohttp
from fake_useragent import FakeUserAgent


def new_session():
    return aiohttp.ClientSession(
        headers={'user-agent': FakeUserAgent().random},
        timeout=aiohttp.ClientTimeout(total=600),  # 将超时时间设置为600秒
        connector=aiohttp.TCPConnector(limit=50),  # 将并发数量降低
    )


LAST_TIME = '.last'
