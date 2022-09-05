from test.logic.test_data import MOCK_HOLIDAYS_MODULE_SUPPORTED_COUNTRIES
from test.utilities import sanitize_mock_path
from unittest.mock import MagicMock, patch

from pytest import fixture

import src.logic.holiday_engine as holiday_engine


@fixture(autouse=True)
def mock_holidays_module():
    path = sanitize_mock_path("src/logic/holiday_engine.py")
    with patch(f"{path}.holidays") as mock_holidays_module:
        mock_holidays_module.list_supported_countries.return_value = (
            MOCK_HOLIDAYS_MODULE_SUPPORTED_COUNTRIES
        )
        yield mock_holidays_module


def test_get_cached_country_holidays_handles_cache_miss():
    ...


def test_get_cached_country_holidays_handles_cache_hit():
    ...


def test_get_holiday_name_returns_expected_response():
    ...


def test_get_supported_countries_returns_expected_response():
    ...


def test_cached_supported_countries_works_as_expected():
    engine = holiday_engine.HolidayEngine()
    supported_countries = engine._cached_supported_countries
    assert set(supported_countries) == {"GB", "MX", "US"}


def test_is_holiday_returns_expected_response():
    ...
