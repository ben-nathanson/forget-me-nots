import datetime as dt
import unittest
from http import HTTPStatus

import pytest
from fastapi import HTTPException

from src.view.models import _convert_to_camel_case  # noqa
from src.view.models import HolidayBasePayload, UpcomingHolidaysPayload


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


class TestUpcomingHolidaysPayload(unittest.TestCase):
    def populates_start_date(self):
        payload = UpcomingHolidaysPayload(
            country_abbreviates="US",
            end_date=dt.date(year=2022, month=1, day=1),
        )
        assert payload.start_date == dt.date.today()

    def populates_end_date(self):
        payload = UpcomingHolidaysPayload(
            country_abbreviates="US",
            start_date=dt.date(year=2022, month=1, day=1),
        )
        six_months = dt.timedelta(weeks=26)
        assert payload.end_date == payload.start_date + six_months

    def populates_both_start_and_end_time(self):

        payload = UpcomingHolidaysPayload(
            country_abbreviates="US",
        )
        six_months = dt.timedelta(weeks=26)
        assert payload.end_date == payload.start_date + six_months

    def test_guarantees_end_date_exceeds_start_date(self):
        with pytest.raises(HTTPException) as exception:
            UpcomingHolidaysPayload(
                country_abbreviation="US",
                start_date=dt.date(year=2022, month=2, day=1),
                end_date=dt.date(year=2022, month=1, day=1),
            )

        assert exception.value.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert exception.value.detail == "End date cannot exceed start date."


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
