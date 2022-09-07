import datetime as dt

import pytest

from src.logic import HolidayEngine, holiday_engine


def test_get_cached_country_holidays_handles_cache_miss():
    # need to ensure a cold start
    engine_instance = HolidayEngine()
    assert engine_instance.is_holiday("US", dt.datetime(2022, 7, 4)) is True


def test_get_cached_country_holidays_handles_cache_hit():
    # need to ensure a cold start
    engine_instance = HolidayEngine()
    assert engine_instance.is_holiday("US", dt.datetime(2022, 7, 4)) is True
    assert engine_instance.is_holiday("US", dt.datetime(2022, 7, 4)) is True


@pytest.mark.parametrize(
    "date,holiday_name",
    [
        (dt.datetime(2022, 7, 4), "Independence Day"),
        (dt.datetime(2022, 9, 5), "Labor Day"),
    ],
)
def test_get_holiday_name_returns_expected_response(date: dt.date, holiday_name: str):
    assert holiday_engine.get_holiday_name("US", date) == holiday_name


def test_get_supported_countries_returns_expected_country_detail():
    supported_countries = holiday_engine.get_supported_countries()
    united_states, *_ = [c for c in supported_countries if c.alpha_2 == "US"]
    assert united_states.flag == "🇺🇸"
    assert united_states.name == "United States"


def test_get_supported_countries_returns_expected_countries():
    supported_countries = holiday_engine.get_supported_countries()
    supported_countries_set = {c.alpha_2 for c in supported_countries}
    assert {"GB", "MX", "US"}.intersection(supported_countries_set)


def test_cached_supported_countries_included_expected_countries():
    cached_countries = holiday_engine._cached_supported_countries
    assert {"GB", "MX", "US"}.intersection(set(cached_countries))


@pytest.mark.parametrize(
    "date,expected_result",
    [
        (dt.datetime(2022, 7, 3), False),
        (dt.datetime(2022, 7, 4), True),
        (dt.datetime(2022, 7, 5), False),
    ],
)
def test_is_holiday_returns_expected_response(date: dt.date, expected_result: bool):
    holiday_decision: bool = holiday_engine.is_holiday("US", date)
    assert holiday_decision is expected_result
