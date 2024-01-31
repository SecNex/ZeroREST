import urllib.parse as parse
import urllib.request as request
import urllib.error as error
import urllib.response as response
import json as js
import webbrowser as browser    

from .__main__ import ZeroREST

class Response:
    def __init__(self, response: response):
        self.text = response.read().decode("utf-8")

    def json(self) -> dict:
        return js.loads(self.text)

class Param:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    def __str__(self) -> str:
        return f"{self.key}={self.value}"

class HTTPClient:
    def __init__(self, auth: any = None, proxy: str = None, base_url: str = None):
        self.auth = auth
        self.proxy = proxy
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"{ZeroREST.APPLICATION}/{ZeroREST.VERSION}"
        }

    def set_header(self, key: str, value: str):
        self.headers[key] = value

    def set_headers(self, headers: dict):
        self.headers = headers

    def get_header(self, key: str) -> str:
        return self.headers[key]
    
    def get_headers(self) -> dict:
        return self.headers

    def __send(self, method: str, url: str, data: dict = None) -> Response:
        # Create a request object
        req = request.Request(url, method=method, headers=self.headers)
        # Add the authentication
        if self.auth:
            req.add_header("Authorization", f"{self.auth.type} {self.auth.token}")
        if data:
            match self.headers["Content-Type"]:
                case "application/json":
                    data = js.dumps(data).encode("utf-8")
                case "application/x-www-form-urlencoded":
                    data = parse.urlencode(data).encode("utf-8")
                case _:
                    data = js.dumps(data).encode("utf-8")
        try:
            response = request.urlopen(req, data=data)
        except error.HTTPError as e:
            print(e.read().decode())
            raise
        # Return the response
        return Response(response)
    
    def get(self, url: str = "", params: list = None) -> Response:
        parameter = ""
        if params:
            parameter = "?"
            parameter_length = len(params)
            for param in params:
                p = Param(param[0], param[1])
                parameter += str(p)
                if params.index(param) != parameter_length - 1:
                    parameter += "&"
        url = self.base_url + url + parameter
        return self.__send("GET", url)
    
    def post(self, url: str = "", data: dict = None, params: list = None) -> Response:
        parameter = ""
        if params:
            parameter = "?"
            parameter_length = len(params)
            for param in params:
                p = Param(param[0], param[1])
                parameter += str(p)
                if params.index(param) != parameter_length - 1:
                    parameter += "&"
        url = self.base_url + url + parameter
        return self.__send("POST", url, data=data)

    def link(self, url: str = "", params: list = None) -> str:
        parameter = "?"
        parameter_length = len(params)
        for param in params:
            p = Param(param[0], param[1])
            parameter += str(p)
            if params.index(param) != parameter_length - 1:
                parameter += "&"
        return self.base_url + url + parameter

    def webbrowser(self, url: str = "", params: list = None):
        parameter = "?"
        parameter_length = len(params)
        for param in params:
            p = Param(param[0], param[1])
            parameter += str(p)
            if params.index(param) != parameter_length - 1:
                parameter += "&"
        url = self.base_url + url + parameter
        browser.open(url)