"""下载数据，更新数据库，并下载最新的图片，保存到指定位置。"""

import argparse
from pathlib import Path

from .core import run
from .log import logger
from .parser import parse

parser = argparse.ArgumentParser(prog=__package__, description=__doc__)
parser.add_argument('config', type=Path, help='TOML config file path')

args = parser.parse_args()

args_config: Path = args.config

if not args_config.is_file():
    logger.error(f'not a file: {args_config}')
    exit(1)

try:
    for uid, save_path, db in parse(args_config):
        run(uid, save_path, db)
except (KeyError, AssertionError) as e:
    logger.error(e)
