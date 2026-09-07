# Initial metric contract

## Accepted behavior

Crapcheck will calculate the CRAP score for individual Python functions and methods:

```text
CRAP(m) = complexity(m)^2 * (1 - coverage(m) / 100)^3 + complexity(m)
```

The first implementation should preserve these invariants:

- Cyclomatic complexity starts at one and increases for documented Python decision points.
- Coverage is measured, not inferred from the presence of tests.
- Coverage is attributed from coverage.py JSON function regions.
- A function without matching coverage data reports coverage and CRAP as `N/A`.
- Reports show function identity, module, complexity, coverage percentage, and CRAP score.
- Human-readable results are sorted by CRAP score from highest to lowest, with `N/A` last.
- The default failure boundary is a CRAP score greater than `8.0`.
- Users can configure the maximum or request report-only behavior.

## Behavioral references

The principal behavioral references are:

- [`crap4java`](https://github.com/unclebob/crap4java), which uses JaCoCo instruction coverage.
- [`crap4go`](https://github.com/unclebob/crap4go), which uses statement-weighted Go coverage.
- [`crap4clj`](https://github.com/unclebob/crap4clj), which maps line coverage to functions.
- Alberto Savoia's [2007 introduction to CRAP](https://www.artima.com/weblogs/viewpost.jsp?thread=215899), which presents the formula and cautions that it is experimental and incomplete.

The references use different language-specific coverage primitives. Crapcheck follows their shared behavior and uses Python's natural executable-line coverage rather than reproducing another language's instrumentation.

## Independent implementation boundary

Crapcheck is not a source port. Reference implementations may be observed for behavior, report conventions, and test cases, but their source must not be copied or translated. Crapcheck's implementation and tests must be independently written.

## Implemented complexity contract

Each named function, asynchronous function, method, and nested function starts at complexity one. Its qualified name includes enclosing classes and functions.

The current analyzer adds:

| Python construct | Complexity increment |
|---|---:|
| `if` or `elif` | 1 |
| `for` or `async for` | 1 |
| `while` | 1 |
| each `except` handler | 1 |
| conditional expression (`x if condition else y`) | 1 |
| Boolean `and` or `or` expression | number of operands minus 1 |
| comprehension generator | 1 |
| comprehension filter | 1 |
| `match` statement | 1 per non-default case |
| `assert` statement | 1 |

An unguarded irrefutable `match` case is the default and does not add complexity. Lambdas are not reported separately because coverage.py does not emit separate lambda function regions; decisions in a lambda body contribute to its enclosing named function. Decisions inside a nested named function or class do not increase the enclosing function's complexity. Named nested functions and methods are analyzed separately.

These Python-specific rules were checked behaviorally against Radon 6 and coverage.py 7. Crapcheck remains an independent implementation and does not depend on either package at runtime.

## Implemented coverage contract

Crapcheck reads coverage.py 7.12 or newer JSON reports containing function-region data and separate statement percentages. For one selected source-file key, it returns each named function region's `percent_statements_covered` value. Coverage.py 7.6 introduced function-region JSON data; 7.12 introduced the separate statement percentage required by this contract.

- Statement coverage is used, not coverage.py's combined statement-and-branch percentage.
- The empty-name module pseudo-region is ignored.
- Qualified names emitted by coverage.py, including methods and nested functions, are preserved.
- An exact source-file key is preferred. Otherwise, one unambiguous whole-component suffix match is accepted in either direction.
- No matching source file produces no function matches, allowing later analysis to report `N/A`.
- Multiple suffix matches produce a clear error rather than selecting one.
- A matching file without function-region data is incompatible and produces a clear error.

## Implemented analysis composition

Given Python source text and a mapping of qualified function names to statement-coverage percentages, Crapcheck emits one immutable result per discovered function in source order. Each result contains the qualified name, source extent, complexity, coverage, and CRAP score. A missing coverage entry preserves both coverage and CRAP score as `N/A`; it is never converted to zero coverage.

## Implemented text report

The human-readable report combines one or more modules and contains function, module, cyclomatic complexity, statement coverage percentage, and CRAP score columns. Numeric values use one decimal place. Rows are sorted stably from highest to lowest CRAP score, preserving module and function input order for equal scores, with `N/A` scores after all numeric scores.

## Implemented command-line analysis

`crapcheck SOURCE [SOURCE ...] --coverage COVERAGE_JSON` accepts one or more UTF-8 Python source files or directories. Directories are searched recursively for `*.py`. Discovered files are resolved, deduplicated, and sorted lexically; each is matched to a coverage-report file key, and all functions are emitted in one globally sorted report. This makes equal-score ordering independent of source argument order. Hidden directories and `__pycache__`, `build`, `dist`, `node_modules`, and `venv` directories are excluded from recursive discovery. Explicit files are not filtered by that directory policy. The module column uses dotted package names established by `__init__.py` files and otherwise uses the filename without its final suffix. The threshold is evaluated across all functions. A command with no arguments continues to print help and succeed.

## Implemented threshold behavior

The default maximum CRAP score is `8.0`. After printing the report, Crapcheck exits with status 1 if any available score is strictly greater than the maximum. A score equal to the maximum succeeds, and an `N/A` score does not cause failure. `--max-crap NUMBER` changes the maximum; non-finite values are invalid. `--no-fail` always returns success after reporting.

## Implemented command-line failures

Status 0 means analysis succeeded without an enforced violation, status 1 means at least one available score exceeded the threshold, and status 2 means command usage or an input was invalid. Missing sources or coverage reports, empty source directories, non-Python explicit files, malformed JSON, incompatible coverage data, invalid UTF-8, invalid Python syntax, and non-finite thresholds produce one concise `crapcheck: error:` message on standard error without a traceback.

## Verified coverage.py workflow

The integration suite runs a real Python test under coverage.py, exports JSON, invokes Crapcheck as a subprocess, and verifies the exact function-level report. The fixture deliberately has 66.7% function statement coverage while its file has 75.0% statement coverage, proving Crapcheck reads the function region rather than the file total.

## Not decided yet

The following should be settled only as their implementation increments begin:

- Cross-platform coverage-report path normalization.
- Additional output formats.
- Repository-wide configuration.
- CI annotation formats.

Each decision should arrive with executable examples and focused tests.
