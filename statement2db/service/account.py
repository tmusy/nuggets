#!flask/bin/python
from flask import request
from flask_restful import fields, Resource, marshal_with, abort, reqparse

from statement2db.app import app, api
from statement2db.database import db_session
from statement2db.model import Account


account_fields = {
    'uri': fields.Url('account'),
    'id': fields.Integer,
    'name': fields.String,
    'type': fields.String,
    'description': fields.String
}


class AccountResource(Resource):
    def __init__(self):
        # reqparse to ensure well-formed arguments passed by the request
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=unicode, location='json')
        self.reqparse.add_argument('type', type=unicode, location='json')
        self.reqparse.add_argument('description', type=unicode, location='json')
        super(AccountResource, self).__init__()

    @marshal_with(account_fields)
    def get(self, id):
        """
        :param   id
        :return: account as JSON: {'id': str, 'name': str, 'description': str}
                 REST status ok code: 200
        """
        account = db_session.query(Account).filter_by(id=int(id)).first()
        if not account:
            abort(404, message="Account {0} doesn't exist".format(id))
        return account

    def delete(self, id):
        """
        :param   id
        :return: ''
                 REST status ok code: 204
        """
        account = db_session.query(Account).filter_by(id=int(id)).first()
        if account:
            db_session.delete(account)
            db_session.commit()
        return '', 204

    @marshal_with(account_fields)
    def put(self, id):
        """
        :param   id
                 request: {'id': '', 'name': '', 'description': ''}
        :return: account as JSON: {'id': '', 'name': '', 'description': ''}
                 REST status ok code: 201
        """
        account = db_session.query(Account).filter_by(id=int(id)).first()
        if not account:
            abort(404, message="Account doesn't exist")

        args = self.reqparse.parse_args()
        account_dict = {}
        for k, v in args.iteritems():
            if v is not None:
                account_dict[k] = v
                account.__setattr__(k, v)

        db_session.commit()
        return account, 201


class AccountListResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=unicode, required=True, location='json')
        self.reqparse.add_argument('type', type=unicode, location='json')
        self.reqparse.add_argument('description', type=unicode, location='json')
        super(AccountListResource, self).__init__()

    @marshal_with(account_fields)
    def get(self):
        """
        :param
        :return: accounts as JSON: [{'id': '', 'name': '', 'description': ''},...]
                 REST status code: 200
        """
        index = request.args.get('index', 0)
        count = request.args.get('count', 5)
        order_by = request.args.get('order', 'name')
        accounts = db_session.query(Account).order_by(order_by).offset(index).limit(count).all()
        #accounts = db_session.query(Account).all()
        if not accounts:
            abort(404, message="No Accounts available")
        return accounts, 200

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
        db_session.add(account)
        db_session.commit()
        return account, 201


api.add_resource(AccountListResource, '/v1.0/accounts', endpoint='accounts')
api.add_resource(AccountResource, '/v1.0/accounts/<string:id>', endpoint='account')


if __name__ == '__main__':
    app.run(debug=True)
