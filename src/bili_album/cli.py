"""下载/更新哔哩哔哩用户相册（space.bilibli.com/{uid}）数据库、图片。"""

import argparse
from pathlib import Path

from .core import run as update_image
from .parser import parse_config


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("config", type=Path, help="config file path")
    args = parser.parse_args()

    try:
        config = parse_config(args.config)
        update_image(config)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
