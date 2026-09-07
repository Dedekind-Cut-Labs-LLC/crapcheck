"""Deterministic discovery of Python source files."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

_EXCLUDED_DIRECTORIES = frozenset(
    {
        "__pycache__",
        "build",
        "dist",
        "node_modules",
        "venv",
    }
)


@dataclass(frozen=True, slots=True)
class DiscoveredSource:
    """One normalized Python source file and its report module name."""

    path: Path
    module: str


def discover_sources(inputs: Iterable[Path]) -> list[DiscoveredSource]:
    """Expand files and directories into a deterministic, deduplicated source list."""
    source_paths: set[Path] = set()
    for input_path in inputs:
        normalized = input_path.resolve()
        if normalized.is_dir():
            source_paths.update(_discover_directory(normalized))
        else:
            source_paths.add(normalized)

    return [
        DiscoveredSource(path=path, module=_module_name(path))
        for path in sorted(source_paths, key=lambda candidate: candidate.as_posix())
    ]


def _discover_directory(root: Path) -> set[Path]:
    sources: set[Path] = set()
    for candidate in root.rglob("*.py"):
        relative = candidate.relative_to(root)
        if _is_excluded(relative) or not candidate.is_file():
            continue
        sources.add(candidate.resolve())
    return sources


def _is_excluded(relative: Path) -> bool:
    return any(
        part.startswith(".") or part in _EXCLUDED_DIRECTORIES for part in relative.parts[:-1]
    )


def _module_name(path: Path) -> str:
    if path.name == "__init__.py":
        parts = [path.parent.name]
        parent = path.parent.parent
    else:
        parts = [path.stem]
        parent = path.parent

    while (parent / "__init__.py").is_file():
        parts.append(parent.name)
        parent = parent.parent
    return ".".join(reversed(parts))
