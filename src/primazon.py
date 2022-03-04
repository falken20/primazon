# by Richi Rod AKA @richionline / falken20

import os
from flask import Flask, render_template, url_for
import psycopg2

from . import init_db


app = Flask(__name__, template_folder='../docs/templates',
            static_folder='../docs/static')
# Set this var to True to be able to make any web change and take the changes with refresh
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def index():
    """
    Show the screen with products

    Returns:
        str: HTML page for products
    """

    # Get the connection to the database
    conn = init_db.get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM t_products;')
    products = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('index.html', products=products)
