import unittest
from flask import Flask

from src.models import Product, db

test_product = {"product_url": "url", "product_price": 1}

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

    def test_product(self):
        product = Product.create_product(test_product)
        print(product)
        db.session.add(product)
        db.session.commit()

        assert product in db.session


"""
    def test_print_product(self):
        self.assertIn("ID", format(self.product))
        
    def test_author(client) -> None:
        rv = client.get("/author/1")
        assert rv.json == {"id": 1, "first_name": "foo", "last_name": "bar"}
"""
