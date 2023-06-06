import sys

sys.path.append('../secrets')

from secrets import secrets

class TTConfig:
    config: configparser.ConfigParser = configparser.ConfigParser()
    use_prod: bool = False
    use_mfa: bool = False
    username: str = None
    password: str = None
    cert_uri: str = None
    prod_uri: str = None
    cert_wss: str = None
    prod_wss: str = None

    def __init__(self, path: str = "./config", filename: str = "tt.config") -> None:
        self.config.read(f"{path}/{filename}")
        self.use_prod = True
        self.use_mfa = True
        self.username = secrets.get('tastytrade_username')
        self.password = secrets.get('tastytrade_password')
        self.cert_uri = "https://api.cert.tastyworks.com"
        self.prod_uri = "https://api.tastyworks.com"
        self.cert_wss = "wss://streamer.cert.tastyworks.com"
        self.prod_wss = "wss://streamer.tastyworks.com"