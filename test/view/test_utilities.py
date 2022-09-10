from http import HTTPStatus
from test.utilities import sanitize_mock_path
from unittest import mock

import pytest
from fastapi import HTTPException

from src.view.utilities import get_country_holidays_safely


@pytest.fixture(autouse=False)
def mock_holidays():
    with mock.patch(f"{sanitize_mock_path('src/view/utilities.py')}.holidays") as m:
        yield m


def test_get_country_holidays_safely_handles_not_implemented(mock_holidays):
    mock_holidays.country_holidays.side_effect = NotImplementedError
    with pytest.raises(HTTPException) as exception:
        get_country_holidays_safely("US")

    assert exception.value.status_code == HTTPStatus.NOT_IMPLEMENTED
    assert exception.value.detail == "Not Implemented"


def test_get_country_holidays_safely_returns_expected_holidays():
    ...
