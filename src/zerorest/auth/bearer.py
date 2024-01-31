import base64

class BearerAuthentication:
    def __init__(self, token: str):
        self.token = token
        self.type = "Bearer"

    # Convert to base64
    def encode(self) -> str:
        """
        Encode the token as a base64 string
        """
        # Encode the string as base64
        encoded_token = base64.b64encode(self.token.encode("utf-8"))
        # Convert the base64 bytes to a string
        self.hash = encoded_token.decode("utf-8")
        # Return the hash
        return self.hash
    
    def __str__(self) -> str:
        return "Bearer " + self.token

        
