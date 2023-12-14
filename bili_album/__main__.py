"""下载数据，更新数据库，并下载最新的图片，保存到指定位置。"""
from .cli import cli

cli(prog_name=__package__)
