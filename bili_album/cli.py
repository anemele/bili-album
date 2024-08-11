import logging
from pathlib import Path

import click

from .core import update_database, update_image
from .parser import parse

logger = logging.getLogger(__package__)


@click.command
@click.argument('config', type=Path)
@click.option(
    '--only-db',
    is_flag=True,
    default=False,
    help='Download both database and pictures by default. '
    'Set this flag to disable picture download.',
)
def cli(config: Path, only_db: bool):
    """下载/更新哔哩哔哩用户相册（space.bilibli.com/{uid}）数据库、图片。"""
    logger.debug(f'{config=}')
    if not config.is_file():
        logger.error(f'not a file: {config}')
        return

    for up in parse(config).up:
        if up.ignore:
            continue
        if not up.root.parent.exists():
            up.root.parent.mkdir(exist_ok=True)
        update_database(up.uid, up.root)
        if only_db:
            continue
        update_image(up.root)
