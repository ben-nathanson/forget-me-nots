import random
import string
import unittest

from src.logic.security import is_strong_password


class TestPasswordChecker(unittest.TestCase):
    @staticmethod
    def _generate_strong_password() -> str:
        uppercase_letter: str = random.choice(string.ascii_uppercase)
        lowercase_letter: str = random.choice(string.ascii_lowercase)
        letters: str = "".join(
            [random.choice(string.ascii_letters) for _ in range(random.randint(3, 97))]
        )
        number: str = str(random.randint(0, 9))
        password_components: list[str] = list(
            f"{letters}{uppercase_letter}{lowercase_letter}{number}"
        )
        random.shuffle(password_components)

        return str(password_components)

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

    def test_fuzz_test_password_requirements(self):
        good_passwords: list[str] = [
            self._generate_strong_password() for _ in range(100)
        ]
        for password in good_passwords:
            with self.subTest():
                assert is_strong_password(password), password
