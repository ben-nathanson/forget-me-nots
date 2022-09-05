from http import HTTPStatus

import holidays
from fastapi import HTTPException
from holidays import HolidayBase


def get_country_holidays_safely(country_code: str) -> HolidayBase:
    try:
        country_holidays: HolidayBase = holidays.country_holidays(country_code)
        return country_holidays
    except NotImplementedError:
        raise HTTPException(HTTPStatus.NOT_IMPLEMENTED)
