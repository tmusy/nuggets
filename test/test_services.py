from test import BaseTestCase

from nuggets.services import calculate_all_saldos


class TestServices(BaseTestCase):

    def test_calculate_all_saldos(self):
        assert(calculate_all_saldos())
