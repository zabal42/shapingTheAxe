from __future__ import annotations

from datetime import date

import pytest

from copilot.periods import Period, current_month, last_n_days, previous_month, today


def test_current_month_starts_on_day_one_and_ends_at_now():
    now = date(2026, 7, 20)
    period = current_month(now)
    assert period.start == date(2026, 7, 1)
    assert period.end == now


def test_previous_month_is_the_full_prior_calendar_month():
    now = date(2026, 7, 20)
    period = previous_month(now)
    assert period.start == date(2026, 6, 1)
    assert period.end == date(2026, 6, 30)


def test_previous_month_handles_january_year_rollover():
    now = date(2026, 1, 15)
    period = previous_month(now)
    assert period.start == date(2025, 12, 1)
    assert period.end == date(2025, 12, 31)


def test_last_n_days_is_inclusive_of_today():
    now = date(2026, 7, 20)
    period = last_n_days(now, 30)
    assert period.days == 30
    assert period.end == now
    assert period.start == date(2026, 6, 21)


def test_today_period_is_a_single_day():
    now = date(2026, 7, 20)
    period = today(now)
    assert period.start == period.end == now
    assert period.days == 1


def test_period_rejects_start_after_end():
    with pytest.raises(ValueError):
        Period(label="invalid", start=date(2026, 2, 1), end=date(2026, 1, 1))
