"""Tests for the initial command-line scaffold."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from crapcheck import __version__
from crapcheck.cli import main


def test_no_arguments_prints_help(capsys: pytest.CaptureFixture[str]) -> None:
    """The empty command should explain itself and succeed."""
    assert main([]) == 0
    captured = capsys.readouterr()
    assert "Calculate function-level CRAP metrics" in captured.out


def test_module_reports_version() -> None:
    """The installed module should expose the package version."""
    result = subprocess.run(
        [sys.executable, "-m", "crapcheck", "--version"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == f"crapcheck {__version__}"


def test_analyzes_one_source_file_with_exact_coverage_key(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    source_path = tmp_path / "sample.py"
    source_path.write_text(
        "def safe():\n"
        "    return 1\n"
        "\n"
        "def risky(flag):\n"
        "    if flag:\n"
        "        return 1\n"
        "    return 0\n",
        encoding="utf-8",
    )
    coverage_path = tmp_path / "coverage.json"
    coverage_path.write_text(
        json.dumps(
            {
                "files": {
                    str(source_path): {
                        "functions": {
                            "safe": {"summary": {"percent_statements_covered": 100.0}},
                            "risky": {"summary": {"percent_statements_covered": 0.0}},
                        }
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    assert main([str(source_path), "--coverage", str(coverage_path)]) == 0
    assert capsys.readouterr().out == (
        "Function  Module  CC   Cov%  CRAP\n"
        "--------  ------  --  -----  ----\n"
        "risky     sample   2    0.0   6.0\n"
        "safe      sample   1  100.0   1.0\n"
    )
