from tradier import tradierAPI
from schwab import schwabAPI
from tasty import tasty
from firstrade import order
import robinhood
import asyncio
import sys


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
    tickers.append(str(sys.argv[i]).upper())

tradier = tradierAPI()
for ticker in tickers:
    tradier.get_val(ticker)

cont = input("You will " + option +
             " one share of these tickers in all accounts, is that ok? Y/N ")
if cont not in {"Y", "y"}:
    print("Exiting")
    exit()
'''
#schwab = schwabAPI()

for ticker in tickers:
    if (option == "buy"):
        schwab.order(ticker, True, True)
    else:
        schwab.order(ticker, False, True)

print("Ordering on Tradier")
for ticker in tickers:
    if (option == "buy"):
        #tradier.order(ticker, True)
        print("Would be buying on Tradier now")
    else:
        #tradier.order(ticker, False)
        print("Would be selling on Tradier now")
'''
print("Ordering on Firstrade")
print("Still testing this one so be careful! Double check on Firstrade everything is correct")
#I think headful is working, need to test headless
if (option == "buy"):
    asyncio.run(order.login_firstrade(tickers, True, False))
    #print("Would be buying on firstrade now")
else:
    asyncio.run(order.login_firstrade(tickers, False, False))
    #print("Would be selling on firstrade now")

'''

for ticker in tickers:
    tt.order(ticker, True)

if (option == "buy"):
    tt.order(tickers, True)
else:
    tt.order(tickers, False)
'''

'''
print("Robinhood")   
rh = robinhood.robinhood_init()
asyncio.run(robinhood.robinhood_holdings(rh))
#asyncio.run(robinhood.robinhood_transaction(rh, "buy", "BBLG", 1, False) )
'''

#tickers = ["BOXL", "ATIP"]
#asyncio.run(firstrade.login_firstrade(tickers, False, False))