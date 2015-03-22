import os

from flask import request, current_app
from flask_restful import fields, Resource, marshal_with, abort, reqparse
from werkzeug.utils import secure_filename

from statement2db.lib.parser import extract_transactions
from statement2db.api.account import account_fields
from statement2db.utils import allowed_file


transaction_fields = {
    'uri': fields.Url('transaction'),
    'id': fields.Integer,
    'amount': fields.Price(decimals=2),
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
        f = request.files['file']
        filename = self._save_file(f)
        if filename:
            transactions = extract_transactions(filename)
            return "Import successful"
        else:
            abort(400, message="Import was not successful")

    def _save_file(self, upload_file):
        if upload_file and allowed_file(upload_file.filename):
            filename = secure_filename(upload_file.filename)
            # if not os.path.exists(UPLOAD_FOLDER):
            #     os.makedirs(UPLOAD_FOLDER)
            full_filename = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            upload_file.save(full_filename)
        return full_filename
