# Initial metric contract

## Accepted behavior

Crapcheck will calculate the CRAP score for individual Python functions and methods:

```text
CRAP(m) = complexity(m)^2 * (1 - coverage(m) / 100)^3 + complexity(m)
```

The first implementation should preserve these invariants:

- Cyclomatic complexity starts at one and increases for documented Python decision points.
- Coverage is measured, not inferred from the presence of tests.
- Coverage is attributed to each function from coverage.py executable-line data.
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

## Not decided yet

The following should be settled only as their implementation increments begin:

- Complexity treatment for comprehensions, `match`, assertions, and lambdas.
- Nested-function coverage attribution.
- Coverage input discovery and command-line shape.
- Additional output formats.
- Repository-wide configuration.
- CI annotation formats.

Each decision should arrive with executable examples and focused tests.
