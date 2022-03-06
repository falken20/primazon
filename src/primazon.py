# by Richi Rod AKA @richionline / falken20

from crypt import methods
import os
import sys
from flask import Flask, render_template, url_for, request, redirect
import psycopg2
from rich.console import Console

from . import init_db


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
    sql = 'SELECT * FROM t_products;'
    products = init_db.exec_sql_statement(sql)

    return render_template('product_list.html', products=products)


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
            product_url = request.form['product_url']
            product_desc = request.form['product_desc']
            product_url_photo = request.form['product_url_photo']
            product_price = request.form['product_price'] if request.form['product_price'] else 0

            sql = f"INSERT INTO t_products (product_url, product_desc, product_url_photo, product_price)"
            sql += f" VALUES ('{product_url}', '{product_desc}', '{product_url_photo}', {product_price})"

            init_db.exec_sql_statement(sql)

            return redirect(url_for('index'))

        return render_template('product_form.html')
    except Exception as err:
        console.print(
            f"[red bold][Line {sys.exc_info()[2].tb_lineno} {type(err).__name__}] Error showing [bold]create product[/bold] page...: {format(err)}")
