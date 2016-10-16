from sqlalchemy import create_engine, Column, Integer, String, Float, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine('sqlite:///../web/database.db', echo=True)


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    search = Column(String)
    url = Column(String)
    source = Column(String)
    product = Column(String)
    brand = Column(String)
    currency = Column(String)
    price = Column(Float)


Base.metadata.create_all(engine)
