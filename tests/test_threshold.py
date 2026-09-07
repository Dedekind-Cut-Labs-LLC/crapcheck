"""Behavior tests for CRAP threshold evaluation."""

from __future__ import annotations

from crapcheck.analysis import FunctionMetrics
from crapcheck.threshold import DEFAULT_MAX_CRAP, exceeds_crap_threshold


def test_threshold_is_strict_and_ignores_missing_scores() -> None:
    functions = [
        FunctionMetrics("at_boundary", 1, 2, 5, 50.4, DEFAULT_MAX_CRAP),
        FunctionMetrics("unknown", 4, 5, 20, None, None),
    ]

    assert exceeds_crap_threshold(functions, DEFAULT_MAX_CRAP) is False
    assert exceeds_crap_threshold(functions, DEFAULT_MAX_CRAP - 0.1) is True
