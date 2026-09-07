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

Decisions inside a nested function, lambda, or class do not increase the enclosing function's complexity. Named nested functions and methods are analyzed separately.

## Implemented coverage contract

Crapcheck reads coverage.py JSON reports containing function-region data. For one exact source-file key, it returns each named function region's `percent_statements_covered` value.

- Statement coverage is used, not coverage.py's combined statement-and-branch percentage.
- The empty-name module pseudo-region is ignored.
- Qualified names emitted by coverage.py, including methods and nested functions, are preserved.
- A source-file key absent from the report produces no function matches, allowing later analysis to report `N/A`.
- A matching file without function-region data is incompatible and produces a clear error.
- Path normalization and suffix matching are not implemented; source-file keys currently match exactly.

## Implemented analysis composition

Given Python source text and a mapping of qualified function names to statement-coverage percentages, Crapcheck emits one immutable result per discovered function in source order. Each result contains the qualified name, source extent, complexity, coverage, and CRAP score. A missing coverage entry preserves both coverage and CRAP score as `N/A`; it is never converted to zero coverage.

## Implemented text report

The human-readable report contains function, module, cyclomatic complexity, statement coverage percentage, and CRAP score columns. Numeric values use one decimal place. Rows are sorted stably from highest to lowest CRAP score, preserving input order for equal scores, with `N/A` scores after all numeric scores.

## Not decided yet

The following should be settled only as their implementation increments begin:

- Complexity treatment for comprehensions, `match`, assertions, and lambdas.
- Coverage-file path normalization and unambiguous suffix matching.
- Coverage input discovery and command-line shape.
- Additional output formats.
- Repository-wide configuration.
- CI annotation formats.

Each decision should arrive with executable examples and focused tests.
