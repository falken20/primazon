from urllib import response
import pytest
from flask import Flask

from src.primazon import app
from src.models import Product, Price, db

TEST_PRODUCT = {"product_url": "url", "product_price": 5}


@pytest.fixture
def setUp():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with app.app_context():
        # Dynamically bind SQLAlchemy to application
        db.init_app(app)
        app.app_context().push()  # this does the binding

        db.create_all()


@pytest.fixture
def client():

    with app.test_client() as client:
        yield client


def test_home(client) -> None:
    # rv = client.get("/author/1")
    # assert rv.json == {"id": 1, "first_name": "foo", "last_name": "bar"}
    Product.create_product(TEST_PRODUCT)
    response = client.get("/home")
    print(response)
