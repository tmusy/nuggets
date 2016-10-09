# -*- coding: utf-8 -*-
"""
    Unit Tests
    ~~~~~~~~~~
    Define TestCase as base class for unit tests.
    Ref: http://packages.python.org/Flask-Testing/
"""
from flask_testing import TestCase as Base

from nuggets import create_app
from nuggets.config import TestConfig
from nuggets.extensions import db
from nuggets.models import Account


class BaseTestCase(Base):
    """Base TestClass for your application."""

    def create_app(self):
        """Create and return a testing flask app."""
        app = create_app(config=TestConfig)

        return app

    def init_data(self):
        self.bank = Account(name=u'Bank',
                            description=u'My Bank')
        db.session.add(self.bank)
        db.session.commit()

    def setUp(self):
        """Reset all tables before testing."""
        db.create_all()
        self.init_data()

    def tearDown(self):
        """Clean db session and drop all tables."""
        db.session.remove()
        db.drop_all()
