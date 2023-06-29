#remove .template from this file and add your credentials
#BE CAREFUL WITH YOUR PASSWORDS
    #I have secrets.py in the .gitignore but make sure you never share this file once edited
secrets = {
    'schwab_username': "",
    'schwab_password': "",
    'totp_secret': "",

    'tradier_token': "",

    'robinhood_username': "",
    'robinhood_password': "",
    'robinhood_secret': "",

    'vanguard_username': "",
    'vanguard_password': "",

    'fidelity_username': "",
    'fidelity_password': "",

    'firstrade_username': "",
    'firstrade_password': "",
    #Enter the 4 digit pin, in the format: "1234"
    'firstrade_pin': "",

    'tastytrade_username': "",
    #if your password has % you may need to enter %%
    'tastytrade_password': "",
    #don't think this actually works, I messed up my 2fa on tasty trade
    'tastytrade_secret': "",
}

#Enter account numbers for each account you want to order in for these brokers
tradier_accounts = ["", ""]
firstrade_accounts = ["",""]
robinhood_accounts = ["", "", ""]