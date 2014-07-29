#!flask/bin/python
import datetime
from flask import Flask, request
from flask_restful import Api, fields, Resource, marshal_with, abort, reqparse

from statement2db.database import db_session
from statement2db.model import Transaction


app = Flask(__name__)
api = Api(app)


transaction_fields = {
    #'uri': fields.Url('transaction'),
    'id': fields.Integer,
    'amount': fields.Integer,
    'currency': fields.String,
    'date': fields.DateTime,
    'name': fields.String,
    'description': fields.String
}


class TransactionResource(Resource):
    def __init__(self):
        # reqparse to ensure well-formed arguments passed by the request
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('amount', type=int, default=None, location='json')
        self.reqparse.add_argument('currency', type=str, default=None, location='json')
        self.reqparse.add_argument('date', type=datetime, default=datetime.datetime.utcnow(), location='json')
        self.reqparse.add_argument('name', type=str, default=None, location='json')
        self.reqparse.add_argument('description', type=str, default=None, location='json')
        super(TransactionResource, self).__init__()

    @marshal_with(transaction_fields)
    def get(self, id):
        """
        :param   id
        :return: transaction_dict: {'id': str, 'amount': int, 'currency': str, 'date': datetime,
        'name': str, 'description': str}
                 REST status ok code: 200
        """
        transaction = db_session.query(Transaction).filter_by(id=int(id)).first()
        if not transaction:
            abort(404, message="Transaction {0} doesn't exist".format(id))
        return transaction

    def delete(self, id):
        """
        :param   id
        :return: ''
                 REST status ok code: 204
        """
        transaction = db_session.query(Transaction).filter_by(id=int(id)).first()
        if transaction:
            db_session.delete(transaction)
            db_session.commit()
        return '', 204

    @marshal_with(transaction_fields)
    def put(self, id):
        """
        :param   id
                 request: {'id': '', 'amount': 0, 'currency': '', 'name': '', 'description': ''}
        :return: transaction_dict: {'id': '', 'amount': 0, 'currency': '', 'name': '', 'description': ''}
                 REST status ok code: 201
        """
        transaction = db_session.query(Transaction).filter_by(id=int(id)).first()
        if not transaction:
            abort(404, message="Transaction doesn't exist")

        args = self.reqparse.parse_args()
        transaction_dict = {}
        for k, v in args.iteritems():
            if v is not None:
                transaction_dict[k] = v
                transaction.__setattr__(k, v)

        db_session.commit()
        return transaction_dict, 201


class TransactionListResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('amount', type=int, required=True,
            help = 'No amount provided', location='json')
        self.reqparse.add_argument('currency', type=str, default="CHF", location='json')
        self.reqparse.add_argument('date', type=datetime, default=datetime.datetime.utcnow(), location='json')
        self.reqparse.add_argument('name', type=str, default='', location='json')
        self.reqparse.add_argument('description', type=str, default="", location='json')
        super(TransactionListResource, self).__init__()

    @marshal_with(transaction_fields)
    def get(self):
        """
        :param
        :return: transaction_list: [{'id': str, 'amount': int, 'currency': str, 'date': datetime,
        'name': str, 'description': str},...]
                 REST status code: 200
        """
        transactions = db_session.query(Transaction).all()
        if not transactions:
            abort(404, message="No Transactions available")
        return transactions, 200

    @marshal_with(transaction_fields)
    def post(self):
        """
        :param
        :return: transaction_list: [{'id': '', 'date': datetime, 'description': '', 'amount': float, 'currency': ''},...]
                 REST status code: 201
        """
        args = self.reqparse.parse_args(req=request)
        transaction_dict = {}
        for k, v in args.iteritems():
            if v is not None:
                transaction_dict[k] = v
        transaction = Transaction(**transaction_dict)
        db_session.add(transaction)
        db_session.commit()
        return transaction_dict, 201


api.add_resource(TransactionListResource, '/v1.0/transactions', endpoint='transactions')
api.add_resource(TransactionResource, '/v1.0/transactions/<string:id>', endpoint='transaction')


if __name__ == '__main__':
    app.run(debug=True)
