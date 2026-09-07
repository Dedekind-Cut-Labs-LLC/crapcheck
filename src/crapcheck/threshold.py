"""CRAP score threshold policy."""

from __future__ import annotations

from collections.abc import Iterable

from crapcheck.analysis import FunctionMetrics

DEFAULT_MAX_CRAP = 8.0


def exceeds_crap_threshold(
    functions: Iterable[FunctionMetrics],
    max_crap: float = DEFAULT_MAX_CRAP,
) -> bool:
    """Return whether any available CRAP score is greater than the maximum."""
    return any(
        function.crap_score is not None and function.crap_score > max_crap for function in functions
    )
