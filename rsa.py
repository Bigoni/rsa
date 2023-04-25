from tradier import tradierAPI
from schwab import schwabAPI
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
    tickers.append(str(sys.argv[i]))

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
        schwab.order(ticker, True)
    else:
        schwab.order(ticker, False)

print("Ordering on Tradier")
for ticker in tickers:
    if (option == "buy"):
        tradier.order(ticker, True)
    else:
        tradier.order(ticker, False)
