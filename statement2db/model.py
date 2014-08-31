from datetime import datetime
from sqlalchemy import Column, Integer, Unicode, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from statement2db.database import Base


class Transaction(Base):
    __tablename__ = 'trx'
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    currency = Column(Unicode(4))
    date = Column(DateTime)
    name = Column(Unicode(240), unique=True)
    description = Column(Unicode(1024))
    debit_id = Column(Integer, ForeignKey('account.id'))
    credit_id = Column(Integer, ForeignKey('account.id'))
    debit = relationship("Account", primaryjoin = "Transaction.debit_id == Account.id")
    credit = relationship("Account", primaryjoin = "Transaction.credit_id == Account.id")

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
    name = Column(Unicode(40))
    description = Column(Unicode(1024))
    type = Column(Unicode(16))

    def __init__(self, name, description=None, type=None):
        self.name = name
        self.description = description
        self.type = type
