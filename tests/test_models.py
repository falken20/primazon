import unittest
from src import models


class TestProduct(unittest.TestCase):
    def setUp(self) -> None:
        self.product = models.Product()

    def test_print_product(self):
        self.assertIn("ID", print(self.product))
