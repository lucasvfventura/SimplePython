from .. import db
from sqlalchemy import Column, Integer, String, Float, Sequence


class Item(db.Model):
    __tablename__ = 'items'

    id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    search = Column(String)
    url = Column(String)
    source = Column(String)
    product = Column(String)
    brand = Column(String)
    currency = Column(String)
    price = Column(Float)

    def __init__(self, search, url, source, product, brand, currency, price):
        self.search = search
        self.url = url
        self.source = source
        self.product = product
        self.brand = brand
        self.currency = currency
        self.price = price
