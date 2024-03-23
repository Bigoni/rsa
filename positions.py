from tradier import tradierAPI
from schwab import schwabAPI
from tasty import tasty
from firstrade import order
import robinhood
import asyncio
import sys
import time

tradier = tradierAPI()
tradier.positions()

#currently I print during init
schwab = schwabAPI()

rh = robinhood.robinhood_init()
asyncio.run(robinhood.robinhood_holdings(rh))

#tt = tasty()
#tt.get_accounts(display=True)


#firstrade need more logic in firstrade class
#asyncio.run(order.login_firstrade(tickers, buy))