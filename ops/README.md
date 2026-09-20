# `ops/` — Operational Assets

Deployment, monitoring, and infrastructure assets for TMPMAS.

## Structure

```
ops/
├── docker/           Dockerfiles for each service
├── compose/          Docker Compose configurations (dev, staging, production)
├── prometheus/       Prometheus scrape configs and alert rules
├── grafana/          Grafana dashboard definitions
├── otel/             OpenTelemetry collector configuration
├── backups/          Backup scripts and retention policies
├── deployment/       Deployment scripts and release tooling
└── runbooks/         Operational runbooks (links to docs/runbooks/)
```

*(Structure to be finalised in Phase 4 Steps 6-8.)*

## What belongs here

- **Dockerfiles** for application services
- **Docker Compose** configurations for the local development environment
- **Prometheus** scrape configs and alert rules
- **Grafana** dashboard JSON definitions
- **OpenTelemetry** collector configuration
- **Backup** scripts and scheduling definitions
- **Deployment** scripts and rollback procedures
- **Infrastructure-as-code** definitions (when adopted)

## What does NOT belong here

- **Application code** — that goes in `src/`
- **Test code** — that goes in `tests/`
- **Developer convenience scripts** — those go in `scripts/`
- **Documentation of operational procedures** — those go in `docs/runbooks/`; `ops/` holds
  the *executable* assets
- **Secrets** — never. Configuration with secrets uses environment variables (see ADR-008)

## The `ops/` vs `scripts/` distinction

This is the most common source of confusion. The rule:

- **`ops/`** contains assets that run **in production or on shared infrastructure** —
  Dockerfiles, monitoring configs, deployment scripts
- **`scripts/`** contains utilities that run **on a developer's machine** for convenience —
  environment setup, database seeding, local testing helpers

If a script is deployed to a server, it goes in `ops/`. If a developer runs it locally, it
goes in `scripts/`.

## Conventions

- Configuration is versioned (git history tracks every change)
- Every operational asset has a corresponding runbook entry in `docs/runbooks/`
- Secrets are injected via environment variables or encrypted configuration (ADR-008)
- No build happens on production — artefacts come from CI (DP-02)

## Pointers

- Deployment standards: [`../CONTRIBUTING.md`](../CONTRIBUTING.md) and Phase 4 §10.10
- Backup ADR: ADR-012
- Observability stack: ADR-011
- Secrets management: ADR-008
