import unittest

import pytest
from fastapi import HTTPException

from src.view.models import HolidayBasePayload, _convert_to_camel_case  # noqa


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


class TestHolidayBasePayload(unittest.TestCase):
    def test_raises_not_implemented_for_unexpected_country(self):
        nonexistent_country_codes = ["//", "??", "(("]
        for country_alpha_2 in nonexistent_country_codes:
            with self.subTest():
                with pytest.raises(HTTPException) as exception:
                    HolidayBasePayload(country_abbreviation=country_alpha_2)

    def test_constructs_class_successfully_for_expected_country(self):
        country_codes = ["US", "FR", "MX"]
        for country_alpha_2 in country_codes:
            with self.subTest():
                HolidayBasePayload(country_abbreviation=country_alpha_2)
