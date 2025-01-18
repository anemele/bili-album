import argparse
from pathlib import Path

from .core_db import run as update_database
from .core_img import run as update_image
from .log import logger
from .parser import parse


def main():
    parser = argparse.ArgumentParser(
        prog=__package__,
        description="""下载/更新哔哩哔哩用户相册（space.bilibli.com/{uid}）数据库、图片。""",
    )
    parser.add_argument("config", type=Path, help="config file path")

    parser.add_argument("--only-db", action="store_true", help="only update database")

    args = parser.parse_args()

    config: Path = args.config
    only_db: bool = args.only_db

    if not config.is_file():
        logger.error(f"not a file: {config}")
        return

    for up in parse(config).up:
        if not up.root.parent.exists():
            up.root.parent.mkdir(exist_ok=True)
        update_database(up.uid, up.root)
        if only_db:
            continue
        update_image(up.root)
