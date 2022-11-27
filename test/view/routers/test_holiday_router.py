import datetime as dt
import json
import unittest
from test.logic.test_data import US_INDEPENDENCE_DAY

from fastapi.testclient import TestClient
from requests import Response  # type: ignore

import src.view.models as view_models
from src.main import app


class TestIsItAHoliday(unittest.TestCase):
    def setUp(self):
        self.client: TestClient = TestClient(app)
        self.route: str = "holidays/is-it-a-holiday"

    def get_response(self, payload: view_models.HolidayBasePayload) -> Response:
        return self.client.post(
            self.route, json=json.loads(payload.json(by_alias=True))
        )

    def test_returns_expected_response(self):
        param_list = [
            (dt.datetime(2022, 7, 3), False),
            (dt.datetime(2022, 7, 4), True),
            (dt.datetime(2022, 7, 5), False),
        ]
        for date, expected_result in param_list:
            with self.subTest():
                payload = view_models.HolidayBasePayload(
                    country_abbreviation="US", date=date
                )
                response: Response = self.get_response(payload)
                parsed_response = view_models.IsHolidayResponse.parse_obj(
                    response.json()
                )
                assert parsed_response.is_holiday == expected_result


class TestSupportedCountries(unittest.TestCase):
    def setUp(self):
        self.client: TestClient = TestClient(app)
        self.route: str = "holidays/supported-countries"

    def get_response(self) -> list[view_models.CountryResponse]:
        raw_response: list[dict] = self.client.get(self.route).json()
        supported_countries = [
            view_models.CountryResponse.parse_obj(c) for c in raw_response
        ]
        return supported_countries

    def test_returns_expected_country_detail(self):
        supported_countries = self.get_response()
        united_states, *_ = [
            c for c in supported_countries if c.country_abbreviation == "US"
        ]
        assert united_states.flag == "🇺🇸"
        assert united_states.name == "United States"

    def test_returns_expected_countries(self):
        supported_countries = self.get_response()
        supported_countries_set = {c.country_abbreviation for c in supported_countries}
        assert {"GB", "MX", "US"}.intersection(supported_countries_set)


class TestUpcomingHolidays(unittest.TestCase):
    def setUp(self):
        self.client: TestClient = TestClient(app)
        self.route: str = "holidays/upcoming-holidays"

    def get_response(self, payload: view_models.UpcomingHolidaysPayload) -> Response:
        raw_payload: dict = {
            "countryAbbreviation": payload.country_abbreviation,
            "startDate": payload.start_date.isoformat(),
            "endDate": payload.end_date.isoformat(),
        }
        return self.client.post(self.route, json=raw_payload)

    def test_handles_no_holidays(self):
        non_us_holiday = dt.date(year=2022, month=9, day=1)
        upcoming_holidays = self.get_response(
            view_models.UpcomingHolidaysPayload(
                country_abbreviation="US",
                start_date=non_us_holiday,
                end_date=non_us_holiday,
            )
        ).json()
        assert upcoming_holidays == []

    def test_handles_single_holiday(self):
        payload = view_models.UpcomingHolidaysPayload(
            country_abbreviation="US",
            start_date=US_INDEPENDENCE_DAY,
            end_date=US_INDEPENDENCE_DAY,
        )
        raw_response = self.get_response(payload).json()
        upcoming_holidays = [
            view_models.Holiday.parse_obj(holiday) for holiday in raw_response
        ]
        assert len(upcoming_holidays) == 1
        upcoming_holiday, *_ = upcoming_holidays
        assert upcoming_holiday.country_abbreviation == "US"
        assert upcoming_holiday.date == US_INDEPENDENCE_DAY
        assert upcoming_holiday.holiday_name == "Independence Day"

    def test_handles_multiple_holidays(self):
        payload = view_models.UpcomingHolidaysPayload(
            country_abbreviation="US",
            start_date=dt.date(year=2022, month=12, day=23),
            # TODO suspect there's a boundary issue with the engine
            end_date=dt.date(year=2022, month=12, day=26),
        )
        raw_response = self.get_response(payload).json()
        upcoming_holidays = [
            view_models.Holiday.parse_obj(holiday) for holiday in raw_response
        ]

        assert len(upcoming_holidays) == 2
        holiday_names = {h.holiday_name for h in upcoming_holidays}
        assert holiday_names == {"Christmas Day", "Christmas Day (Observed)"}
