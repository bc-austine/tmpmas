# `scripts/` — Developer Convenience Scripts

Helper scripts that developers run locally to set up, seed, inspect, or maintain their
development environment.

## What belongs here

- **Setup scripts** — one-shot environment bootstrapping helpers
- **Database seeding** — load synthetic fixtures into a local database
- **Data inspection** — utilities for examining local data (e.g. dumping a snapshot)
- **Migration helpers** — wrapper scripts around Alembic or equivalent
- **Local maintenance** — clearing caches, resetting the local environment
- **Debug utilities** — targeted diagnostics for local development issues

## What does NOT belong here

- **Production scripts** — those go in `ops/` (see the distinction below)
- **Application code** — that goes in `src/`
- **Test code** — that goes in `tests/`
- **CI pipeline scripts** — those are defined in `.github/workflows/` and their helpers
  live in `ops/` if they're shared with production

## The `scripts/` vs `ops/` distinction

The rule of thumb:

- **`scripts/`** → runs on a **developer's machine**, never touches production
- **`ops/`** → runs on **shared infrastructure or production**, part of the deployment

If you're unsure, ask: *"Would I run this on my laptop while developing, or on the server
during deployment?"* The answer tells you which directory.

## Conventions

- **Idempotent** — running a script twice does not produce different results than running
  it once (unless explicitly a one-shot migration)
- **Self-documenting** — each script starts with a docstring or comment explaining what it
  does, what it requires, and what it changes
- **No secrets hardcoded** — read from environment or `.env` files
- **Executable bit set** — `chmod +x` so scripts can be run directly
- **Errors fail loudly** — scripts use `set -e` (bash) or explicit error handling (Python)
  to exit on first failure

## Running scripts

```bash
# From repo root
./scripts/some-script.sh
```

## Pointers

- Repository layout: [`../CONTRIBUTING.md#repository-layout`](../CONTRIBUTING.md#repository-layout)
