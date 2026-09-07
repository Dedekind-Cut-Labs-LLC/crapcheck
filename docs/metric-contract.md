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

## Not decided yet

The following should be settled only as their implementation increments begin:

- The exact complexity contribution of every Python syntax construct.
- Nested-function coverage attribution.
- Coverage input discovery and command-line shape.
- Additional output formats.
- Repository-wide configuration.
- CI annotation formats.

Each decision should arrive with executable examples and focused tests.
