"""Composition of complexity, coverage, and CRAP scores."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from crapcheck.complexity import analyze_complexity
from crapcheck.score import calculate_crap_score


@dataclass(frozen=True, slots=True)
class FunctionMetrics:
    """Combined metrics for one named function."""

    name: str
    line: int
    end_line: int
    complexity: int
    coverage_percent: float | None
    crap_score: float | None


def analyze_source(
    source: str,
    coverage_by_function: Mapping[str, float],
) -> list[FunctionMetrics]:
    """Combine source complexity with function coverage and CRAP scores."""
    results: list[FunctionMetrics] = []
    for function in analyze_complexity(source):
        coverage_percent = coverage_by_function.get(function.name)
        results.append(
            FunctionMetrics(
                name=function.name,
                line=function.line,
                end_line=function.end_line,
                complexity=function.complexity,
                coverage_percent=coverage_percent,
                crap_score=calculate_crap_score(function.complexity, coverage_percent),
            )
        )
    return results
