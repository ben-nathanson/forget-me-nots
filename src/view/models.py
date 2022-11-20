import datetime as dt
from http import HTTPStatus

import humps  # noqa, PyCharm confuses pyhumps and humps packages
import pycountry
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, root_validator


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
                detail="Country abbreviation should be a string.",
            )

        if len(v) > 2:
            raise HTTPException(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                detail="Country abbreviation should be no more than two characters.",
            )

        country = pycountry.countries.get(alpha_2=v)
        if country is None:
            raise HTTPException(
                HTTPStatus.NOT_IMPLEMENTED, detail=f"'{v}' has not been implemented."
            )
        return v


class UpcomingHolidaysPayload(ViewModel):
    country_abbreviation: CountryAbbreviation
    start_date: dt.date
    end_date: dt.date

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
                "startDate": dt.date.today(),
                "endDate": dt.date.today() + dt.timedelta(weeks=26),
            }
        }


class HolidayBasePayload(ViewModel):
    country_abbreviation: CountryAbbreviation
    date: dt.date = dt.date.today()  # type: ignore

    class Config:
        schema_extra = {
            "example": {
                "date": dt.date(year=2022, month=9, day=5),
                "countryAbbreviation": "US",
            }
        }


class IsHolidayResponse(ViewModel):
    holiday_name: str
    is_holiday: bool

    class Config:
        schema_extra = {"example": {"holidayName": "Labor Day", "isHoliday": True}}


class Holiday(ViewModel):
    holiday_name: str
    date: dt.date
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


class CreateUserPayload(ViewModel):
    email: EmailStr
    password: str


class CreateUserResponse(ViewModel):
    email: EmailStr


class LoginPayload(ViewModel):
    email: EmailStr
    password: str


class LoginResponse(ViewModel):
    email: EmailStr
    expires_in: int
    id_token: str
    access_token: str
