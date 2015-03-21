from test import BaseTestCase

from statement2db.lib.parser import parse_csv, extract_transactions


class TestParser(BaseTestCase):
    def test_parse(self):
        result = parse_csv('lib/test.csv')
        print(result)
        assert(len(result) == 5)

        # client = self._get_test_client()
        # headers = {'Authorization': 'Basic ' + base64.b64encode('t1' + ':' + 'p1')}
        # response = client.get('/pass', headers=headers)
        # assert response.status_code == 200, response.status

    def test_extract_transactions(self):
        result = extract_transactions('lib/test.csv')
        assert (len(result) == 4)
