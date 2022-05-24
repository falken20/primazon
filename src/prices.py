# by Richi Rod AKA @richionline / falken20

import sys

from src import utils_db
from src.utils_logs import console


def get_prices_product(product_id):
    """
    Get all the prices from a product order by price_date_added DESC

    Args:
        product_id (str): ID from product to search for prices.
    """
    try:
        sql = f"SELECT * FROM t_prices WHERE product_id = {product_id}"
        sql += " ORDER BY price_date_added DESC"

        product_prices = utils_db.exec_sql_statement(sql)

        return product_prices
    except Exception as err:
        console.print(
            "Error in get_prices_product method:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")


def insert_product_price(product_id, product_price):
    """
    Insert a distinct price from a product

    Args:
        product_id (str): ID from the product
        product_price (float): Price from the product
    """
    try:
        sql = "INSERT INTO t_prices (product_id, product_price)"
        sql += f" VALUES ('{product_id}', {product_price})"

        utils_db.exec_sql_statement(sql)

    except Exception as err:
        console.print(
            "Error in insert_product_price method:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")
