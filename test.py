<<<<<<< HEAD
# this file is just for testing as I implement new brokers, feel free to disregard

=======
>>>>>>> 02df004c5a1ab209290af6c7d194732da5a23cc6
from tradier import tradierAPI
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
<<<<<<< HEAD
for ticker in tickers:
    tradier.get_val(ticker)
for ticker in tickers:
    if (option == "buy"):
        tradier.order(ticker, True)
    else:
        tradier.order(ticker, False)
=======
# for ticker in tickers:
# tradier.get_val(ticker)

for ticker in tickers:
    tradier.order(ticker)
>>>>>>> 02df004c5a1ab209290af6c7d194732da5a23cc6
