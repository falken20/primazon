from urllib import response
import pytest
from flask import Flask

from src.primazon import app
from src.models import Product, Price, db

TEST_PRODUCT = {"product_url": "url", "product_price": 5}


def create_app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    # Dynamically bind SQLAlchemy to application
    db.init_app(app)
    app.app_context().push()  # this does the binding
    return app


@pytest.fixture
def setUp():
    app = create_app()

    with app.app_context():
        db.create_all()


@pytest.fixture
def client():
    app.config.update({'TESTING': True})

    with app.test_client() as client:
        yield client


def test_home(client) -> None:
    # rv = client.get("/author/1")
    # assert rv.json == {"id": 1, "first_name": "foo", "last_name": "bar"}
    Product.create_product(TEST_PRODUCT)
    response = client.get("/home")
    print(response)
