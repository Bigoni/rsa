from schwab_api import Schwab
import pprint
from secrets import secrets


class schwabAPI:
    def __init__(self):
<<<<<<< HEAD
        # authenticate with the Tradier API
=======
>>>>>>> feat/firsttrade
        self.api = Schwab()
        # Login using playwright
        print("Logging into Schwab")
        logged_in = self.api.login(
            username=secrets.get('schwab_username'),
            password=secrets.get('schwab_password'),
            # Get this by generating TOTP at https://itsjafer.com/#/schwab
            totp_secret=secrets.get('totp_secret')
        )
        self.account_info = self.api.get_account_info()
        pprint.pprint(self.account_info)

<<<<<<< HEAD
    def order(self, ticker):
        for key in self.account_info.keys():
            print("Placing a trade for " + ticker +
                  " stock in account " + str(key))
            messages, success = self.api.trade(
                ticker=ticker,
                side="Buy",  # or Sell
                qty=1,
                account_id=key,  # account number
                # If dry_run=True, we won't place the order, we'll just verify it.
                dry_run=False
            )
=======
    def order(self, ticker, buy):
        for key in self.account_info.keys():
            print("Placing a trade for " + ticker +
                  " stock in account " + str(key))
            if buy == True:
                messages, success = self.api.trade(
                    ticker=ticker,
                    side="Buy",  # or Sell
                    qty=1,
                    account_id=key,  # account number
                    # If dry_run=True, we won't place the order, we'll just verify it.
                    dry_run=False
                )
            else:
                messages, success = self.api.trade(
                    ticker=ticker,
                    side="Sell",  # or Sell
                    qty=1,
                    account_id=key,  # account number
                    # If dry_run=True, we won't place the order, we'll just verify it.
                    dry_run=False
                )
>>>>>>> feat/firsttrade
            print("The order verification was " +
                  "successful" if success else "unsuccessful")
            print("The order verification produced the following messages: ")
            pprint.pprint(messages)
<<<<<<< HEAD

    def sell(self, ticker):
        for key in self.account_info.keys():
            print("Placing a trade for " + ticker +
                  " stock in account " + str(key))
            messages, success = self.api.trade(
                ticker=ticker,
                side="Sell",  # or Sell
                qty=1,
                account_id=key,  # account number
                # If dry_run=True, we won't place the order, we'll just verify it.
                dry_run=False
            )
            print("The order verification was " +
                  "successful" if success else "unsuccessful")
            # print("The order verification produced the following messages: ")
            # pprint.pprint(messages)
=======
>>>>>>> feat/firsttrade
