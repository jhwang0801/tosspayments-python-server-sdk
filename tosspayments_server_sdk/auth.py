import base64
from typing import Dict


class Auth:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def get_headers(self) -> Dict[str, str]:
        credentials = f"{self.secret_key}:"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        return {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json",
        }
