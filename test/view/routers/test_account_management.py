import secrets
import unittest
import uuid
from http import HTTPStatus

from fastapi.testclient import TestClient
from firebase_admin import auth
from firebase_admin.auth import UserRecord
from requests import Response  # type: ignore

from src.main import app


class AccountManagementFixture(unittest.TestCase):
    random_guid = str(uuid.uuid4())
    email_address: str = f"ben+automatedtesting+{random_guid}@nathanson.dev"
    password: str = secrets.token_urlsafe(15)

    def setUp(self):  # noqa
        self.client: TestClient = TestClient(app)

    def tearDown(self):  # noqa
        user: UserRecord | None = auth.get_user_by_email(self.email_address)
        if user:
            auth.delete_user(user.uid)


class TestCreateUser(AccountManagementFixture):
    route: str = "users/create"

    def test_that_we_can_create_a_user(self):
        raw_payload: dict = {"email": self.email_address, "password": self.password}
        response: Response = self.client.post(self.route, json=raw_payload)
        assert response.ok
        assert response.json()["email"] == self.email_address

    def test_that_we_validate_inputs(self):
        param_list = [
            (self.email_address, None),
            (None, self.password),
            ("", self.password),
        ]
        for email, password in param_list:
            raw_payload: dict = {"email": email, "password": password}

            response: Response = self.client.post(self.route, json=raw_payload)
            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
