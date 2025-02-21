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
    parser.add_argument(
        "--get-img",
        action="store_true",
        help="download images if not exist",
    )

    args = parser.parse_args()

    config_path: Path = args.config
    get_img: bool = args.get_img

    try:
        config = parse_config(config_path)
        update_image(config, get_img)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
