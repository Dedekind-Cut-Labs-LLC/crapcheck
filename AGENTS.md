# Agent instructions

`CLAUDE.md` is the canonical repository instruction file. Read and follow it before modifying this project.

Use small, tested increments. State the current increment and its verification before editing. Do not expand scope for hypothetical future needs.

Run all deterministic gates before commit or handoff:

```console
uv run ruff format --check .
uv run ruff check .
uv run mypy src tests
uv run pytest
uv build
```

Crapcheck is an independent implementation. Use Bob Martin's CRAP tools as behavioral references, but do not copy or translate their source code.
