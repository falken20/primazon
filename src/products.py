# by Richi Rod AKA @richionline / falken20

import sys
import datetime

from . import utils_db
from src.logger import loggear

IDX_PRODUCT_ID = 0
IDX_PRODUCT_URL = 1
IDX_PRODUCT_DESC = 2
IDX_PRODUCT_URL_PHOTO = 3
IDX_PRODUCT_PRICE = 4
IDX_PRODUCT_RATING = 5
IDX_PRODUCT_REVIEWS = 6
IDX_PRODUCT_MIN_PRICE = 7
IDX_PRODUCT_MAX_PRICE = 8
IDX_PRODUCT_DATE_ADDED = 9
IDX_PRODUCT_DATE_UPDATED = 10


def get_all_products():
    """
    Get all the products from products database

    Returns:
        list[Tuple]: Rows from products database
    """
    try:
        sql = 'SELECT * FROM t_products ORDER BY product_date_updated DESC, product_id;'
        products = utils_db.exec_sql_statement(sql)

        return products
    except Exception as err:
        loggear("Error in method get_all_products:", "ERROR", err, sys)
        return False


def get_product(product_id):
    """
    Search for a product in the database with a product_id

    Args:
        product_id (int): id from the product to get

    Returns:
        list[Tuple]: Fields from the product searched
    """
    try:
        sql = f'SELECT * FROM t_products WHERE product_id = {product_id};'
        product = utils_db.exec_sql_statement(sql)

        return product
    except Exception as err:
        loggear("Error in method get_product:", "ERROR", err, sys)
        return False


def create_product(values):
    """
    Insert a product in the database

    Args:
        values (ImmutableMultiDict[str, str]): key/value pairs in the body, from a HTML post form

    Returns:
        boolean: True if everything ok, False in other case
    """
    try:
        product_url = values.get('product_url')
        product_desc = values.get('product_desc')
        product_url_photo = values.get('product_url_photo')
        product_price = values.get(
            'product_price') if values.get('product_price') else 0
        product_rating = values.get('product_rating')
        product_reviews = values.get('product_reviews')

        sql = "INSERT INTO t_products (product_url, product_desc, product_url_photo, product_price, product_rating, "
        sql += " product_reviews, product_min_price, product_max_price)"
        sql += f" VALUES ('{product_url}', '{product_desc}', '{product_url_photo}', {product_price}, '{product_rating}',"
        sql += f" '{product_reviews}', {product_price}, {product_price})"

        utils_db.exec_sql_statement(sql)

        return True
    except Exception as err:
        loggear("Error in method create_product:", "ERROR", err, sys)
        return False


def delete_product(product_id):
    """
    Delete a product from the database

    Args:
        product_id (int): id from the product to delete

    Returns:
        boolean: True if everything ok, False in other case
    """
    try:
        sql = f"DELETE FROM t_products WHERE product_id = {product_id}"
        utils_db.exec_sql_statement(sql)

        return True

    except Exception as err:
        loggear("Error in method delete_product:", "ERROR", err, sys)
        return False


def update_product(values):
    """
    Update a product in the database

    Args:
        values (ImmutableMultiDict[str, str]): key/value pairs in the body, from a HTML post form

    Returns:
        boolean: True if everything ok, False in other case
    """
    try:
        product_id = values.get('product_id')
        product_url = values.get('product_url')
        product_desc = values.get('product_desc')
        product_url_photo = values.get('product_url_photo')
        product_price = values.get(
            'product_price') if values.get('product_price') else 0
        product_rating = values.get('product_rating')
        product_reviews = values.get('product_reviews')
        product_min_price = values.get(
            'product_min_price') if values.get('product_min_price') else 0
        product_max_price = values.get(
            'product_max_price') if values.get('product_max_price') else 0

        sql = "UPDATE t_products"
        sql += f" SET product_url = '{product_url}', product_desc = '{product_desc}', "
        sql += f" product_url_photo = '{product_url_photo}', product_price = {product_price},"
        sql += f" product_rating = '{product_rating}', product_reviews = '{product_reviews}',"
        sql += f" product_min_price = {product_min_price}, product_max_price = {product_max_price},"
        sql += f" product_date_updated = '{datetime.datetime.now()}'"
        sql += f" WHERE product_id = {product_id}"

        utils_db.exec_sql_statement(sql)

        return True
    except Exception as err:
        loggear("Error in method create_product:", "ERROR", err, sys)
        return False
