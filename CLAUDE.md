# Project instructions

## Purpose

Crapcheck is an independent Python CLI implementation of the CRAP metric. It combines function-level cyclomatic complexity and measured coverage using:

```text
complexity^2 * (1 - coverage / 100)^3 + complexity
```

Read `README.md` and `docs/metric-contract.md` before changing metric behavior.

## Working method

- State the current small, coherent increment before editing.
- Inspect existing behavior first.
- Write or expose a failing behavioral test before implementation when practical.
- Implement only enough to complete the current increment.
- Do not generalize for hypothetical report formats, coverage providers, frameworks, or language constructs.
- Unexpected scope growth is a stop signal. Discuss it with Dave before expanding the design.
- Complete the increment, run deterministic checks, inspect the diff, summarize what was learned, and stop.
- Do not invoke Compound Engineering workflows unless Dave explicitly requests them.
- Run `/hermes-summary` after each meaningful completed increment.

## Behavioral authority and clean implementation

Use these projects as behavioral references:

- https://github.com/unclebob/crap4java
- https://github.com/unclebob/crap4go
- https://github.com/unclebob/crap4clj

Do not copy or translate their source. The Go and Clojure repositories state `All rights reserved`, and the Java repository does not declare an open-source license. Reimplement behavior independently from the published formula, observed behavior, documentation, and our own tests.

Every change to complexity counting, coverage attribution, score calculation, sorting, threshold handling, or missing-data behavior requires a focused golden test that shows the inputs and expected result.

## Current product decisions

- Analyze individual Python functions, asynchronous functions, and methods.
- Use coverage.py executable-line data mapped to each function.
- Missing coverage is `N/A`, not zero.
- Use the established CRAP formula without alteration.
- Sort the human-readable report from highest CRAP score to lowest.
- Default maximum CRAP score is `8.0` for compatibility with Bob Martin's current Java tool.
- The maximum is configurable, and report-only use must be possible without failure enforcement.
- Treat CRAP as a diagnostic signal, not a complete measure of design quality.

These are governing decisions, not authorization to implement all behavior in one increment.

## Repository structure

```text
src/crapcheck/       package and CLI
 tests/              behavioral and unit tests
 docs/               concise governing behavior
 .github/workflows/  deterministic CI gates
```

Keep reusable production code under `src/crapcheck/`. Delete obsolete one-off scripts rather than accumulating them.

## Commands

```console
uv sync --all-groups
uv run ruff format --check .
uv run ruff check .
uv run mypy src tests
uv run pytest
uv build
uv run crapcheck --help
```

All commands must pass before commit or handoff. Do not weaken a gate merely to make it green.

## Scope of the initial scaffold

The current CLI only proves packaging and invocation. The next implementation increment should be selected with Dave; do not silently treat the full metric contract as one implementation task.
