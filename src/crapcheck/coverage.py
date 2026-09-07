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


def _paths_match_by_suffix(first: str, second: str) -> bool:
    first_parts = Path(first).parts
    second_parts = Path(second).parts
    return (
        len(first_parts) <= len(second_parts) and second_parts[-len(first_parts) :] == first_parts
    ) or (
        len(second_parts) <= len(first_parts) and first_parts[-len(second_parts) :] == second_parts
    )


def _select_file(
    files: dict[str, object],
    source_file: str | Path,
) -> tuple[str, object] | None:
    source_key = str(source_file)
    if source_key in files:
        return (source_key, files[source_key])

    matches = [
        (report_key, value)
        for report_key, value in files.items()
        if _paths_match_by_suffix(report_key, source_key)
    ]
    if len(matches) > 1:
        match_names = ", ".join(sorted(report_key for report_key, _ in matches))
        raise CoverageReportError(
            f"Source file {source_file} matches multiple coverage files: {match_names}"
        )
    return matches[0] if matches else None


def load_function_coverage(
    report_path: str | Path,
    source_file: str | Path,
) -> dict[str, float]:
    """Load statement coverage for one exact or unambiguous suffix-matched source file."""
    report: object = json.loads(Path(report_path).read_text(encoding="utf-8"))
    root = _mapping(report, "coverage report")
    files = _mapping(root.get("files"), "coverage report files")

    selected_file = _select_file(files, source_file)
    if selected_file is None:
        return {}
    report_key, file_data = selected_file

    file_report = _mapping(file_data, f"coverage data for {report_key}")
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
