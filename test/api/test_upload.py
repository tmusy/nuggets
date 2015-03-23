from test import BaseTestCase


class TestAccount(BaseTestCase):
    def test_get_existing_account(self):
        res = self.client.get('/v1.0/accounts/1')
        assert res.status_code == 200

    def save_file(self):
        pass

    def test_post_upload(self):
        with open('lib/test.csv', 'rb') as testfile:
            res = self.client.post('/v1.0/import/transactions', data= {'file': testfile})
            assert res.status_code == 200
            self.assertEqual(res.json, "Import successful", res.json)
            res = self.client.post('/v1.0/import/transactions', data= {'file': None})
            assert res.status_code == 400
