import unittest
import json
from flask import Flask

from src import main
from src.models import Product, db

TEST_PRODUCT = {"product_url": "url", "product_price": 5}


class TestPrimazon(unittest.TestCase):

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
        main.app.config["TESTING"] = True
        self.app = main.app.test_client()
        db.create_all()

        self.info = {"product_url": "an_url",
                     "product_desc": "value2",
                     "product_url_photo": "value2",
                     "product_rating": "value2",
                     "product_reviews": "value2",
                     "product_price": 10
                     }

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = self.create_app()
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    """
    def setUp(self):
        primazon.app.config["TESTING"] = True
        self.app = primazon.app.test_client()

        self.info = {"product_url": "an_url",
                     "product_desc": "value2",
                     "product_url_photo": "value2",
                     "product_rating": "value2",
                     "product_reviews": "value2",
                     "product_price": 10
                     }
    """

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
                                 follow_redirects=True,
                                 # content_type='application/json',
                                 headers={
                                     "Content-Type": "application/x-www-form-urlencoded"}
                                 )
        self.assertEqual(200, response.status_code)

        response = self.app.post("/products/add/",
                                 data=json.dumps(dict(self.info)),
                                 follow_redirects=False,
                                 headers={
                                     "Content-Type": "application/x-www-form-urlencoded"}
                                 )
        self.assertEqual(302, response.status_code)

    def test_delete_product(self):
        product = Product.create_product(TEST_PRODUCT)
        response = self.app.get(f"/products/delete/{product.product_id}")
        self.assertEqual(302, response.status_code)  # Redirecting to home
        self.assertIn("/home/Product%20deleted%20sucesfully", response.text)

    def test_show_grouped(self) -> None:
        response = self.app.get("/show_grouped", follow_redirects=True)
        self.assertEqual(200, response.status_code)  # Redirecting

    def test_edit_product(self):
        product = Product.create_product(TEST_PRODUCT)
        response = self.app.get(f"/products/edit/{product.product_id}", follow_redirects=True)
        self.assertEqual(200, response.status_code)  # Redirecting to home

    def test_update_product(self):
        response = self.app.post("/products/update",
                                 data=json.dumps(dict(self.info)),
                                 follow_redirects=True,
                                 headers={
                                     "Content-Type": "application/x-www-form-urlencoded"}
                                 )
        self.assertEqual(200, response.status_code)

    def test_run_process(self):
        response = self.app.get("/run_process", follow_redirects=True)
        self.assertEqual(200, response.status_code)  # Redirecting
        response = self.app.get("/run_process_cron", follow_redirects=True)
        self.assertEqual(200, response.status_code)  # Redirecting
