import aiohttp
from fake_useragent import FakeUserAgent
from requests import Session

_FakeUA = FakeUserAgent()


def new_session_a():
    return aiohttp.ClientSession(
        headers={"user-agent": _FakeUA.random},
        timeout=aiohttp.ClientTimeout(total=600),  # 将超时时间设置为600秒
        connector=aiohttp.TCPConnector(limit=50),  # 将并发数量降低
    )


def new_session():
    sess = Session()
    sess.headers.update({"User-Agent": _FakeUA.random})
    return sess
