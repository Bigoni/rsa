from tradier import tradierAPI
from schwab import schwabAPI
from tasty import tasty
import robinhood
import asyncio
import firstrade
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
schwab = schwabAPI()
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

print("Ordering on Firstrade")
print("Still testing this one so be careful! Double check on Firstrade everything is correct")
#I think headful is working, need to test headless
if (option == "buy"):
    #asyncio.run(firstrade.login_firstrade(tickers, True))
    print("Would be buying on firstrade now")
else:
    #asyncio.run(firstrade.login_firstrade(tickers, False))
    print("Would be selling on firstrade now")
'''

print("Ordering on TastyTrade")
tt = tasty()
tt.get_accounts(True)
for ticker in tickers:
    tt.order(ticker, True)
'''
if (option == "buy"):
    tt.order(tickers, True)
else:
    tt.order(tickers, False)
'''
'''
print("Ordering on Robinhood")   
print("Still testing so double check on Robinhood")
rh = robinhood.robinhood_init()
asyncio.run(robinhood.robinhood_holdings(rh))
if (option == "buy"):
    for ticker in tickers: 
        asyncio.run(robinhood.robinhood_transaction(rh, option, ticker, 1, False))
else:
    print("Skipping sell on rh because it takes an extra few days to appear")
'''


