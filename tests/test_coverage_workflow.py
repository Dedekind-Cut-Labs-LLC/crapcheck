"""End-to-end compatibility test for the documented coverage.py workflow."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def test_coverage_json_to_crapcheck_report(tmp_path: Path) -> None:
    source_dir = tmp_path / "src"
    tests_dir = tmp_path / "tests"
    source_dir.mkdir()
    tests_dir.mkdir()
    source_path = source_dir / "demo.py"
    source_path.write_text(
        'def classify(flag):\n    if flag:\n        return "yes"\n    return "no"\n',
        encoding="utf-8",
    )
    test_path = tests_dir / "test_demo.py"
    test_path.write_text(
        'from demo import classify\n\ndef test_classify():\n    assert classify(True) == "yes"\n',
        encoding="utf-8",
    )
    data_path = tmp_path / ".coverage"
    report_path = tmp_path / "coverage.json"
    environment = {**os.environ, "PYTHONPATH": str(source_dir)}

    subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            f"--data-file={data_path}",
            f"--source={source_dir}",
            "-m",
            "pytest",
            "-q",
            str(test_path),
        ],
        check=True,
        capture_output=True,
        text=True,
        env=environment,
    )
    subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "json",
            f"--data-file={data_path}",
            "-o",
            str(report_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "crapcheck",
            str(source_dir),
            "--coverage",
            str(report_path),
            "--no-fail",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert result.stderr == ""
    assert result.stdout == (
        "Function  Module  CC  Cov%  CRAP\n"
        "--------  ------  --  ----  ----\n"
        "classify  demo     2  66.7   2.1\n"
    )
