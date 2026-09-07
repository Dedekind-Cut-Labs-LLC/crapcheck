"""Behavior tests for human-readable reports."""

from __future__ import annotations

from crapcheck.analysis import FunctionMetrics
from crapcheck.report import format_text_report


def test_formats_worst_first_table_with_missing_scores_last() -> None:
    functions = [
        FunctionMetrics("safe_first", 1, 2, 1, 100.0, 1.0),
        FunctionMetrics("missing_coverage", 4, 7, 2, None, None),
        FunctionMetrics("risky", 9, 12, 5, 0.0, 30.0),
        FunctionMetrics("safe_second", 14, 15, 1, 100.0, 1.0),
        FunctionMetrics("medium", 17, 20, 5, 50.0, 8.125),
    ]

    assert format_text_report("sample", functions) == (
        "Function          Module  CC   Cov%  CRAP\n"
        "----------------  ------  --  -----  ----\n"
        "risky             sample   5    0.0  30.0\n"
        "medium            sample   5   50.0   8.1\n"
        "safe_first        sample   1  100.0   1.0\n"
        "safe_second       sample   1  100.0   1.0\n"
        "missing_coverage  sample   2    N/A   N/A"
    )
