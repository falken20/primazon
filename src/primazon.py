# by Richi Rod AKA @richionline / falken20

from crypt import methods
import os
import sys
from flask import Flask, render_template, url_for, request, redirect
import psycopg2
from rich.console import Console

from . import utils_db, products, prices


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
    query = products.get_all_products()

    return render_template('product_list.html', products=query)


@app.route('/about/')
def about():
    console.print("Method to show [bold]about[/bold] page...", style="blue")
    return render_template('about.html')


@app.route('/add/', methods=('GET', 'POST'))
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


@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    try:
        console.print(
            "Method to [bold]delete product[/bold]...", style="blue")
        products.delete_product(product_id)

        return redirect(url_for('index'))

    except Exception as err:
        console.print(
            f"Error in delete_product method:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")


@app.route('/edit/<int:product_id>')
def edit_product(product_id):
    try:
        console.print(
            "Method to [bold]edit product[/bold]...", style="blue")
        product = products.get_product(product_id)

        return render_template('product_form.html', product=product)

    except Exception as err:
        console.print(
            f"Error in edit_product method:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")
