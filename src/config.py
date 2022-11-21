import json
import os
from typing import Optional

from firebase_admin.credentials import Certificate


class CredentialManager:
    _raw_firebase_credentials: dict
    _firebase_credentials_path: str
    _firebase_environment_key: str

    def __init__(
        self,
        firebase_credentials_path: Optional[str] = None,
        firebase_environment_key: Optional[str] = None,
    ):
        self._firebase_credentials_path = (
            firebase_credentials_path or "src/firebase-credentials.json"
        )
        self._firebase_environment_key = (
            firebase_environment_key or "SECRET_FIREBASE_CREDENTIALS"
        )
        if os.path.exists(self._firebase_credentials_path):
            self._raw_firebase_credentials: dict = json.load(
                open(self._firebase_credentials_path)
            )
        else:
            self._raw_firebase_credentials: dict = json.loads(
                os.environ.get(self._firebase_environment_key)
            )

    def get_firebase_api_key(self) -> str:
        return self._raw_firebase_credentials["api_key"]

    def get_firebase_cert(self) -> Certificate:
        return Certificate(self._raw_firebase_credentials)
