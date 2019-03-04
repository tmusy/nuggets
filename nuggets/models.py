from collections import Counter
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

    def suggest_account(self):
        res = {'credit': None, 'debit': None}

        if not self.credit_id:
            if self.name in ['BANCOMAT', 'CASH SERVICE AUTOMATENBEZUG', 'MAESTRO-BEZUG CHF', 'Cash Service-Automatenbezug', 'EC/MAESTRO-BEZUG CHF',
                             'Maestro-Bezug CHF', 'Bezug CHF am Geldautomaten', 'Maestro-Bezug']:
                a = Account.query.filter_by(name='Bankomat').first()
                res['credit'] = a
                return res

            if self.description:
                trxs = Trx.query.filter_by(name=self.name, description=self.description).all()
                accounts = [t.credit for t in trxs if t.credit]
                if accounts:
                    counter = Counter(accounts)
                    account, count = counter.most_common(1)[0]
                    res['credit'] = account if count > 2 and account is not self.debit else None

        if not self.debit_id:
            if self.description:
                trxs = Trx.query.filter_by(name=self.name, description=self.description).all()
                accounts = [t.debit for t in trxs if t.debit]
                if accounts:
                    counter = Counter(accounts)
                    account, count = counter.most_common(1)[0]
                    res['debit'] = account if count > 2 and account is not self.credit else None
        return res

    def __repr__(self):
        return '<Transaction {id}: {amount} {currency} - {name}>'\
            .format(id=self.id, amount=self.amount, currency=self.currency, name=self.name)


class Account(db.Model):
    id = Column(db.Integer, primary_key=True)
    nr = Column(db.Integer)
    name = Column(db.Unicode(40))
    description = Column(db.Unicode(1024))
    type = Column(db.Unicode(16))


def find_trx_by_name(name):
    trxs = Trx.query.filter_by(name= name).all()
    return trxs
