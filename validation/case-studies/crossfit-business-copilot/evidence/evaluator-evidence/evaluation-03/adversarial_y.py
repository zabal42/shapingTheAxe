#!/usr/bin/env python3
"""Evaluator-generated adversarial harness for candidate-y (Python).

Usage:
    python3 adversarial_y.py /path/to/extracted/candidate-y

Imports candidate-y's REAL metric engine (src/copilot/metrics.py) and the
InMemoryDataSource, and exercises them with evaluator-built datasets that are
independent of the candidate's own tests. It does not touch the committed
dataset. Each check prints OBSERVED behaviour; interpretation lives in the
evaluation report.

The eight checks A1..A8 mirror adversarial_x.mjs one-for-one so the same
scenario is applied to both candidates.

Reproducible by another evaluator: extract candidate-y.tar.gz anywhere and
pass the resulting candidate-y directory as argv[1].
"""
from __future__ import annotations

import json
import sys
from datetime import date, datetime, time

root = sys.argv[1] if len(sys.argv) > 1 else None
if not root:
    print("ERROR: pass the extracted candidate-y directory as argv[1]", file=sys.stderr)
    sys.exit(2)
sys.path.insert(0, f"{root}/src")

from copilot import metrics  # noqa: E402
from copilot.datasource.memory import InMemoryDataSource  # noqa: E402
from copilot.domain import Booking, ClassSession, Client  # noqa: E402
from copilot.periods import Period  # noqa: E402

ASOF = date(2026, 6, 30)
JUNE = Period(label="junio", start=date(2026, 6, 1), end=date(2026, 6, 30))

_bt = datetime(2026, 5, 1, 10, 0, 0)  # generic booked_at


def sess(id, day, capacity, class_name="WOD", class_id=1, t="07:00"):
    hh, mm = (int(x) for x in t.split(":"))
    return ClassSession(id=id, class_id=class_id, class_name=class_name, day=day,
                        time=time(hh, mm), duration_minutes=60, capacity=capacity)


def book(id, client_id, session_id, state="confirmed", attended=False, cancelled_at=None):
    return Booking(id=id, client_id=client_id, session_id=session_id, state=state,
                   attended=attended, booked_at=_bt, cancelled_at=cancelled_at)


def client(id, name="Ana", last="Test", joined=date(2025, 1, 1), deactivated=None):
    return Client(id=id, first_name=name, last_name=last, joined_on=joined, deactivated_on=deactivated)


results = []


def run(id, desc, fn):
    print(f"\n=== {id}: {desc} ===")
    try:
        observed = fn()
        results.append((id, True, None))
        print(json.dumps(observed, indent=2, default=str, ensure_ascii=False))
    except Exception as e:  # noqa: BLE001
        results.append((id, False, str(e)))
        print(f"THREW: {type(e).__name__}: {e}")


# A1 — Empty dataset
def a1():
    d = InMemoryDataSource([], [], [])
    r = metrics.average_occupancy(d, JUNE)
    return {"result": r.result, "data_included": r.data_included, "limitations": r.limitations}


run("A1", "Empty dataset -> average occupancy", a1)


# A2 — Zero-capacity session mixed with a normal session
def a2():
    d = InMemoryDataSource(
        [client(1)],
        [sess("s0", date(2026, 6, 5), 0), sess("s1", date(2026, 6, 6), 10)],
        [book(f"b{i}", 1, "s1") for i in range(5)],
    )
    r = metrics.average_occupancy(d, JUNE)
    return {"result": r.result, "data_included": r.data_included, "exclusions": r.exclusions}


run("A2", "Zero-capacity session excluded? (cap0 + cap10 with 5 confirmed)", a2)


# A3 — Waiting-list bookings excluded from occupancy numerator
def a3():
    d = InMemoryDataSource(
        [client(1)],
        [sess("s1", date(2026, 6, 6), 10)],
        [book(f"c{i}", 1, "s1", state="confirmed") for i in range(4)]
        + [book(f"w{i}", 1, "s1", state="waiting_list") for i in range(3)],
    )
    r = metrics.average_occupancy(d, JUNE)
    return {"result": r.result, "data_included": r.data_included}


run("A3", "Waiting-list excluded from occupancy (cap10, 4 confirmed + 3 waiting_list)", a3)


# A4 — Active user whose ONLY booking is cancelled (never attended), recent session
def a4():
    d = InMemoryDataSource(
        [client(1, name="Ana")],
        [sess("s1", date(2026, 6, 25), 10)],
        [book("b1", 1, "s1", state="confirmed", attended=False,
              cancelled_at=datetime(2026, 6, 24, 10, 0, 0))],
    )
    r = metrics.inactive_users(d, as_of=ASOF, inactivity_days=21)
    return {"flagged": r.result}


run("A4", "Active user with only a cancelled recent booking -> inactive?", a4)


# A5 — Attendance linked to a box-cancelled session.
# Y's ClassSession has NO 'cancelled' field, so a box-cancelled session cannot
# be represented. We build the nearest equivalent (a normal recent session with
# attended=True) and record that Y cannot express/exclude a cancelled session.
def a5():
    d = InMemoryDataSource(
        [client(1, name="Ana")],
        [sess("s1", date(2026, 6, 25), 10)],
        [book("b1", 1, "s1", state="confirmed", attended=True)],
    )
    r = metrics.inactive_users(d, as_of=ASOF, inactivity_days=21)
    occ = metrics.average_occupancy(d, JUNE)
    return {
        "flagged": r.result,
        "note": "ClassSession has no 'cancelled' field; a box-cancelled session cannot be modelled or excluded.",
        "occupancy_result": occ.result,
        "occupancy_sessions": occ.data_included,
    }


run("A5", "attended=true on a (would-be) box-cancelled session", a5)


# A6 — Period with no valid sessions (data only in May, ask June)
def a6():
    d = InMemoryDataSource(
        [client(1)],
        [sess("s1", date(2026, 5, 10), 10)],
        [book("b1", 1, "s1")],
    )
    avg = metrics.average_occupancy(d, JUNE)
    canc = metrics.cancellation_rate_by_timeslot(d, JUNE)
    return {"avg_result": avg.result, "avg_limitations": avg.limitations,
            "canc_result": canc.result, "canc_limitations": canc.limitations}


run("A6", "Period with no sessions (data only in May, ask June)", a6)


# A7 — Determinism / stable ordering under repeated runs (ties in low-occupancy)
def a7():
    d = InMemoryDataSource(
        [client(1)],
        [sess("sa", date(2026, 6, 5), 10, class_name="Zumba", class_id=9, t="19:00"),
         sess("sb", date(2026, 6, 5), 10, class_name="Aero", class_id=2, t="19:00")],
        [book(f"a{i}", 1, "sa") for i in range(3)] + [book(f"b{i}", 1, "sb") for i in range(3)],
    )
    r1 = json.dumps(metrics.lowest_occupancy_classes(d, JUNE, 3).result, default=str)
    r2 = json.dumps(metrics.lowest_occupancy_classes(d, JUNE, 3).result, default=str)
    return {"identical_across_runs": r1 == r2,
            "order": [row["clase"] for row in json.loads(r1)]}


run("A7", "Deterministic ordering across repeated runs (two equal-occupancy classes)", a7)


# A8 — Occupancy over 100% (confirmed > capacity)
def a8():
    d = InMemoryDataSource(
        [client(1)],
        [sess("s1", date(2026, 6, 6), 5)],
        [book(f"b{i}", 1, "s1") for i in range(7)],
    )
    r = metrics.average_occupancy(d, JUNE)
    return {"result": r.result, "limitations": r.limitations}


run("A8", "Over-capacity occupancy (cap5, 7 confirmed) not truncated?", a8)


print("\n\n===== SUMMARY (candidate-y) =====")
for id, ok, err in results:
    print(f"{id}: {'ran' if ok else 'THREW ' + err}")
