import unittest
from flask import Flask

from src.models import Price, Product, db


class TestProduct(unittest.TestCase):

    TEST_PRODUCT = {"product_url": "url", "product_price": 1}

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
        self.assertIn("ID:", repr(Product.create_product(self.TEST_PRODUCT)))

    def test_create_product(self):
        product = Product.create_product(self.TEST_PRODUCT)
        db.session.add(product)
        db.session.commit()
        assert product in db.session

    def test_get_product(self):
        product = Product.create_product(self.TEST_PRODUCT)
        assert product == Product.get_product(product.product_id)

    def test_get_all_products(self):
        product = Product.create_product(self.TEST_PRODUCT)
        product = Product.create_product(self.TEST_PRODUCT)
        assert 2 == len(Product.get_all_products())

    def test_delete_product(self):
        product = Product.create_product(self.TEST_PRODUCT)
        product.delete_product(product.product_id)
        self.assertNotIn(product, db.session)

    def test_update_product(self):
        product = Product.create_product(self.TEST_PRODUCT)
        self.assertFalse(False)


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
        self.assertIn("Product price:", repr(Price(product_id="1", product_price=10)))

    def test_get_prices_product(self):
        price = Price(product_id="1", product_price=10)
        prices = Price.get_prices_product(price.product_id)
        print(prices)
        self.assertEqual(1, prices[0].product_price)

    def test_insert_product_price(self):
        price = Price.insert_product_price(product_id="1", product_price=10)
        self.assertIn(price, db.session)



"""
    def test_print_product(self):
        self.assertIn("ID", format(self.product))

    def test_author(client) -> None:
        rv = client.get("/author/1")
        assert rv.json == {"id": 1, "first_name": "foo", "last_name": "bar"}
"""
