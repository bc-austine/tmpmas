# `.github/` — GitHub-Specific Files

This directory contains files that GitHub reads automatically. Nothing here is part of
the TMPMAS application; it exists to configure repository-level behaviours on GitHub.

## Structure

```
.github/
├── workflows/           GitHub Actions CI/CD workflow definitions
├── ISSUE_TEMPLATE/      Templates for issue creation
├── PULL_REQUEST_TEMPLATE.md    Template for new pull requests
├── CODEOWNERS           Automatic reviewer assignment (when team grows)
├── dependabot.yml       Dependabot update configuration
└── README.md            ← you are here
```

*(Files will be created as their corresponding features are set up.)*

## What belongs here

- **GitHub Actions workflows** (`.github/workflows/*.yml`)
- **Issue templates** (`.github/ISSUE_TEMPLATE/*.md`)
- **Pull request template** (`.github/PULL_REQUEST_TEMPLATE.md`)
- **Code owners** (`.github/CODEOWNERS`) — routes PRs to reviewers automatically
- **Dependabot configuration** (`.github/dependabot.yml`)
- **Funding configuration** (`.github/FUNDING.yml`) — not used
- **Security policy** — actually lives at the repo root as `SECURITY.md`, not here

## What does NOT belong here

- **Application code** — that goes in `src/`
- **CI helper scripts** — those go in `ops/` if shared, or reference existing tools
- **Documentation** — that goes in `docs/`
- **Anything GitHub doesn't read from this location** — the directory exists solely for
  GitHub's file-discovery conventions

## Conventions

- Workflow files are named by their purpose: `ci.yml`, `release.yml`, `security-scan.yml`
- Branch protection requires all checks defined in `workflows/` to pass before merge
- Secrets are stored in GitHub's repository settings, not in workflow files
- Workflows are reviewed by a maintainer before merging — they execute on every push

## Pointers

- CI/CD ADR: ADR-013 (GitHub public repository with GitHub-hosted runners)
- CONTRIBUTING.md: [`../CONTRIBUTING.md`](../CONTRIBUTING.md)
