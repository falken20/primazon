import unittest

from src import primazon

TEST_PRODUCT = {"product_url": "url", "product_price": 5}


class TestPrimazon(unittest.TestCase):

    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        primazon.app.config["TESTING"] = True
        self.app = primazon.app.test_client()

    def test_home(self) -> None:

        response = self.app.get("/")
        self.assertEqual(200, response.status_code)
        response = self.app.get("/home")
        self.assertEqual(200, response.status_code)
