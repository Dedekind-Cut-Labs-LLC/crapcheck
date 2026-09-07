"""Tests for the initial command-line scaffold."""

from __future__ import annotations

import subprocess
import sys

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
