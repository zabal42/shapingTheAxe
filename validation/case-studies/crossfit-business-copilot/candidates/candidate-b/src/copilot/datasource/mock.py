"""Mock data source.

Loads the simulated, reproducible dataset committed under `data/`, parses it
into domain objects, and delegates all querying to `InMemoryDataSource`.
This is the only data source used by the MVP (Core Constraint: simulated
data only, no real API access).
"""

from __future__ import annotations

import json
from datetime import date, datetime, time
from pathlib import Path

from copilot.datasource.memory import InMemoryDataSource
from copilot.domain import Booking, ClassSession, Client

DEFAULT_DATA_DIR = Path(__file__).resolve().parents[3] / "data"


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


def _parse_optional_date(value: str | None) -> date | None:
    return _parse_date(value) if value else None


def _parse_time(value: str) -> time:
    return time.fromisoformat(value)


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _parse_optional_datetime(value: str | None) -> datetime | None:
    return _parse_datetime(value) if value else None


class MockDataSource(InMemoryDataSource):
    def __init__(self, data_dir: Path | str = DEFAULT_DATA_DIR) -> None:
        data_dir = Path(data_dir)

        clients_raw = json.loads((data_dir / "clients.json").read_text())
        sessions_raw = json.loads((data_dir / "sessions.json").read_text())
        bookings_raw = json.loads((data_dir / "bookings.json").read_text())

        clients = [
            Client(
                id=c["id"],
                first_name=c["first_name"],
                last_name=c["last_name"],
                joined_on=_parse_date(c["joined_on"]),
                deactivated_on=_parse_optional_date(c.get("deactivated_on")),
            )
            for c in clients_raw
        ]

        sessions = [
            ClassSession(
                id=s["id"],
                class_id=s["class_id"],
                class_name=s["class_name"],
                day=_parse_date(s["day"]),
                time=_parse_time(s["time"]),
                duration_minutes=s["duration_minutes"],
                capacity=s["capacity"],
            )
            for s in sessions_raw
        ]

        bookings = [
            Booking(
                id=b["id"],
                client_id=b["client_id"],
                session_id=b["session_id"],
                state=b["state"],
                attended=b["attended"],
                booked_at=_parse_datetime(b["booked_at"]),
                cancelled_at=_parse_optional_datetime(b.get("cancelled_at")),
            )
            for b in bookings_raw
        ]

        super().__init__(clients=clients, sessions=sessions, bookings=bookings)
