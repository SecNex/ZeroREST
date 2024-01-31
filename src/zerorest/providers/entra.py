from ..http import HTTPClient
from ..auth import InteractiveProvider, BearerAuthentication

import base64
import string
import random

class Entra:
    def __init__(self, tenant: str, client: tuple, scope: str, token_url: str = None, authorization_url: str = None, open: bool = True):
        self.tenant = tenant
        self.client_id = client[0]
        self.client_secret = client[1]
        self.scope = scope
        self.token_url = token_url
        self.authorization_url = authorization_url
        self.__check_urls()
        self.provider = None
        self.client = None
        self.open = open
    
    def __check_urls(self):
        if not self.token_url:
            self.token_url = f"https://login.microsoftonline.com/{self.tenant}/oauth2/v2.0/token"
        if not self.authorization_url:
            self.authorization_url = f"https://login.microsoftonline.com/{self.tenant}/oauth2/v2.0/authorize"

    def __create_provider(self):
        self.provider = InteractiveProvider(
            name="Microsoft",
            client_id=self.client_id,
            client_secret=self.client_secret,
            token_url=self.token_url,
            authorization_url=self.authorization_url,
            scope=self.scope,
            open=self.open
        )

    def authenticate(self) -> BearerAuthentication:
        if not self.provider:
            self.__create_provider()
        token = self.provider.authenticate()
        return BearerAuthentication(token)
    
class EntraApp:
    def __init__(self, tenant: str, client: tuple, scope: str = None, token_url: str = None):
        self.tenant = tenant
        self.client_id = client[0]
        self.client_secret = client[1]
        self.scope = scope
        self.token_url = token_url
        self.state = self.__generate_state()

        self.__check_urls()
        self.__check_scope()

    def __check_scope(self):
        if not self.scope:
            self.scope = "https://graph.microsoft.com/.default"

    def __check_urls(self):
        if not self.token_url:
            self.token_url = f"https://login.microsoftonline.com/{self.tenant}/oauth2/v2.0/token"

    def __generate_state(self) -> str:
        # Generate a random string
        state = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        # Encode the string as base64
        encoded_state = base64.b64encode(state.encode("utf-8"))
        # Convert the base64 bytes to a string
        return encoded_state.decode("utf-8")

    def authenticate(self) -> BearerAuthentication:
        client = HTTPClient(base_url=self.token_url)
        client.set_header("Content-Type", "application/x-www-form-urlencoded")
        data = {
            "client_id": self.client_id,
            "scope": self.scope,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        response = client.post(data=data)
        token = response.json()["access_token"]
        return BearerAuthentication(token)
