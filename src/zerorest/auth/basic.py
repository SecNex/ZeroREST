import base64

class BasicAuthentication:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.hash = self.encode()

    def encode(self) -> str:
        """
        Encode the username and password as a base64 string
        """
        # Create a string in the format "username:password"
        credentials = f"{self.username}:{self.password}"
        # Encode the string as base64
        encoded_credentials = base64.b64encode(credentials.encode("utf-8"))
        # Convert the base64 bytes to a string
        return encoded_credentials.decode("utf-8")
    
    def decode(self, encoded_credentials: str) -> tuple:
        """
        Decode the base64 string into a username and password
        """
        # Decode the base64 string into bytes
        decoded_credentials = base64.b64decode(encoded_credentials)
        # Convert the bytes to a string
        credentials = decoded_credentials.decode("utf-8")
        # Split the string into a username and password
        username, password = credentials.split(":")
        # Return the username and password
        return username, password
    
    def __str__(self) -> str:
        return "Basic " + self.hash