#!flask/bin/python
import datetime
from flask import Flask, request
#from flask.ext.restful import Resource, Api, fields, marshal_with, abort
from flask_restful import Api, fields, Resource, marshal_with, abort, reqparse


app = Flask(__name__)
api = Api(app)

transactions = [
    {
        'id': 1,
        'date': datetime.datetime.utcnow(),
        'amount': 10.50,
        'currency': 'CHF',
        'description': u'Coop Oerlikon'
    },
    {
        'id': 2,
        'date': datetime.datetime.utcnow(),
        'amount': 150.00,
        'currency': 'CHF',
        'description': u'Migros Wint'
    }
]

resource_fields = {
    'id': fields.Integer,
    'description': fields.String,
    'date': fields.DateTime,
    'amount': fields.Float,
    'currency': fields.String
}


class TransactionResource(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        transaction = filter(lambda t: t['id'] == int(id), transactions)
        if len(transaction) == 0:
            abort(404, message="Transaction doesn't exist".format(id))
        return transaction[0]


class TransactionListResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('amount', type=float, required=True,
            help = 'No amount provided', location='json')
        self.reqparse.add_argument('currency', type=str, default="CHF", location='json')
        self.reqparse.add_argument('date', type=datetime, default=datetime.datetime.utcnow(), location='json')
        self.reqparse.add_argument('description', type=str, default="", location='json')
        super(TransactionListResource, self).__init__()

    @marshal_with(resource_fields)
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
