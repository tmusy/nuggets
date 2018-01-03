from sqlalchemy import Column, Integer, Unicode, DateTime, ForeignKey, Float

from nuggets.extensions import db


class Trx(db.Model):
    id = Column(db.Integer, primary_key=True)
    amount = Column(db.FLOAT)
    currency = Column(db.Unicode(4))
    date = Column(db.DateTime)
    name = Column(db.Unicode(240))
    description = Column(db.Unicode(1024))
    debit_id = Column(db.Integer, db.ForeignKey('account.id'))
    credit_id = Column(db.Integer, db.ForeignKey('account.id'))
    debit = db.relationship('Account', primaryjoin='Trx.debit_id == Account.id')
    credit = db.relationship('Account', primaryjoin='Trx.credit_id == Account.id')
    valuta_date = Column(db.DateTime)
    category = Column(db.Unicode(64))

    saldo = Column(db.Float)
    # just to safe from imported data
    reported_saldo = Column(db.Float)

    def __repr__(self):
        return '<Transaction: {0} {1}>'.format(self.amount, self.currency)


class Account(db.Model):
    id = Column(db.Integer, primary_key=True)
    nr = Column(db.Integer)
    name = Column(db.Unicode(40))
    description = Column(db.Unicode(1024))
    type = Column(db.Unicode(16))
