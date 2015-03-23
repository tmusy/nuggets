from test import BaseTestCase

from statement2db.lib.parser import parse_csv, extract_transactions, extract_transactions_cs


class TestParser(BaseTestCase):
    def test_parse(self):
        result = parse_csv('lib/test.csv')
        print(result)
        assert len(result) == 5, len(result)

    def test_extract_transactions(self):
        result = extract_transactions('lib/test.csv')
        assert len(result) == 4, len(result)

    def test_extract_transactions_cs(self):
        result = extract_transactions_cs('lib/test2.csv')
        assert len(result) == 6, len(result)
        assert result[0].amount == 100, result[0]
