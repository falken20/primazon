<div align="center">
<img src="./static/img/logo_app.png" alt="drawing" width="400"/>
<a href="https://richionline-portfolio.nw.r.appspot.com"><img src="https://richionline-portfolio.nw.r.appspot.com/static/assets/falken_logo.ico" width=50 alt="Personal Portfolio web"></a>

![Version](https://img.shields.io/badge/version-1.6.0-blue) ![GitHub language count](https://img.shields.io/github/languages/count/falken20/primazon) ![GitHub Top languaje](https://img.shields.io/github/languages/top/falken20/primazon) ![Test coverage](https://img.shields.io/badge/test%20coverage-78%25-green) ![GitHub License](https://img.shields.io/github/license/falken20/search_extensions)


[![Richi web](https://img.shields.io/badge/web-richionline-blue)](https://richionline-portfolio.nw.r.appspot.com) [![Twitter](https://img.shields.io/twitter/follow/richionline?style=social)](https://twitter.com/richionline)

</div>



Flask web where you can save products from Amazon to observe prices along a period of time

---
##### Deploy
```bash
gcloud app deploy
```

##### Setup

```bash
pip install -r requirements.txt
```

##### Running the app

```bash
flask run
```

##### Setup tests

```bash
pip install -r requirements-tests.txt
```

##### Running the tests with pytest and coverage

```bash
./check_app.sh
```
or
```bash
coverage run -m pytest -v && coverage html --omit=*/venv/*,*/tests/*
```

##### Environment vars
```bash
PROXY=N
LEVEL_LOG = ["DEBUG", "INFO", "WARNING", "ERROR"]

# To use Supabase PostgreSQL DB
DATABASE_URL=postgres://postgres:XXXXXX@db.rhsrwnntcqvjpgamytve.supabase.co:6543/postgres

# SQlite database data (only for local)
DB_SQLITE_URL=sqlite://
DB_SQLITE_NAME=primazon.db

# MailJet keys
MAILJET_APIKEY_PUBLIC=...
MAILJET_APIKEY_PRIVATE=...
RECEIVER_EMAIL=...
```

---

##### Versions
- 1.6.0 Send email from cron when prices change
- 1.5.0 New cron for checking product prices in background
- 1.4.0 New screen vision and cron process to validate prices
- 1.3.0 New DB hosting
- 1.2.0 New Log model integrated
- 1.1.0 Adaptations to ORM SQLAlchemy

---
##### Learning tips
- Send emails with smtplib and ssl
- Scraping web with selectorlib and BeautifulSoup
- Use MailJet as free SMTP server (mailjet-apiv3-python): https://dev.mailjet.com/
