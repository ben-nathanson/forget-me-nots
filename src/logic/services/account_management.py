import json
from dataclasses import dataclass
from typing import Optional

import requests
from fastapi import HTTPException
from firebase_admin import auth as firebase_auth
from requests import Response

from src.config import CredentialManager


@dataclass
class SessionToken:
    email: str
    expires_in: int
    id_token: str
    access_token: str


class AccountManagementService:
    _auth_service: firebase_auth
    _credential_manager: CredentialManager

    def __init__(
        self,
        auth_service: Optional[firebase_auth] = None,
        credential_service: Optional[CredentialManager] = None,
    ):
        self._auth_service = auth_service or firebase_auth
        self._credential_manager = credential_service or CredentialManager()

    def create_user(self, email: str, password: str):
        self._auth_service.create_user(email=email, password=password)

    def login(self, email: str, password: str) -> SessionToken:
        url: str = (
            f"https://www.googleapis.com/identitytoolkit/v3/relyingparty"
            f"/verifyPassword?key={self._credential_manager.get_firebase_api_key()}"
        )
        headers = {"content-type": "application/json; charset=UTF-8"}
        request_body = json.dumps(
            {
                "email": email,
                "password": password,
                "returnSecureToken": True,
            }
        )
        response: Response = requests.post(url, headers=headers, data=request_body)

        if not response.ok:
            raise HTTPException(status_code=403, detail="Authentication error.")

        response_json: dict = response.json()
        session_token: SessionToken = SessionToken(
            response_json["email"],
            response_json["expiresIn"],
            response_json["idToken"],
            response_json["refreshToken"],
        )
        return session_token
