import src.logic.holiday_engine as holiday_engine


def test_get_cached_country_holidays_handles_cache_miss():
    ...


def test_get_cached_country_holidays_handles_cache_hit():
    ...


def test_get_holiday_name_returns_expected_response():
    ...


def test_get_supported_countries_returns_expected_response():
    ...


def test_cached_supported_countries_included_expected_countries():
    engine = holiday_engine.HolidayEngine()
    cached_countries = engine._cached_supported_countries
    assert {"GB", "MX", "US"}.intersection(set(cached_countries))


def test_is_holiday_returns_expected_response():
    ...
