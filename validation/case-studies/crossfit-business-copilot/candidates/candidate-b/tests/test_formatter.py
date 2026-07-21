from __future__ import annotations

from datetime import date

from copilot import metrics
from copilot.datasource.memory import InMemoryDataSource
from copilot.formatter import format_answer
from copilot.periods import Period


def test_regression_compare_periods_with_an_empty_side_does_not_render_literal_none(scripted_data_source):
    # Finding #6 (code review): comparing a period with data against a
    # period with zero scheduled sessions used to render the literal text
    # "None%" instead of an explanatory fallback.
    period_with_data = Period(label="con datos", start=date(2026, 1, 5), end=date(2026, 1, 5))
    empty_period = Period(label="vacío", start=date(2026, 3, 1), end=date(2026, 3, 31))

    answer = metrics.compare_periods(scripted_data_source, period_with_data, empty_period)
    rendered = format_answer(answer)

    assert "None%" not in rendered
    assert "sin datos" in rendered


def test_average_occupancy_result_renders_the_percentage(scripted_data_source):
    answer = metrics.average_occupancy(
        scripted_data_source, Period(label="p", start=date(2026, 1, 5), end=date(2026, 1, 6))
    )
    rendered = format_answer(answer)
    assert "56.7%" in rendered


def test_no_sessions_answer_never_renders_a_bare_none(scripted_data_source):
    empty = InMemoryDataSource(clients=[], sessions=[], bookings=[])
    answer = metrics.average_occupancy(empty, Period(label="p", start=date(2026, 1, 1), end=date(2026, 1, 31)))
    rendered = format_answer(answer)
    assert "None" not in rendered
