# by Richi Rod AKA @richionline / falken20

from crypt import methods
import os
import sys
import re
from click import style
from flask import Flask, render_template, url_for, request, redirect
import psycopg2
from rich.console import Console

from .  import products
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


@app.route('/product/refresh/<int:product_id>')
def refresh_data(product_id):
    try:
        console.print(f"Method to [bold]refresh data product[/bold] with id: {product_id}", style="blue")

        product_url = products.get_product(product_id)[0][1]

        amazon_data = utils.scrap_web(product_url)
        
        product_to_update = dict()
        product_to_update['product_id'] = product_id
        product_to_update['product_url'] = product_url
        product_to_update['product_desc'] = amazon_data['name']
        product_to_update['product_url_photo'] = amazon_data['images']

        float_price = re.findall("\d+\.\d+", amazon_data['price'])
        print(float_price)
        product_to_update['product_price'] = float_price if float_price else 0

        products.update_product(product_to_update)

        return redirect(url_for('index'))
        # return redirect(url_for('edit_product', product_id=product_id))

    except Exception as err:
        console.print(
            f"Error in refresh_data method:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")
