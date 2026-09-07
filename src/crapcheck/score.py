"""CRAP score calculation."""

from __future__ import annotations


def calculate_crap_score(complexity: int, coverage_percent: float | None) -> float | None:
    """Calculate a CRAP score, preserving unknown coverage as ``None``."""
    if coverage_percent is None:
        return None

    uncovered = 1.0 - (coverage_percent / 100.0)
    return complexity * complexity * uncovered * uncovered * uncovered + complexity
