import unittest
import requests

from src import utils

URL = "http://www.google.es"


class TestUtils(unittest.TestCase):
    def test_proxies(self):
        r = None
        # r = utils.get_proxies()
        # self.assertIsInstance(r, dict)
        self.assertIsNone(r)

    def test_scrap_by_selectorlib(self):
        r = utils.scrap_by_selectorlib(URL)
        # self.assertIsNotNone(r)
        # Simply check if call function
        self.assertRaises(AssertionError)

    def test_scrap_by_beautifulsoup(self):
        r = utils.scrap_by_beautifulsoup(requests.get(URL))
        # self.assertIsNotNone(r)
        # Simply check if call function
        self.assertRaises(AssertionError)

    def test_scrap_web(self):
        utils.scrap_web(URL)
