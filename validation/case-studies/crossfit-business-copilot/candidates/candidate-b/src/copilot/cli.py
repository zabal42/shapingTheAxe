"""CLI entry point for the Business Intelligence Copilot MVP.

Usage:
    python -m copilot.cli                       # interactive mode
    python -m copilot.cli "<question in Spanish>"  # single-question mode
"""

from __future__ import annotations

import sys
from datetime import date

from copilot import metrics, nlp
from copilot.datasource import DataSource, MockDataSource
from copilot.formatter import format_answer


class EmptyDatasetError(RuntimeError):
    """Raised when the data source has no sessions to anchor "now" to."""


def _dataset_anchor_day(data_source: DataSource) -> date:
    """The latest session day present in the data source.

    Used as `now` instead of the real system clock so that "este mes" /
    "el mes anterior" always resolve against the fixed, reproducible
    simulated dataset (see docs/05_Architecture.md, decision D3). Falling
    back to the real clock here would silently break that guarantee, so an
    empty dataset is a hard, explicit error instead — see
    docs/07_Acceptance_Evaluation.md, "Code review findings".
    """
    sessions = data_source.list_sessions(date.min, date.max)
    if not sessions:
        raise EmptyDatasetError(
            "El dataset simulado no contiene sesiones. Ejecuta "
            "'python3 scripts/generate_dataset.py' antes de usar el CLI."
        )
    return max(s.day for s in sessions)


def answer_question(data_source: DataSource, question: str, now: date) -> str:
    routed = nlp.route(question, now)

    if routed.intent is None:
        return routed.unsupported_message or nlp.SUPPORTED_QUESTIONS_HELP

    notes = []
    if routed.clarification_message:
        notes.append(routed.clarification_message)
    elif routed.period_was_defaulted and routed.periods:
        notes.append(f"No se especificó un periodo; asumo '{routed.periods[0].label}'.")

    if routed.intent == "average_occupancy":
        result = metrics.average_occupancy(data_source, routed.periods[0])
    elif routed.intent == "lowest_occupancy":
        top_n = routed.top_n if routed.top_n is not None else 3
        result = metrics.lowest_occupancy_classes(data_source, routed.periods[0], top_n=top_n)
    elif routed.intent == "cancellation_rate":
        result = metrics.cancellation_rate_by_timeslot(data_source, routed.periods[0])
    elif routed.intent == "inactive_users":
        inactivity_days = routed.inactivity_days if routed.inactivity_days is not None else 21
        result = metrics.inactive_users(data_source, as_of=now, inactivity_days=inactivity_days)
    elif routed.intent == "compare_periods":
        result = metrics.compare_periods(data_source, routed.periods[0], routed.periods[1])
    else:  # pragma: no cover - defensive, all intents handled above
        return "No he podido interpretar la pregunta.\n" + nlp.SUPPORTED_QUESTIONS_HELP

    rendered = format_answer(result)
    if notes:
        rendered = "\n".join(notes) + "\n\n" + rendered
    return rendered


def main(argv: list[str] | None = None) -> None:
    argv = argv if argv is not None else sys.argv[1:]
    data_source = MockDataSource()
    try:
        now = _dataset_anchor_day(data_source)
    except EmptyDatasetError as exc:
        print(f"Error: {exc}")
        return

    if argv:
        question = " ".join(argv)
        print(answer_question(data_source, question, now))
        return

    print("Business Intelligence Copilot — CrossFit (MVP, datos simulados)")
    print(f"Fecha de referencia del dataset simulado (as_of): {now.isoformat()}")
    print(nlp.SUPPORTED_QUESTIONS_HELP)
    print("Escribe 'salir' para terminar.\n")

    while True:
        try:
            question = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not question:
            continue
        if question.lower() in {"salir", "exit", "quit"}:
            break
        print()
        print(answer_question(data_source, question, now))
        print()


if __name__ == "__main__":
    main()
