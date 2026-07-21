"""Period resolution.

`now` is always passed in explicitly rather than read from the system clock,
so that the CLI can anchor "this month" / "last month" to the latest day
actually present in the (fixed, reproducible) simulated dataset instead of
the real wall-clock date. See docs/05_Architecture.md, decision D3.
"""

from __future__ import annotations

from calendar import monthrange
from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class Period:
    label: str
    start: date
    end: date

    def __post_init__(self) -> None:
        if self.start > self.end:
            raise ValueError(f"Period start {self.start} is after end {self.end}")

    @property
    def days(self) -> int:
        return (self.end - self.start).days + 1


def current_month(now: date) -> Period:
    start = date(now.year, now.month, 1)
    return Period(label="este mes", start=start, end=now)


def previous_month(now: date) -> Period:
    first_of_this_month = date(now.year, now.month, 1)
    last_day_prev_month = first_of_this_month - timedelta(days=1)
    start = date(last_day_prev_month.year, last_day_prev_month.month, 1)
    return Period(label="el mes anterior", start=start, end=last_day_prev_month)


def last_n_days(now: date, n: int) -> Period:
    start = now - timedelta(days=n - 1)
    return Period(label=f"los últimos {n} días", start=start, end=now)


def today(now: date) -> Period:
    return Period(label="hoy", start=now, end=now)
