import datetime as dt
from typing import Optional

import holidays
import pycountry  # noqa, Pycharm is confused

import src.logic.models as logic_models


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
            # TODO this can raise NotImplemented because holidays doesn't support all
            # countries in the pycountry db.
            # Need to either update the CountryAbbreviation model to prevent this from
            # getting past the route handler
            country_holidays = holidays.country_holidays(country_code)
            # primes holidays to actually fetch its list of holidays
            current_year: int = dt.date.today().year
            one_hundred_years_ago: int = current_year - 100
            one_hundred_years_from_now: int = current_year + 100
            for year in range(one_hundred_years_ago, one_hundred_years_from_now):
                country_holidays.get(f"01-01-{str(year)}")
            self._country_holidays_cache[country_code] = country_holidays
            return country_holidays

        return cached_holidays

    def get_holiday_name(self, country_code: str, date: dt.date) -> str:
        country_holidays = self._get_cached_country_holidays(country_code)
        return country_holidays.get(date) if date in country_holidays else ""

    # TODO define a custom model or find a way to get a better type hint from pycountry
    def get_supported_countries(self) -> list:
        supported_countries = [
            pycountry.countries.get(alpha_2=abbreviation)
            for abbreviation in self._cached_supported_countries
        ]
        return supported_countries

    def get_upcoming_holidays(
        self, country_code: str, start: dt.date, end: dt.date
    ) -> list[logic_models.Holiday]:
        country_holidays = self._get_cached_country_holidays(country_code)
        upcoming_holiday_dates: list[dt.date] = sorted(
            [
                day
                for day in country_holidays
                if start <= dt.date(day.year, day.month, day.day) <= end
            ]
        )
        return [
            logic_models.Holiday(country_holidays.get(day), day, country_code)
            for day in upcoming_holiday_dates
        ]

    def is_holiday(self, country_code: str, date: dt.date) -> bool:
        country_holidays = self._get_cached_country_holidays(country_code)
        _is_holiday: bool = date in country_holidays
        return _is_holiday
