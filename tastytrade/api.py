from .TastyConfig import TastyConfig
import requests
import json

__base_url__="https://api.tastyworks.com"
__sessions__="/sessions"
__accounts__="/customers/me/accounts"
__order_endpoint__="/accounts/{account_number}/orders"
__dry__ = "/dry-run"

class tastyAPI:
    headers: dict = {}
    legs: list = []

    def __init__(self):
        conf = TastyConfig()
        conf.__init__()
        self.conf = conf
        self.headers["Content-Type"] = "application/json"
        self.headers["Accept"] = "application/json"
        self.accounts = []

    def get_auth(self):
        response = requests.post(__base_url__ + __sessions__,
                                params={'login': self.conf.username,
                                        'password':self.conf.password},
                                headers = self.headers
                                )
        json_response = response.json()
        self.user_data = json_response["data"]["user"]
        self.session_token = json_response["data"]["session-token"]
        self.headers["Authorization"] = self.session_token
        
    def validate(self):
        url = __base_url__+"/sessions/validate"

        response = requests.post(url, headers=self.headers)

        print(response)
        print(response.json())


    def get_accounts(self, display=False):
        response = requests.get(__base_url__ + __accounts__,
                                headers = self.headers)
        json_response = response.json()
        #print(json_response)
        for account in json_response["data"]['items']:
            self.accounts.append(account['account']['account-number'])
            if display:
                print(account['account']['account-number'])

    #might implement limit order logic later
    def order(self, ticker, dry=True, buy=True, market=True, price=None):
        action = 'Buy to Open'
        effect = 'Debit'
        if not buy:
            action = 'Sell to Close'
            effect = 'Credit'
        #could have multiple ticker logic to limit API calls, not worth implementing now
        self.legs.append({'instrument-type': 'Equity','symbol': ticker,
                            'quantity': 1, 'action': action})
        for account in self.accounts:
            if dry:
                print(f"TastyTrade: Dry {action} {ticker} in {account} ")
                endpoint = __order_endpoint__.format(account_number=account)+__dry__
                order_data = {
                    'time-in-force': 'Day',
                    'order-type': 'Market',
                    'price-effect': effect,
                    'legs': self.legs
                }
                #print(order_data)
                response = requests.post(__base_url__ + endpoint, 
                    json=order_data,
                    headers = self.headers)
                #print(response)
                #print(response.json())
                #could check if status is 201
            else:
                print(f"TastyTrade: {action} {ticker} in {account} ")
                endpoint = __order_endpoint__.format(account_number=account)
                if market:
                    order_data = {
                        "time-in-force": "Day",
                        "order-type": "Market",
                        "price-effect": effect,
                        "legs": self.legs
                    }
                else:
                    order_data = {
                        "time-in-force": "Day",
                        "order-type": "Limit",
                        "price": price,
                        "price-effect": effect,
                        "legs": self.legs
                    }
                response = requests.post(__base_url__ + endpoint, 
                    json=order_data,
                    headers = self.headers)
                #print(response)
                #print(response.json())