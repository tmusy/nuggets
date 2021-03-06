# -*- coding: utf-8 -*-

from flask_script import Manager

from statement2db import create_app
from statement2db.extensions import db
from statement2db.models import Account

app = create_app()
manager = Manager(app)


@manager.command
def run():
    """Run in local machine."""

    app.run()


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
