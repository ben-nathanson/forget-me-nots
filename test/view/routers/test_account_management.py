import secrets
import unittest
import uuid
from http import HTTPStatus

from fastapi.testclient import TestClient
from firebase_admin import auth
from firebase_admin.auth import UserNotFoundError, UserRecord
from requests import Response  # type: ignore

from src.main import app


class AccountManagementFixture(unittest.TestCase):
    create_route: str = "users/create"
    login_route: str = "users/login"
    random_guid = str(uuid.uuid4())
    email_address: str = f"ben+automatedtesting+{random_guid}@nathanson.dev"
    password: str = secrets.token_urlsafe(15)

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
        assert response.ok
        assert response.json()["email"] == self.email_address

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

        assert response.ok
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
