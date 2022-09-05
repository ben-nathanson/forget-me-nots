import datetime as dt

import holidays
import pycountry  # noqa, Pycharm is confused


def get_supported_countries() -> list:
    country_abbreviations = holidays.list_supported_countries().keys()
    supported_countries = [
        pycountry.countries.get(alpha_2=abbreviation)
        for abbreviation in country_abbreviations
    ]
    return supported_countries


def get_holiday_name(country_code: str, date: dt.date) -> str:
    country_holidays = holidays.country_holidays(country_code)
    return country_holidays.get(date) if date in country_holidays else ""


def is_holiday(country_code: str, date: dt.date) -> bool:
    country_holidays = holidays.country_holidays(country_code)
    _is_holiday: bool = date in country_holidays
    return _is_holiday
