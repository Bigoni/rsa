from tradier import tradierAPI
from schwab import schwabAPI
from tasty import tasty
from firstrade import order
import robinhood
import asyncio
import sys
import time

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

# schwab = schwabAPI()
#for ticker in tickers:
    #schwab.order(ticker, buy)

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
tt = tasty()
tt.get_accounts()
# if you place multiple orders to the same account quickly TT considers it separate legs which isn't allowed
# Example API log:
'''
    {'error': {'code': 'preflight_check_failure', 'message': 'One or more preflight checks failed', 'errors': [{'code': 'spread_market_order_check_failed', 'message': 'Orders with 2 or more legs cannot be placed as "Market" orders.'}, {'code': 'multiple_equity_legs_invalid', 'message': 'Orders may not have multiple equity legs.'}, {'code': 'invalid_combined_option_stock_amount', 'message': 'Order contains equity leg and more than one option leg'}]}}
'''
# to try and fix this, I put a sleep, lets see if it works
# don't really need it on first iteration, should do something like i,member in enumerate(tickers)
for ticker in tickers:
    tt.order(ticker, buy)
    if (len(tickers) > 1):
        time.sleep(5)

print("Ordering on Firstrade")
print("This one is buggy so double check on Firstrade everything is correct")
asyncio.run(order.login_firstrade(tickers, buy, False))