# by Richi Rod AKA @richionline / falken20

import sys
from rich import console
from rich.console import Console

from . import utils_db


# Create console object for logs
console = Console()

def get_all_products():
    """
    Get all the products from products database

    Returns:
        list[Tuple]: Rows from products database
    """
    sql = 'SELECT * FROM t_products;'
    products = utils_db.exec_sql_statement(sql)

    return products


def create_product(values):
    try:
        product_url = values.get('product_url')
        product_desc = values.get('product_desc')
        product_url_photo = values.get('product_url_photo')
        product_price = values.get('product_price') if values.get('product_price') else 0

        sql = f"INSERT INTO t_products (product_url, product_desc, product_url_photo, product_price, product_min_price, product_max_price)"
        sql += f" VALUES ('{product_url}', '{product_desc}', '{product_url_photo}', {product_price}, {product_price}, {product_price})"

        utils_db.exec_sql_statement(sql)

        return True
    except Exception as err:
        console.print(
            f"Error in method create_product:" + 
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " + 
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " + 
            f"\n{format(err)}", style="red bold")
        return False


def delete_product(product_id):
    try:
        sql = f"DELETE FROM t_products WHERE product_id = {product_id}"  
        utils_db.exec_sql_statement(sql)

        return True

    except Exception as err:
        console.print(
            f"Error in method delete_product:" + 
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " + 
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " + 
            f"\n{format(err)}", style="red bold")
        return False
