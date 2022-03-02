from sqlalchemy import Column, ForeignKey, Integer, String, Table, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

user_jd = Table(
    'user_jd',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.user_id')),
    Column('jd_id', Integer, ForeignKey('jd.jd_id')),
    Column('watch_price', Numeric),
    Column('is_done', Integer, default=0)
)

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    wecom_id = Column(String)
    jd = relationship('JdItem', secondary=user_jd, back_populates='user')

class JdItem(Base):
    __tablename__ = 'jd'
    jd_id = Column(Integer, primary_key=True)
    item_name = Column(String)
    user = relationship('User', secondary=user_jd, back_populates='jd')
