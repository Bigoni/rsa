import json, requests
import pyotp
from .TTConfig import *
from .order import *

class Api:
    session_token: str = None
    remember_token: str = None
    streamer_token: str = None
    streamer_uri: str = None
    streamer_websocket_uri: str = None
    streamer_level: str = None
    tt_uri: str = None
    wss_uri: str = None
    headers: dict = {}
    user_data: dict = {}
    use_prod: bool = False
    use_mfa: bool = False

    def __init__(self, tt_config: TTConfig = TTConfig()) -> None:
        self.headers["Content-Type"] = "application/json"
        self.headers["Accept"] = "application/json"
        self.tt_config = tt_config

        if self.tt_config.use_prod:
            self.tt_uri = self.tt_config.prod_uri
            self.tt_wss = self.tt_config.prod_wss
        else:
            self.tt_uri = self.tt_config.cert_uri
            self.tt_wss = self.tt_config.prod_wss

    def __post(
        self, endpoint: str = None, body: dict = {}, headers: dict = None
    ) -> requests.Response:
        if headers is None:
            headers = self.headers
        response = requests.post(
            self.tt_uri + endpoint, data=json.dumps(body), headers=headers
        )
        if response.status_code == 201:
            return response.json()
        print(f"Error {response.status_code}")
        print(f"Endpoint: {endpoint}")
        print(f"Body: {body}")
        print(f"Headers: {headers}")
        print(f"Response: {response.text}")
        return None

    def __get(
        self, endpoint, body: dict = {}, headers: dict = None, params: dict = {}
    ) -> requests.Response:
        if headers is None:
            headers = self.headers
        response = requests.get(
            self.tt_uri + endpoint,
            data=json.dumps(body),
            headers=headers,
            params=params,
        )
        if response.status_code == 200:
            return response.json()
        print(f"Error {response.status_code}")
        print(f"Endpoint: {endpoint}")
        print(f"Body: {body}")
        print(f"Headers: {headers}")
        print(f"Response: {response.text}")
        return None

    def __delete(
        self, endpoint: str = None, body: dict = {}, headers: dict = None
    ) -> requests.Response:
        if headers is None:
            headers = self.headers
        response = requests.delete(
            self.tt_uri + endpoint, data=json.dumps(body), headers=headers
        )
        if response.status_code == 204:
            return response
        print(f"Error {response.status_code}")
        print(f"Endpoint: {endpoint}")
        print(f"Body: {body}")
        print(f"Headers: {headers}")
        print(f"Response: {response.text}")
        return None

    def login(self) -> bool:
        body = {
            "login": self.tt_config.username,
            "password": self.tt_config.password,
            "remember-me": True,
        }

        if self.tt_config.use_mfa is True:
            if self.tt_config.totp_secret == "":
                mfa = input("MFA: ")
            else:
                #this is actually messed up slightly for now, need to contact support
                mfa = str(pyotp.TOTP(self.tt_config.totp_secret).now())
            self.headers["X-Tastyworks-OTP"] = mfa

        response = self.__post("/sessions", body=body)
        if response is None:
            return False

        self.user_data = response["data"]["user"]
        self.session_token = response["data"]["session-token"]
        self.headers["Authorization"] = self.session_token

        if self.tt_config.use_mfa is True:
            del self.headers["X-Tastyworks-OTP"]

        return True

    def logout(self) -> bool:
        self.__delete("/sessions")
        return True

    def validate(self) -> bool:
        response = self.__post("/sessions/validate")

        if response is None:
            return False

        self.user_data["external-id"] = response["data"]["external-id"]
        self.user_data["id"] = response["data"]["id"]

        return True

    def fetch_accounts(self) -> bool:
        response = self.__get("/customers/me/accounts")

        if response is None:
            return False

        self.user_data["accounts"] = []
        for account in response["data"]["items"]:
            self.user_data["accounts"].append(account)

        return True

    def market_metrics(self, symbols: list[str] = []) -> any:
        symbols = ",".join(str(x) for x in symbols)
        query = {"symbols": symbols}
        response = self.__get(f"/market-metrics", params=query)
        return response

    def simple_order(self, ticker, buy) -> bool:
        order = TTOrder() 
        body=order.build_simple_order(ticker, buy)
        
        for account in self.user_data["accounts"]:
            response = self.__post(
                f'/accounts/{account["account"]["account-number"]}/orders/dry-run',
                body,
            )

            if response is None:
                print("Error ordering on tastytrade account " + account["account"]["account-number"])

        print(json.dumps(response))
        return True