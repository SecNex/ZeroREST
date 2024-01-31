from ..http import HTTPClient
from ..auth import BearerAuthentication

import base64
import string
import random
import threading
import socketserver
import urllib.parse as parse

import http.server

def handler_factory(state, provider):
    def create_handler(*args, **kwargs):
        return InteractiveCallbackHandler(*args, state=state, provider=provider, **kwargs)
    return create_handler

class InteractiveCallbackHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server, state: str, provider: any):
        self.state = state
        self.provider = provider
        super().__init__(request, client_address, server)

    def do_GET(self):
        if self.path == '/favicon.ico':
            self.send_response(404)
            self.end_headers()
            return
        
        query_params = parse.parse_qs(parse.urlparse(self.path).query)
        self.provider.authorization_code = query_params["code"][0]
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><head><title>Authentication Successful</title></head>")
        self.wfile.write(b"<body><p>You have successfully authenticated with the provider.</p>")
        self.wfile.write(b"</body></html>")

        self.provider.authorization_received.set()  
        
class InteractiveProvider:
    def __init__(self, name: str, client_id: str, client_secret: str, token_url: str, authorization_url: str, scope: str, open: bool = True):
        self.name = name
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = "http://localhost:8000/redirect"
        self.token_url = token_url
        self.authorization_url = authorization_url
        self.scope = scope
        self.authorization_code = None
        self.access_token = None
        self.server = None
        self.open = open
        self.state = self.__generate_state()
        self.authorization_received = threading.Event()  

    def start_server(self):
        handler = handler_factory(self.state, self)
        self.server = socketserver.TCPServer(("", 8000), handler)
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.start()

    def stop_server(self):
        if self.server:
            def shutdown_server():
                self.server.shutdown()
                self.server.server_close()
                self.server = None
            shutdown_thread = threading.Thread(target=shutdown_server)
            shutdown_thread.start()

    def __generate_state(self) -> str:
        # Generate a random string
        state = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        # Encode the string as base64
        encoded_state = base64.b64encode(state.encode("utf-8"))
        # Convert the base64 bytes to a string
        return encoded_state.decode("utf-8")

    def __get_authorization_code(self) -> str:
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()
        login_client = HTTPClient(base_url=self.authorization_url)
        if self.open:
            login_client.webbrowser(params=[("client_id", self.client_id), ("response_type", "code"), ("redirect_uri", self.redirect_uri), ("response_mode", "query"), ("scope", self.scope), ("state", self.__generate_state())])
        else:
            login_client.webbrowser(params=[("client_id", self.client_id), ("response_type", "code"), ("redirect_uri", self.redirect_uri), ("response_mode", "query"), ("scope", self.scope), ("state", self.__generate_state())])
        self.authorization_received.wait()  # Wait for the event here
        return self.authorization_code

    def authenticate(self) -> str:
        # Get the authorization code
        authorization_code = self.__get_authorization_code()
        # Create a client object
        client = HTTPClient(base_url="")
        client.set_header("Content-Type", "application/x-www-form-urlencoded")
        # client_id=11111111-1111-1111-1111-111111111111
        # &scope=user.read%20mail.read
        # &code=OAAABAAAAiL9Kn2Z27UubvWFPbm0gLWQJVzCTE9UkP3pSx1aXxUjq3n8b2JRLk4OxVXr...
        # &redirect_uri=http%3A%2F%2Flocalhost%2Fmyapp%2F
        # &grant_type=authorization_code
        # &client_secret=HF8Q~Krjqh4r... 
        # Send the request
        data = {
            "client_id": self.client_id,
            "scope": self.scope,
            "code": authorization_code,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
            "client_secret": self.client_secret
        }
        res = client.post(url=self.token_url, data=data)
        # Get the response
        res_json = res.json()
        self.access_token = res_json["access_token"]
        self.stop_server()
                          
        return self.access_token