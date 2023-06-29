from tastytrade.api import tastyAPI

class tasty:
    def __init__(self):
        self.api = tastyAPI()
        print("Logging into TastyTrade")
        self.api.get_auth()
   
    def order(self, ticker, buy, dry=False):
        print( "ordering " + ticker + " on tastytrade")
        self.api.order(ticker, dry, buy)
        
    def get_accounts(self, display=False):
        self.api.get_accounts(display)
