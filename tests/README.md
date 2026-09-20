# `tests/` — Test Suites

All test code lives here, mirroring the structure of `src/`.

## Structure

The directory structure under `tests/` mirrors the structure under `src/`:

```
tests/
├── unit/           Unit tests (fast, isolated)
├── integration/    Integration tests (component interactions)
├── system/         End-to-end system tests
├── acceptance/     Acceptance tests against criteria
├── performance/    Performance and load tests
├── security/       Security tests
├── fixtures/       Shared test data and factories
└── conftest.py     Shared pytest configuration
```

### Naming convention

For a module at `src/ingestion/adapters/tennis_abstract.py`, the corresponding unit tests
live at `tests/unit/ingestion/adapters/test_tennis_abstract.py`. This symmetry makes it
easy to navigate between code and its tests.

## What belongs here

- Unit tests for any function with non-trivial logic
- Integration tests for API endpoints and cross-component interactions
- System tests for analyst-facing and operations-facing workflows
- Test fixtures, factories, and shared utilities
- Synthetic test data

## What does NOT belong here

- **Production code** — that goes in `src/`
- **Real production data** — never. Test data must be synthetic or anonymised
- **One-off debug scripts** — if you need to reproduce a bug, either fix the test or
  document the reproduction in an issue
- **Manual test scripts** — manual testing procedures belong in `docs/testing/`

## Conventions

- Framework: **pytest**
- Coverage target: **80% line, 70% branch** on new code
- Tests are **deterministic** — no flaky tests. A flaky test is fixed or deleted
- Tests are **independent** — no ordering dependencies between tests
- Test data is **synthetic** — never real fixtures from production sources
- Test evidence (reports, coverage) is uploaded to GitHub Artifacts by CI

## Running tests

*(Once the environment and test framework are fully wired up in Phase 4 Steps 6-7, this
section will list the exact commands. For now, standard pytest invocation applies.)*

```bash
# All tests
pytest

# Unit tests only (fast)
pytest tests/unit/

# With coverage
pytest --cov=src --cov-report=html

# A specific test file
pytest tests/unit/ingestion/adapters/test_tennis_abstract.py
```

## Pointers

- Testing standards: [`../CONTRIBUTING.md#testing`](../CONTRIBUTING.md#testing)
- Test framework ADR: ADR-016 (pytest primary; Robot Framework optional)