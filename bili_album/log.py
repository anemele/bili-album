import datetime
import logging
import sys

logger = logging.getLogger(__package__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

now = datetime.datetime.now().strftime("%Y-%m-%d")
fp = f"{__package__} {now}.log"
fh = logging.FileHandler(filename=fp, encoding="utf-8")
fh.setFormatter(formatter)
logger.addHandler(fh)

sh = logging.StreamHandler(stream=sys.stdout)
sh.setFormatter(formatter)
logger.addHandler(sh)
