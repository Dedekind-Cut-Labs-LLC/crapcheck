# Crapcheck

Crapcheck is a Python command-line implementation of the Change Risk Analysis and Predictions (CRAP) metric.

The project is in initial development. It can analyze one Python source file against function-region data in a coverage.py JSON report and print a function-level CRAP table.

## Intended use

Crapcheck will combine function-level cyclomatic complexity with measured test coverage:

```text
CRAP(m) = complexity(m)^2 * (1 - coverage(m) / 100)^3 + complexity(m)
```

Its initial behavioral references are Robert C. Martin's `crap4java`, `crap4go`, and `crap4clj` tools. Crapcheck is an independent implementation; their source code is not copied.

## Usage

```console
crapcheck path/to/module.py --coverage coverage.json
```

By default, Crapcheck exits with status 1 when any available CRAP score is greater than `8.0`. Use `--max-crap NUMBER` to change that boundary or `--no-fail` to produce a report without threshold failure.

An exact source-path key in the coverage report is preferred. Otherwise, Crapcheck accepts one unambiguous whole-component suffix match, allowing an absolute source argument to match a relative coverage key. It fails clearly rather than guessing when multiple report keys match. Recursive source discovery and filesystem path resolution are deferred.

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
