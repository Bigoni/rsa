import sys
import traceback
import robin_stocks.robinhood as rh
from time import sleep
import pprint
import pyotp
from dotenv import load_dotenv

from config.secrets import secrets
from config.secrets import robinhood_accounts

def robinhood_init():
    # Initialize .env file
    load_dotenv()
    # Import Robinhood account
    if not secrets.get("robinhood_username") or not secrets.get("robinhood_password"):
        print("Robinhood not found, skipping...")
        return None
    RH_USERNAME = secrets.get("robinhood_username")
    RH_PASSWORD = secrets.get("robinhood_password")
    if secrets.get("robinhood_secret") and secrets.get("robinhood_secret")!= "":
        RH_TOTP = secrets.get("robinhood_secret")
        totp = pyotp.TOTP(RH_TOTP).now()
    else:
        totp = None
    # Log in to Robinhood account
    print("Logging in to Robinhood...")
    try:
        if not totp:
            rh.login(RH_USERNAME, RH_PASSWORD)
        else:
            print("Using Robinhood TOTP")
            rh.login(RH_USERNAME, RH_PASSWORD, mfa_code=totp)
    except Exception as e:
        print(f"Error: Unable to log in to Robinhood: {e}")
        return None
    print("Logged in to Robinhood!")
    return rh

async def robinhood_holdings(rh, ctx=None):
    print()
    print("==============================")
    print("Robinhood Holdings")
    print("==============================")
    print()
    # Make sure init didn't return None
    if rh is None:
        print("Error: No Robinhood account")
        return None
    try:
        # Get account holdings
        positions = rh.get_open_stock_positions()
        if positions == []:
            print("No holdings in Robinhood")
            if ctx:
                await ctx.send("No holdings in Robinhood")
        else:
            print("Holdings in Robinhood:")
            if ctx:
                await ctx.send("Holdings in Robinhood:")
            for item in positions:
                # Get symbol, quantity, price, and total value
                sym = item['symbol'] = rh.get_symbol_by_url(item['instrument'])
                qty = float(item['quantity'])
                try:
                    current_price = round(float(rh.stocks.get_latest_price(sym)[0]), 2)
                    total_value = round(qty * current_price, 2)
                except TypeError as e:
                    if "NoneType" in str(e):
                        current_price = "N/A"
                        total_value = "N/A"
                print(f"{sym}: {qty} @ ${(current_price)} = ${total_value}")
                if ctx:
                    await ctx.send(f"{sym}: {qty} @ ${(current_price)} = ${total_value}")
    except Exception as e:
        print(f'Robinhood: Error getting account holdings: {e}')
        print(traceback.format_exc())
        if ctx:
            await ctx.send(f'Robinhood: Error getting account holdings: {e}')

async def robinhood_transaction(rh, action, stock, amount, DRY=True, ctx=None):
    print()
    print("==============================")
    print("Robinhood")
    print("==============================")
    print()
    accounts = robinhood_accounts
    action = action.lower()
    stock = stock.upper()
    if amount == "all" and action == "sell":
        all_amount = True
    elif amount < 1:
        amount = float(amount)
    else:
        amount = int(amount)
        all_amount = False
    # Make sure init didn't return None
    if rh is None:
        print("Error: No Robinhood account")
        return None
    if not DRY:
        try:
            # Buy Market order
            if action == "buy":
                #rh.order_buy_market(stock, amount)
                extendedHours=False
                jsonify=True
                for account in accounts:
                    #probably can just do first 4 args and not worry about rest, test after this
                    #order(symbol, quantity, side, account_number=None, limitPrice=None, stopPrice=None, timeInForce='gtc', extendedHours=False, jsonify=True)
                    rh.order(stock, amount, "buy", account)
                    print(f"Robinhood: Bought {amount} of {stock} in {account}")
                if ctx:
                    await ctx.send(f"Robinhood: Bought {amount} of {stock}")
            # Sell Market order
            elif action == "sell":
                if all_amount:
                    # Get account holdings
                    positions = rh.get_open_stock_positions()
                    for item in positions:
                        sym = item['symbol'] = rh.get_symbol_by_url(item['instrument'])
                        if sym.upper() == stock:
                            amount = float(item['quantity'])
                            break
                rh.order_sell_market(stock, amount)
                print(f"Robinhood: Sold {amount} of {stock}")
                if ctx:
                    await ctx.send(f"Robinhood: Sold {amount} of {stock}")
            else:
                print("Error: Invalid action")
                return None
        except Exception as e:
            print(f'Robinhood: Error submitting order: {e}')
            if ctx:
                await ctx.send(f'Robinhood: Error submitting order: {e}')
    else:
        print(f"Robinhood: Running in DRY mode. Transaction would've been: {action} {amount} of {stock}")
        if ctx:
            await ctx.send(f"Robinhood: Running in DRY mode. Transaction would've been: {action} {amount} of {stock}")
