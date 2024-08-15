from sqlalchemy import Boolean, Column, Integer, Numeric, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Info(Base):
    __tablename__ = 'info'
    cid = Column('cid', String, nullable=False, primary_key=True)
    ctime = Column('ctime', Integer, nullable=False)
    desc = Column('desc', String)


class Picture(Base):
    __tablename__ = 'pics'
    cid = Column('cid', String, nullable=False)
    pid = Column('pid', String, nullable=False, primary_key=True)
    src = Column('src', String, nullable=False)
    width = Column('width', Integer, nullable=False)
    height = Column('height', Integer, nullable=False)
    size = Column('size', Numeric, nullable=False)
    valid = Column('valid', Boolean, nullable=False)
