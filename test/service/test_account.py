import json
from nose import with_setup
from statement2db.database import init_db, clear_db, db_session
from statement2db.models import Account
from statement2db.service.account import app


test_app = app.test_client()


def setup():
    init_db()


def teardown():
    #clear_db()
    pass


@with_setup(setup, teardown)
def test_get_existing_account():
    a = _create_test_account(1)

    res = test_app.get('/v1.0/accounts/' + str(a.id))
    assert res.status_code == 200

    response_data = json.loads(res.data)
    assert response_data['name'] == 'test_account_1'

@with_setup(setup, teardown)
def test_get_not_existing_account():
    res = test_app.get('/v1.0/accounts/5847')
    assert res.status_code == 404

@with_setup(setup, teardown)
def test_delete_existing_account():
    a = _create_test_account(1)

    res = test_app.delete('/v1.0/accounts/' + str(a.id))
    assert res.status_code == 204

@with_setup(setup, teardown)
def test_delete_not_existing_account():
    res = test_app.delete('/v1.0/accounts/5847')
    assert res.status_code == 204

@with_setup(setup, teardown)
def test_create_account():
    new_account = {'name': 'test_account_1', 'description': 'test description'}
    res = test_app.post('/v1.0/accounts', data=json.dumps(new_account), content_type='application/json')
    assert res.status_code == 201

    our_account = db_session.query(Account).filter_by(name='test_account_1',
                                                      description='test description').first()
    assert our_account


@with_setup(setup, teardown)
def test_edit_account():
    a = _create_test_account(1)

    edited_account = {'name': 'test_account_2', 'description': 'desc'}

    res = test_app.put('/v1.0/accounts/' + str(a.id),
                       data=json.dumps(edited_account),
                       content_type='application/json')
    assert res.status_code == 201
    our_account = db_session.query(Account).filter_by(name='test_account_2',
                                                      description='desc').first()
    assert our_account

    edited_account = {'name': 'test_account_1', 'description': ''}
    res = test_app.put('/v1.0/accounts/' + str(a.id),
                       data=json.dumps(edited_account),
                       content_type='application/json')
    assert res.status_code == 201
    our_account = db_session.query(Account).filter_by(name='test_account_1',
                                                      description='').first()
    assert our_account

@with_setup(setup, teardown)
def test_get_account_list():
    a1 = _create_test_account(1)
    a2 = _create_test_account(2)

    res = test_app.get('/v1.0/accounts')
    assert res.status_code == 200

    response_data = json.loads(res.data)
    assert len(response_data) == 2
    assert 'test_account_2' in [data['name'] for data in response_data]


def _create_test_account(id):
    a = Account('test_account_'+str(id))
    db_session.add(a)
    db_session.commit()
    return a
