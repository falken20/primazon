# by Richi Rod AKA @richionline / falken20

import datetime
from .primazon import db


class Product(db.Model):
    __tablename__ = "products"

    product_id = db.Column(db.Serial, primary_key=True)
    product_url = db.Column(db.String(500), nullable=False)
    product_desc = db.Column(db.String(150))
    product_url_photo = db.Column(db.String(500), nullable=True)
    product_price = db.Column(db.Float)
    product_rating = db.Column(db.String(50), nullable=True)
    product_reviews = db.Column(db.String(100), nullable=True)
    product_min_price = db.Column(db.Float)
    product_max_price = db.Column(db.Float)
    product_date_added = db.Column(db.Date, default=datetime.date.now)
    product_date_update = db.Column(db.Date)

    def __repr__(self) -> str:
        return f"Product: {self.product_desc}"


class Price(db.Model):
    __tablename__ = "prices"

    price_id = db.Column(db.Serial, primary_hey=True)
    product_price = db.Column(db.Float)
    price_date_added = db.Column(db.Date, default=datetime.date.now)

    product_id = db.Column(
        db.Serial,
        db.ForeignKey('products.product_id', ondelete='CASCADE'),
        nullable=False
    )
    price = db.relationship('Product', backref=db.backref('prices', lazy=True))

    def __repr__(self) -> str:
        return f"Product price: {self.product_id} - {self.product_price}"
