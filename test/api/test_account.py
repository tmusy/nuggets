import json

from test import BaseTestCase

from nuggets.models import Account
from nuggets.extensions import db


class TestAccount(BaseTestCase):
    def test_get_existing_account(self):
        res = self.client.get('/v1.0/accounts/1')
        assert res.status_code == 200

        response_data = json.loads(res.data)
        assert response_data['name'] == 'Bank'

    def test_get_not_existing_account(self):
        res = self.client.get('/v1.0/accounts/5847')
        assert res.status_code == 404

    def test_delete_existing_account(self):
        res = self.client.delete('/v1.0/accounts/1')
        assert res.status_code == 204

    def test_delete_not_existing_account(self):
        res = self.client.delete('/v1.0/accounts/5847')
        assert res.status_code == 204

    def test_create_account(self):
        new_account = {'name': 'test_account_1', 'description': 'test description'}
        res = self.client.post('/v1.0/accounts', data=json.dumps(new_account), content_type='application/json')
        assert res.status_code == 201

        our_account = Account.query.filter_by(name='test_account_1',
                                                          description='test description').first()
        assert our_account

    def test_edit_account(self):
        edited_account = {'name': 'test_account_2', 'description': 'desc'}
        res = self.client.put('/v1.0/accounts/1',
                           data=json.dumps(edited_account),
                           content_type='application/json')
        assert res.status_code == 201
        our_account = Account.query.filter_by(name='test_account_2',
                                                          description='desc').first()
        assert our_account

        edited_account = {'name': 'test_account_1', 'description': ''}
        res = self.client.put('/v1.0/accounts/1',
                           data=json.dumps(edited_account),
                           content_type='application/json')
        assert res.status_code == 201
        our_account = Account.query.filter_by(name='test_account_1',
                                                          description='').first()
        assert our_account

    def test_get_account_list(self):
        a = Account(name='a')
        b = Account(name='b')
        db.session.add(a)
        db.session.add(b)
        db.session.commit()

        res = self.client.get('/v1.0/accounts')
        assert res.status_code == 200

        response_data = json.loads(res.data)
        assert len(response_data) == 3
        assert 'b' in [data['name'] for data in response_data]


# def _create_test_account(id):
#     a = Account('test_account_'+str(id))
#     db_session.add(a)
#     db_session.commit()
#     return a
