import datetime as dt
from typing import Optional, Union

import holidays
import pycountry  # noqa, Pycharm is confused

import src.logic.models as logic_models

holiday_date = Union[dt.date, str]


class HolidayEngine:
    def __init__(self):
        self._country_holidays_cache: dict[str, holidays.HolidayBase] = dict()
        self._cached_supported_countries: list[str] = list(
            holidays.list_supported_countries().keys()
        )

    def _get_cached_country_holidays(self, country_code: str) -> holidays.HolidayBase:
        cached_holidays: Optional[
            holidays.HolidayBase
        ] = self._country_holidays_cache.get(country_code, None)

        if cached_holidays is None:
            country_holidays = holidays.country_holidays(country_code)
            self._country_holidays_cache[country_code] = country_holidays
            return country_holidays

        return cached_holidays

    def get_holiday_name(self, country_code: str, date: holiday_date) -> str:
        country_holidays = self._get_cached_country_holidays(country_code)
        return country_holidays.get(date) if date in country_holidays else ""

    def get_supported_countries(self) -> list:
        supported_countries = [
            pycountry.countries.get(alpha_2=abbreviation)
            for abbreviation in self._cached_supported_countries
        ]
        return supported_countries

    def get_upcoming_holidays(
        self, country_code: str, start: holiday_date, end: holiday_date
    ) -> list[logic_models.Holiday]:
        return []

    def is_holiday(self, country_code: str, date: holiday_date) -> bool:
        country_holidays = self._get_cached_country_holidays(country_code)
        _is_holiday: bool = date in country_holidays
        return _is_holiday
