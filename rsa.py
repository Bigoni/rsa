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

#maybe add sell logic to sell in rh also, like a new flag option
if sys.argv[1] not in {"b", "B", "s", "S"}:
    print("incorrect usage ")
    print("Usage:python rsa.py (b/s) Ticker1 Ticker2 ...")
    print("First option must be either buy (b), sell (s)")
    exit()
option = ""
buy = True
if (sys.argv[1] in {"b", "B"}):
    option = "buy"
else:
    option = "sell"
    buy = False
tickers = []
for i in range(2, len(sys.argv)):
    tickers.append(str(sys.argv[i]).upper())

tradier = tradierAPI()

for ticker in tickers:
    tradier.get_val(ticker)

cont = input(f"You will {option} one share of these tickers in all accounts, is that ok? Y/N ")
if cont not in {"Y", "y"}:
    print("Exiting")
    exit()

schwab = schwabAPI()
for ticker in tickers:
    schwab.order(ticker, buy)

print("Ordering on Tradier")
for ticker in tickers:
    tradier.order(ticker, buy)

if (option == "buy"):
    rh = robinhood.robinhood_init()
    asyncio.run(robinhood.robinhood_holdings(rh))
    for ticker in tickers: 
        asyncio.run(robinhood.robinhood_transaction(rh, option, ticker, 1, False))
else:
    print("Skipping sell on rh because it takes an extra few days to appear")

print("Ordering on TastyTrade")
print("Just starting to test this one :)")
tt = tasty()
tt.get_accounts()
for ticker in tickers:
    tt.order(ticker, buy)

print("Ordering on Firstrade")
print("This one is buggy so double check on Firstrade everything is correct")
asyncio.run(order.login_firstrade(tickers, buy))