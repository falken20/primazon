<div align="center">
<img src="./docs/static/img/logo_app.png" alt="drawing" width="400"/>
<a href="https://richionline-portfolio.nw.r.appspot.com"><img src="https://falken-home.herokuapp.com/static/home_project/img/falken_logo.png" width=50 alt="Personal Portfolio web"></a>

![Version](https://img.shields.io/badge/version-1.2.0-blue) ![GitHub language count](https://img.shields.io/github/languages/count/falken20/primazon) ![GitHub Top languaje](https://img.shields.io/github/languages/top/falken20/primazon) ![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/falken20/primazon?logo=python&logoColor=white) ![Test coverage](https://img.shields.io/badge/test%20coverage-0%25-green) ![GitHub License](https://img.shields.io/github/license/falken20/search_extensions)


[![Richi web](https://img.shields.io/badge/web-richionline-blue)](https://richionline-portfolio.nw.r.appspot.com) [![Twitter](https://img.shields.io/twitter/follow/richionline?style=social)](https://twitter.com/richionline)

</div>



Flask web where you can save products from Amazon to observe prices along a period of time

---

##### Setup

```bash
pipenv install
```

##### Running the app

```bash
python ./src/primazon.py
```

##### Setup tests

```bash
pipenv install --dev
```

##### Running the tests with pytest and coverage

```bash
./scripts/coverage.sh
```
or
```bash
coverage run -m pytest -v && coverage html --omit=*/venv/*,*/tests/*
```
---

##### Versions

1.2.0 New Log model integrated
1.1.0 Adaptations to ORM SQLAlchemy