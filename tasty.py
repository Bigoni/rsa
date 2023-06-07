from tastytrade import api
from tastytrade import order

class tasty:
    def __init__(self):
        self.api = api.Api()
        # Login using playwright
        print("Logging into TastyTrade")
        logged_in = self.api.login()
        if not logged_in:
            print("error logging in on tastytrade")

    def order(self, ticker, buy):
        print( "ordering " + ticker + " on tastytrade")
        self.api.simple_order(ticker, buy)

        
    def get_accounts(self, display=False):
        got = self.api.fetch_accounts()
        if not got:
            print("Error fetching tastytrade accounts")
        else:
            if display:
                for account in self.api.user_data["accounts"]:
                    print (account["account"]["account-number"])

