import hashlib


def md5_str(sth: str | int) -> str:
    data = str(sth).encode()

    return hashlib.md5(data).hexdigest()
