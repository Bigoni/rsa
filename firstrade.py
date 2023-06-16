from config.secrets import secrets
from config.secrets import firstrade_accounts
from firsttrade import urls
import asyncio
import pyotp
from playwright.async_api import Playwright, async_playwright
import time


username = secrets.get('firstrade_username')
password = secrets.get('firstrade_password')
pin = secrets.get('firstrade_pin')
accounts = firstrade_accounts

#TODO optimize the sleeps I use
#I probably have like 10x the amount of sleeps I need haha
    #probably should figure out how something like wait for selector would work in playwright
    
async def login_firstrade(tickers, buy, head=True):
    async with async_playwright() as p:
        # Launch a new browser context
        browser = await p.chromium.launch(headless=head)
        page = await browser.new_page()

        await page.goto(urls.login())

        # Fill in the login form
        await page.get_by_label("User ID").fill(username)
        await page.get_by_label("Password").fill(password)
   
        # Click the login button
        await page.get_by_role("button").click()
        time.sleep(1)

        # Wait for the dashboard to load
        for digit in str(pin):
            await page.get_by_title(digit).click()

        #<div class="keypad" id="submit"></div>
        await page.click("#submit.keypad")

        time.sleep(1)

        for ticker in tickers:
            for account in accounts:
                await page.goto(urls.order())

                #select account
                #<select id="accountId1" name="accountId" value=""><option selected="" value="87848537">87848537</option><option value="91297538">91297538</option></select>
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

# Example usage: log in to Firstrade and order SEAC
#tickers = ["SEAC"]
#buy = True
#asyncio.run(login_firstrade(tickers, buy))