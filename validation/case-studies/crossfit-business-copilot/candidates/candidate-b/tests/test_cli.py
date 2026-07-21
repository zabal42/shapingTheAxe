from __future__ import annotations

from datetime import date

import pytest

from copilot.cli import EmptyDatasetError, _dataset_anchor_day, answer_question, main
from copilot.datasource.memory import InMemoryDataSource


def test_dataset_anchor_day_returns_the_latest_session_day(scripted_data_source):
    assert _dataset_anchor_day(scripted_data_source) == date(2026, 1, 6)


def test_regression_empty_dataset_raises_instead_of_using_the_real_clock():
    # Finding #4 (code review): _dataset_anchor_day used to silently fall
    # back to date.today() when there were no sessions, contradicting the
    # documented determinism guarantee (docs/05_Architecture.md, D3). It
    # must now fail loudly and explicitly instead.
    empty = InMemoryDataSource(clients=[], sessions=[], bookings=[])
    with pytest.raises(EmptyDatasetError):
        _dataset_anchor_day(empty)


def test_regression_main_reports_empty_dataset_gracefully(monkeypatch, capsys):
    monkeypatch.setattr(
        "copilot.cli.MockDataSource",
        lambda: InMemoryDataSource(clients=[], sessions=[], bookings=[]),
    )
    main([])  # no crash / traceback
    captured = capsys.readouterr()
    assert "Error" in captured.out
    assert "generate_dataset" in captured.out


def test_regression_explicit_zero_top_n_is_honored_not_defaulted(scripted_data_source):
    # Finding #7: cli.py used `routed.top_n or 3`, so a legitimately-parsed
    # 0 was silently replaced by the default instead of being honored.
    # With top_n=0 honored, lowest_occupancy_classes returns zero rows even
    # though the period has classes to rank.
    now = date(2026, 1, 31)
    rendered = answer_question(scripted_data_source, "Dame las 0 clases con menor ocupación este mes.", now)
    assert "(sin filas — ver limitaciones)" in rendered


def test_regression_explicit_zero_inactivity_days_is_honored_not_defaulted(inactivity_data_source):
    now = date(2026, 2, 1)
    rendered = answer_question(
        inactivity_data_source, "¿Qué usuarios llevan más de 0 días sin asistir?", now
    )
    # With a 0-day cutoff, even client 1 (last booking 2026-01-25, i.e. 7
    # days before as_of) counts as "inactive" under the requested threshold.
    assert "Cliente1" in rendered
