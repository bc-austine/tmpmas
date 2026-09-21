"""Smoke test for the `src` package import chain.

Verifies that:
  - The `src` package is importable from the test suite.
  - The package exposes `__version__` (used in user agents, diagnostics,
    and version-pinned reports).
  - The version string is well-formed.

This test does not exercise application logic — it verifies that the
Python path configuration is correct and pytest can import from `src/`.
"""

from __future__ import annotations

import src


def test_src_package_importable() -> None:
    """The `src` package can be imported."""
    assert src is not None


def test_src_package_exposes_version() -> None:
    """The `src` package exposes a `__version__` string."""
    assert hasattr(src, "__version__")
    assert isinstance(src.__version__, str)


def test_src_version_is_semver_shaped() -> None:
    """`__version__` follows a major.minor.patch pattern."""
    parts = src.__version__.split(".")
    assert len(parts) == 3, f"Expected 3 version segments; got {len(parts)}"
    for part in parts:
        assert part.isdigit(), f"Version segment {part!r} is not numeric"


def test_src_version_info_matches_version_string() -> None:
    """`__version_info__` is consistent with `__version__`."""
    expected = tuple(int(p) for p in src.__version__.split("."))
    assert src.__version_info__ == expected