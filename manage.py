# -*- coding: utf-8 -*-

from flask_script import Manager

from nuggets import create_app
from nuggets.extensions import db
from nuggets.models import Account, Trx
from nuggets.services import calculate_all_saldos

app = create_app()
manager = Manager(app)


@manager.command
def run():
    """Run in local machine."""

    app.run()
#    calculate_all_saldos()

    for trx in Trx.query.all():
        suggest = trx.suggest_account()
        if suggest.get('credit'):
            trx.credit = suggest.get('credit')
            trx.credit_id = suggest.get('credit').id
            db.session.commit()
        if suggest.get('debit'):
            trx.debit = suggest.get('debit')
            trx.debit_id = suggest.get('debit').id
            db.session.commit()
        print(trx)
        print(suggest)


@manager.command
def initdb():
    """Init/reset database."""

    db.session.remove()
    db.drop_all(bind=None)
    db.create_all()

    bank = Account(name=u'Bank',
                   description=u'My Bank')
    db.session.add(bank)
    db.session.commit()

    # admin = Admin(
    #         username=u'admin',
    #         email=u'musy@zhaw.ch',
    #         password=u'pw123')
    #
    # db_session.add(admin)
    # db_session.commit()


manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()
