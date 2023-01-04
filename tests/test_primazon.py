import unittest
import json

from src import primazon

TEST_PRODUCT = {"product_url": "url", "product_price": 5}


class TestPrimazon(unittest.TestCase):

    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        primazon.app.config["TESTING"] = True
        self.app = primazon.app.test_client()
        self.info = {"product_url": "an_url",
                     "product_desc": "value2",
                     "product_url_photo": "value2",
                     "product_rating": "value2",
                     "product_reviews": "value2",
                     "product_price": 10
                     }

    def test_home(self) -> None:
        response = self.app.get("/")
        self.assertEqual(200, response.status_code)
        response = self.app.get("/home")
        self.assertEqual(200, response.status_code)

    def test_about(self):
        response = self.app.get("/about/")
        self.assertEqual(200, response.status_code)

    def test_add_product(self):
        response = self.app.get("/products/add/")
        self.assertEqual(200, response.status_code)

        response = self.app.post("/products/add/",
                                 data=json.dumps(dict(self.info)),
                                 content_type='application/json')
        self.assertEqual(200, response.status_code)
