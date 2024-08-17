import datetime
import logging

now = datetime.datetime.now().strftime('%Y-%m-%d %H%M%S')

logging.basicConfig(
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
    encoding='utf-8',
)
logger = logging.getLogger(__package__)
logger.addHandler(logging.StreamHandler())
logger.addHandler(logging.FileHandler(f'{__package__} {now}.log'))
