import datetime as dt
from http import HTTPStatus
from typing import Optional

import humps  # noqa, PyCharm confuses pyhumps and humps packages
import pycountry
from fastapi import HTTPException
from pydantic import BaseModel, validator


def _convert_to_camel_case(string: str) -> str:
    return humps.camelize(string)  # type: ignore


class ViewModel(BaseModel):
    class Config:
        alias_generator = _convert_to_camel_case
        allow_population_by_field_name = True


class HolidayBasePayload(ViewModel):
    country_abbreviation: str
    date: dt.date = dt.date.today()

    @validator("country_abbreviation", pre=True)
    def must_be_supported(cls, v):
        country = pycountry.countries.get(alpha_2=v)
        if country is None:
            raise HTTPException(
                HTTPStatus.NOT_IMPLEMENTED, detail=f"'{v}' has not been implemented."
            )
        return v

    class Config:
        schema_extra = {"example": {"date": "2022-09-05", "countryAbbreviation": "US"}}


class IsHolidayResponse(ViewModel):
    holiday_name: str
    is_holiday: bool

    class Config:
        schema_extra = {"example": {"holidayName": "Labor Day", "isHoliday": True}}


class CountryResponse(ViewModel):
    abbreviation: str
    name: str
    flag: str

    class Config:
        schema_extra = {
            "example": {"abbreviation": "US", "name": "United States", "flag": "🇺🇸"},
        }


class SupportedCountriesResponse(ViewModel):
    countries: list[CountryResponse]
