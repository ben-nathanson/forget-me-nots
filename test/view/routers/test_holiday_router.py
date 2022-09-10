class TestIsItAHoliday:
    def test_returns_expected_response(self):
        ...
        # param_list = [
        #     (dt.datetime(2022, 7, 3), False),
        #     (dt.datetime(2022, 7, 4), True),
        #     (dt.datetime(2022, 7, 5), False),
        # ]
        # for date, expected_result in param_list:
        #     with self.subTest():
        #         holiday_decision: bool = holiday_engine.is_holiday("US", date)
        #         assert holiday_decision is expected_result


class TestSupportedCountries:
    def test_returns_expected_country_detail(self):
        ...
        # supported_countries = holiday_engine.get_supported_countries()
        # united_states, *_ = [c for c in supported_countries if c.alpha_2 == "US"]
        # assert united_states.flag == "🇺🇸"
        # assert united_states.name == "United States"

    def test_returns_expected_countries(self):
        ...
        # supported_countries = holiday_engine.get_supported_countries()
        # supported_countries_set = {c.alpha_2 for c in supported_countries}
        # assert {"GB", "MX", "US"}.intersection(supported_countries_set)


class TestUpcomingHolidays:
    def test_handles_no_holidays(self):
        ...
        # non_us_holiday = dt.date(year=2022, month=9, day=1)
        # upcoming_holidays = holiday_engine.get_upcoming_holidays(
        #     "US", non_us_holiday, non_us_holiday
        # )
        # assert upcoming_holidays == []

    def test_handles_single_holiday(self):
        ...
        # upcoming_holidays = holiday_engine.get_upcoming_holidays(
        #     "US", US_INDEPENDENCE_DAY, US_INDEPENDENCE_DAY
        # )
        # assert len(upcoming_holidays) == 1
        # upcoming_holiday, *_ = upcoming_holidays
        # assert upcoming_holiday.country_abbreviation == "US"
        # assert upcoming_holiday.date == US_INDEPENDENCE_DAY
        # assert upcoming_holiday.holiday_name == "Independence Day"

    def test_handles_multiple_holidays(self):
        ...
        # upcoming_holidays = holiday_engine.get_upcoming_holidays(
        #     "US", NEW_YEARS_DAY, dt.date(year=2023, month=1, day=2)
        # )
        # assert len(upcoming_holidays) == 2
        # new_years_day, new_years_day_observed = upcoming_holidays
        # assert new_years_day.holiday_name == "New Year's Day"
        # assert new_years_day_observed.holiday_name == "New Year's Day (Observed)"
