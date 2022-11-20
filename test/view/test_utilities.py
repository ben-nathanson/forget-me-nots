from http import HTTPStatus

import holidays
import pytest
from fastapi import HTTPException

from src.view.utilities import get_country_holidays_safely


class TestGetCountryHolidaysSafely:
    def test_handles_not_implemented(self):
        with pytest.raises(HTTPException) as exception:
            get_country_holidays_safely("NONEXISTENT")

        assert exception.value.status_code == HTTPStatus.NOT_IMPLEMENTED
        assert exception.value.detail == "Not Implemented"

    def test_returns_expected_object(self):
        country_holidays = get_country_holidays_safely("US")
        assert type(country_holidays) == holidays.countries.united_states.US
