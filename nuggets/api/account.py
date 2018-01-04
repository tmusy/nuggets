#!flask/bin/python
from flask import request, url_for
from flask_restful import fields, Resource, marshal_with, abort, reqparse
from sqlalchemy import desc

from nuggets.models import Account, Trx
from nuggets.extensions import db
from nuggets.schemas import AccountSchema, TrxSchema
from nuggets.decorators import paginate, marshal


account_fields = {
    'uri': fields.Url('account'),
    'nr': fields.Integer,
    'name': fields.String,
    'type': fields.String,
    'description': fields.String
}


class AccountResource(Resource):
    def __init__(self):
        # reqparse to ensure well-formed arguments passed by the request
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('type', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        super(AccountResource, self).__init__()

    @marshal_with(account_fields)
    def get(self, id):
        """
        :param   id
        :return: account as JSON: {'id': str, 'name': str, 'description': str}
                 REST status ok code: 200
        """
        account = Account.query.filter_by(id=int(id)).first()
        if not account:
            abort(404, message="Account {0} doesn't exist".format(id))
        return account

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

    @marshal_with(account_fields)
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

        args = self.reqparse.parse_args()
        account_dict = {}
        for k, v in args.iteritems():
            if v is not None:
                account_dict[k] = v
                account.__setattr__(k, v)

        db.session.commit()
        return account, 201


class AccountListResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('nr', type=str, required=True, location='json')
        self.reqparse.add_argument('name', type=str, required=True, location='json')
        self.reqparse.add_argument('type', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        super(AccountListResource, self).__init__()

    @marshal(AccountSchema(many=True))
    @paginate('accounts')
    def get(self):
        """
        :param
        :return: accounts as JSON: [{'id': '', 'name': '', 'description': ''},...]
                 REST status code: 200
        """
        return Account.query

    @marshal_with(account_fields)
    def post(self):
        """
        :param
        :return: account as JSON: {'id': '', 'name': '', 'description': ''}
                 REST status code: 201
        """
        args = self.reqparse.parse_args(req=request)
        account_dict = {}
        for k, v in args.iteritems():
            if v is not None:
                account_dict[k] = v
        account = Account(**account_dict)
        db.session.add(account)
        db.session.commit()
        return account, 201

    def get_url(self):
        return request.url_root[:-1] + url_for('accounts')


class AccountTransactionListResource(Resource):

    @marshal(TrxSchema(many=True))
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
