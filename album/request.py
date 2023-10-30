from typing import Optional

from requests import Response, Session

from .constants import UA

_session = Session()
_headers = {'user-agent': UA}


def request(url: str) -> Optional[Response]:
    response = _session.get(url, headers=_headers)
    if response.status_code == 200:
        return response
    if response.status_code == 404:
        return
    print(response, '@', url)
