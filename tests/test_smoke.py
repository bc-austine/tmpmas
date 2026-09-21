"""Smoke test to verify the CI pipeline runs end-to-end.

This test proves the toolchain works — pytest discovers and executes tests,
coverage measurement runs, and the workflow completes successfully. It will
be joined by real tests as application code is developed in Phase 5.

The single assertion below is intentionally trivial.
"""

from __future__ import annotations


def test_pipeline_is_operational() -> None:
    """Confirm the test framework is wired up correctly."""
    assert True


def test_python_version_is_supported() -> None:
    """TMPMAS requires Python 3.12 or later."""
    import sys

    assert sys.version_info >= (3, 12), f"Python 3.12+ required; got {sys.version}"
