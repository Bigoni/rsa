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

if sys.argv[1] not in {"b", "B", "s", "S", "sl"}:
    print("incorrect usage ")
    print("Usage:python rsa.py (b/s) Ticker1 Ticker2 ...")
    print("First option must be either buy (b), sell (s) or sell limit(sl)")
    exit()
option = ""
buy = True
if (sys.argv[1] in {"b", "B"}):
    option = "buy"
elif (sys.argv[1] in {"sl", "SL"}):
    option = "sell limit"
else:
    option = "sell"
    buy = False
tickers = []
use_robinhood = false
price = 0.0
if option == "sell limit":
    print(option)
    try:
        price = float(sys.argv[2])
    except:
        print("for sell limit argv[2] must be parceable as a float")
    for i in range(3, len(sys.argv)):
        tickers.append(str(sys.argv[i]).upper())
    print(f"price: {price}")
    #print("haven't finished implementing limit orders yet")
    #exit()
else:
    for i in range(2, len(sys.argv)):
        tickers.append(str(sys.argv[i]).upper())

tradier = tradierAPI()

for ticker in tickers:
    tradier.get_val(ticker)

cont = input(f"You will {option} one share of these tickers in all accounts, is that ok? Y/N ")
if cont not in {"Y", "y"}:
    print("Exiting")
    exit()

#this dependency doesn't support limit orders, maybe will implement it later
schwab = schwabAPI()
print("Will just be placing market orders on Schwab")
for ticker in tickers:
    schwab.order(ticker, buy)

print("Ordering on Tradier")
for ticker in tickers:
    tradier.limit_order(ticker, buy, price)


#gonna skip sell on rh, maybe implement logic later
if(use_robinhood):
    rh = robinhood.robinhood_init()
    asyncio.run(robinhood.robinhood_holdings(rh))
    for ticker in tickers:
        asyncio.run(robinhood.robinhood_transaction(rh, option, ticker, 1, False))
    #print("Skipping sell on rh because it takes an extra few days to appear")


print("Ordering on TastyTrade")
tt = tasty()
tt.get_accounts()
for ticker in tickers:
    tt.order(ticker, buy, False, False, price)

#not gonna bother with limit orders on this for now
#will be some different playwright logic
print("Ordering on Firstrade, just doing Market orders")
print("This one is buggy so double check on Firstrade everything is correct")
asyncio.run(order.login_firstrade(tickers, buy))
