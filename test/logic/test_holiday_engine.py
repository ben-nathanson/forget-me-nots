from src.logic import holiday_engine


def test_get_cached_country_holidays_handles_cache_miss():
    ...


def test_get_cached_country_holidays_handles_cache_hit():
    ...


def test_get_holiday_name_returns_expected_response():
    ...


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


def test_is_holiday_returns_expected_response():
    ...
