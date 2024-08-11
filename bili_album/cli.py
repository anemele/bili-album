import logging
from pathlib import Path

import click

from .core import update_database, update_image
from .parser import parse

logger = logging.getLogger(__package__)


class OrderedGroup(click.Group):
    def list_commands(self, _):
        return self.commands.keys()


@click.group(cls=OrderedGroup)
def cli():
    """下载/更新哔哩哔哩用户相册（space.bilibli.com/{uid}）数据库、图片。"""


@cli.command()
@click.argument('config', type=Path)
def up_db(config: Path):
    """下载/更新数据库"""
    logger.debug(f'{config=}')
    if not config.is_file():
        logger.error(f'not a file: {config}')
        return

    try:
        for up in parse(config).up:
            if up.ignore:
                continue
            update_database(up.uid, up.root)
    except (KeyError, AssertionError) as e:
        logger.error(e)


@cli.command()
@click.argument('config', type=Path)
def up_img(config: Path):
    """下载/更新图片"""
    logger.debug(f'{config=}')
    if not config.is_file():
        logger.error(f'not a file: {config}')
        return

    try:
        for up in parse(config).up:
            if up.ignore:
                continue
            update_image(up.root)
    except (KeyError, AssertionError) as e:
        logger.error(e)
