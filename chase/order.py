try:
    from config.secrets import secrets
except ImportError:
    import sys
    sys.path.append(sys.path[0] + '/..')
    from config.secrets import secrets

import urls
import asyncio
import pyotp
from playwright.async_api import Playwright, async_playwright
import time

username = secrets.get('chase_username')
password = secrets.get('chase_password')
    
async def login_chase(tickers, buy, headless=True):
    async with async_playwright() as p:
        # Launch a new browser context
        browser = await p.chromium.launch(headless=headless)
        page = await browser.new_page()

        await page.goto(urls.login())
        time.sleep(.5)
        # Fill in the login form
        #<input min="0" class="jpui input logon-xs-toggle clientSideError" id="userId-text-input-field" placeholder="" format="" aria-describedby="  userId-input-field-label aggregator-security-banner" autocomplete="username" type="text" name="userId" data-validate="userId" required="" value="">
        username_input = await page.wait_for_selector('#userId-text-input-field')
        await username_input.fill(username)
        time.sleep(2)
        #<input min="0" class="jpui input logon-xs-toggle clientSideError" id="password-text-input-field" placeholder="" format="" aria-describedby="  password-input-field-label" autocomplete="current-password" type="password" name="password" data-validate="password" required="" value="">
        #await page.get_by_label("Password").fill(password)
        password_input = await page.wait_for_selector('#password-text-input-field')
        await password_input.fill(password)

        # Click the login button
        #<button type="submit" id="signin-button" class="jpui button focus fluid primary"><span class="label">Sign in</span> </button>
        await page.get_by_role("button").click()
        time.sleep(1)

        #<div class="radiobutton-label-content">Send a notification to my phone</div>
        button_2fa = await page.wait_for_selector('.radiobutton-label-content:has-text("Send a notification to my phone")')
        time.sleep(3)
        await button_2fa.click()

        #<button type="submit" id="requestIdentificationCode-sm" class="jpui button focus fluid primary"><span class="label">Next</span> </button>
        submit_button = await page.wait_for_selector('#requestIdentificationCode-sm')
        await submit_button.click()
        #ask for input from user to confirm you did 2fa
        user_code = input("Confirm on the chase app, enter something when it's approved: ")
        time.sleep(3)
        accounts = {"Self-Directed (...1884)", "Self-Directed-Ret (...3938)"}
        for account in accounts:
            for ticker in tickers:
                print(f"Chase: ordering {ticker} in {account}")
                await page.goto(urls.order())
                time.sleep(1)
                #<a class="list-item__navigational list-item__navigational--divider" href="javascript:void(0)" aria-label="Self-Directed (...1884)"><span class="list-item__navigational-icon" aria-hidden="true" __skip="true"><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48"><path fill="inherit" d="M15.835 43.949a2.974 2.974 0 01-2.001-5.175l16.244-14.77L13.834 9.238a2.974 2.974 0 114-4.4L36.5 21.806a2.974 2.974 0 010 4.402L17.835 43.177a2.967 2.967 0 01-2 .772z"></path></svg></span></a>
                print("going to '[aria-label={account}]'")
                account_button = await page.query_selector('[aria-label="{account}"]')
                await account_button.click()
                
                #<input class="mds-text-input__input mds-text-input__input--leading-icon mds-text-input__input--line" id="symbolLookupInput-input" placeholder="Search" autocomplete="off" type="text">
                ticker_input = await page.wait_for_selector('#symbolLookupInput-input')
                await ticker_input.fill(ticker)
                time.sleep(1)
                await input_element.press('Enter')
                time.sleep(.5)
                #<a class="list-item__navigational list-item__navigational--divider" href="javascript:void(0)" aria-label="Market order"><span class="list-item__navigational-icon" aria-hidden="true" __skip="true"><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48"><path fill="inherit" d="M15.835 43.949a2.974 2.974 0 01-2.001-5.175l16.244-14.77L13.834 9.238a2.974 2.974 0 114-4.4L36.5 21.806a2.974 2.974 0 010 4.402L17.835 43.177a2.967 2.967 0 01-2 .772z"></path></svg></span></a>
                market_order = await page.query_selector('[aria-label="Market order"]')
                await market_order.click()

                #<input class="mds-text-input__input mds-text-input__input--error mds-text-input__input--hero mds-text-input__input--line" id="orderQuantity-input" placeholder="0" name="orderQuantity" autocomplete="off" type="text" aria-describedby="orderQuantity-error-text0 " aria-invalid="true">
                time.sleep(1)
                order_quantity_element = await page.query_selector('#orderQuantity-input')
                await order_quantity_element.fill('1')

                #<button type="button" class="button button--primary button--fluid" tabindex="0"><span class="button__label">Preview</span></button>
                time.sleep(.5)
                preview_button = await page.query_selector('button.button--primary')
                await preview_button.click()
                '''
                account_dropdown_button = await page.wait_for_selector('#header-accountDropDown')
                await account_dropdown_button.click()
                account_option = await page.wait_for_selector(f'#container-primary-1-accountDropDown:has-text("{account}")')
                await account_option.click()
                #<input class="mds-text-input__input mds-text-input__input--leading-icon mds-text-input__input--line" id="symbolLookupInput-input" placeholder="Search" autocomplete="off" type="text">
                ticker_input = await page.wait_for_selector('#equitySymbolLookup-block-autocomplete-validate-input-field')
                await ticker_input.fill(ticker)
                time.sleep(4)
                if buy:
                    #<label class="input-label" for="input-tradeActions-0">Buy</label>
                    buy_button = await page.wait_for_selector('.input-label:has-text("Buy")')
                    await buy_button.click()
                else:
                    #<label class="input-label" for="input-tradeActions-1">Sell</label>
                    sell_button = await page.wait_for_selector('.input-label:has-text("Sell")')
                    await sell_button.click()
                #<label class="input-label" for="input-tradeOrderTypeOptions-0">Market</label>
                market_button = await page.wait_for_selector('.input-label:has-text("Market")')
                await market_button.click()
                #<input min="0" class="jpui input error" id="tradeQuantity-text-input-field" placeholder="Enter quantity" format="" aria-invalid="true" aria-describedby="tradeQuantity-text-placeHolderAdaText  " type="tel" name="tradeQuantity" data-validate="tradeQuantity" value="">
                quantity_input_field = await page.wait_for_selector('#tradeQuantity-text-input-field')
                await quantity_input_field.fill('1')
                time.sleep(.1)
                #<label class="input-label" for="input-tradeExecutionOptions-0">Day</label>
                day_button = await page.wait_for_selector('.input-label:has-text("Day")')
                await day_button.click()
                #<button type="submit" class="button button--primary button--fluid" tabindex="0"><span class="button__label">Preview</span></button>
                #<span class="button__label">Preview</span>
                time.sleep(1)
                preview_button = await page.wait_for_selector('button.button--primary')
                await preview_button.click()
                '''
                time.sleep(10)
        time.sleep(30)
        await browser.close()

asyncio.run(login_chase({"EAST"}, True, False))