import json
import os
import unittest

from src.config import CredentialManager

MOCK_CREDENTIALS: dict = {
    "api_key": "test_api_key",  # nosec
    "auth_provider_x509_cert_url": "www.test.test",
    "auth_uri": "www.test.test",
    "client_email": "test@nathanson.dev",
    "client_id": "123456789123456789123",
    "client_x509_cert_url": "www.test.test",
    "private_key": "test_private_key",  # nosec
    "private_key_id": "test-key-id",
    "project_id": "test-project-id-123",
    "token_uri": "www.test.test",
    "type": "service_account",
}


class TestCredentialManager(unittest.TestCase):
    firebase_credentials_path: str = "test/test_credentials.json"
    firebase_environment_key: str = "TEST_CREDENTIALS"

    def tearDown(self):
        if os.path.exists(self.firebase_credentials_path):
            os.remove(self.firebase_credentials_path)
        os.environ.pop(self.firebase_credentials_path, None)

    def test_can_get_credentials_from_env_variable(self):
        os.environ[self.firebase_environment_key] = json.dumps(MOCK_CREDENTIALS)
        credential_manager: CredentialManager = CredentialManager(
            firebase_credentials_path=self.firebase_credentials_path,
            firebase_environment_key=self.firebase_environment_key,
        )

        assert credential_manager._raw_firebase_credentials == MOCK_CREDENTIALS

    def test_can_get_credentials_from_file(self):
        with open(self.firebase_credentials_path, "w") as credentials_file:
            credentials_file.write(json.dumps(MOCK_CREDENTIALS))

        credential_manager: CredentialManager = CredentialManager(
            firebase_credentials_path=self.firebase_credentials_path,
            firebase_environment_key=self.firebase_environment_key,
        )

        assert credential_manager._raw_firebase_credentials == MOCK_CREDENTIALS
