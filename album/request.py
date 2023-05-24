import random

from faker import Faker
from requests import Session

__all__ = ['request']
session = Session()
faker = Faker()
user_agent_list = [faker.user_agent() for _ in range(10)]


def request(url):
    headers = {'user-agent': random.choice(user_agent_list)}
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        return response
    if response.status_code == 404:
        return
    print(response, '@', url)
