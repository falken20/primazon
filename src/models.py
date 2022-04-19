# by Richi Rod AKA @richionline / falken20

# This file is to set all the db models and use the ORM flask_sqlalchemy
# With this file it is no neccesary to use prices.py and products.py

import datetime
from rich.console import Console

from .primazon import db

# Create console object for logs
console = Console()


class Product(db.Model):
    # Table name in class name in camel_case. You can override with __tablename__
    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True)
    product_url = db.Column(db.String(500), nullable=False)
    product_desc = db.Column(db.String(150))
    product_url_photo = db.Column(db.String(500), nullable=True)
    product_price = db.Column(db.Float)
    product_rating = db.Column(db.String(50), nullable=True)
    product_reviews = db.Column(db.String(100), nullable=True)
    product_min_price = db.Column(db.Float)
    product_max_price = db.Column(db.Float)
    product_date_added = db.Column(db.Date, default=datetime.date.today)
    product_date_update = db.Column(db.Date)

    # prices = db.relationship('Price', backref='product', lazy=True)

    def __repr__(self) -> str:
        return f"Product: {self.product_desc}"


class Price(db.Model):
    __tablename__ = "prices"

    price_id = db.Column(db.Integer, primary_key=True)
    product_price = db.Column(db.Float)
    price_date_added = db.Column(db.Date, default=datetime.date.today)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.product_id', ondelete='CASCADE'),
        nullable=False
    )

    product = db.relationship(
        'Product', backref=db.backref('prices', lazy=True))

    def __repr__(self) -> str:
        return f"Product price: {self.product_id} - {self.product_price}"


def init_db():
    console.print("Creating Database if doesn't exist", style="blue")
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    init_db()
