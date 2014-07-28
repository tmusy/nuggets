import json
from statement2db.database import init_db, clear_db, db_session
from statement2db.model import Transaction
from statement2db.service.transaction import app


test_app = app.test_client()


def setup():
    init_db()


def teardown():
    clear_db()


def test_get_existing_transaction():
    t = Transaction(10,name='test_transaction_1')
    db_session.add(t)
    db_session.commit()
    our_transaction = db_session.query(Transaction).filter_by(name='test_transaction_1').first()

    res = test_app.get('/v1.0/transactions/' + str(1))
    data = json.loads(res.data)
    assert res.status_code == 200 and data['id'] == 1


def test_get_transactions():
    t = Transaction(10,name='test_transaction_1')
    db_session.add(t)
    db_session.commit()
    our_transaction = db_session.query(Transaction).filter_by(name='test_transaction_1').first()

    res = test_app.get('/v1.0/transactions')
    data = json.loads(res.data)
    assert res.status_code == 200 and len(data) == 2


def test_post_transaction():
    # t = Transaction('test_transaction_1')
    # db_session.add(t)
    # db_session.commit()
    # our_transaction = db_session.query(Transaction).filter_by(name='test_transaction_1').first()
    test_transaction = {'amount': 55.60}
    res = test_app.post('/v1.0/transactions', data=json.dumps(test_transaction), content_type='application/json')
    data = json.loads(res.data)
    assert res.status_code == 201 and len(data) == 5
