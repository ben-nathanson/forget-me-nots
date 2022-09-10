from fastapi import APIRouter

import src.view.models as view_models
from src.logic import holiday_engine
from src.logic.models import DateRange

holiday_router = APIRouter(
    prefix="/holidays",
    tags=["holidays"],
)


@holiday_router.post(
    "/is-it-a-holiday",
    response_model=view_models.IsHolidayResponse,
    responses={501: {"model": view_models.NotImplementedResponse}},
)
def is_it_a_holiday(payload: view_models.HolidayBasePayload):
    return view_models.IsHolidayResponse(
        is_holiday=holiday_engine.is_holiday(
            payload.country_abbreviation, payload.date
        ),
        holiday_name=holiday_engine.get_holiday_name(
            payload.country_abbreviation, payload.date
        ),
    )


@holiday_router.get(
    "/supported-countries", response_model=list[view_models.CountryResponse]
)
def supported_countries():
    return [
        view_models.CountryResponse(
            country_abbreviation=country.alpha_2, name=country.name, flag=country.flag
        )
        for country in holiday_engine.get_supported_countries()
    ]


@holiday_router.post(
    "/upcoming-holidays",
    response_model=list[view_models.Holiday],
    responses={501: {"model": view_models.NotImplementedResponse}},
)
def upcoming_holidays(payload: view_models.UpcomingHolidaysPayload):
    upcoming_holiday_results = holiday_engine.get_upcoming_holidays(
        payload.country_abbreviation,
        DateRange(payload.start_date, payload.end_date),  # type: ignore
    )
    return [
        view_models.Holiday(
            country_abbreviation=holiday.country_abbreviation,
            date=holiday.date,
            holiday_name=holiday.holiday_name,
        )
        for holiday in upcoming_holiday_results
    ]
