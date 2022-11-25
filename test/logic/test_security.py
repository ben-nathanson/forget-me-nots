import unittest

from src.logic.security import is_strong_password


class TestPasswordChecker(unittest.TestCase):
    def test_rejects_bad_passwords(self):
        bad_passwords = [
            123,
            "",
            "password",
            "lks~!",
            "lowercase",
            "UPPERCASE",
            "NoSpecialCharacters",
            "NoNumbers!",
            "cH^qmmjSj",
            "2cH88qmmjSj",
        ]
        for password in bad_passwords:
            with self.subTest():
                assert not is_strong_password(password)

    def test_accepts_good_passwords(self):
        good_passwords = [
            "2cH88^qmmjSj",
            "7S$u37M8M^kF",
            "wK27*rv7@$Jx",
            "dL_aR1qq8KTk1hl2oMxg",
        ]
        for password in good_passwords:
            with self.subTest():
                assert is_strong_password(password)
