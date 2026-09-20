# Contributing to TMPMAS

Thank you for your interest in the Tennis Match Probability & Market Analysis System (TMPMAS).

This document defines how to work on the project: how to set up your environment, how to
structure changes, how to submit them, and what standards apply. Following it ensures your
contributions integrate smoothly and reach `main` without unnecessary friction.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Repository Layout](#repository-layout)
4. [Branching](#branching)
5. [Commit Messages](#commit-messages)
6. [Pull Requests](#pull-requests)
7. [Code Review](#code-review)
8. [Coding Standards](#coding-standards)
9. [Testing](#testing)
10. [Where to Get Help](#where-to-get-help)

---

## Code of Conduct

Participation in this project is governed by [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
By contributing, you agree to uphold its standards.

---

## Getting Started

### Prerequisites

- **Python 3.12+** — `python --version`
- **Git 2.40+** — `git --version`
- **Docker 24+ with the `docker compose` plugin** — `docker compose version`
- **GitHub CLI (`gh`) 2.x** — `gh --version`, authenticated via `gh auth login`

### Clone the repository

```bash
git clone https://github.com/bc-austine/tmpmas.git
cd tmpmas
```

**Windows note:** Clone into a location **outside of OneDrive, Dropbox, or any other cloud-sync
folder**, and **without spaces in the path**. Recommended: `C:\dev\tmpmas`.

### Environment setup

*(Docker Compose environment is under construction. This section will be updated once available.
For now, the application stack can be run manually.)*

### Verify your setup

```bash
git status                    # should show: On branch main, clean
git remote -v                 # origin should be HTTPS
gh auth status                # should show: Logged in to github.com
```

---

## Repository Layout

```
tmpmas/
├── .github/          GitHub-specific files (workflows, issue templates, PR template)
├── docs/             Documentation (architecture, ADRs, runbooks)
├── ops/              Operational assets (Docker, Prometheus, Grafana configs)
├── scripts/          Developer convenience scripts (setup, migration, backup)
├── src/              Application source code
├── tests/            Test suites
├── CONTRIBUTING.md   ← you are here
├── CODE_OF_CONDUCT.md
├── LICENSE
├── README.md
├── SECURITY.md
└── STANDARDS-EXCEPTIONS.md
```

**Rules:**

- Application code goes in `src/` — nowhere else.
- Tests go in `tests/`, mirroring the structure of `src/`.
- Operational files (Docker, monitoring) go in `ops/`.
- Documentation goes in `docs/` unless it's a top-level governance file.
- Do not create new top-level directories without discussion.

---

## Branching

### Rules

- **`main` is protected.** No direct pushes. All changes arrive via pull request.
- **Branch from `main`.** Keep your branch up to date via `git rebase main` (never merge `main` into your branch).
- **Use short-lived branches.** One logical change per branch.
- **Branch names** follow the pattern `<type>/<short-description>`:

| Type | Use for | Example |
|------|---------|---------|
| `feature/` | New functionality | `feature/odds-ingestion` |
| `bugfix/` | Non-urgent fixes | `bugfix/timestamp-parsing` |
| `hotfix/` | Urgent production fixes | `hotfix/auth-bypass` |
| `chore/` | Tooling, configs, dependencies | `chore/update-ruff` |
| `docs/` | Documentation only | `docs/adr-019` |
| `refactor/` | Internal restructuring, no behaviour change | `refactor/validation-service` |

**Example:**

```bash
git checkout main
git pull
git checkout -b feature/odds-ingestion
```

---

## Commit Messages

This project uses **Conventional Commits**. Every commit message must follow the format:

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

### Types

| Type | Use for |
|------|---------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation changes |
| `style` | Formatting, whitespace (no logic change) |
| `refactor` | Code restructuring (no behaviour change) |
| `test` | Adding or updating tests |
| `chore` | Build tooling, dependency updates, CI |
| `perf` | Performance improvements |

### Rules

- **Imperative mood** — "add feature", not "added feature" or "adds feature"
- **Lowercase description** — do not capitalise the first word
- **No full stop** at the end
- **Subject ≤ 72 characters**
- **Reference the story or issue** in the body if applicable

### Examples

Good:

```
feat(ingestion): add TennisAbstract adapter
fix(temporal): respect prediction cut-off for odds history
docs(contributing): clarify branch naming rules
chore(deps): bump pytest to 8.2.0
```

Bad:

```
Added some stuff
WIP
Fixed the bug.
FEAT: New feature!!!
```

---

## Pull Requests

### Before opening a PR

1. **Rebase on latest `main`:** `git fetch && git rebase origin/main`
2. **Run the test suite locally** (once available): `pytest`
3. **Run any pre-commit hooks:** `pre-commit run --all-files`
4. **Verify your branch is a single logical change.** If it's two, split it into two PRs.

### PR rules

- **Small PRs.** Target: **≤ 400 lines changed** (excluding generated files). If your PR exceeds this, split it.
- **Descriptive title.** Follows the same format as commits: `feat(ingestion): add TennisAbstract adapter`.
- **Reference the story.** If the change is motivated by a user story (`US-XX`) or feature (`F-XX`), mention it in the PR description.
- **Fill in the PR template.** When the template lands (Step 5), it will ask for context, testing, and checklist items.
- **All CI checks must pass.** A PR with failing checks cannot be merged.
- **One approval required.** The reviewer must not be the author.
- **All review conversations must be resolved** before merge.

### Merge method

**Squash merge only.** All commits on your branch are collapsed into a single commit on `main`.
This is enforced at the repository level — the merge-commit and rebase-merge buttons are disabled.

### After merge

Your branch will be deleted automatically. Switch back to `main` and pull:

```bash
git checkout main
git pull
```

---

## Code Review

### As the author

- **Keep PRs small.** Reviewers are more effective on small, focused changes.
- **Self-review before assigning.** Read your own diff in the browser before requesting review.
- **Respond to every comment.** Even if only to acknowledge.
- **Do not merge your own PR.** Even if you have admin rights (branch protection prevents this).

### As the reviewer

- **Review within one working day.** If you can't, tell the author so they can find another reviewer.
- **Check for:**
  - Correctness (does it do what it claims?)
  - Security (any injection, auth, or data-leak issues?)
  - Coverage (are there tests? do they exercise the new behaviour?)
  - Standards (does it follow the coding standards in §"Coding Standards"?)
  - Readability (would you understand this in six months?)
- **Be specific.** "This is wrong" is less useful than "this will throw a `KeyError` if `data` is empty — see line 42."
- **Approve explicitly** when ready. Do not approve with unresolved concerns.
- **Re-review after changes.** Approval applies to the state you reviewed, not the branch in general.

---

## Coding Standards

The full standards are in the Phase 4 Technical Standards document. Summary of the essentials:

### Python

- **Follow PEP 8** (style) and PEP 257 (docstrings).
- **Type-hint all functions.** Mypy/pyright is enforced in CI.
- **Lint with ruff or flake8**, format with black or ruff format.
- **Functions ≤ 50 lines.** If it's longer, refactor.
- **Cyclomatic complexity ≤ 10.**
- **No dead code.** Delete it; Git remembers.
- **Comments explain *why*, not *what*.** "Increment counter" is noise; "Increment because the API returns 1-indexed offsets" is signal.
- **Dependencies are pinned** with a lockfile. Update intentionally, not accidentally.

### Repository

- **Secrets are never committed.** Ever. Pre-commit hooks will enforce this; GitHub's push protection is the last line of defence.
- **Large binaries are not committed.** Use Git LFS if we must (we shouldn't).
- **Every top-level directory has a README.**

### API (when applicable)

- REST over HTTPS
- OpenAPI 3.1 documentation
- Versioned prefixes (`/v1/...`)
- Standard error envelope
- Every endpoint authenticated and authorised
- Rate limits documented

---

## Testing

- **Unit tests** cover every module with non-trivial logic.
- **Integration tests** cover every API endpoint and cross-component interaction.
- **System tests** cover every analyst-facing workflow end-to-end.
- **Coverage target:** 80% line, 70% branch on new code.
- **Tests are deterministic.** No flaky tests. If one is flaky, fix it or delete it.
- **Tests are independent.** No ordering dependencies.
- **Test data is synthetic.** Never use production data.

Specific test tooling and commands will be documented once the test framework is fully wired up (Step 7 of the infrastructure bootstrap).

---

## Where to Get Help

- **Project documentation:** see the `docs/` directory and the project's Phase packs.
- **Architecture questions:** see the ADRs (recorded in the Phase 4 pack).
- **Bug reports and feature requests:** open a GitHub issue using the appropriate template.
- **Security issues:** see [`SECURITY.md`](SECURITY.md) — do not open a public issue.

---

*This document is maintained by the project maintainers. If something is unclear, outdated, or
missing, open a PR to improve it.*