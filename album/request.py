import random
from typing import Optional

from requests import Session, Response

from .constants import UA_LIST, REQ_BOUND

_session = Session()
_request_counter = 0
_headers = {'user-agent': random.choice(UA_LIST)}


def request(url: str) -> Optional[Response]:
    global _request_counter
    response = _session.get(url, headers=_headers)
    _request_counter += 1
    if _request_counter == REQ_BOUND:
        _request_counter = 0
        _headers['user-agent'] = random.choice(UA_LIST)
    if response.status_code == 200:
        return response
    if response.status_code == 404:
        return
    print(response, '@', url)
