import unittest

from src.logic.services.account_management import (
    AccountManagementService,
    generate_strong_password,
)


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
