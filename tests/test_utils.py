import unittest
from src import utils

URL = "http:/"


class TestUtils(unittest.TestCase):
    def test_proxies(self):
        r = utils.get_proxies()
        self.assertIsInstance(r, dict)

    def test_scrap_by_selectorlib(self):
        r = utils.scrap_by_selectorlib(URL)
        self.assertIsNotNone(r)

    def test_scrap_by_beautifulsoup(self):
        utils.test_scrap_by_beautifulsoup()

    def test_scrap_web(self):
        utils.scrap_web(URL)
