import json
from nose import with_setup
from statement2db.database import init_db, clear_db, db_session
from statement2db.models import Transaction
from statement2db.service.transaction import app


test_app = app.test_client()


def setup():
    init_db()


def teardown():
    #clear_db()
    pass


@with_setup(setup, teardown)
def test_get_existing_exercise():
    t = _create_test_transaction(1)

    res = test_app.get('/v1.0/transactions/' + str(t.id))
    assert res.status_code == 200

    response_data = json.loads(res.data)
    assert response_data['amount'] == 10
    assert response_data['name'] == 'test_transaction_1'

@with_setup(setup, teardown)
def test_get_not_existing_exercise():
    res = test_app.get('/v1.0/transactions/5847')
    assert res.status_code == 404

@with_setup(setup, teardown)
def test_delete_existing_exercise():
    t = _create_test_transaction(1)

    res = test_app.delete('/v1.0/transactions/' + str(t.id))
    assert res.status_code == 204

@with_setup(setup, teardown)
def test_delete_not_existing_exercise():
    res = test_app.delete('/v1.0/transactions/5847')
    assert res.status_code == 204

@with_setup(setup, teardown)
def test_create_exercise():
    new_transaction = {'amount': 22, 'name': 'test_transaction_1', 'description': 'test description'}
    res = test_app.post('/v1.0/transactions', data=json.dumps(new_transaction), content_type='application/json')
    assert res.status_code == 201

    our_transaction = db_session.query(Transaction).filter_by(name='test_transaction_1',
                                                           description='test description').first()
    assert our_transaction


@with_setup(setup, teardown)
def test_edit_exercise():
    t = _create_test_transaction(1)

    edited_transaction = {'name': 'test_transaction_2', 'description': 'desc'}

    res = test_app.put('/v1.0/transactions/' + str(t.id),
                       data=json.dumps(edited_transaction),
                       content_type='application/json')
    assert res.status_code == 201
    our_transaction = db_session.query(Transaction).filter_by(amount=10, name='test_transaction_2',
                                                              description='desc').first()
    assert our_transaction

    edited_transaction = {'amount': 33, 'name': 'test_transaction_1', 'description': ''}
    res = test_app.put('/v1.0/transactions/' + str(t.id),
                       data=json.dumps(edited_transaction),
                       content_type='application/json')
    assert res.status_code == 201
    our_transaction = db_session.query(Transaction).filter_by(amount=33, name='test_transaction_1',
                                                              description='').first()
    assert our_transaction

@with_setup(setup, teardown)
def test_get_exercise_list():
    t1 = _create_test_transaction(1)
    t2 = _create_test_transaction(2)

    res = test_app.get('/v1.0/transactions')
    assert res.status_code == 200

    response_data = json.loads(res.data)
    assert len(response_data) == 2
    assert 'test_transaction_2' in [data['name'] for data in response_data]


def _create_test_transaction(id):
    t = Transaction(10, name='test_transaction_'+str(id))
    db_session.add(t)
    db_session.commit()
    return t
