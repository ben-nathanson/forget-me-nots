import datetime as dt
from http import HTTPStatus

import humps  # noqa, PyCharm confuses pyhumps and humps packages
import pycountry
from fastapi import HTTPException
from pydantic import BaseModel


def _convert_to_camel_case(string: str) -> str:
    return humps.camelize(string)  # type: ignore


class ViewModel(BaseModel):
    class Config:
        alias_generator = _convert_to_camel_case
        allow_population_by_field_name = True


class CountryAbbreviation(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("String required")

        if len(v) > 2:
            raise HTTPException(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=f"Country abbreviation should be no more than two characters.",
            )

        country = pycountry.countries.get(alpha_2=v)
        if country is None:
            raise HTTPException(
                HTTPStatus.NOT_IMPLEMENTED, detail=f"'{v}' has not been implemented."
            )
        return v


class HolidayBasePayload(ViewModel):
    country_abbreviation: CountryAbbreviation
    date: dt.date = dt.date.today()

    class Config:
        schema_extra = {"example": {"date": "2022-09-05", "countryAbbreviation": "US"}}


class IsHolidayResponse(ViewModel):
    holiday_name: str
    is_holiday: bool

    class Config:
        schema_extra = {"example": {"holidayName": "Labor Day", "isHoliday": True}}


class CountryResponse(ViewModel):
    country_abbreviation: CountryAbbreviation
    name: str
    flag: str

    class Config:
        schema_extra = {
            "example": {"abbreviation": "US", "name": "United States", "flag": "🇺🇸"},
        }


class SupportedCountriesResponse(ViewModel):
    countries: list[CountryResponse]
