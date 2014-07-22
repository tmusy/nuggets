#!flask/bin/python
import datetime
from flask import Flask
from flask.ext.restful import Resource, Api, fields, marshal_with, abort


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


api.add_resource(TransactionListResource, '/v1.0/transactions', endpoint='transactions')
api.add_resource(TransactionResource, '/v1.0/transactions/<string:id>', endpoint='transaction')


if __name__ == '__main__':
    app.run(debug=True)
