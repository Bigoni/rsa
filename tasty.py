from tastytrade.api import tastyAPI

#I've realized this class is useless
#should just do all this in my rsa/test file
class tasty:
    def __init__(self):
        self.api = tastyAPI()
        print("Logging into TastyTrade")
        self.api.get_auth()
   
    def order(self, ticker, buy, dry=False, market=True, price=None):
        if buy:
            print("Buying " + ticker + " on tastytrade")
        else:
            print("Selling " + ticker + " on tastytrade")
        self.api.order(ticker, dry, buy, market, price)
        
    def get_accounts(self, display=False):
        self.api.get_accounts(display)
