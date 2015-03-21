import os

import flask
from flask_restful import fields, Resource, marshal_with, abort, reqparse
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from statement2db.app import app, api
from statement2db.lib.parser import extract_transactions
from statement2db.service.account import account_fields

UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

transaction_fields = {
    'uri': fields.Url('transaction'),
    'id': fields.Integer,
    'amount': fields.Float,
    'currency': fields.String,
    'date': fields.DateTime,
    'name': fields.String,
    'description': fields.String,
    'credit': fields.List(fields.Nested(account_fields)),
    'debit': fields.List(fields.Nested(account_fields))
}


class ImportTransactionsResource(Resource):

    #tr@marshal_with(transaction_fields)
    def post(self):
        """
        :return: list of transaction as JSON: [{'id': '', 'name': '', 'description': ''}, ...]
                 REST status ok code: 201
        """
        f = flask.request.files['file']
        filename = do_the_upload(f)
        if filename:
            transactions = extract_transactions(filename)
            return "Import successful"
        else:
            abort(400, message="Import was not successful")


def do_the_upload(upload_file):
    if upload_file and allowed_file(upload_file.filename):
        filename = secure_filename(upload_file.filename)
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        upload_file.save(full_filename)
    return full_filename


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


api.add_resource(ImportTransactionsResource, '/v1.0/import/transactions', endpoint='import')


if __name__ == '__main__':
    app.run()
