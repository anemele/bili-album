import hashlib
from itertools import chain
from pathlib import Path
from typing import Iterable

from sqlalchemy import Boolean, Column, Integer, Numeric, String, and_, create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from .rest import Item

Base = declarative_base()


class Info(Base):
    __tablename__ = "info"
    cid = Column("cid", String, nullable=False, primary_key=True)
    ctime = Column("ctime", Integer, nullable=False)
    desc = Column("desc", String)


class Picture(Base):
    __tablename__ = "pics"
    cid = Column("cid", String, nullable=False)
    pid = Column("pid", String, nullable=False, primary_key=True)
    src = Column("src", String, nullable=False)
    width = Column("width", Integer, nullable=False)
    height = Column("height", Integer, nullable=False)
    size = Column("size", Numeric, nullable=False)
    valid = Column("valid", Boolean, nullable=False)


class Connect:
    def __init__(self, path: Path | str, **kw):
        self._engine = create_engine(f"sqlite:///{path}")
        if kw.get("IS_TEST") is not None:
            Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)

        self._session = scoped_session(sessionmaker(self._engine))

    def disconnect(self):
        self._session.remove()
        self._engine.dispose()

    @staticmethod
    def _wrap_data(data: Item) -> Iterable:
        cid = hashlib.md5(str(data.ctime).encode()).hexdigest()
        yield Info(ctime=data.ctime, desc=data.description, cid=cid)
        for pic in data.pictures:
            yield Picture(
                cid=cid,
                pid=hashlib.sha1(pic.img_src.encode()).hexdigest(),
                src=pic.img_src,
                width=pic.img_width,
                height=pic.img_height,
                size=pic.img_size,
                # the valid is of `img_src`, default True, update to False if it is invalid.
                valid=True,
            )

    def insert(self, data: Item):
        self._session.add_all((self._wrap_data(data)))
        self._session.commit()

    def insert_all(self, data: Iterable[Item]):
        self._session.add_all(chain.from_iterable(map(self._wrap_data, data)))
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
            .join(Info, Info.cid == Picture.cid)
            .all()
        )

    def select_newer_than(self, ctime: int):
        query = (
            self._session.query(Picture.src)
            .select_from(Picture)
            .filter(and_(Picture.cid == Info.cid, Info.ctime > ctime))
            .all()
        )
        return (x[0] for x in query)
