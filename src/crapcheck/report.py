"""Human-readable Crapcheck report formatting."""

from __future__ import annotations

from collections.abc import Iterable

from crapcheck.analysis import FunctionMetrics


def _report_order(function: FunctionMetrics) -> tuple[int, float]:
    if function.crap_score is None:
        return (1, 0.0)
    return (0, -function.crap_score)


def format_text_report(module: str, functions: Iterable[FunctionMetrics]) -> str:
    """Format function metrics as a stable, worst-first text table."""
    headers = ("Function", "Module", "CC", "Cov%", "CRAP")
    rows = [
        (
            function.name,
            module,
            str(function.complexity),
            "N/A" if function.coverage_percent is None else f"{function.coverage_percent:.1f}",
            "N/A" if function.crap_score is None else f"{function.crap_score:.1f}",
        )
        for function in sorted(functions, key=_report_order)
    ]
    widths = tuple(
        max(len(header), *(len(row[index]) for row in rows)) for index, header in enumerate(headers)
    )

    def format_row(row: tuple[str, str, str, str, str]) -> str:
        return (
            f"{row[0]:<{widths[0]}}  "
            f"{row[1]:<{widths[1]}}  "
            f"{row[2]:>{widths[2]}}  "
            f"{row[3]:>{widths[3]}}  "
            f"{row[4]:>{widths[4]}}"
        )

    separator = (
        "-" * widths[0],
        "-" * widths[1],
        "-" * widths[2],
        "-" * widths[3],
        "-" * widths[4],
    )
    return "\n".join(
        (format_row(headers), format_row(separator), *(format_row(row) for row in rows))
    )
