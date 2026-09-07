"""Behavior tests for composing per-function CRAP analysis."""

from __future__ import annotations

from textwrap import dedent

from crapcheck.analysis import FunctionMetrics, analyze_source


def test_analyze_source_combines_complexity_coverage_and_crap_scores() -> None:
    source = dedent(
        """
        def covered():
            return 1

        def missing_coverage(flag):
            if flag:
                return 1
            return 0

        def zero_coverage(flag):
            if flag:
                return 1
            return 0
        """
    ).lstrip()

    assert analyze_source(
        source,
        {
            "covered": 100.0,
            "zero_coverage": 0.0,
        },
    ) == [
        FunctionMetrics("covered", 1, 2, 1, 100.0, 1.0),
        FunctionMetrics("missing_coverage", 4, 7, 2, None, None),
        FunctionMetrics("zero_coverage", 9, 12, 2, 0.0, 6.0),
    ]
