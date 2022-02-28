# by Richi Rod AKA @richionline / falken20

from flask import Flask, render_template, url_for
import os

app = Flask(__name__, template_folder='../docs/templates', static_folder='../docs/static')
# Set this var to True to be able to make any web change and take the changes with refresh
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def index():
    # url_for('docs/static/css', filename='static.css')
    return render_template('index.html')