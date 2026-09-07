# Usability validation

Crapcheck 0.1.0 crossed its initial general-usability bar on 2026-09-07. This record distinguishes verified behavior from future enhancements.

## Acceptance evidence

| Criterion | Evidence |
|---|---|
| Repository-wide analysis | File and directory inputs are resolved, recursively discovered, filtered, deduplicated, and lexically ordered. One globally sorted report and one threshold decision cover all functions. |
| Defensible Python complexity | Golden tests cover named, async, nested, and class functions plus conditionals, loops, exception handlers, Boolean operations, comprehensions, `match`, assertions, and lambda-body decisions. The rules are explicit in `docs/metric-contract.md`. |
| Reliable coverage association | Exact paths win; one whole-component suffix match is accepted; ambiguity is rejected. A real coverage.py integration test distinguishes 66.7% function statement coverage from the surrounding file's 75.0%. |
| Stable quality-gate behavior | The default maximum is 8.0; comparison is strictly greater-than; equal scores pass; missing coverage remains `N/A`; `--max-crap` and `--no-fail` are tested; statuses 0, 1, and 2 are documented. |
| Production-quality failures | Subprocess tests cover missing and invalid sources, empty directories, missing/malformed/incompatible coverage, syntax errors, and non-finite thresholds. Expected failures have no traceback. |
| Real-project repeatability | The full package source was analyzed twice from coverage produced by its own test suite. Both 3,240-byte, 38-function reports had SHA-256 `aef8f4650aebacf61f88b1ea4225d0ca62e46ad5a612c96d1d1d72697ca7ed0b`; both enforced runs exited 1. |
| Installable release | The 0.1.0 wheel was installed into a fresh Python 3.11 environment with an empty `PYTHONPATH`. Metadata reported no runtime dependencies. Two clean-install reports matched each other and the development report byte-for-byte with status 1. CI repeats wheel installation. |

## Verification environment

- Linux
- Python 3.11.15 for local release validation
- coverage.py 7.16.0
- CI test matrix: Python 3.11, 3.12, 3.13, and 3.14
- 44 automated tests at the validation checkpoint

## Known boundaries

- Python 3.11 or newer is required.
- Coverage input must be JSON from coverage.py 7.12 or newer.
- The release provides deterministic text output only. Other formats, repository configuration, and CI-specific annotations are future enhancements, not requirements for the initial tool.
- Cross-operating-system movement of coverage reports is not validated. Reports generated and consumed on the same operating system are supported.
- CRAP is a diagnostic signal combining complexity and coverage. It is not a complete measure of design quality and should not be used as one.
