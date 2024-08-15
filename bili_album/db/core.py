from itertools import chain
from pathlib import Path
from typing import Iterable

from sqlalchemy import and_, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from ..core.core_db import Item
from .model import Base, Info, Picture
from .utils import md5_str


class Connect:
    def __init__(self, path: Path | str, **kw):
        self._engine = create_engine(f'sqlite:///{path}')
        if kw.get('IS_TEST') == True:
            Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)

        self._session = scoped_session(sessionmaker(self._engine))

    def disconnect(self):
        self._session.remove()
        self._engine.dispose()

    @staticmethod
    def wrap_data(data: Item) -> tuple[Info, Picture]:
        pid = md5_str(data.ctime)
        p = data.pictures[0]
        return (
            Info(ctime=data.ctime, desc=data.description, pid=pid),
            Picture(
                pid=pid,
                src=p.img_src,
                width=p.img_width,
                height=p.img_height,
                size=p.img_size,
                # the valid is of `img_src`, default True, update to False if it is invalid.
                valid=True,
            ),
        )

    def insert(self, data: Item):
        self._session.add_all((self.wrap_data(data)))
        self._session.commit()

    def insert_all(self, data: Iterable[Item]):
        self._session.add_all(chain.from_iterable(map(self.wrap_data, data)))
        self._session.commit()

    def select_newest(self):
        ctime = self._session.query(Info.ctime).order_by(Info.ctime.desc()).first()
        if ctime is not None:
            ctime = ctime[0]
        if ctime is None:
            return 0
        return ctime

    def select_desc_src(self):
        return (
            self._session.query(Info.desc, Picture.src)
            .filter(Picture.valid)
            .join(Info, Info.pid == Picture.pid)
            .all()
        )

    def select_newer_than(self, ctime: int):
        query = (
            self._session.query(Picture.src)
            .select_from(Picture)
            .filter(and_(Picture.pid == Info.pid, Info.ctime > ctime))
            .all()
        )
        return (x[0] for x in query)
