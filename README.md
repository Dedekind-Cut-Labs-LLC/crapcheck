# Crapcheck

Crapcheck is a Python command-line implementation of the Change Risk Analysis and Predictions (CRAP) metric.

The project is in initial development. It analyzes Python source files and directories against function-region data in a coverage.py JSON report and prints a function-level CRAP table.

## Intended use

Crapcheck will combine function-level cyclomatic complexity with measured test coverage:

```text
CRAP(m) = complexity(m)^2 * (1 - coverage(m) / 100)^3 + complexity(m)
```

Its initial behavioral references are Robert C. Martin's `crap4java`, `crap4go`, and `crap4clj` tools. Crapcheck is an independent implementation; their source code is not copied.

## Installation

Crapcheck requires Python 3.11 or newer and has no runtime dependencies. From a source checkout:

```console
python -m pip install .
```

The project being analyzed must produce a JSON report with coverage.py 7.12 or newer. Version 7.6 introduced function regions, and version 7.12 added the separate statement percentage Crapcheck uses. See the [coverage.py change history](https://coverage.readthedocs.io/en/latest/changes.html).

## Usage

Generate coverage while running the project's tests, export the JSON report, and analyze the source tree:

```console
python -m pip install "coverage>=7.12"
coverage run --source=src -m pytest
coverage json -o coverage.json
crapcheck src --coverage coverage.json
```

Replace `src` and `pytest` with the source root and test command used by the project. Crapcheck consumes existing measured coverage; it does not run tests itself.

By default, Crapcheck exits with status 1 when any available CRAP score is greater than `8.0`. Use `--max-crap NUMBER` to change that boundary or `--no-fail` to produce a report without threshold failure.

Exit statuses are stable: 0 means the analysis succeeded without an enforced violation, 1 means at least one available score exceeded the threshold, and 2 means the command or an input was invalid. Missing files, empty source directories, non-Python files, malformed or incompatible coverage reports, invalid UTF-8, invalid Python syntax, and non-finite thresholds produce a concise error on standard error without a traceback.

One or more Python files or directories may be supplied. Directories are searched recursively for `*.py` files. Crapcheck resolves, deduplicates, and lexically sorts the files before producing one globally sorted report and evaluating the threshold across all files. Hidden directories and common generated environments (`__pycache__`, `build`, `dist`, `node_modules`, and `venv`) are excluded from recursive discovery. An explicitly supplied file remains explicit.

The report uses dotted package names when `__init__.py` files establish a package, such as `crapcheck.cli`; standalone files use their filename without the `.py` suffix.

An exact source-path key in the coverage report is preferred. Otherwise, Crapcheck accepts one unambiguous whole-component suffix match, allowing an absolute source argument to match a relative coverage key. It fails clearly rather than guessing when multiple report keys match.

## Development setup

Crapcheck requires Python 3.11 or newer and uses [uv](https://docs.astral.sh/uv/) for development.

```console
uv sync --all-groups
uv run crapcheck --help
```

Run all local gates:

```console
uv run ruff format --check .
uv run ruff check .
uv run mypy src tests
uv run pytest
uv build
```

## Initial metric contract

The accepted starting behavior is recorded in [`docs/metric-contract.md`](docs/metric-contract.md). It is deliberately narrow and will be extended only through completed, tested increments.

## License

Crapcheck is licensed under the MIT License. See [`LICENSE`](LICENSE).
