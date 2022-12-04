import json
import random
import secrets
import string
import time
from dataclasses import dataclass
from typing import Optional

import requests
from firebase_admin import auth as firebase_auth
from requests import Response

from src.config import CredentialManager

SPECIAL_CHARACTERS = " !\"#$%&'()*+,-.:;<=>?@[]^_`{|}~"


class AuthenticationError(Exception):
    ...


@dataclass
class SessionToken:
    email: str
    expires_in: int
    id_token: str  # short-lived JSON web token (JWT)
    access_token: str  # long-lived, used to fetch more id tokens, a.k.a. refresh token


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

    def create_user(self, email: str, password: str) -> None:
        if email == password:
            raise ValueError("Email and password should not match.")

        if not self.is_strong_password(password):
            raise ValueError("Password is too weak.")

        self._auth_service.create_user(email=email, password=password)

    @staticmethod
    def is_strong_password(password: str) -> bool:
        if not isinstance(password, str):
            return False

        contains_lowercase: bool = password.upper() != password
        contains_uppercase: bool = password.lower() != password
        contains_numbers: bool = any(
            [character for character in password if character.isnumeric()]
        )
        contains_special_characters: bool = any(
            [character for character in password if character in SPECIAL_CHARACTERS]
        )
        is_at_least_six_characters = len(password) >= 6
        if (
            contains_lowercase
            and contains_uppercase
            and contains_numbers
            and contains_special_characters
            and is_at_least_six_characters
        ):
            return True
        else:
            return False

    def login(self, email: str, password: str) -> SessionToken:
        url: str = (
            f"https://www.googleapis.com/identitytoolkit/v3/relyingparty"
            f"/verifyPassword?key={self._credential_manager.get_firebase_api_key()}"
        )
        headers: dict = {"content-type": "application/json; charset=UTF-8"}
        request_body = json.dumps(
            {
                "email": email,
                "password": password,
                "returnSecureToken": True,
            }
        )
        response: Response = requests.post(url, headers=headers, data=request_body)

        if not response.ok:
            raise AuthenticationError

        response_json: dict = response.json()
        session_token: SessionToken = SessionToken(
            response_json["email"],
            response_json["expiresIn"],
            response_json["idToken"],
            response_json["refreshToken"],
        )
        return session_token

    def logout(self, id_token: str):
        ...

    def verify_token_and_get_user(self, id_token: str):
        # TODO this is an unfortunate hack while I wait for this issue to be resolved
        # https://github.com/firebase/firebase-admin-python/issues/624
        # https://github.com/firebase/firebase-admin-python/issues/625
        time.sleep(3)
        user: dict = self._auth_service.verify_id_token(id_token)
        return user


def generate_strong_password() -> str:
    uppercase_letter: str = secrets.choice(string.ascii_uppercase)
    lowercase_letter: str = secrets.choice(string.ascii_lowercase)
    letters: str = "".join(
        [secrets.choice(string.ascii_letters) for _ in range(secrets.randbelow(2) + 3)]
    )
    number: str = str(secrets.randbelow(10))
    special_character: str = secrets.choice(SPECIAL_CHARACTERS)
    password_components: list[str] = list(
        letters + uppercase_letter + lowercase_letter + number + special_character
    )

    random.shuffle(password_components)

    password: str = "".join(password_components)
    return password
