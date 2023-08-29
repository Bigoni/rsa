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
        time.sleep(1)
        accounts = {"Self-Directed (...1884)", "Self-Directed-Ret (...3938)"}
        for account in accounts:
            for ticker in tickers:
                print(f"Chase: ordering {ticker} in {account}")
                await page.goto(urls.order())
                #<input type="button" id="header-accountDropDown" name="" form="" class="jpui input header focus-on-header wrap right text-float-left account-dropDown-styled-select" aria-haspopup="true" aria-disabled="false" aria-expanded="true" aria-label="  Filter by account, updates content below: Select Account" value="Select Account">
                #<ul class="list" id="ul-list-container-accountDropDown" role="listbox"><li role="presentation"><a class="option js-option STYLED_SELECT" id="container-0-accountDropDown" href="javascript:void(0);" rel="" role="option" aria-setsize="4" aria-posinset="1" tabindex="0"><span class="primary" id="container-primary-0-accountDropDown">Select Account</span><span class="secondary" id="container-secondary-0-accountDropDown"> </span><span class="util accessible-text" id="option-accessible-0-accountDropDown">   </span></a></li><li role="presentation"><a class="option js-option STYLED_SELECT" id="container-1-accountDropDown" href="javascript:void(0);" rel="" role="option" aria-setsize="4" aria-posinset="2" tabindex="0"><span class="primary" id="container-primary-1-accountDropDown">Self-Directed (...1884)</span><span class="secondary" id="container-secondary-1-accountDropDown"> </span><span class="util accessible-text" id="option-accessible-1-accountDropDown">   </span></a></li><li role="presentation"><a class="option js-option STYLED_SELECT" id="container-2-accountDropDown" href="javascript:void(0);" rel="" role="option" aria-setsize="4" aria-posinset="3" tabindex="0"><span class="primary" id="container-primary-2-accountDropDown">Self-Directed-Ret (...3938)</span><span class="secondary" id="container-secondary-2-accountDropDown"> </span><span class="util accessible-text" id="option-accessible-2-accountDropDown">   </span></a></li><li role="presentation"><a class="option js-option STYLED_SELECT" id="container-3-accountDropDown" href="javascript:void(0);" rel="" role="option" aria-setsize="4" aria-posinset="4" tabindex="0"><span class="primary" id="container-primary-3-accountDropDown">Self-Directed-Ret (...9399)</span><span class="secondary" id="container-secondary-3-accountDropDown"> </span><span class="util accessible-text" id="option-accessible-3-accountDropDown">   , you've reached the end of the menu</span></a></li></ul>
                time.sleep(1)
                account_dropdown_button = await page.wait_for_selector('#header-accountDropDown')
                await account_dropdown_button.click()
                account_option = await page.wait_for_selector(f'#container-primary-1-accountDropDown:has-text("{account}")')
                await account_option.click()
                #<input min="0" class="jpui input validation__error" id="equitySymbolLookup-block-autocomplete-validate-input-field" placeholder="Get a quote" format="" aria-describedby="equitySymbolLookup-block-autocomplete-validate-placeHolderAdaText" autocomplete="off" type="text" value="" aria-invalid="true">
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
                time.sleep(10)
        time.sleep(30)
        await browser.close()

asyncio.run(login_chase({"EAST"}, True, False))