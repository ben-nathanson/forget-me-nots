import json
import random
import secrets
import string
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
            raise AuthenticationError

        response_json: dict = response.json()
        session_token: SessionToken = SessionToken(
            response_json["email"],
            response_json["expiresIn"],
            response_json["idToken"],
            response_json["refreshToken"],
        )
        return session_token


def generate_strong_password() -> str:
    uppercase_letter: str = secrets.choice(string.ascii_uppercase)
    lowercase_letter: str = secrets.choice(string.ascii_lowercase)
    letters: str = "".join(
        [secrets.choice(string.ascii_letters) for _ in range(random.randint(3, 5))]
    )
    number: str = str(secrets.randbelow(9))
    special_character: str = secrets.choice(SPECIAL_CHARACTERS)
    password_components: list[str] = list(
        letters + uppercase_letter + lowercase_letter + number + special_character
    )

    random.shuffle(password_components)

    password: str = "".join(password_components)
    return password
