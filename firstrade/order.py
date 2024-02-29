try:
    from config.secrets import secrets
    from config.secrets import firstrade_accounts
except ImportError:
    import sys
    sys.path.append(sys.path[0] + '/..')
    from config.secrets import secrets
    from config.secrets import firstrade_accounts

from .urls import *
import asyncio
import pyotp
from playwright.async_api import Playwright, async_playwright
import time


username = secrets.get('firstrade_username')
password = secrets.get('firstrade_password')
pin = secrets.get('firstrade_pin')
accounts = firstrade_accounts

#TODO optimize the sleeps I use
#I probably have like 10x the amount of sleeps I need lol
    #probably should figure out how something like wait for selector works in playwright

#headless mode is buggy sometimes so maybe use headful mode to debug
async def login_firstrade(tickers, buy, headless=True):
    async with async_playwright() as p:
        # Launch a new browser context
        browser = await p.chromium.launch(headless=headless)
        page = await browser.new_page()

        await page.goto(login())

        # Fill in the login form
        await page.get_by_label("User ID").fill(username)
        await page.get_by_label("Password").fill(password)
   
        # Click the login button
        await page.get_by_role("button").click()
        time.sleep(1)

        # Click verify another way
        await page.click(".text-azure")
        time.sleep(1)

        # <input type="password" title="PIN" name="pin" id="pin" data-msg-minlength="Please enter 4 digits." class="h-11 w-full border border-slate-300 border-solid rounded text-zinc-700 bg-transparent flex px-2 py-1.5 transition-colors placeholder:text-gray-700 placeholder:opacity-50 outline-none text-sm" required="" minlength="4" maxlength="4" data-mask="0000" autocomplete="off">
        await page.get_by_title("PIN").fill(pin)
        # <button type="submit" class="w-full h-12 px-4 py-3 bg-azure rounded justify-center items-center flex text-center text-white text-base font-bold leading-snug border-0 cursor-pointer hover:opacity-90 disabled:pointer-events-none disabled:opacity-50">Continue</button>
        time.sleep(1)
        await page.click(".bg-azure")

        
        '''
        old 2fa form
        # Wait for the dashboard to load
        for digit in str(pin):
            await page.get_by_title(digit).click()

        #<div class="keypad" id="submit"></div>
        await page.click("#submit.keypad")
        '''

        time.sleep(1)

        for ticker in tickers:
            for account in accounts:
                await page.goto(order())

                #select account
                await page.select_option("#accountId1", value=account)

                # Find the element to click
                element = await page.query_selector("#transactionType_Buy1")

                time.sleep(1)
                if buy:
                    await page.click("#transactionType_Buy1")
                else:
                    await page.click("#transactionType_Sell1")
                time.sleep(1)
                await page.fill("#quantity1", "1")
                time.sleep(1)
                await page.fill("#symbol1", ticker)
                time.sleep(1)
                await page.keyboard.press("Enter")
                time.sleep(2)
                #<a class="send btn btn-action" name="submitOrder" id="submitOrder1" href="javascript:void(0);">Send Order</a>
                await page.click("#submitOrder1")
                time.sleep(.5)

        await browser.close()