"""Renders an `AnalyticalAnswer` as a human-readable response.

Every rendered answer includes metric, period, data used, exclusions,
assumptions and limitations, as required by US-06 / AC-03. This module only
formats already-computed, deterministic results — it never computes or
alters a figure.
"""

from __future__ import annotations

from copilot.metrics import AnalyticalAnswer


def _format_result(result: object) -> str:
    if result is None:
        return "  (sin resultado numérico — ver limitaciones)"

    if isinstance(result, dict) and "ocupacion_media_pct" in result:
        return f"  Ocupación media: {result['ocupacion_media_pct']}%"

    if isinstance(result, dict) and "periodo_a" in result:
        a, b = result["periodo_a"], result["periodo_b"]

        def _side(side: dict) -> str:
            if side["ocupacion_media_pct"] is None:
                return f"  {side['label']}: sin datos ({side['sesiones']} sesiones — ver limitaciones)"
            return f"  {side['label']}: {side['ocupacion_media_pct']}% ({side['sesiones']} sesiones)"

        lines = [_side(a), _side(b)]
        if result["diferencia_puntos_porcentuales"] is not None:
            lines.append(
                f"  Diferencia: {result['diferencia_puntos_porcentuales']:+.1f} puntos porcentuales"
            )
        if result["variacion_relativa_pct"] is not None:
            lines.append(f"  Variación relativa: {result['variacion_relativa_pct']:+.1f}%")
        return "\n".join(lines)

    if isinstance(result, list) and result and "clase" in result[0]:
        lines = [
            f"  {i}. {row['clase']}: {row['ocupacion_media_pct']}% ({row['sesiones']} sesiones)"
            for i, row in enumerate(result, start=1)
        ]
        return "\n".join(lines)

    if isinstance(result, list) and result and "franja" in result[0]:
        lines = [
            f"  {i}. {row['franja']}: {row['tasa_cancelacion_pct']}% "
            f"({row['cancelaciones']}/{row['reservas_totales']} reservas)"
            for i, row in enumerate(result, start=1)
        ]
        return "\n".join(lines)

    if isinstance(result, list) and result and "cliente" in result[0]:
        lines = []
        for row in result:
            last = row["ultima_reserva"] or "nunca ha reservado"
            days = row["dias_sin_reservar"]
            days_str = f"{days} días sin reservar" if days is not None else "sin reservas registradas"
            lines.append(f"  - {row['cliente']} (id {row['cliente_id']}): última reserva {last}, {days_str}")
        return "\n".join(lines)

    if isinstance(result, list) and not result:
        return "  (sin filas — ver limitaciones)"

    return f"  {result}"


def format_answer(answer: AnalyticalAnswer) -> str:
    lines = [
        f"Métrica: {answer.metric}",
        f"Periodo: {answer.period_label}"
        + (
            f" ({answer.period_start.isoformat() if answer.period_start else '—'} a "
            f"{answer.period_end.isoformat() if answer.period_end else '—'})"
            if answer.period_start or answer.period_end
            else ""
        ),
        "",
        "Resultado:",
        _format_result(answer.result),
    ]

    if answer.data_included:
        lines += ["", "Datos utilizados: " + ", ".join(f"{k}={v}" for k, v in answer.data_included.items())]
    if answer.exclusions:
        lines += ["Exclusiones: " + "; ".join(answer.exclusions)]
    if answer.assumptions:
        lines += ["Supuestos: " + "; ".join(answer.assumptions)]
    if answer.limitations:
        lines += ["Limitaciones: " + "; ".join(answer.limitations)]

    return "\n".join(lines)
