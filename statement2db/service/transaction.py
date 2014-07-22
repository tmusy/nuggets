#!flask/bin/python
import datetime
from flask import Flask, jsonify
from werkzeug.exceptions import abort

app = Flask(__name__)

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

@app.route('/v1.0/transactions', methods=['GET'])
def get_tasks():
    return jsonify({'transactions': transactions})


@app.route('/v1.0/transactions/<int:transaction_id>', methods = ['GET'])
def get_task(transaction_id):
    transaction = filter(lambda t: t['id'] == transaction_id, transactions)
    if len(transaction) == 0:
        abort(404)
    return jsonify({'transaction': transaction[0]})


if __name__ == '__main__':
    app.run(debug=True)
