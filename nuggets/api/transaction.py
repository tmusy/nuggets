#!flask/bin/python
import dateutil.parser
from flask import request
from flask_restful import fields, Resource, marshal_with, abort, reqparse, url_for
from sqlalchemy import desc

from nuggets.decorators import paginate, marshal
from nuggets.extensions import db
from nuggets.models import Trx, Account
from nuggets.schemas import TrxSchema


transaction_fields = {
    'uri': fields.Url('transaction'),
    'id': fields.Integer,
    'amount': fields.Price(decimals=2),
    'currency': fields.String,
    'saldo': fields.Price(decimals=2),
    'date': fields.DateTime,
    'name': fields.String,
    'description': fields.String
}


class TransactionResource(Resource):
    def __init__(self):
        # reqparse to ensure well-formed arguments passed by the request
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('amount', type=float, location='json')
        self.reqparse.add_argument('currency', type=str, location='json')
        self.reqparse.add_argument('date', type=str, location='json')
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        super(TransactionResource, self).__init__()

    @marshal_with(transaction_fields)
    def get(self, id):
        """
        :param   id
        :return: transaction as JSON: {'id': '', 'amount': 0, 'currency': '', 'date': datetime,
        'name': '', 'description': ''}
                 REST status ok code: 200
        """
        transaction = Trx.query.filter_by(id=int(id)).first()
        if not transaction:
            abort(404, message="Transaction {0} doesn't exist".format(id))
        return transaction

    def delete(self, id):
        """
        :param   id
        :return: ''
                 REST status ok code: 204
        """
        transaction = Trx.query.filter_by(id=int(id)).first()
        if transaction:
            db.session.delete(transaction)
            db.session.commit()
        return '', 204

    @marshal_with(transaction_fields)
    def put(self, id):
        """
        :param   id
                 request: {'id': '', 'amount': 0, 'currency': '', 'name': '', 'description': ''}
        :return: transaction as JSON: {'id': '', 'amount': 0, 'currency': '', 'name': '', 'description': ''}
                 REST status ok code: 201
        """
        transaction = Trx.query.filter_by(id=int(id)).first()
        if not transaction:
            abort(404, message="Transaction doesn't exist")

        args = self.reqparse.parse_args()
        transaction_dict = {}
        for k, v in args.iteritems():
            if v is not None:
                if k == 'date':
                    v = dateutil.parser.parse(v)
                transaction_dict[k] = v
                transaction.__setattr__(k, v)

        db.session.commit()
        return transaction, 201


class TransactionListResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('amount', type=float, required=True, location='json')
        self.reqparse.add_argument('currency', type=str, location='json')
        self.reqparse.add_argument('date', type=str, location='json')
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('debit', type=dict, location='json')

        self.p_reqparse = reqparse.RequestParser()
        self.p_reqparse.add_argument('page', type=str, location='path')

        super(TransactionListResource, self).__init__()

    @marshal(TrxSchema(many=True))
    @paginate('transactions')
    def get(self):
        """
        :param
        :return: transactions as JSON: [{'id': '', 'amount': 0, 'currency': '',
        'date': datetime, 'name': '', 'description': ''},...]
                 REST status code: 200
        """
        return Trx.query.order_by(desc(Trx.id))

    @marshal_with(transaction_fields)
    def post(self):
        """
        :param
        :return: transaction as JSON: {'id': '', 'amount': 0, 'currency': '',
        'date': datetime, 'name': '', 'description': '', }
                 REST status code: 201
        """
        args = self.reqparse.parse_args(req=request)
        transaction_dict = {}
        debit = None
        credit = None
        for k, v in args.iteritems():
            if v:
                transaction_dict[k] = v

        if 'date' in transaction_dict:
            transaction_dict['date'] = dateutil.parser.parse(transaction_dict['date'])
        if 'debit' in transaction_dict:
            debit = transaction_dict.pop('debit')
        if 'credit' in transaction_dict:
            credit = transaction_dict.pop('credit')

        transaction = Trx(**transaction_dict)

        if debit:
            account = Account.query.filter_by(name=debit['name']).first()
            transaction.debit = account
        if credit:
            account = Account.query.filter_by(name=credit['name']).first()
            transaction.credit = account
        db.session.add(transaction)
        db.session.commit()
        return transaction, 201

    def get_url(self):
        return request.url_root[:-1] + url_for('transactions')
