from tastytrade import *

class tasty:
    def __init__(self):
        self.api = api.TTApi()
        # Login using playwright
        print("Logging into TastyTrade")

    def order(self, ticker, buy):
        print( "ordering" + ticker + " on tastytrade")