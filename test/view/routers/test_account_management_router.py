import secrets
import unittest
import uuid
from http import HTTPStatus

import firebase_admin.auth
from fastapi.testclient import TestClient
from firebase_admin import auth
from firebase_admin.auth import UserNotFoundError, UserRecord
from httpx import Response

from src.logic.services.account_management import generate_strong_password
from src.main import app


class AccountManagementBaseFixture(unittest.TestCase):
    class Routes:
        create_route: str = "users/create"
        create_token_route: str = "/users/token"
        login_route: str = "users/login"
        logout_route: str = "users/logout"
        verify_token_route: str = "/users/verify-token"

    random_guid = str(uuid.uuid4())
    email_address: str = f"ben+automatedtesting+{random_guid}@nathanson.dev"
    password: str = generate_strong_password()

    def setUp(self):  # noqa
        self.client: TestClient = TestClient(app, raise_server_exceptions=False)

    def create_user(self) -> Response:
        raw_payload: dict = {"email": self.email_address, "password": self.password}
        return self.client.post(self.Routes.create_route, json=raw_payload)

    def login(self) -> Response:
        raw_payload: dict = {"email": self.email_address, "password": self.password}
        response: Response = self.client.post(self.Routes.login_route, json=raw_payload)
        return response

    def tearDown(self):  # noqa
        try:
            user: UserRecord = auth.get_user_by_email(self.email_address)
            auth.delete_user(user.uid)
        except UserNotFoundError:
            pass


class TestCreateUser(AccountManagementBaseFixture):
    def test_that_we_can_create_a_user(self):
        raw_payload: dict = {"email": self.email_address, "password": self.password}
        response: Response = self.client.post(
            self.Routes.create_route, json=raw_payload
        )
        assert response.status_code == 200, (self.email_address, self.password)
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
                    self.Routes.create_route, json=raw_payload
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
                    self.Routes.create_route, json=raw_payload
                )
                assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


class TestLogin(AccountManagementBaseFixture):
    def setUp(self):
        super().setUp()
        self.create_user()

    def test_that_we_can_login(self):
        response: Response = self.login()
        response_json: dict = response.json()

        assert response.status_code == 200, (self.email_address, self.password)
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
                    self.Routes.login_route, json=raw_payload
                )
                assert response.status_code == HTTPStatus.FORBIDDEN


class TestSwaggerOpenApiLogin(AccountManagementBaseFixture):
    def setUp(self):
        super().setUp()
        self.create_user()

    def test_that_we_can_create_a_valid_token(self):
        request_form = {"username": self.email_address, "password": self.password}
        create_token_response: Response = self.client.post(
            self.Routes.create_token_route, data=request_form
        )
        assert (
            create_token_response.status_code == 200
        ), create_token_response.status_code
        id_token: str = create_token_response.json()["idToken"]
        headers: dict = {"Authorization": f"Bearer {id_token}"}
        validate_token_response: Response = self.client.get(
            self.Routes.verify_token_route, headers=headers
        )
        assert (
            create_token_response.status_code == 200
        ), validate_token_response.status_code
        assert validate_token_response.json()["idToken"] == id_token


class TestLogout(AccountManagementBaseFixture):
    def setUp(self):
        super().setUp()
        self.create_user()

    def test_that_we_can_logout(self):
        login_response: Response = self.login()
        id_token: str = login_response.json()["idToken"]
        headers: dict = {"Authorization": f"Bearer {id_token}"}
        first_verification: Response = self.client.get(
            self.Routes.verify_token_route, headers=headers
        )
        assert first_verification.status_code == 200
        self.client.post(self.Routes.logout_route, headers=headers)
        second_verification: Response = self.client.get(
            self.Routes.verify_token_route, headers=headers
        )
        assert second_verification.status_code == 403
