"""Command-line interface for Crapcheck."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from crapcheck import __version__
from crapcheck.analysis import FunctionMetrics, analyze_source
from crapcheck.coverage import load_function_coverage
from crapcheck.discovery import discover_sources
from crapcheck.report import format_text_report
from crapcheck.threshold import DEFAULT_MAX_CRAP, exceeds_crap_threshold


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="crapcheck",
        description="Calculate function-level CRAP metrics for Python code.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "sources",
        nargs="*",
        type=Path,
        metavar="SOURCE",
        help="Python source file or directory to analyze",
    )
    parser.add_argument(
        "--coverage",
        type=Path,
        help="coverage.py JSON report containing function-region data",
    )
    parser.add_argument(
        "--max-crap",
        type=float,
        default=DEFAULT_MAX_CRAP,
        help=f"fail when a CRAP score is greater than this value (default: {DEFAULT_MAX_CRAP})",
    )
    parser.add_argument(
        "--no-fail",
        action="store_true",
        help="report results without failing on CRAP scores",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the Crapcheck command-line interface."""
    parser = build_parser()
    args = parser.parse_args(argv)
    source_inputs: list[Path] = args.sources
    coverage_path: Path | None = args.coverage
    max_crap: float = args.max_crap
    no_fail: bool = args.no_fail
    if not source_inputs:
        parser.print_help()
        return 0
    if coverage_path is None:
        parser.error("--coverage is required when SOURCE is provided")

    modules: list[tuple[str, list[FunctionMetrics]]] = []
    all_metrics: list[FunctionMetrics] = []
    for discovered in discover_sources(source_inputs):
        source = discovered.path.read_text(encoding="utf-8")
        coverage = load_function_coverage(coverage_path, discovered.path)
        metrics = analyze_source(source, coverage)
        modules.append((discovered.module, metrics))
        all_metrics.extend(metrics)

    print(format_text_report(modules))
    return int(not no_fail and exceeds_crap_threshold(all_metrics, max_crap))
