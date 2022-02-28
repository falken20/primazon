<div align="center">
<img src="./docs/static/img/logo_app.png" alt="drawing" width="400"/>
<a href="https://richionline-portfolio.nw.r.appspot.com"><img src="https://falken-home.herokuapp.com/static/home_project/img/falken_logo.png" width=50 alt="Personal Portfolio web"></a>

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![GitHub language count](https://img.shields.io/github/languages/count/falken20/primazon) ![GitHub Top languaje](https://img.shields.io/github/languages/top/falken20/primazon) ![Test coverage](https://img.shields.io/badge/test%20coverage-0%25-green) ![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/falken20/primazon)

[![Richi web](https://img.shields.io/badge/web-richionline-blue)](https://richionline-portfolio.nw.r.appspot.com) [![Twitter](https://img.shields.io/twitter/follow/richionline?style=social)](https://twitter.com/richionline)

</div>


# primazon
Flask web where you can save products from Amazon to observe prices along a period of time

---

##### Setup

```bash
pip install -r requirements.txt
```

##### Running the app

```bash
python ./src/primazon.py
```

##### Setup tests

```bash
pip install -r requirements-tests.txt
```

##### Running the tests with pytest and coverage

```bash
./scripts/coverage.sh
```
or
```bash
coverage run -m pytest -v && coverage html --omit=*/venv/*,*/test/*
```
