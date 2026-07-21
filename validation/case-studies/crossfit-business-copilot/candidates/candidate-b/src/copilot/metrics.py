"""Deterministic business-metrics engine (AC-02).

Every function here is a pure computation over `DataSource` output: no
randomness, no LLM call, no invented figures. Each function returns an
`AnalyticalAnswer` that always carries the metric, the period, what data was
included/excluded, the assumptions applied and known limitations — required
by US-06 / AC-03 for every analytical response.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta
from statistics import mean

from copilot.datasource.base import DataSource
from copilot.domain import Booking, ClassSession
from copilot.periods import Period


@dataclass(frozen=True)
class AnalyticalAnswer:
    metric: str
    period_label: str
    period_start: date | None
    period_end: date | None
    result: object
    data_included: dict = field(default_factory=dict)
    exclusions: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)


_OCCUPANCY_ASSUMPTIONS = [
    "Ocupación de una sesión = reservas confirmadas y no canceladas / capacidad de esa sesión (Asunción A3/A5, docs/03_API_Discovery.md).",
    "La ocupación media de un periodo es la media (no ponderada) de la ocupación de cada sesión programada en ese periodo.",
]


def _session_occupancy(sessions, bookings) -> dict[int, float]:
    counts: dict[int, int] = defaultdict(int)
    for b in bookings:
        if b.counts_toward_occupancy:
            counts[b.session_id] += 1
    return {s.id: (counts.get(s.id, 0) / s.capacity if s.capacity else 0.0) for s in sessions}


def _load_sessions_and_bookings(
    data_source: DataSource, period: Period
) -> tuple[list[ClassSession], list[Booking]] | None:
    """Fetches sessions/bookings for a period, or None if the period is empty.

    Shared by every per-period metric below so the "no sessions in this
    period" guard is written once instead of duplicated per metric.
    """
    sessions = data_source.list_sessions(period.start, period.end)
    if not sessions:
        return None
    bookings = data_source.list_bookings(period.start, period.end)
    return sessions, bookings


def _no_sessions_answer(metric: str, period: Period, empty_result: object) -> AnalyticalAnswer:
    return AnalyticalAnswer(
        metric=metric,
        period_label=period.label,
        period_start=period.start,
        period_end=period.end,
        result=empty_result,
        data_included={"sesiones": 0},
        limitations=["No hay sesiones programadas en el periodo solicitado; no es posible calcular esta métrica."],
    )


def average_occupancy(data_source: DataSource, period: Period) -> AnalyticalAnswer:
    loaded = _load_sessions_and_bookings(data_source, period)
    if loaded is None:
        return _no_sessions_answer("ocupación media", period, None)
    sessions, bookings = loaded

    occ_by_session = _session_occupancy(sessions, bookings)
    avg_pct = round(mean(occ_by_session.values()) * 100, 1)

    return AnalyticalAnswer(
        metric="ocupación media",
        period_label=period.label,
        period_start=period.start,
        period_end=period.end,
        result={"ocupacion_media_pct": avg_pct},
        data_included={
            "sesiones": len(sessions),
            "reservas_confirmadas": sum(1 for b in bookings if b.counts_toward_occupancy),
        },
        exclusions=["Reservas en lista de espera y reservas canceladas no cuentan como ocupación."],
        assumptions=list(_OCCUPANCY_ASSUMPTIONS),
    )


def lowest_occupancy_classes(
    data_source: DataSource, period: Period, top_n: int = 3
) -> AnalyticalAnswer:
    loaded = _load_sessions_and_bookings(data_source, period)
    if loaded is None:
        return _no_sessions_answer("clases con menor ocupación", period, [])
    sessions, bookings = loaded

    occ_by_session = _session_occupancy(sessions, bookings)

    by_class: dict[str, list[float]] = defaultdict(list)
    for s in sessions:
        by_class[s.class_name].append(occ_by_session[s.id])

    ranked = sorted(
        (
            {
                "clase": class_name,
                "ocupacion_media_pct": round(mean(values) * 100, 1),
                "sesiones": len(values),
            }
            for class_name, values in by_class.items()
        ),
        key=lambda row: row["ocupacion_media_pct"],
    )

    limitations = []
    if len(ranked) < top_n:
        limitations.append(
            f"Solo hay {len(ranked)} clase(s) distinta(s) programada(s) en el periodo; se muestran todas."
        )

    return AnalyticalAnswer(
        metric="clases con menor ocupación",
        period_label=period.label,
        period_start=period.start,
        period_end=period.end,
        result=ranked[:top_n],
        data_included={"sesiones": len(sessions), "clases_distintas": len(ranked)},
        exclusions=["Reservas en lista de espera y reservas canceladas no cuentan como ocupación."],
        assumptions=list(_OCCUPANCY_ASSUMPTIONS),
        limitations=limitations,
    )


def cancellation_rate_by_timeslot(
    data_source: DataSource, period: Period, top_n: int = 3
) -> AnalyticalAnswer:
    loaded = _load_sessions_and_bookings(data_source, period)
    if loaded is None:
        return _no_sessions_answer("tasa de cancelación por franja horaria", period, [])
    sessions, bookings = loaded

    session_time = {s.id: s.time.strftime("%H:%M") for s in sessions}

    totals: dict[str, int] = defaultdict(int)
    cancelled: dict[str, int] = defaultdict(int)
    for b in bookings:
        slot = session_time.get(b.session_id)
        if slot is None:
            continue
        totals[slot] += 1
        if b.is_cancelled:
            cancelled[slot] += 1

    low_sample_slots = [slot for slot, total in totals.items() if total < 5]

    ranked = sorted(
        (
            {
                "franja": slot,
                "reservas_totales": total,
                "cancelaciones": cancelled.get(slot, 0),
                "tasa_cancelacion_pct": round(cancelled.get(slot, 0) / total * 100, 1),
            }
            for slot, total in totals.items()
            if total > 0
        ),
        key=lambda row: row["tasa_cancelacion_pct"],
        reverse=True,
    )

    limitations = []
    if low_sample_slots:
        limitations.append(
            "Algunas franjas horarias tienen menos de 5 reservas en el periodo; su tasa puede no ser representativa: "
            + ", ".join(sorted(low_sample_slots)) + "."
        )

    return AnalyticalAnswer(
        metric="tasa de cancelación por franja horaria",
        period_label=period.label,
        period_start=period.start,
        period_end=period.end,
        result=ranked[:top_n],
        data_included={"sesiones": len(sessions), "reservas_totales": sum(totals.values())},
        exclusions=["Las reservas en lista de espera se cuentan como reserva a efectos de esta tasa si figuran canceladas o no."],
        assumptions=[
            "La franja horaria es la hora de inicio programada de la sesión (HH:MM), no un rango.",
            "Tasa de cancelación = reservas canceladas / total de reservas realizadas para esa franja en el periodo.",
        ],
        limitations=limitations,
    )


def inactive_users(
    data_source: DataSource, as_of: date, inactivity_days: int = 21
) -> AnalyticalAnswer:
    cutoff = as_of - timedelta(days=inactivity_days)
    clients = data_source.clients_without_booking_since(cutoff)

    rows = []
    for c in clients:
        last_day = data_source.last_booking_day(c.id)
        days_without = (as_of - last_day).days if last_day else None
        rows.append(
            {
                "cliente": f"{c.first_name} {c.last_name}",
                "cliente_id": c.id,
                "ultima_reserva": last_day.isoformat() if last_day else None,
                "dias_sin_reservar": days_without,
            }
        )
    rows.sort(key=lambda r: (r["dias_sin_reservar"] is None, r["dias_sin_reservar"] or 0), reverse=True)

    return AnalyticalAnswer(
        metric=f"usuarios activos sin reservas en más de {inactivity_days} días",
        period_label=f"a fecha de {as_of.isoformat()}, corte de {inactivity_days} días",
        period_start=None,
        period_end=as_of,
        result=rows,
        data_included={"usuarios_activos_evaluados": len(data_source.list_active_clients())},
        exclusions=["Usuarios dados de baja (deactivated_on no nulo) no se consideran, aunque lleven tiempo sin reservar."],
        assumptions=[
            "Un usuario se considera 'activo' si no tiene fecha de baja registrada (Asunción A1, docs/03_API_Discovery.md).",
            "La inactividad se mide por ausencia de reservas (cualquier estado), no de asistencia confirmada, porque la API documentada solo expone un endpoint de 'sin reserva desde fecha', no de 'sin asistencia desde fecha'.",
        ],
        limitations=(
            ["No hay usuarios activos que cumplan el criterio de inactividad en este corte."] if not rows else []
        ),
    )


def compare_periods(
    data_source: DataSource, period_a: Period, period_b: Period
) -> AnalyticalAnswer:
    answer_a = average_occupancy(data_source, period_a)
    answer_b = average_occupancy(data_source, period_b)

    occ_a = answer_a.result["ocupacion_media_pct"] if answer_a.result else None
    occ_b = answer_b.result["ocupacion_media_pct"] if answer_b.result else None

    diff_points = round(occ_b - occ_a, 1) if occ_a is not None and occ_b is not None else None
    relative_pct = (
        round(diff_points / occ_a * 100, 1) if diff_points is not None and occ_a not in (None, 0) else None
    )

    limitations = list(answer_a.limitations) + list(answer_b.limitations)
    sessions_a = answer_a.data_included.get("sesiones", 0)
    sessions_b = answer_b.data_included.get("sesiones", 0)
    if sessions_a and sessions_b and abs(sessions_a - sessions_b) / max(sessions_a, sessions_b) > 0.3:
        limitations.append(
            f"El número de sesiones difiere considerablemente entre periodos ({sessions_a} vs {sessions_b}); "
            "la comparación puede no ser directamente equivalente."
        )

    return AnalyticalAnswer(
        metric="comparación de ocupación entre dos periodos",
        period_label=f"{period_a.label} vs {period_b.label}",
        period_start=min(period_a.start, period_b.start),
        period_end=max(period_a.end, period_b.end),
        result={
            "periodo_a": {"label": period_a.label, "ocupacion_media_pct": occ_a, "sesiones": sessions_a},
            "periodo_b": {"label": period_b.label, "ocupacion_media_pct": occ_b, "sesiones": sessions_b},
            "diferencia_puntos_porcentuales": diff_points,
            "variacion_relativa_pct": relative_pct,
        },
        data_included={"sesiones_periodo_a": sessions_a, "sesiones_periodo_b": sessions_b},
        # Order-preserving dedup (not set()): this module's whole premise is
        # deterministic, reproducible output (AC-02), so the rendered
        # "Exclusiones:" line must not depend on set-iteration/hash order.
        exclusions=list(dict.fromkeys(answer_a.exclusions + answer_b.exclusions)),
        assumptions=list(_OCCUPANCY_ASSUMPTIONS),
        limitations=limitations,
    )
