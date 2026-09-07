"""Behavior tests for coverage.py JSON ingestion."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from crapcheck.coverage import CoverageReportError, load_function_coverage


def write_report(tmp_path: Path, report: dict[str, Any]) -> Path:
    """Write a coverage JSON fixture and return its path."""
    report_path = tmp_path / "coverage.json"
    report_path.write_text(json.dumps(report), encoding="utf-8")
    return report_path


def test_loads_statement_coverage_for_named_function_regions(tmp_path: Path) -> None:
    report_path = write_report(
        tmp_path,
        {
            "meta": {"format": 3, "version": "7.16.0", "branch_coverage": True},
            "files": {
                "src/example.py": {
                    "functions": {
                        "classify": {
                            "start_line": 1,
                            "summary": {
                                "percent_covered": 60.0,
                                "percent_statements_covered": 66.66666666666667,
                            },
                        },
                        "outer.inner": {
                            "start_line": 7,
                            "summary": {
                                "percent_covered": 0.0,
                                "percent_statements_covered": 0.0,
                            },
                        },
                        "Calculator.run": {
                            "start_line": 12,
                            "summary": {
                                "percent_covered": 75.0,
                                "percent_statements_covered": 80.0,
                            },
                        },
                        "": {
                            "start_line": 1,
                            "summary": {
                                "percent_covered": 100.0,
                                "percent_statements_covered": 100.0,
                            },
                        },
                    }
                }
            },
        },
    )

    assert load_function_coverage(report_path, "src/example.py") == {
        "classify": pytest.approx(66.66666666666667),
        "outer.inner": pytest.approx(0.0),
        "Calculator.run": pytest.approx(80.0),
    }


def test_missing_exact_source_file_returns_no_function_coverage(tmp_path: Path) -> None:
    report_path = write_report(
        tmp_path,
        {"meta": {"format": 3}, "files": {"src/example.py": {"functions": {}}}},
    )

    assert load_function_coverage(report_path, "example.py") == {}


def test_rejects_reports_without_function_region_data(tmp_path: Path) -> None:
    report_path = write_report(
        tmp_path,
        {"meta": {"format": 2}, "files": {"src/example.py": {"executed_lines": [1]}}},
    )

    with pytest.raises(CoverageReportError, match="function-region data"):
        load_function_coverage(report_path, "src/example.py")


def test_rejects_nonnumeric_statement_coverage(tmp_path: Path) -> None:
    report_path = write_report(
        tmp_path,
        {
            "files": {
                "src/example.py": {
                    "functions": {"run": {"summary": {"percent_statements_covered": "100"}}}
                }
            }
        },
    )

    with pytest.raises(CoverageReportError, match="function run has no numeric"):
        load_function_coverage(report_path, "src/example.py")
