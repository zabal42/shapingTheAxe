"""Generates the simulated, reproducible dataset used by the MVP.

Run with: python scripts/generate_dataset.py

Deterministic by construction (AC-02): a fixed random seed and a fixed
history window mean re-running this script always produces byte-identical
output. The window's end date is a fixed constant, not "today" — so the
demo dataset does not silently change depending on when it is regenerated
or when the CLI is later run (see docs/05_Architecture.md, decision D3).
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

SEED = 1337
ANCHOR_DAY = date(2026, 7, 20)  # fixed "latest day" of the simulated dataset
HISTORY_DAYS = 180  # ~6 months of history ending at ANCHOR_DAY
DATA_DIR = Path(__file__).resolve().parents[1] / "data"

FIRST_NAMES = [
    "Laura", "Carlos", "Marta", "Javier", "Lucia", "Diego", "Sara", "Pablo",
    "Elena", "Alvaro", "Nuria", "Sergio", "Cristina", "Ruben", "Paula",
    "Adrian", "Irene", "Hugo", "Marina", "Daniel", "Andrea", "Victor",
    "Beatriz", "Raul", "Silvia", "Mario", "Carmen", "Ivan", "Alba", "Jorge",
    "Rocio", "Fernando", "Noelia", "Oscar", "Patricia", "Guillermo",
    "Monica", "Alberto", "Eva", "Manuel",
]
LAST_NAMES = [
    "Garcia", "Martinez", "Lopez", "Sanchez", "Perez", "Gomez", "Fernandez",
    "Ruiz", "Diaz", "Moreno", "Alvarez", "Romero", "Navarro", "Torres",
    "Dominguez", "Vazquez", "Ramos", "Gil", "Serrano", "Blanco",
]

# Weekly template: weekday (0=Mon..6=Sun) -> list of
# (time, class_name, duration_min, capacity, target_fill, cancel_rate)
WEEKLY_TEMPLATE: dict[int, list[tuple[str, str, int, int, float, float]]] = {}
for wd in range(5):  # Mon-Fri
    WEEKLY_TEMPLATE[wd] = [
        ("07:00", "WOD", 60, 12, 0.85, 0.25),
        ("09:00", "Movilidad", 60, 10, 0.25, 0.10),
        ("12:00", "WOD", 60, 12, 0.80, 0.12),
        ("17:00", "Halterofilia", 60, 8, 0.60, 0.08),
        ("18:00", "WOD", 60, 15, 0.90, 0.06),
        ("19:00", "Gimnasia", 60, 10, 0.55, 0.07),
        ("20:00", "WOD", 60, 15, 0.85, 0.05),
    ]
WEEKLY_TEMPLATE[5] = [  # Saturday
    ("10:00", "CrossFit Kids", 45, 8, 0.50, 0.09),
    ("11:00", "Open Box", 90, 20, 0.35, 0.10),
]
WEEKLY_TEMPLATE[6] = []  # Sunday: box closed

CLASS_IDS = {
    name: idx
    for idx, name in enumerate(
        ["WOD", "Movilidad", "Halterofilia", "Gimnasia", "CrossFit Kids", "Open Box"],
        start=1,
    )
}


@dataclass
class GenClient:
    id: int
    first_name: str
    last_name: str
    joined_on: date
    deactivated_on: date | None
    # Days before ANCHOR_DAY this client's activity stops (None = active through the end).
    inactive_since_days_before_anchor: int | None


def build_clients(rng: random.Random) -> list[GenClient]:
    clients: list[GenClient] = []
    n_clients = 40
    for i in range(1, n_clients + 1):
        first = FIRST_NAMES[(i - 1) % len(FIRST_NAMES)]
        last = LAST_NAMES[(i - 1) % len(LAST_NAMES)]
        joined_on = ANCHOR_DAY - timedelta(days=rng.randint(200, 900))

        deactivated_on = None
        if i in (5, 14, 23, 31):  # 4 deactivated (former) clients
            deactivated_on = ANCHOR_DAY - timedelta(days=rng.randint(20, 120))

        inactive_since = None
        if deactivated_on is None:
            # Roughly a fifth of active clients have gone quiet for >21 days
            # (they are the expected US-04 answer set).
            if i % 5 == 0:
                inactive_since = rng.randint(25, 90)
            elif i % 11 == 0:
                inactive_since = rng.randint(22, 40)

        clients.append(
            GenClient(
                id=i,
                first_name=first,
                last_name=last,
                joined_on=joined_on,
                deactivated_on=deactivated_on,
                inactive_since_days_before_anchor=inactive_since,
            )
        )
    return clients


def build_sessions(rng: random.Random) -> list[dict]:
    sessions = []
    session_id = 1
    start_day = ANCHOR_DAY - timedelta(days=HISTORY_DAYS)
    day = start_day
    while day <= ANCHOR_DAY:
        for time_str, class_name, duration, capacity, target_fill, cancel_rate in WEEKLY_TEMPLATE[day.weekday()]:
            sessions.append(
                {
                    "id": session_id,
                    "class_id": CLASS_IDS[class_name],
                    "class_name": class_name,
                    "day": day.isoformat(),
                    "time": time_str,
                    "duration_minutes": duration,
                    "capacity": capacity,
                    "_target_fill": target_fill,
                    "_cancel_rate": cancel_rate,
                }
            )
            session_id += 1
        day += timedelta(days=1)
    return sessions


def build_bookings(
    rng: random.Random, clients: list[GenClient], sessions: list[dict]
) -> list[dict]:
    bookings: list[dict] = []
    booking_id = 1

    for session in sessions:
        session_day: date = date.fromisoformat(session["day"])
        session_time = session["time"]
        capacity = session["capacity"]
        target_fill = session["_target_fill"]
        cancel_rate = session["_cancel_rate"]

        eligible: list[int] = []
        for c in clients:
            if c.joined_on > session_day:
                continue
            if c.deactivated_on is not None and c.deactivated_on <= session_day:
                continue
            if c.inactive_since_days_before_anchor is not None:
                inactive_from = ANCHOR_DAY - timedelta(days=c.inactive_since_days_before_anchor)
                if session_day >= inactive_from:
                    continue
            eligible.append(c.id)

        if not eligible:
            continue

        target_bookings = min(round(capacity * target_fill), len(eligible))
        chosen = rng.sample(eligible, k=target_bookings) if target_bookings > 0 else []

        hour, minute = (int(x) for x in session_time.split(":"))
        session_datetime = datetime.combine(session_day, datetime.min.time()).replace(
            hour=hour, minute=minute
        )

        for client_id in chosen:
            days_before_booking = rng.randint(1, 10)
            booked_at = session_datetime - timedelta(
                days=days_before_booking, hours=rng.randint(0, 12)
            )

            is_cancelled = rng.random() < cancel_rate
            cancelled_at = None
            state = "confirmed"
            attended = False

            if is_cancelled:
                # Cancelled sometime between booking and the session start.
                cancel_delay = rng.uniform(0, max(days_before_booking - 0.1, 0.1))
                cancelled_at = booked_at + timedelta(days=cancel_delay)
                if cancelled_at >= session_datetime:
                    cancelled_at = session_datetime - timedelta(hours=1)
            elif session_day <= ANCHOR_DAY:
                # Only past/present sessions have a real attendance outcome.
                attended = rng.random() < 0.90

            bookings.append(
                {
                    "id": booking_id,
                    "client_id": client_id,
                    "session_id": session["id"],
                    "state": state,
                    "attended": attended,
                    "booked_at": booked_at.isoformat(timespec="seconds"),
                    "cancelled_at": cancelled_at.isoformat(timespec="seconds") if cancelled_at else None,
                }
            )
            booking_id += 1

    return bookings


def main() -> None:
    rng = random.Random(SEED)

    clients = build_clients(rng)
    sessions = build_sessions(rng)
    bookings = build_bookings(rng, clients, sessions)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    clients_out = [
        {
            "id": c.id,
            "first_name": c.first_name,
            "last_name": c.last_name,
            "joined_on": c.joined_on.isoformat(),
            "deactivated_on": c.deactivated_on.isoformat() if c.deactivated_on else None,
        }
        for c in clients
    ]
    sessions_out = [
        {k: v for k, v in s.items() if not k.startswith("_")} for s in sessions
    ]

    (DATA_DIR / "clients.json").write_text(json.dumps(clients_out, indent=2, ensure_ascii=False) + "\n")
    (DATA_DIR / "sessions.json").write_text(json.dumps(sessions_out, indent=2, ensure_ascii=False) + "\n")
    (DATA_DIR / "bookings.json").write_text(json.dumps(bookings, indent=2, ensure_ascii=False) + "\n")

    print(f"Generated {len(clients_out)} clients, {len(sessions_out)} sessions, {len(bookings)} bookings.")
    print(f"Dataset anchor day (latest day present): {ANCHOR_DAY.isoformat()}")


if __name__ == "__main__":
    main()
