import datetime
import logging
import sys

now = datetime.datetime.now().strftime('%Y-%m-%d %H%M%S')

logging.basicConfig(
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
    # stream=sys.stdout,
    filename=f'{__package__} {now}.log',
    encoding='utf-8',
)

__all__ = []
