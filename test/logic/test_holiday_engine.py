import datetime as dt
import unittest

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
        united_states, *_ = [c for c in supported_countries if c.alpha_2 == "US"]
        assert united_states.flag == "🇺🇸"
        assert united_states.name == "United States"

    def test_returns_expected_countries(self):
        supported_countries = holiday_engine.get_supported_countries()
        supported_countries_set = {c.alpha_2 for c in supported_countries}
        assert {"GB", "MX", "US"}.intersection(supported_countries_set)


class TestGetCachedSupportedCountries(unittest.TestCase):
    def test_cached_supported_countries_included_expected_countries(self):
        cached_countries = holiday_engine._cached_supported_countries
        assert {"GB", "MX", "US"}.intersection(set(cached_countries))


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
