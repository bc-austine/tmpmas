# `src/` — Application Source Code

Application code for the TMPMAS platform lives here, organised by service.

## Structure

Each subdirectory under `src/` corresponds to a logical component from the Phase 4
Architecture Description:

| Subdirectory | Responsibility |
|--------------|----------------|
| `ingestion/` | External data acquisition via per-source adapters |
| `validation/` | Data validation, completeness, cross-source conflict detection |
| `temporal/` | Event/information/acquisition time tracking, prediction cut-off enforcement |
| `analytical/` | Probability estimation, calibration, uncertainty, confidence, stability |
| `value/` | Fair-odds calculation, price comparison, value assessment |
| `opportunity/` | Opportunity qualification, ranking, lifecycle |
| `decision/` | Analyst decision capture, snapshot preservation |
| `ticket/` | Ticket construction and management |
| `outcome/` | Outcome acquisition, evaluation |
| `governance/` | Approval workflows, effective dating, investigation |
| `auth/` | Authentication, session management |
| `authorisation/` | Role-based access control, approval separation |
| `audit/` | Hash-chained audit event recording |
| `notification/` | Alert generation and routing |
| `observability/` | Metrics, logs, traces |
| `web/` | Web application, API gateway |

*(Subdirectories will be created as their components are implemented. The structure above
reflects the Phase 4 architecture baseline and may be refined during Phase 5 Sprint planning.)*

## What belongs here

- Production application code (Python modules)
- Configuration files specific to a service
- Type definitions and interfaces
- Internal utility functions used by more than one component

## What does NOT belong here

- **Tests** — those go in `tests/` (mirroring this structure)
- **Development scripts** — those go in `scripts/`
- **Operational configuration** — Dockerfiles, Prometheus configs, etc. go in `ops/`
- **Documentation** — architecture and design docs go in `docs/`
- **Notebooks or exploratory code** — those go in `docs/analysis/` (or a separate sandbox, if added later)

## Conventions

All code in `src/` follows the standards in [`../CONTRIBUTING.md`](../CONTRIBUTING.md):

- Python 3.12+
- Type hints on all functions
- PEP 8 style, formatted with `black` or `ruff format`
- Linted with `ruff` or `flake8`
- Functions ≤ 50 lines
- Cyclomatic complexity ≤ 10
- No dead code

## Pointers

- Architecture baseline: Phase 4 Architecture Description
- Coding standards: [`../CONTRIBUTING.md`](../CONTRIBUTING.md)
- ADRs: Phase 4 Architecture Decision Records
