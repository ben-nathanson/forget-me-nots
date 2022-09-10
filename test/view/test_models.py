import unittest

from src.view.models import _convert_to_camel_case  # noqa


class TestConvertToCamelCase(unittest.TestCase):
    def test_returns_expected_values(self):
        param_list = [
            ("country_name", "countryName"),
            ("one_two_three", "oneTwoThree"),
            ("one", "one"),
        ]
        for snake_cased_word, camel_cased_word in param_list:
            with self.subTest():
                assert _convert_to_camel_case(snake_cased_word) == camel_cased_word
