import unittest
from src import models

class TestProduct(unittest.TestCase):
    def setUp(self) -> None:
        self.product = models.Product(product_id="10")

    def test_print_product(self):
        self.assertIn("ID", format(self.product))