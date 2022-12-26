import datetime as dt
import unittest
from test.test_data import NEW_YEARS_DAY, US_INDEPENDENCE_DAY

from src.logic import HolidayEngine, holiday_engine


class TestGetCachedCountryHolidays(unittest.TestCase):
    def test_handles_cache_miss(self):
        # need to ensure a cold start
        engine_instance = HolidayEngine()
        assert engine_instance.is_holiday("US", dt.datetime(2022, 7, 4)) is True

    def test_handles_cache_hit(self):
        # need to ensure a cold start
        engine_instance = HolidayEngine()
        assert engine_instance.is_holiday("US", dt.datetime(2022, 7, 4)) is True
        assert engine_instance.is_holiday("US", dt.datetime(2022, 7, 4)) is True


class TestGetHolidayName(unittest.TestCase):
    def test_returns_expected_response(self):
        param_list = [
            (dt.datetime(2022, 7, 4), "Independence Day"),
            (dt.datetime(2022, 9, 5), "Labor Day"),
        ]
        for date, holiday_name in param_list:
            with self.subTest():
                assert holiday_engine.get_holiday_name("US", date) == holiday_name


class TestGetSupportedCountries(unittest.TestCase):
    def test_returns_expected_country_detail(self):
        supported_countries = holiday_engine.get_supported_countries()
        united_states, *_ = [c for c in supported_countries if c.abbreviation == "US"]
        assert united_states.flag == "🇺🇸"
        assert united_states.name == "United States"

    def test_returns_expected_countries(self):
        supported_countries = holiday_engine.get_supported_countries()
        supported_countries_set = {c.abbreviation for c in supported_countries}
        assert {"GB", "MX", "US"}.intersection(supported_countries_set)


class TestGetCachedSupportedCountries(unittest.TestCase):
    def test_cached_supported_countries_included_expected_countries(self):
        cached_countries = holiday_engine._cached_supported_countries
        assert {"GB", "MX", "US"}.intersection(set(cached_countries))


class TestGetUpcomingHolidays(unittest.TestCase):
    def test_handles_no_holidays(self):
        non_us_holiday = dt.date(year=2022, month=9, day=1)
        upcoming_holidays = holiday_engine.get_upcoming_holidays(
            "US", non_us_holiday, non_us_holiday
        )
        assert upcoming_holidays == []

    def test_handles_single_holiday(self):
        upcoming_holidays = holiday_engine.get_upcoming_holidays(
            "US", US_INDEPENDENCE_DAY, US_INDEPENDENCE_DAY
        )
        assert len(upcoming_holidays) == 1
        upcoming_holiday, *_ = upcoming_holidays
        assert upcoming_holiday.country_abbreviation == "US"
        assert upcoming_holiday.date == US_INDEPENDENCE_DAY
        assert upcoming_holiday.holiday_name == "Independence Day"

    def test_handles_multiple_holidays(self):
        upcoming_holidays = holiday_engine.get_upcoming_holidays(
            "US", NEW_YEARS_DAY, dt.date(year=2023, month=1, day=2)
        )
        assert len(upcoming_holidays) == 2
        new_years_day, new_years_day_observed = upcoming_holidays
        assert new_years_day.holiday_name == "New Year's Day"
        assert new_years_day_observed.holiday_name == "New Year's Day (Observed)"


class TestIsHoliday(unittest.TestCase):
    def test_returns_expected_response(self):
        param_list = [
            (dt.datetime(2022, 7, 3), False),
            (dt.datetime(2022, 7, 4), True),
            (dt.datetime(2022, 7, 5), False),
        ]
        for date, expected_result in param_list:
            with self.subTest():
                holiday_decision: bool = holiday_engine.is_holiday("US", date)
                assert holiday_decision is expected_result
