# `docs/` — Documentation

Architecture, design, and operational documentation for TMPMAS.

## Structure

```
docs/
├── architecture/     Architecture diagrams, descriptions, decisions
├── adrs/             Architecture Decision Records (ADR-NNN)
├── api/              API specifications (OpenAPI, protocol docs)
├── runbooks/         Operational runbooks (incident response, recovery)
├── user/             User-facing documentation (analyst workflows)
├── admin/            Administrator documentation (governance workflows)
├── analysis/         Exploratory analysis, research notes
└── testing/          Manual test procedures, verification evidence
```

## What belongs here

- Architecture descriptions and diagrams
- Architecture Decision Records (ADRs) — one file per decision
- API specifications
- Operational runbooks (startup, shutdown, backup, recovery, incident response)
- User guides for analysts
- Administrator guides for governance workflows
- Research notes and exploratory analysis
- Manual test procedures

## What does NOT belong here

- **Marketing copy** — nothing in `docs/` is promotional
- **External references** — link to them, don't copy them
- **Secrets or credentials** — never
- **Ephemeral notes** — if it's not worth maintaining, it doesn't go here
- **Code examples that duplicate `src/`** — reference the source

## Conventions

- Markdown format
- One ADR per file, named `ADR-NNN-short-title.md`
- Every runbook has an owner and a last-reviewed date
- Diagrams are stored as source (e.g. Mermaid, PlantUML) and rendered images

## Pointers

- Repository layout: [`../CONTRIBUTING.md#repository-layout`](../CONTRIBUTING.md#repository-layout)
- ADR template: `docs/adrs/000-template.md` (to be added)