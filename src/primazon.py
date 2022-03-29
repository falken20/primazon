# by Richi Rod AKA @richionline / falken20

from crypt import methods
import os
from src import prices
import sys
from click import style
from flask import Flask, render_template, url_for, request, redirect
from numpy import product
import psycopg2
from rich.console import Console

from . import products
from . import utils


app = Flask(__name__, template_folder='../docs/templates',
            static_folder='../docs/static')
# Set this var to True to be able to make any web change and take the changes with refresh
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Create console object for logs
console = Console()


@app.route('/')
def index():
    console.print("Method to show [bold]index[/bold] page...", style="blue")
    # Get all the products
    all_products = products.get_all_products()

    return render_template('product_list.html', products=all_products)


@app.route('/about/')
def about():
    console.print("Method to show [bold]about[/bold] page...", style="blue")
    return render_template('about.html')


@app.route('/products/add/', methods=('GET', 'POST'))
def create_product():
    try:
        console.print(
            "Method to show [bold]create product[/bold] page...", style="blue")
        if request.method == 'POST':
            products.create_product(request.form)
            return redirect(url_for('index'))

        return render_template('product_form.html')

    except Exception as err:
        console.print(
            f"Error showing create product page:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")


@app.route('/products/delete/<int:product_id>')
def delete_product(product_id):
    try:
        console.print(
            "Method to [bold]delete product[/bold] with id: {product_id}", style="blue")
        products.delete_product(product_id)

        return redirect(url_for('index'))

    except Exception as err:
        console.print(
            f"Error in delete_product method:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")


@app.route('/products/edit/<int:product_id>')
def edit_product(product_id):
    try:
        console.print(
            "Method to [bold]edit product[/bold] with id: {product_id}", style="blue")
        product = products.get_product(product_id)

        return render_template('product_edit.html', product=product)

    except Exception as err:
        console.print(
            f"Error in edit_product method:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")


@app.route('/products/update', methods=["POST"])
def update_product():
    try:
        console.print(
            "Method to [bold]update product[/bold]...", style="blue")
        products.update_product(request.form)

        return redirect(url_for('index'))

    except Exception as err:
        console.print(
            f"Error in edit_product method:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")


def update_product_from_amazon(product, amazon_data):
    """
    Update data product from amazon data

    Args:
        product (list): Current data product
        amazon_data (dict): Data product from Amazon

    Returns:
        product_to_update: Object product to update
    """
    try:
        product_to_update = dict()
        product_to_update['product_id'] = product[products.IDX_PRODUCT_ID]
        product_to_update['product_url'] = product[products.IDX_PRODUCT_URL]
        product_to_update['product_desc'] = amazon_data['name'][0:150]
        product_to_update['product_url_photo'] = amazon_data['images']

        float_price = float(amazon_data['price'].replace(
            '.', '').replace(',', '.').replace('€', ''))

        if float_price > 0:
            product_to_update['product_price'] = float_price
            # Update min and max price
            if float_price > product[products.IDX_PRODUCT_MAX_PRICE] or product[products.IDX_PRODUCT_MAX_PRICE] == 0:
                product_to_update['product_max_price'] = float_price
            else:
                product_to_update['product_max_price'] = product[products.IDX_PRODUCT_MAX_PRICE]

            if float_price < product[products.IDX_PRODUCT_MIN_PRICE] or product[products.IDX_PRODUCT_MIN_PRICE] == 0:
                product_to_update['product_min_price'] = float_price
            else:
                product_to_update['product_min_price'] = product[products.IDX_PRODUCT_MIN_PRICE]

            # When the price changes insert the price in prices table
            if  product_to_update['product_price'] != product[products.IDX_PRODUCT_PRICE]:
                prices.insert_product_price(product_to_update['product_id'], product_to_update['product_price'])

        else:
            product_to_update['product_price'] = product[products.IDX_PRODUCT_PRICE]
            product_to_update['product_max_price'] = product[products.IDX_PRODUCT_MAX_PRICE]
            product_to_update['product_min_price'] = product[products.IDX_PRODUCT_MIN_PRICE]

        product_to_update['product_rating'] = amazon_data['rating']
        product_to_update['product_reviews'] = amazon_data['reviews']

        return product_to_update

    except Exception as err:
        console.print(
            f"Error in update_product_from_amazon method:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")


@app.route('/product/refresh/<int:product_id>')
def refresh_data(product_id):
    try:
        console.print(
            f"Method to [bold]refresh data product[/bold] with id: {product_id}", style="blue")

        product = products.get_product(product_id)[0]
        product_url = product[products.IDX_PRODUCT_URL]
        console.print(f"Product to check: {product}", style="blue")
        console.print(f"Amazon url to check: {product_url}", style="blue")

        amazon_data = utils.scrap_web(product_url)
        console.print(
            f"Getting [bold]Amazon[/bold] data: {amazon_data}", style="blue")

        if amazon_data is None:
            console.print(
                f"Impossible to get data from Amazon for the product url '{product_url}'", style="red bold")
        else:
            product_to_update = update_product_from_amazon(
                product, amazon_data)
            products.update_product(product_to_update)
            console.print(
                f"Product with id {product[products.IDX_PRODUCT_ID]} succesfully updated", style="blue")

        return redirect(url_for('index'))
        # return redirect(url_for('edit_product', product_id=product_id))

    except Exception as err:
        console.print(
            f"Error in refresh_data method:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")


@app.route('/run_process')
def run_process():
    try:
        console.print(
            f"Process to [bold]refresh [bold]ALL[/bold] data product[/bold]", style="blue")

        all_products = products.get_all_products()

        for product in all_products:
            amazon_data = utils.scrap_web(product[products.IDX_PRODUCT_URL])
            console.print(
                f"Getting [bold]Amazon[/bold] data: {amazon_data}", style="blue")

            if amazon_data is None:
                console.print(
                    f"Impossible to get data from Amazon for the product url '{product[products.IDX_PRODUCT_URL]}'", style="red bold")
            else:
                product_to_update = update_product_from_amazon(
                    product, amazon_data)
                products.update_product(product_to_update)
                console.print(
                    f"Product with id {product[0]} succesfully updated", style="blue")

        console.print(
            f"Process to [bold]refresh [bold]ALL[/bold] data product[/bold] finished succesfully", style="blue")

        return redirect(url_for('index'))

    except Exception as err:
        console.print(
            f"Error in run_process method:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")
