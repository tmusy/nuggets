from .models import Trx
from nuggets.extensions import db


def calculate_all_saldos(account_id=1):
    transactions = Trx.query.order_by(Trx.id).all()

    previous_saldo = 0.0
    for trx in transactions:
        if trx.credit_id == account_id:
            previous_saldo += trx.amount
        elif trx.debit_id == account_id:
            previous_saldo -= trx.amount
        trx.saldo = previous_saldo

        db.session.commit()
