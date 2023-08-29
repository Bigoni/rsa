from config.secrets import secrets
from config.secrets import tradier_accounts
import requests
import json


class tradierAPI:
    def get_auth(self):
        response = requests.get('https://api.tradier.com/v1/oauth/authorize',
                                params={'client_id': secrets.get('tradier_token'),
                                        'scope': 'read, write, trade, market',
                                        'state': 'rsa_gen_1234'}
                                )
        json_response = response.json()

    def get_val(self, ticker):
        url = "{}markets/quotes".format("https://api.tradier.com/v1/")

        headers = {
            'Authorization': 'Bearer {}'.format(secrets.get('tradier_token')),
            'Accept': 'application/json'
        }

        response = requests.get(url,
                                params={'symbols': ticker},
                                headers=headers
                                )

        fmt = (response.json())
        print(fmt.get('quotes').get('quote').get('symbol') +
              " Bid: " + str(fmt.get('quotes').get('quote').get('bid')))
        print(fmt.get('quotes').get('quote').get('symbol') +
              " Ask: " + str(fmt.get('quotes').get('quote').get('ask')))

    def order(self, ticker, buy):
        #new version, using multiple accounts functionality
        for account in tradier_accounts:
            url = '{}accounts/{}/orders'.format(
                "https://api.tradier.com/v1/", account)

            headers = {
                'Authorization': 'Bearer {}'.format(secrets.get('tradier_token')),
                'Accept': 'application/json'
            }
            if (buy == True):
                print("Buying " + ticker + " in account " +
                    account + " on Tradier")
                response = requests.post(url,
                                        data={'class': 'equity', 'symbol': ticker,
                                            'side': 'buy', 'quantity': '1', 'type': 'market', 'duration': 'day'},
                                        headers=headers
                                        )
            else:
                print("Selling " + ticker + " in account " +
                    account + " on Tradier")
                response = requests.post(url,
                                        data={'class': 'equity', 'symbol': ticker,
                                            'side': 'sell', 'quantity': '1', 'type': 'market', 'duration': 'day'},
                                        headers=headers
                                        )

    def limit_order(self, ticker, buy, price):
        #new version, using multiple accounts functionality
        for account in tradier_accounts:
            url = '{}accounts/{}/orders'.format(
                "https://api.tradier.com/v1/", account)

            headers = {
                'Authorization': 'Bearer {}'.format(secrets.get('tradier_token')),
                'Accept': 'application/json'
            }
            if (buy == True):
                print("Buying " + ticker + " in account " +
                    account + " on Tradier")
                response = requests.post(url,
                                        data={'class': 'equity', 'symbol': ticker,
                                            'side': 'buy', 'quantity': '1', 'type': 'limit','price' :price,
                                            'duration': 'day'},
                                        headers=headers
                                        )
            else:
                print("Selling " + ticker + " in account " +
                    account + " on Tradier")
                response = requests.post(url,
                                        data={'class': 'equity', 'symbol': ticker,
                                            'side': 'sell', 'quantity': '1', 'type': 'limit','price':price,
                                            'duration': 'day'},
                                        headers=headers
                                        )