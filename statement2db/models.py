from datetime import datetime

from sqlalchemy import Column, Integer, Unicode, DateTime, ForeignKey, Float

from statement2db.extensions import db


class Transaction(db.Model):
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    currency = Column(Unicode(4))
    date = Column(DateTime)
    name = Column(Unicode(240), unique=True)
    description = Column(Unicode(1024))
    debit_id = Column(Integer, ForeignKey('account.id'))
    credit_id = Column(Integer, ForeignKey('account.id'))
    debit = db.relationship('Account', primaryjoin='Transaction.debit_id == Account.id')
    credit = db.relationship('Account', primaryjoin='Transaction.credit_id == Account.id')
    valuta_date = Column(DateTime)

    # just to safe from imported data
    reported_saldo = Column(Float)

    def __repr__(self):
        return '<Transaction: {0} {1}>'.format(self.amount, self.currency)


class Account(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(40))
    description = Column(Unicode(1024))
    type = Column(Unicode(16))
