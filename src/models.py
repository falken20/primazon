# by Richi Rod AKA @richionline / falken20

# This file is to set all the db models and use the ORM flask_sqlalchemy
# With this file it is no neccesary to use prices.py and products.py

import datetime
import sys
from rich.console import Console
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy


# Create console object for logs
console = Console()

# Create db object
db = SQLAlchemy()


class Product(db.Model):
    # Table name in class name in camel_case. You can override with __tablename__
    __tablename__ = "t_products"

    product_id = db.Column(db.Integer, primary_key=True)
    product_url = db.Column(db.String(500), nullable=False)
    product_desc = db.Column(db.String(150))
    product_url_photo = db.Column(db.String(500), nullable=True)
    product_price = db.Column(db.Float)
    product_rating = db.Column(db.String(50), nullable=True)
    product_reviews = db.Column(db.String(100), nullable=True)
    product_min_price = db.Column(db.Float)
    product_max_price = db.Column(db.Float)
    product_date_added = db.Column(db.Date, default=func.now())
    product_date_update = db.Column(db.Date)

    product_prices = db.relationship('Price')

    def __repr__(self) -> str:
        return f"Product: {self.product_desc} / URL: {self.product_url}"
    
    @staticmethod
    def get_by_id(id):
        return Product.query.filter_by(product_id=id).first()


class Price(db.Model):
    __tablename__ = "t_prices"

    price_id = db.Column(db.Integer, primary_key=True)
    product_price = db.Column(db.Float)
    price_date_added = db.Column(db.Date, default=func.now())

    product_id = db.Column(
        db.Integer,
        db.ForeignKey('t_products.product_id', ondelete='CASCADE'),
        nullable=False
    )

    product = db.relationship(
        'Product', backref=db.backref('t_prices', order_by=price_id), lazy=True)

    def __repr__(self) -> str:
        return f"Product price: {self.product_id} - {self.product_price}"


def init_db():
    """
    Main process to create the needed tables for the application
    """
    console.print("Init DB process starting...", style="bold green")

    try:
        if input("Could you drop the tables if they exist(y/n)? ") in ["Y", "y"]:
            db.drop_all()
            console.print("Tables dropped", style="blue")

        if input("Could you create the tables(y/n)? ") in ["Y", "y"]:
            console.print("Creating tables...", style="blue")
            db.create_all()

        db.session.commit()

        console.print("Process finished succesfully", style="bold green")

    except Exception as err:
        console.print(
            "Execution Error in init_db:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")


if __name__ == '__main__':
    init_db()
