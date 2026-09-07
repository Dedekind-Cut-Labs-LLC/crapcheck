"""Function-level coverage ingestion."""

from __future__ import annotations

import json
from pathlib import Path


class CoverageReportError(ValueError):
    """Raised when a coverage report lacks required function-region data."""


def _mapping(value: object, context: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise CoverageReportError(f"Expected {context} to be a JSON object")
    return value


def load_function_coverage(
    report_path: str | Path,
    source_file: str | Path,
) -> dict[str, float]:
    """Load statement-coverage percentages for one exact source-file key."""
    report: object = json.loads(Path(report_path).read_text(encoding="utf-8"))
    root = _mapping(report, "coverage report")
    files = _mapping(root.get("files"), "coverage report files")

    file_data = files.get(str(source_file))
    if file_data is None:
        return {}

    file_report = _mapping(file_data, f"coverage data for {source_file}")
    functions_value = file_report.get("functions")
    if functions_value is None:
        raise CoverageReportError(
            f"Coverage data for {source_file} does not contain function-region data"
        )
    functions = _mapping(functions_value, f"function-region data for {source_file}")

    coverage_by_function: dict[str, float] = {}
    for name, value in functions.items():
        if not name:
            continue
        function = _mapping(value, f"coverage data for function {name}")
        summary = _mapping(function.get("summary"), f"coverage summary for function {name}")
        percentage = summary.get("percent_statements_covered")
        if isinstance(percentage, bool) or not isinstance(percentage, int | float):
            raise CoverageReportError(
                f"Coverage summary for function {name} has no numeric percent_statements_covered"
            )
        coverage_by_function[name] = float(percentage)

    return coverage_by_function
