from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from statement2db.database import Base


class Transaction(Base):
    __tablename__ = 'trx'
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    currency = Column(String(4))
    date = Column(DateTime)
    name = Column(String(240), unique=True)
    description = Column(String(1024))
    debit = Column(Integer, ForeignKey('account.id'))
    credit = Column(Integer, ForeignKey('account.id'))

    def __init__(self, amount, currency='CHF', date=datetime.utcnow(), name=None, description=None):
        self.amount = amount
        self.currency = currency
        self.date = date
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Transaction: {0} {1}>'.format(self.amount, self.currency)


class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    description = Column(String(1024))
    type = Column(String(16))

    def __init__(self, name, description=None, type=None):
        self.name = name
        self.description = description
        self.type = type
