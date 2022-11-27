import datetime as dt
import uuid
from http import HTTPStatus

import humps  # noqa, PyCharm confuses pyhumps and humps packages
import pycountry
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field, root_validator

from src.logic import holiday_engine
from src.logic.services.account_management import generate_strong_password


def _convert_to_camel_case(string: str) -> str:
    return humps.camelize(string)  # type: ignore


EXAMPLE_EMAIL = f"ben+{str(uuid.uuid4())}@nathanson.dev"
EXAMPLE_PASSWORD = generate_strong_password()
SUPPORTED_COUNTRY_ABBREVIATIONS: list[str] = [
    c.abbreviation for c in holiday_engine.get_supported_countries()
]


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
            raise ValueError("Country abbreviation should be a string.")

        if len(v) > 2:
            raise ValueError(
                "Country abbreviation should be no more than two characters."
            )

        country = pycountry.countries.get(alpha_2=v)
        if country is None:
            raise NotImplementedError(f"'{v}' has not been implemented.")

        if country.alpha_2 not in SUPPORTED_COUNTRY_ABBREVIATIONS:
            raise NotImplementedError(f"'{v}' has not been implemented.")
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
        json_encoders = {
            CountryAbbreviation: lambda c: c,
            dt.date: lambda d: str(d.isoformat()),
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
    password: str = Field(
        min_length=6,
        max_length=100,
        description="A password containing between 6 and 100 characters, including at "
        "least one lowercase letter, one uppercase letter, one number, "
        "and one special character",
    )

    class Config:
        schema_extra = {
            "example": {"email": EXAMPLE_EMAIL, "password": EXAMPLE_PASSWORD}
        }


class LoginPayload(ViewModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {"email": EXAMPLE_EMAIL, "password": EXAMPLE_PASSWORD}
        }


class LoginResponse(ViewModel):
    email: EmailStr
    expires_in: int
    id_token: str
    access_token: str
