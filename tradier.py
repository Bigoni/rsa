from secrets import secrets
from PyTradier.pytradier import Tradier

# tradier = Tradier(token=secrets.get('tradier_token'), account_id=secrets.get('tradier_account_id'), endpoint='brokerage')

# git submodule add https://github.com/rleonard21/PyTradier.git PyTradier


class tradierAPI:
    def __init__(self):
        # authenticate with the Tradier API
        self.tradier = Tradier(token=secrets.get('tradier_token'), account_id=secrets.get(
            'tradier_account_id'), endpoint='brokerage')

    def get_val(self, ticker):
        # create an instance of the stock class with ticker we want to buy
        stocks = self.tradier.stock(ticker)
        # and print the current ask price:
        print("Ask: " + str(stocks.ask()))
        print("Bid: " + str(stocks.bid()))

    def order(self, ticker):
        # orders = self.tradier.account().orders()
        # order = self.tradier.order().create(duration="day", side="buy", quantity=1, _type="market", price=None, stop=None,
        #       option_symbol=None, symbol=ticker, preview=False)
        # self.tradier.account().orders()
        """ Submit an order.
        :param limit_price: The limit price, or list of limit prices
            for multileg orders. Required for any limit or stop-limit
            order legs and for debit or credit orders.
        :param stop_price: The stop price, or list of stop prices for
            multileg orders. Required only for stop and stop-limit
            order legs.
        :param tag: User identifier for this order, maximum length of
            255 characters containing only letters, numbers and ``-``.
        :param option: Overrides deduction of order kind (option vs
            equity) based on the symbol. Only ever necessary if orders
            are not being correctly identified automatically.
        """
        self.tradier.Order.submit_order(order_class="equity", symbol="ticker", side="buy",
                                        qty=1, order_type="market", time_in_force="day",)

    def validateAccount(self):
        account = tradier.account()
        print(account.balance().cash_available())
