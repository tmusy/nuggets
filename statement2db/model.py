from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from statement2db.database import Base


class Transaction(Base):
    __tablename__ = 'trx'
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    currency = Column(String(4))
    date = Column(DateTime)
    name = Column(String(240), unique=True)
    description = Column(String(1024))

    def __init__(self, amount, currency='CHF', date=datetime.utcnow(), name=None, description=None):
        self.amount = amount
        self.currency = currency
        self.date = date
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Transaction: {0} {1}>'.format(self.amount, self.currency)
