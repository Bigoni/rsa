#sys.path.append('../config')
try:
    from config.secrets import secrets
except ImportError:
    import sys
    sys.path.append(sys.path[0] + '/..')
    from config.secrets import secrets

class TastyConfig:
    use_prod: bool = False
    use_mfa: bool = False
    username: str = None
    password: str = None
    totp_secret: str = None
    cert_uri: str = None
    prod_uri: str = None
    cert_wss: str = None
    prod_wss: str = None

    def __init__(self) -> None:
        self.use_prod = True
        self.use_mfa = True
        self.username = secrets.get('tastytrade_username')
        self.password = secrets.get('tastytrade_password')
        self.totp_secret = secrets.get('tastytrade_secret')
        self.cert_uri = "https://api.cert.tastyworks.com"
        self.prod_uri = "https://api.tastyworks.com"
        self.cert_wss = "wss://streamer.cert.tastyworks.com"
        self.prod_wss = "wss://streamer.tastyworks.com"