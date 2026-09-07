"""Command-line interface for Crapcheck."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from crapcheck import __version__


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
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the Crapcheck command-line interface."""
    parser = build_parser()
    parser.parse_args(argv)
    parser.print_help()
    return 0
