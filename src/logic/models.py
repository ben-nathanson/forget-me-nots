import datetime as dt
from dataclasses import dataclass


@dataclass
class Holiday:
    holiday_name: str
    date: dt.date
    country_abbreviation: str


@dataclass
class DateRange:
    start: dt.date
    end: dt.date
