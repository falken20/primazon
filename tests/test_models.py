from flask import Flask
from flask_testing import TestCase

from src.models import db


class TestProduct(TestCase):

    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"

        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
            self.populate_db()  # Your function that adds test data.

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()

    def test_print_product(self):
        self.assertIn("ID", format(self.product))

    def test_author(client) -> None:
        rv = client.get("/author/1")
        assert rv.json == {"id": 1, "first_name": "foo", "last_name": "bar"}
