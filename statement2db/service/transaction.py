#!flask/bin/python
import datetime
from flask import Flask, request
from flask_restful import Api, fields, Resource, marshal_with, abort, reqparse

from statement2db.database import db_session
from statement2db.model import Transaction


app = Flask(__name__)
api = Api(app)


transaction_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'date': fields.DateTime,
    'amount': fields.Float,
    'currency': fields.String
}


class TransactionResource(Resource):
    def __init__(self):
        # reqparse to ensure well-formed arguments passed by the request
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('amount', type=int, default=0, location='json')
        self.reqparse.add_argument('currency', type=str, default="CHF", location='json')
        self.reqparse.add_argument('date', type=datetime, default=datetime.datetime.utcnow(), location='json')
        self.reqparse.add_argument('name', type=str, default='', location='json')
        self.reqparse.add_argument('description', type=str, default='', location='json')
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


class TransactionListResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('amount', type=float, required=True,
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
        :return: transaction_list: [{'id': '', 'date': datetime, 'description': '', 'amount': float, 'currency': ''},...]
                 REST status code: 200
        """
        if len(transactions) == 0:
            abort(404, message="No Transactions available")
        return transactions, 200

    @marshal_with(resource_fields)
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
        return transaction_dict, 201


api.add_resource(TransactionListResource, '/v1.0/transactions', endpoint='transactions')
api.add_resource(TransactionResource, '/v1.0/transactions/<string:id>', endpoint='transaction')


if __name__ == '__main__':
    app.run(debug=True)
