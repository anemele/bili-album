import argparse
import os.path

import tomli

from .album import Download


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config')

    args = parser.parse_args()

    def parse_toml(toml_file):
        with open(toml_file, 'rb') as fp:
            config = tomli.load(fp)
        uid = config.get('uid')
        root = config.get('root')
        name = config.get('name')
        db = f'db_{name}.db'

        return (uid, os.path.join(root, name), os.path.join(root, db))

    if os.path.isfile(args.config):
        args = parse_toml(args.config)
        assert all(args)
        Download(*args).run()


if __name__ == '__main__':
    main()
