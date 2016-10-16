# -*- coding: utf-8 -*-
from . import engine
from sqlalchemy.orm import sessionmaker
from . import Item

Session = sessionmaker(bind=engine)


class InsertDatabasePipeline(object):
    session = Session()

    def process_item(self, item, spider):
        print(item)
        item = Item(search=item['search'], url=item['url'], source=item['source'],
                    product=item['product'], brand=item['brand'],
                    currency=item['currency'], price=item['price'])

        self.session.add(item)
        self.session.commit()
        return item
