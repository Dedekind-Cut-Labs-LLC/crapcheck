"""Tests for deterministic Python source discovery."""

from pathlib import Path

from crapcheck.discovery import DiscoveredSource, discover_sources


def _write_python(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("def run():\n    return 1\n", encoding="utf-8")
    return path.resolve()


def test_discovers_python_files_deterministically_with_package_names(tmp_path: Path) -> None:
    source_root = tmp_path / "src"
    alpha = _write_python(source_root / "alpha.py")
    package = _write_python(source_root / "package" / "__init__.py")
    nested = _write_python(source_root / "package" / "nested.py")
    _write_python(source_root / ".hidden" / "ignored.py")
    _write_python(source_root / ".venv" / "ignored.py")
    _write_python(source_root / "__pycache__" / "ignored.py")
    _write_python(source_root / "build" / "ignored.py")
    _write_python(source_root / "dist" / "ignored.py")

    assert discover_sources([source_root, alpha]) == [
        DiscoveredSource(path=alpha, module="alpha"),
        DiscoveredSource(path=package, module="package"),
        DiscoveredSource(path=nested, module="package.nested"),
    ]


def test_explicit_file_is_resolved_and_uses_its_package_name(tmp_path: Path) -> None:
    package = tmp_path / "package"
    _write_python(package / "__init__.py")
    module = _write_python(package / "module.py")

    assert discover_sources([package / ".." / "package" / "module.py"]) == [
        DiscoveredSource(path=module, module="package.module")
    ]
