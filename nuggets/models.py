from sqlalchemy import Column, Integer, Unicode, DateTime, ForeignKey, Float

from nuggets.extensions import db


class Transaction(db.Model):
    id = Column(db.Integer, primary_key=True)
    amount = Column(db.Float)
    currency = Column(db.Unicode(4))
    date = Column(db.DateTime)
    name = Column(db.Unicode(240))
    description = Column(db.Unicode(1024))
    debit_id = Column(db.Integer, db.ForeignKey('account.id'))
    credit_id = Column(db.Integer, db.ForeignKey('account.id'))
    debit = db.relationship('Account', primaryjoin='Transaction.debit_id == Account.id')
    credit = db.relationship('Account', primaryjoin='Transaction.credit_id == Account.id')
    valuta_date = Column(db.DateTime)
    category = Column(db.Unicode(64))

    # just to safe from imported data
    reported_saldo = Column(db.Float)

    def __repr__(self):
        return '<Transaction: {0} {1}>'.format(self.amount, self.currency)


class Account(db.Model):
    id = Column(db.Integer, primary_key=True)
    name = Column(db.Unicode(40))
    description = Column(db.Unicode(1024))
    type = Column(db.Unicode(16))
