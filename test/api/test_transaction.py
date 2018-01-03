import json

from test import BaseTestCase

from nuggets.models import Trx
from nuggets.extensions import db


class TestAccount(BaseTestCase):
    def test_get_existing_exercise(self):
        t = _create_test_transaction(1)
    
        res = self.client.get('/v1.0/transactions/' + str(t.id))
        assert res.status_code == 200
    
        response_data = json.loads(res.data)
        assert response_data['amount'] == '10.00', response_data
        assert response_data['name'] == 'test_transaction_1'

    def test_get_not_existing_exercise(self):
        res = self.client.get('/v1.0/transactions/5847')
        assert res.status_code == 404

    def test_delete_existing_exercise(self):
        t = _create_test_transaction(1)
    
        res = self.client.delete('/v1.0/transactions/' + str(t.id))
        assert res.status_code == 204

    def test_delete_not_existing_exercise(self):
        res = self.client.delete('/v1.0/transactions/5847')
        assert res.status_code == 204

    def test_create_exercise(self):
        new_transaction = {'amount': 22, 'name': 'test_transaction_1', 'description': 'test description'}
        res = self.client.post('/v1.0/transactions', data=json.dumps(new_transaction), content_type='application/json')
        assert res.status_code == 201
    
        our_transaction = Trx.query.filter_by(name='test_transaction_1',
                                              description='test description').first()
        assert our_transaction

    def test_edit_exercise(self):
        t = _create_test_transaction(1)
    
        edited_transaction = {'name': 'test_transaction_2', 'description': 'desc'}
    
        res = self.client.put('/v1.0/transactions/' + str(t.id),
                              data=json.dumps(edited_transaction),
                              content_type='application/json')
        assert res.status_code == 201
        our_transaction = Trx.query.filter_by(amount=10,
                                              name='test_transaction_2',
                                              description='desc').first()
        assert our_transaction
    
        edited_transaction = {'amount': 33, 'name': 'test_transaction_1', 'description': ''}
        res = self.client.put('/v1.0/transactions/' + str(t.id),
                              data=json.dumps(edited_transaction),
                              content_type='application/json')
        assert res.status_code == 201
        our_transaction = Trx.query.filter_by(amount=33,
                                              name='test_transaction_1',
                                              description='').first()
        assert our_transaction

    def test_get_exercise_list(self):
        t1 = _create_test_transaction(1)
        t2 = _create_test_transaction(2)
    
        res = self.client.get('/v1.0/transactions')
        assert res.status_code == 200
    
        response_data = json.loads(res.data)
        assert len(response_data) == 2
        assert 'test_transaction_2' in [data['name'] for data in response_data]


def _create_test_transaction(id):
    t = Trx(amount=10, name='test_transaction_' + str(id))
    db.session.add(t)
    db.session.commit()
    return t
