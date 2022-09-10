import datetime as dt
from http import HTTPStatus
from typing import Optional

import humps  # noqa, PyCharm confuses pyhumps and humps packages
import pycountry
from fastapi import HTTPException
from pydantic import BaseModel, root_validator

DATE_FORMAT: str = "%d-%m-%Y"  # day-month-year, e.g. 05-09-2022


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
            raise HTTPException(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=f"Country abbreviation should be a string.",
            )

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


class Date(dt.date):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, (str, dt.date, dt.datetime)):
            raise HTTPException(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=f"Unrecognized date format, expected {DATE_FORMAT}.",
            )

        if isinstance(v, str):
            try:
                v = dt.datetime.strptime(v, DATE_FORMAT)
            except ValueError as e:
                raise HTTPException(
                    HTTPStatus.UNPROCESSABLE_ENTITY,
                    detail=f"Unrecognized date format, expected {DATE_FORMAT}.",
                )
        return dt.date(v.year, v.month, v.day)


class UpcomingHolidaysPayload(ViewModel):
    country_abbreviation: CountryAbbreviation
    start_date: Optional[Date]
    end_date: Optional[Date]

    @root_validator(pre=True)
    def dates_must_be_populated(cls, values):
        start_date, end_date = values.get("start_date"), values.get("end_date")
        if start_date is None:
            start_date = dt.date.today()

        if end_date is None:
            six_months = dt.timedelta(weeks=26)
            end_date = start_date + six_months

        if end_date < start_date:
            raise HTTPException(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                detail="End date cannot exceed start date.",
            )

        values["start_date"], values["end_date"] = start_date, end_date
        return values

    class Config:
        schema_extra = {
            "example": {
                "countryAbbreviation": "US",
                "startDate": dt.date.today().strftime(DATE_FORMAT),
                "endDate": (dt.date.today() + dt.timedelta(weeks=26)).strftime(
                    DATE_FORMAT
                ),
            }
        }


class HolidayBasePayload(ViewModel):
    country_abbreviation: CountryAbbreviation
    date: Date = dt.date.today()  # type: ignore

    class Config:
        schema_extra = {"example": {"date": "05-09-2022", "countryAbbreviation": "US"}}


class IsHolidayResponse(ViewModel):
    holiday_name: str
    is_holiday: bool

    class Config:
        schema_extra = {"example": {"holidayName": "Labor Day", "isHoliday": True}}


class Holiday(ViewModel):
    holiday_name: str
    date: Date
    country_abbreviation: CountryAbbreviation


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


class NotImplementedResponse(BaseModel):
    message: str = "Not implemented"
