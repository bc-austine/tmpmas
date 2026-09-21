"""Pytest configuration and shared fixtures for the TMPMAS test suite.

This file is automatically discovered by pytest. Fixtures defined here are
available to every test in the project. See https://docs.pytest.org/en/stable/
for the full pytest fixture reference.

Conventions:
    - Fixtures in this file are project-wide. For fixtures specific to one
      subsystem, place a conftest.py inside the relevant subdirectory.
    - Custom markers used by tests are registered here so pytest does not warn
      about unknown markers.

Adding a marker:
    1. Add the name to `MARKERS` below with a description.
    2. In `pytest_configure`, add it via `config.addinivalue_line`.
    3. Use it in tests with `@pytest.mark.<name>`.
"""

from __future__ import annotations

# -----------------------------------------------------------------------------
# Custom markers
# -----------------------------------------------------------------------------
# Registered markers avoid PytestUnknownMarkWarning and document intent.
# Usage in a test: @pytest.mark.<name>
MARKERS = [
    ("slow", "Test takes more than 1 second; deselected in fast runs."),
    ("integration", "Requires external resources (database, network)."),
    ("security", "Security-specific test (authentication, authorisation)."),
]


def pytest_configure(config: object) -> None:
    """Register custom markers with pytest.

    pytest calls this function during startup. The ``config`` argument is a
    pytest Config object; we use ``addinivalue_line`` to register each marker
    so pytest recognises them and reports them in --markers output.
    """
    # ``config`` is typed as ``object`` to avoid importing pytest for
    # type-checking purposes only. Runtime behaviour is unaffected.
    addinivalue_line = getattr(config, "addinivalue_line")
    for name, description in MARKERS:
        addinivalue_line("markers", f"{name}: {description}")


# -----------------------------------------------------------------------------
# Shared fixtures
# -----------------------------------------------------------------------------
# No project-wide fixtures yet. Add them here as Phase 5 Sprint 1 introduces
# shared test dependencies (e.g. a database session, a temporary directory,
# a fake clock for temporal tests).