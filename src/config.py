import json
import os

from firebase_admin.credentials import Certificate


class CredentialManager:
    _raw_firebase_credentials: dict
    firebase_credentials_path: str = "src/firebase-credentials.json"
    firebase_environment_key: str = "SECRET_FIREBASE_CREDENTIALS"
    firebase_cert: Certificate
    firebase_api_key: str

    def __init__(self):
        if os.path.exists(self.firebase_credentials_path):
            self._raw_firebase_credentials: dict = json.load(
                open(self.firebase_credentials_path)
            )
        else:
            self._raw_firebase_credentials: dict = json.loads(
                os.environ.get(self.firebase_environment_key)
            )
        self.firebase_cert = Certificate(self._raw_firebase_credentials)
        self.firebase_api_key = self._raw_firebase_credentials["api_key"]

    def get_firebase_cert(self) -> Certificate:
        return self.firebase_cert

    def get_firebase_api_key(self) -> str:
        return self.firebase_api_key
