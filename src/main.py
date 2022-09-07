from fastapi import FastAPI
from pydantic import BaseModel

import src.view.models as view_models
from src.logic import holiday_engine


class NotImplementedResponse(BaseModel):
    message: str = "Not implemented"


app = FastAPI(title="Forget Me Nots")


@app.post(
    "/is-it-a-holiday",
    response_model=view_models.IsHolidayResponse,
    responses={501: {"model": NotImplementedResponse}},
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


@app.get("/supported-countries", response_model=list[view_models.CountryResponse])
def supported_countries():
    return [
        view_models.CountryResponse(
            country_abbreviation=country.alpha_2, name=country.name, flag=country.flag
        )
        for country in holiday_engine.get_supported_countries()
    ]
