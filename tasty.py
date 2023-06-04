from secrets import secrets
from decimal import Decimal

from tastytrade.session import Session
from tastytrade.account import Account
from tastytrade.instruments import Equity
from tastytrade.order import NewOrder, OrderAction, OrderTimeInForce, OrderType, PriceEffect

class tasty:
    def __init__(self):
        username = secrets.get('tastytrade_username')
        password = secrets.get('tastytrade_password')

        self.session = Session(username, password)
        session = Session(username, password)
        self.accounts = Account.get_accounts(session)
        account = Account.get_accounts(session)[0]
        for account in self.accounts:
            print(account.account_number)
        positions = account.get_positions(session)
        #print(positions[0])

    def order(self, tickers, buy):
        for ticker in tickers:
            for account in self.accounts:
                if buy == True:
                    print("Buying " + ticker +
                    " stock in account " + str(account.account_number) + " on tastytrade")
                    symbol = Equity.get_equity(self.session, ticker)
                    leg = symbol.build_leg(Decimal('1'), OrderAction.BUY_TO_OPEN)  # buy to open 1 share
                    order = NewOrder(
                    time_in_force=OrderTimeInForce.DAY,
                    order_type=OrderType.MARKET,
                    legs=[leg],  # you can have multiple legs in an order
                    price_effect=PriceEffect.DEBIT
                    )
                    response = account.place_order(self.session, order, dry_run=False)  # a test order
                    print(response)
                else:
                    print("Selling " + ticker +
                    " stock in account " + str(account.account_number) + " on tastytrade")
                    symbol = Equity.get_equity(self.session, ticker)
                    leg = symbol.build_leg(Decimal('1'), OrderAction.SELL_TO_CLOSE)  # sell to close 1 share
                    order = NewOrder(
                    time_in_force=OrderTimeInForce.DAY,
                    order_type=OrderType.MARKET,
                    legs=[leg],  # you can have multiple legs in an order
                    price_effect=PriceEffect.CREDIT
                    )
                    response = account.place_order(self.session, order, dry_run=False)  # a test order
                    print(response)