from tradier import tradierAPI
from schwab import schwabAPI
<<<<<<< HEAD
=======
from tasty import tasty
import robinhood
import asyncio
import firstrade
>>>>>>> feat/firsttrade
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
<<<<<<< HEAD
    tickers.append(str(sys.argv[i]))
=======
    tickers.append(str(sys.argv[i]).upper())
>>>>>>> feat/firsttrade

tradier = tradierAPI()
for ticker in tickers:
    tradier.get_val(ticker)

cont = input("You will " + option +
             " one share of these tickers in all accounts, is that ok? Y/N ")
if cont not in {"Y", "y"}:
    print("Exiting")
    exit()

schwab = schwabAPI()
for ticker in tickers:
    if (option == "buy"):
<<<<<<< HEAD
        schwab.order(ticker)
    else:
        schwab.sell(ticker)

# This dependency I used doesn't actually have this functionality lmao
# tradier.order(ticker)
=======
        schwab.order(ticker, True)
    else:
        schwab.order(ticker, False)

print("Ordering on Tradier")
for ticker in tickers:
    if (option == "buy"):
        tradier.order(ticker, True)
    else:
        tradier.order(ticker, False)

print("Ordering on Firstrade")
print("Still testing this one so be careful! Double check on Firstrade everything is correct")
#I think headful is working, need to test headless
if (option == "buy"):
    asyncio.run(firstrade.login_firstrade(tickers, True))
else:
    asyncio.run(firstrade.login_firstrade(tickers, False))

'''
print("Ordering on TastyTrade")
print("I havent tested this yet but fuck it")
tt = tasty()
if (option == "buy"):
    tt.order(tickers, True)
else:
    tt.order(tickers, False)

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
>>>>>>> feat/firsttrade
