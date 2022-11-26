import random
import secrets
import string
import unittest
import uuid
from http import HTTPStatus

import firebase_admin.auth
from fastapi.testclient import TestClient
from firebase_admin import auth
from firebase_admin.auth import UserNotFoundError, UserRecord
from requests import Response  # type: ignore

from src.logic.services.account_management import (
    SPECIAL_CHARACTERS,
    AccountManagementService,
)
from src.main import app


def generate_strong_password() -> str:
    uppercase_letter: str = random.choice(string.ascii_uppercase)
    lowercase_letter: str = random.choice(string.ascii_lowercase)
    letters: str = "".join(
        [random.choice(string.ascii_letters) for _ in range(random.randint(3, 5))]
    )
    number: str = str(random.randint(0, 9))
    special_character: str = random.choice(SPECIAL_CHARACTERS)
    password_components: list[str] = list(
        letters + uppercase_letter + lowercase_letter + number + special_character
    )

    random.shuffle(password_components)

    password: str = "".join(password_components)
    return password


class AccountManagementFixture(unittest.TestCase):
    create_route: str = "users/create"
    login_route: str = "users/login"
    random_guid = str(uuid.uuid4())
    email_address: str = f"ben+automatedtesting+{random_guid}@nathanson.dev"
    password: str = generate_strong_password()

    def setUp(self):  # noqa
        self.client: TestClient = TestClient(app)

    def tearDown(self):  # noqa
        try:
            user: UserRecord = auth.get_user_by_email(self.email_address)
            auth.delete_user(user.uid)
        except UserNotFoundError:
            pass


class TestCreateUser(AccountManagementFixture):
    def test_that_we_can_create_a_user(self):
        raw_payload: dict = {"email": self.email_address, "password": self.password}
        response: Response = self.client.post(self.create_route, json=raw_payload)
        assert response.ok, (self.email_address, self.password)
        assert firebase_admin.auth.get_user_by_email(self.email_address)

    def test_that_we_reject_weak_passwords(self):
        param_list = [
            (self.email_address, "password"),
            (self.email_address, "123"),
            (self.email_address, self.email_address),
        ]
        for email, password in param_list:
            with self.subTest():
                raw_payload: dict = {"email": email, "password": password}

                response: Response = self.client.post(
                    self.create_route, json=raw_payload
                )
                assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, password

    def test_that_we_validate_inputs(self):
        param_list = [
            (self.email_address, None),
            (None, self.password),
            ("", self.password),
            (self.email_address, ""),
        ]
        for email, password in param_list:
            with self.subTest():
                raw_payload: dict = {"email": email, "password": password}

                response: Response = self.client.post(
                    self.create_route, json=raw_payload
                )
                assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


class TestLogin(AccountManagementFixture):
    def setUp(self):
        super().setUp()
        raw_payload: dict = {"email": self.email_address, "password": self.password}
        self.client.post(self.create_route, json=raw_payload)

    def test_that_we_can_login(self):
        raw_payload: dict = {"email": self.email_address, "password": self.password}
        response: Response = self.client.post(self.login_route, json=raw_payload)
        response_json: dict = response.json()

        assert response.ok, (self.email_address, self.password)
        assert response_json["email"] == self.email_address
        assert len(response_json["idToken"])
        assert len(response_json["accessToken"])

    def test_that_we_cant_login_with_wrong_password(self):
        wrong_passwords = [
            self.password[::-1],
            self.password[1:],
            self.password[:-1],
            secrets.token_urlsafe(15),
            "password",
        ]
        for password in wrong_passwords:
            with self.subTest():
                raw_payload: dict = {"email": self.email_address, "password": password}
                response: Response = self.client.post(
                    self.login_route, json=raw_payload
                )
                assert response.status_code == HTTPStatus.FORBIDDEN


class TestPasswordChecker(unittest.TestCase):
    def test_rejects_bad_passwords(self):
        bad_passwords = [
            123,
            "",
            "password",
            "lks~!",
            "lowercase",
            "UPPERCASE",
            "NoSpecialCharacters123",
            "NoNumbers!",
            "cH^qmmjSj",
            "2cH88qmmjSj",
        ]
        for password in bad_passwords:
            with self.subTest():
                assert not AccountManagementService.is_strong_password(password)

    def test_accepts_good_passwords(self):
        good_passwords = [
            "2cH88^qmmjSj",
            "7S$u37M8M^kF",
            "wK27*rv7@$Jx",
            "dL_aR1qq8KTk1hl2oMxg",
        ]
        for password in good_passwords:
            with self.subTest():
                assert AccountManagementService.is_strong_password(password)

    def test_fuzz_test_password_requirements(self):
        good_passwords: list[str] = [generate_strong_password() for _ in range(100)]
        for password in good_passwords:
            with self.subTest():
                assert AccountManagementService.is_strong_password(password), password
