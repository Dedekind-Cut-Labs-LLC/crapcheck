"""Golden tests for the canonical CRAP score formula."""

from __future__ import annotations

import pytest

from crapcheck.score import calculate_crap_score


@pytest.mark.parametrize(
    ("complexity", "coverage_percent", "expected"),
    [
        (1, 100.0, 1.0),
        (1, 0.0, 2.0),
        (5, 0.0, 30.0),
        (5, 50.0, 8.125),
        (10, 80.0, 10.8),
        (20, 100.0, 20.0),
    ],
)
def test_calculate_crap_score_matches_hand_computed_examples(
    complexity: int,
    coverage_percent: float,
    expected: float,
) -> None:
    """Known inputs should produce the canonical formula's results."""
    assert calculate_crap_score(complexity, coverage_percent) == pytest.approx(expected)


def test_calculate_crap_score_preserves_missing_coverage() -> None:
    """Unknown coverage must remain unknown rather than becoming zero."""
    assert calculate_crap_score(5, None) is None
