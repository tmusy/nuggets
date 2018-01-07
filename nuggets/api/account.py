#!flask/bin/python
from flask import request, url_for
from flask_restful import Resource, abort
from sqlalchemy import desc

from nuggets.models import Account, Trx
from nuggets.extensions import db
from nuggets.schemas import AccountSchema, TrxByAccountSchema
from nuggets.decorators import paginate, marshal


class AccountResource(Resource):
    def __init__(self):
        self.schema = AccountSchema()

    def get(self, id):
        """
        :param   id
        :return: account as JSON: {'id': str, 'name': str, 'description': str}
                 REST status ok code: 200
        """
        account = Account.query.filter_by(id=int(id)).first()
        if not account:
            abort(404, message="Account {0} doesn't exist".format(id))
        return self.schema.dump(account)

    def delete(self, id):
        """
        :param   id
        :return: ''
                 REST status ok code: 204
        """
        account = Account.query.filter_by(id=int(id)).first()
        if account:
            db.session.delete(account)
            db.session.commit()
        return '', 204

    def put(self, id):
        """
        :param   id
                 request: {'id': '', 'name': '', 'description': ''}
        :return: account as JSON: {'id': '', 'name': '', 'description': ''}
                 REST status ok code: 201
        """
        account = Account.query.filter_by(id=int(id)).first()
        if not account:
            abort(404, message="Account doesn't exist")

        data = request.json
        updated_account = self.schema.load(data, instance=account)

        db.session.commit()
        return self.schema.dump(account), 201


class AccountListResource(Resource):

    @marshal(AccountSchema(many=True))
    @paginate('accounts')
    def get(self):
        """
        :param
        :return: accounts as JSON: [{'id': '', 'name': '', 'description': ''},...]
                 REST status code: 200
        """
        return Account.query

    def post(self):
        """
        :param
        :return: account as JSON: {'id': '', 'name': '', 'description': ''}
                 REST status code: 201
        """
        data = request.json

        schema = AccountSchema()
        result = schema.load(data)
        account = result.data

        db.session.add(account)
        db.session.commit()
        return schema.dump(account), 201

    def get_url(self):
        return request.url_root[:-1] + url_for('accounts')


class AccountTransactionListResource(Resource):

    @marshal(TrxByAccountSchema(many=True))
    @paginate('transactions')
    def get(self, id):
        """
        :param
        :return: transactions as JSON: [{'id': '', 'amount': 0, 'currency': '',
        'date': datetime, 'name': '', 'description': ''},...]
                 REST status code: 200
        """
        res = Trx.query.filter((Trx.credit_id == id) | (Trx.debit_id == id)).order_by(desc(Trx.id))
        return res
