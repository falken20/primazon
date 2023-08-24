import unittest
from unittest.mock import patch
from io import StringIO
from flask import Flask

from src.models import Price, Product, db, init_db

TEST_PRODUCT = {"product_url": "url", "product_price": 5}
TEST_PRODUCT_UPDATE = {"product_id": 1,
                       "product_url": "url", "product_price": 10}


class TestProduct(unittest.TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

        # Dynamically bind SQLAlchemy to application
        db.init_app(app)
        app.app_context().push()  # this does the binding
        return app

    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        app = self.create_app()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        app = self.create_app()
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_repr(self):
        self.assertIn("ID:", repr(Product.create_product(TEST_PRODUCT)))

    def test_create_product(self):
        product = Product.create_product(TEST_PRODUCT)
        assert product in db.session

    def test_get_product(self):
        product = Product.create_product(TEST_PRODUCT)
        assert product == Product.get_product(product.product_id)

    def test_get_all_products(self):
        product = Product.create_product(TEST_PRODUCT)
        self.assertIsNotNone(product)
        product = Product.create_product(TEST_PRODUCT)
        self.assertIsNotNone(product)
        assert 2 == len(Product.get_all_products())

    def test_delete_product(self):
        product = Product.create_product(TEST_PRODUCT)
        id = product.product_id
        product.delete_product(product.product_id)
        self.assertIsNone(product.get_product(id))
        # self.assertNotIn(product, db.session)

    def test_update_product(self):
        product = Product.create_product(TEST_PRODUCT)
        # Test update with higher price
        product.update_product(TEST_PRODUCT_UPDATE)
        self.assertIn(product, db.session)
        # Test update with lower price
        TEST_PRODUCT_UPDATE["product_price"] = 1
        product.update_product(TEST_PRODUCT_UPDATE)
        self.assertIn(product, db.session)
        # Test update with the same price
        product.update_product(TEST_PRODUCT_UPDATE)
        self.assertIn(product, db.session)


class TestPrice(unittest.TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

        # Dynamically bind SQLAlchemy to application
        db.init_app(app)
        app.app_context().push()  # this does the binding
        return app

    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        self.app = self.create_app()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        app = self.create_app()
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_repr(self):
        self.assertIn("Product price:", repr(
            Price(product_id="1", product_price=10)))

    def test_get_prices_product(self):
        product = Product.create_product(TEST_PRODUCT)
        prices = Price.get_prices_product(product.product_id)
        self.assertEqual(1, len(prices))

    def test_insert_product_price(self):
        price = Price.insert_product_price(product_id="1", product_price=10)
        self.assertIn(price, db.session)

    @patch('sys.stdin', StringIO('Y\nY'))  # Simulate user input
    def test_init_db(self):
        init_db(self.app)
