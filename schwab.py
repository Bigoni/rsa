from schwab_api import Schwab
import pprint
from config.secrets import secrets


class schwabAPI:
    def __init__(self):
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

    def order(self, ticker, buy, test=False):
        for key in self.account_info.keys():
            print(f"Schwab: Placing a trade for {ticker} stock in account {key}")
            if buy == True:
                messages, success = self.api.trade(
                    ticker=ticker,
                    side="Buy",
                    qty=1,
                    account_id=key,  # account number
                    # If dry_run=True, we won't place the order, we'll just verify it.
                    dry_run=test
                )
            else:
                messages, success = self.api.trade(
                    ticker=ticker,
                    side="Sell",
                    qty=1,
                    account_id=key,  # account number
                    # If dry_run=True, we won't place the order, we'll just verify it.
                    dry_run=test
                )
            print("The order verification was " +
                  "successful" if success else "unsuccessful")
            print("The order verification produced the following messages: ")
            pprint.pprint(messages)
