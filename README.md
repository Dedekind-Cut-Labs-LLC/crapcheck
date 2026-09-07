# Crapcheck

Crapcheck is a Python command-line implementation of the Change Risk Analysis and Predictions (CRAP) metric.

The project is in initial development. The repository currently provides the package, CLI, tests, and quality gates; metric analysis is the next implementation increment.

## Intended use

Crapcheck will combine function-level cyclomatic complexity with measured test coverage:

```text
CRAP(m) = complexity(m)^2 * (1 - coverage(m) / 100)^3 + complexity(m)
```

Its initial behavioral references are Robert C. Martin's `crap4java`, `crap4go`, and `crap4clj` tools. Crapcheck is an independent implementation; their source code is not copied.

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
