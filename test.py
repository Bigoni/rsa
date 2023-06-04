<<<<<<< HEAD
from tradier import tradierAPI
import sys

=======
# this file is just for testing as I implement new brokers, feel free to disregard

from tradier import tradierAPI
from tasty import tasty
import sys
import robinhood
import asyncio

'''
>>>>>>> feat/firsttrade
if len(sys.argv) <= 2:
    print("incorrect usage ")
    print("Usage:python rsa.py (b/s) Ticker1 Ticker2 ...")
    exit()
print('Argument List:', str(sys.argv))

if sys.argv[1] not in {"b", "B", "s", "S"}:
    print("incorrect usage ")
    print("Usage:python rsa.py (b/s) Ticker1 Ticker2 ...")
    print("First option must be either buy (b) or sell (s)")
    exit()
option = ""
if (sys.argv[1] in {"b", "B"}):
    option = "buy"
else:
    option = "sell"
tickers = []
for i in range(2, len(sys.argv)):
    tickers.append(str(sys.argv[i]))

tradier = tradierAPI()
<<<<<<< HEAD
# for ticker in tickers:
# tradier.get_val(ticker)

for ticker in tickers:
    tradier.order(ticker)
=======
for ticker in tickers:
    tradier.get_val(ticker)
for ticker in tickers:
    if (option == "buy"):
        tradier.order(ticker, True)
    else:
        tradier.order(ticker, False)
'''

'''
rh = robinhood.robinhood_init()
asyncio.run(robinhood.robinhood_holdings(rh))
asyncio.run(robinhood.robinhood_transaction(rh, "buy", "ACOR", 1, False))
'''

tt = tasty()
>>>>>>> feat/firsttrade
