# by Richi Rod AKA @richionline / falken20

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'