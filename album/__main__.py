import argparse
from pathlib import Path

from .album import Download
from .parser import parse_config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=Path, help='TOML config file path')

    args = parser.parse_args()

    args_config: Path = args.config

    if args_config.is_file():
        try:
            config = parse_config(args_config)
            Download(*config).run()
        except AssertionError as e:
            print(e)
    else:
        raise FileNotFoundError(args_config)


if __name__ == '__main__':
    main()
