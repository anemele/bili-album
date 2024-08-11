import logging
import sys

logging.basicConfig(
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    level=logging.INFO,
    stream=sys.stdout,
    datefmt="%Y-%m-%d %H:%M:%S",
)

__all__ = []
