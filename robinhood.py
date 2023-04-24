import robin_stocks.robinhood as r
from secrets import secrets

login = r.login(secrets.robinhood_username, secrets.robinhood_password)
