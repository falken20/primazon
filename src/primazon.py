# by Richi Rod AKA @richionline / falken20

import sys
import os
from flask import Flask, render_template, url_for, request, redirect

from . import utils
from src.models import Product
from src.models import Price
from src.models import db
from src.utils_logs import loggear

app = Flask(__name__, template_folder='../docs/templates',
            static_folder='../docs/static')
# Set this var to True to be able to make any web change and take the changes with refresh
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Set the database params for SQLAlchemy ORM library
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# Secret key for creating session coockie. It has to be different for each user
app.secret_key = os.urandom(24)

db.init_app(app)


@app.route('/')
@app.route('/home')
def index():
    loggear("Method to show [bold]index[/bold] page...", "INFO")
    # Get all the products
    # NO_ORM all_products = products.get_all_products()
    all_products = Product.get_all_products()

    return render_template('product_list.html', products=all_products)


@app.route('/about/')
def about():
    loggear("Method to show [bold]about[/bold] page...", "INFO")
    return render_template('about.html')


@app.route('/products/add/', methods=('GET', 'POST'))
def create_product():
    try:
        loggear(
            "Method to show [bold]create product[/bold] page...", "INFO")
        if request.method == 'POST':
            # NO_ORM products.create_product(request.form)
            Product.create_product(request.form)
            return redirect(url_for('index'))

        return render_template('product_form.html')

    except Exception as err:
        loggear("Error showing create product page:", "ERROR", err, sys)


@app.route('/products/delete/<int:product_id>')
def delete_product(product_id):
    try:
        loggear(
            f"Method to [bold]delete product[/bold] with id: {product_id}", "INFO")
        # NO_ORM products.delete_product(product_id)
        Product.delete_product(product_id)

        return redirect(url_for('index'))

    except Exception as err:
        loggear("Error in delete_product method:", "ERROR", err, sys)


@app.route('/products/edit/<int:product_id>')
def edit_product(product_id):
    try:
        loggear(
            f"Method to [bold]edit product[/bold] with id: {product_id}", "INFO")
        # NO_ORM product = products.get_product(product_id)
        product = Product.get_product(product_id)

        return render_template('product_edit.html', product=product)

    except Exception as err:
        loggear("Error in edit_product method:", "ERROR", err, sys)


@app.route('/products/update', methods=["POST"])
def update_product():
    try:
        loggear("Method to [bold]update product[/bold]...", "INFO")
        # NO_ORM products.update_product(request.form)
        Product.update_product(request.form)

        return redirect(url_for('index'))

    except Exception as err:
        loggear("Error in edit_product method:", "ERROR", err, sys)


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
        product_to_update['product_id'] = product.product_id
        product_to_update['product_url'] = product.product_url
        product_to_update['product_desc'] = amazon_data['name'][0:150]
        product_to_update['product_url_photo'] = amazon_data['images']

        float_price = float(amazon_data['price'].replace(
            '.', '').replace(',', '.').replace('€', ''))

        if float_price > 0:
            product_to_update['product_price'] = float_price
            # Update min and max price
            if float_price > product.product_max_price or product.product_max_price == 0:
                product_to_update['product_max_price'] = float_price
            else:
                product_to_update['product_max_price'] = product.product_max_price

            if float_price < product.product_min_price or product.product_min_price == 0:
                product_to_update['product_min_price'] = float_price
            else:
                product_to_update['product_min_price'] = product.product_min_price

            # When the price changes insert the price in prices table
            if product_to_update['product_price'] != product.product_price:
                Price.insert_product_price(
                    product_to_update['product_id'], product_to_update['product_price'])

        else:
            product_to_update['product_price'] = product.product_price
            product_to_update['product_max_price'] = product.product_max_price
            product_to_update['product_min_price'] = product.product_min_price

        product_to_update['product_rating'] = amazon_data['rating']
        product_to_update['product_reviews'] = amazon_data['reviews']

        return product_to_update

    except Exception as err:
        loggear("Error in update_product_from_amazon method:", "ERROR", err, sys)


@app.route('/product/refresh/<int:product_id>')
def refresh_data(product_id):
    try:
        loggear(
            f"Method to [bold]refresh data product[/bold] with id: {product_id}", "INFO")

        # NO_ORM product = products.get_product(product_id)[0]
        product = Product.get_product(product_id)
        # NO_ORM product_url = product[products.IDX_PRODUCT_URL]
        loggear(f"Product to check: {product}", "DEBUG")
        loggear(f"Amazon url to check: {product.product_url}", "DEBUG")

        amazon_data = utils.scrap_web(product.product_url)
        loggear(
            f"Getting [bold]Amazon[/bold] data: {amazon_data}", "DEBUG")

        if amazon_data is None:
            loggear(
                f"Impossible to get data from Amazon for the product url '{product.product_url}'", "WARNING")
        else:
            product_to_update = update_product_from_amazon(
                product, amazon_data)
            # NO_ORM products.update_product(product_to_update)
            Product.update_product(product_to_update)
            loggear(
                f"Product with id {product.product_id} succesfully updated", "INFO")

        return redirect(url_for('index'))
        # return redirect(url_for('edit_product', product_id=product_id))

    except Exception as err:
        loggear("Error in refresh_data method:", "ERROR", err, sys)


@app.route('/run_process')
def run_process():
    try:
        loggear(
            "Process to [bold]refresh [bold]ALL[/bold] data product[/bold]", "INFO")

        # NO_ORM all_products = products.get_all_products()
        all_products = Product.get_all_products()

        for product in all_products:
            # NO_ORM amazon_data = utils.scrap_web(product[products.IDX_PRODUCT_URL])
            amazon_data = utils.scrap_web(product.product_url)
            loggear(
                f"Getting [bold]Amazon[/bold] data: {amazon_data}", "DEBUG")

            if amazon_data is None:
                loggear(
                    f"Impossible to get data from Amazon for the product url '{product.product_url}'",
                    "WARNING")
            else:
                product_to_update = update_product_from_amazon(
                    product, amazon_data)
                # NO_ORM products.update_product(product_to_update)
                Product.update_product(product_to_update)
                loggear(
                    f"Product with id {product.product_id} succesfully updated", "DEBUG")

        loggear(
            "Process to [bold]refresh [bold]ALL[/bold] data product[/bold] finished succesfully", "INFO")

        return redirect(url_for('index'))

    except Exception as err:
        loggear("Error in run_process method:", "ERROR", err, sys)
