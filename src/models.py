# by Richi Rod AKA @richionline / falken20

# ######################################################################
# This file is to set all the db models and use the ORM flask_sqlalchemy
# With this file it is no neccesary to use prices.py and products.py
# ######################################################################


import datetime
import os
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from dotenv import load_dotenv, find_dotenv

# from src.logger import Log
import logging

FORMAT = '%(asctime)s %(levelname)s %(lineno)d %(filename)s %(funcName)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

# Load .env file
load_dotenv(find_dotenv())

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
    product_date_updated = db.Column(db.Date)

    # product_prices = db.relationship('Price')
    product_prices = db.relationship('Price', backref='product')

    def __repr__(self) -> str:
        return f"ID: {self.product_id} / Product: {self.product_desc} / URL: {self.product_url} / Price: {self.product_price}"

    @staticmethod
    def get_all_products():
        return Product.query.order_by(Product.product_date_updated.desc(), Product.product_id).all()

    @staticmethod
    def get_product(id):
        return Product.query.filter_by(product_id=id).first()

    @staticmethod
    def delete_product(id):
        Price.delete_product_prices(id)
        Product.query.filter_by(product_id=id).delete()
        db.session.commit()

    @staticmethod
    def create_product(values):
        new_product = Product(
            product_url=values.get('product_url'),
            product_desc=values.get('product_desc'),
            product_url_photo=values.get('product_url_photo'),
            product_price=values.get(
                'product_price') if values.get('product_price') else 0,
            product_rating=values.get('product_rating'),
            product_reviews=values.get('product_reviews'),
            product_min_price=values.get(
                'product_price') if values.get('product_price') else 0,
            product_max_price=values.get(
                'product_price') if values.get('product_price') else 0,
            product_date_updated=datetime.datetime.now(),
        )
        db.session.add(new_product)
        db.session.commit()

        # Add the first price
        if float(new_product.product_price) != 0:
            Price.insert_product_price(
                new_product.product_id, new_product.product_price)

        return new_product

    @staticmethod
    def update_product(values) -> bool:
        product_to_update = Product.get_product(values.get('product_id'))

        product_to_update.product_date_updated = datetime.datetime.now()
        product_to_update.product_url = values.get('product_url')
        product_to_update.product_desc = values.get('product_desc')
        product_to_update.product_url_photo = values.get('product_url_photo')

        if float(product_to_update.product_price) != float(values.get('product_price')):
            update_price = True
        else:
            update_price = False

        product_to_update.product_price = values.get(
            'product_price') if values.get('product_price') else 0
        product_to_update.product_rating = values.get('product_rating')
        product_to_update.product_reviews = values.get('product_reviews')

        product_price = float(product_to_update.product_price)
        product_min_price = float(product_to_update.product_min_price)
        product_max_price = float(product_to_update.product_max_price)

        if product_price < product_min_price or product_min_price == 0:
            product_to_update.product_min_price = product_to_update.product_price

        if product_price > product_max_price or product_max_price == 0:
            product_to_update.product_max_price = product_to_update.product_price

        db.session.commit()

        if update_price:
            Price.insert_product_price(
                product_to_update.product_id, product_to_update.product_price)

        # To know if the price has been updated
        return update_price


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

    # product = db.relationship(
    #    'Product', backref=db.backref('t_prices', cascade='all,delete', order_by=price_id), lazy=True)

    def __repr__(self) -> str:
        return f"Product price: {self.product_id} - {self.product_price}"

    @staticmethod
    def get_prices_product(product_id):
        product_prices = Price.query.filter_by(product_id=product_id).order_by(
            Price.price_date_added.desc()).all()
        return product_prices

    @staticmethod
    def insert_product_price(product_id, product_price):
        new_price = Price(product_id=product_id, product_price=product_price)
        print("*****************************")
        db.session.add(new_price)
        db.session.commit()
        return new_price

    @staticmethod
    def delete_product_prices(product_id):
        Price.query.filter_by(product_id=product_id).delete()
        db.session.commit()


def init_db(app):
    """
    Main process to create the needed tables for the application
    """
    logging.info("Init DB process starting...")

    try:
        if input("Could you drop the tables if they exist(y/n)? ") in ["Y", "y"]:
            with app.app_context():
                db.drop_all()
            logging.info("Tables dropped")

        if input("Could you create the tables(y/n)? ") in ["Y", "y"]:
            logging.info("Creating tables...")
            with app.app_context():
                db.create_all()

        with app.app_context():
            db.session.commit()

        logging.info("Process finished succesfully")

    except Exception as err:
        logging.error(f"Execution Error in init_db: {err}", exc_info=True)


if __name__ == '__main__':
    logging.info("Preparing app vars...")
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace(
        "://", "ql://", 1)
    db.init_app(app)
    init_db(app)
