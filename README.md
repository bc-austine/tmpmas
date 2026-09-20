# Tennis Match Probability & Market Analysis System (TMPMAS)

> An operational, evidence-based, time-aware, multi-market analytical platform for tennis matches.

---

## Purpose

TMPMAS is an **operational decision-support system** for tennis match analysis. It integrates
reliable tennis and market data, applies shared tennis intelligence and market-specific
probability analysis, evaluates calibration, uncertainty, confidence and stability, compares
estimated probabilities with bookmaker prices, and ranks or withholds decisions according to
predefined validation and risk criteria.

The system supports **disciplined human analytical decision-making**.

---

## What TMPMAS is NOT

- **It does not place bets.** Ever.
- **It does not transfer funds.** Ever.
- **It does not execute financial transactions.** Ever.
- **It does not represent predictions as guaranteed outcomes.**
- **It does not treat a prediction as a decision.** The human analyst retains final authority.

The system is a tool that supports a human analyst. It is not an autonomous betting system.

---

## Core Principle

> **The system optimises for analytical reliability, not the production of a prediction for every match.**

NO DECISION is a first-class, valid outcome. When conditions for reliable analysis are not
satisfied, the system withholds a decision rather than forcing one.

---

## Scope

### In scope (initial)

- **Tours:** ATP and WTA singles
- **Markets:** Match Winner, Game Handicap, Set Handicap, Total Games, Set Betting
- **Analysis:** Shared tennis intelligence + market-specific probability analysis
- **Data:** Current and historical tennis data, fixture acquisition, market-price acquisition
- **Outputs:** Estimated probability, validated probability, fair odds, market odds, uncertainty,
  confidence, stability, value assessment, ranking, decision status
- **Governance:** Model registry, configuration versioning, full audit trail
- **Evaluation:** Immutable prediction snapshots, outcome evaluation, model vs. ticket performance

### Out of scope (initial)

- Automatic wager placement or financial execution
- Doubles
- Automatic model replacement or retraining
- Automatic modification of approved analytical thresholds
- Arbitrary model combination without validation
- Cross-market prediction without validated methodology
- Bookmaker-subset influence on model probability or fair odds

---

## Current Status

**Lifecycle phase:** Phase 4 — Risk-Based Architecture & Technical Foundation *(complete, G4 passed)*

**Next phase:** Phase 5 — Iterative Agile/Scrum Development

**Repository state:** Bootstrap — infrastructure scaffolding in progress.

---

## Getting Started

Setup instructions for developers are in [`CONTRIBUTING.md`](CONTRIBUTING.md).

Quick summary once the environment is ready:

```
git clone https://github.com/bc-austine/tmpmas.git
cd tmpmas
docker compose up
```

*(Docker Compose environment is being built in Phase 4 Step 6 — see the project documentation for current status.)*

---

## Documentation

The system's requirements, architecture, and governance are captured across four lifecycle phases:

| Phase | Document | Status |
|-------|----------|--------|
| Phase 1 | Initiation & Feasibility Pack | G1 passed |
| Phase 2 | Software Requirements Specification & Requirements Baseline | G2 passed |
| Phase 3 | Product & Release Planning Pack | G3 passed |
| Phase 4 | Risk-Based Architecture & Technical Foundation Pack | G4 passed |

### Architecture Decision Records

All significant technical decisions are recorded as ADRs. Key decisions:

| ADR | Decision |
|-----|----------|
| ADR-001 | Programming language: Python 3.12+ |
| ADR-003 | Primary data store: PostgreSQL (+ DuckDB for analytics) |
| ADR-005 | Temporal model: append-only + hash-chained + separate snapshot store |
| ADR-007 | Application-managed authentication (vetted libraries, external review) |
| ADR-009 | Hash-chained audit log |
| ADR-013 | CI/CD: GitHub public repository with GitHub-hosted runners |
| ADR-014 | Development environment: Docker Compose |
| ADR-017 | Hosting: free-tier cloud for production; local for development |

Full ADR set is captured in the Phase 4 pack.

---

## Governance

- **Contributing:** see [`CONTRIBUTING.md`](CONTRIBUTING.md)
- **Code of conduct:** see [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)
- **Security policy:** see [`SECURITY.md`](SECURITY.md)
- **Standards exceptions:** see [`STANDARDS-EXCEPTIONS.md`](STANDARDS-EXCEPTIONS.md)

---

## Licence

Licensed under the **Apache License, Version 2.0** — see [`LICENSE`](LICENSE).

Copyright © 2026 the TMPMAS project contributors.
