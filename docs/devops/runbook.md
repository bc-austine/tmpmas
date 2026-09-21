# TMPMAS — DevOps Runbook

**Owner:** DevOps Engineer
**Last reviewed:** 2026-09-21
**Review cadence:** Every 4 weeks

---

## 1. Purpose

This runbook documents routine operational procedures, common failures, and
their resolutions. It is the authoritative source for "how do I do X on this
project?" questions at the infrastructure layer.

---

## 2. Daily Operations

### 2.1 Bring up the environment

```bash
cd /c/dev/tmpmas
make up
make ps
```

Five containers should be `Up` (or `Up (healthy)`):
- `tmpmas-app`
- `tmpmas-db`
- `tmpmas-prometheus`
- `tmpmas-grafana`
- `tmpmas-otel-collector`

### 2.2 Stop the environment (preserves database)

```bash
make down
```

### 2.3 Stop and delete database (destroys local state)

```bash
make clean     # prompts for confirmation
```

### 2.4 Run tests

```bash
make test      # runs pytest inside the app container
```

### 2.5 Run pre-commit against all files

```bash
pre-commit run --all-files
```

---

## 3. Common Failures

### 3.1 `docker: command not found`

Docker Desktop is not running or not on PATH.
**Fix:** Start Docker Desktop. Wait for the whale icon to stop animating.

### 3.2 gitleaks hook reports `[WinError 4551]`

Windows 11 Smart App Control blocked the native gitleaks binary.
**Fix:** Our pre-commit hook runs gitleaks inside a Linux container, so
this error should not appear in normal operation. If it does:
1. Confirm `make init` has been run (pulls the gitleaks image)
2. Confirm Docker Desktop is running
3. Confirm `.pre-commit-config.yaml` uses the containerised hook

### 3.3 gitleaks reports "Passed" but a real secret is committed

This is the dangerous false-negative case.
**Cause:** gitleaks `protect --staged` silently fails on Docker Desktop for
Windows. It falls back to scanning commits and misses staged content.
**Fix:** Our config uses `detect --source` instead of `protect --staged`.
If the config is ever reverted to `protect --staged`, this failure returns.
**Verification:** To test the hook, write a synthetic file containing a
randomly-generated string matching the AWS access-key shape
(`AKIA` followed by 16 random alphanumeric characters), and commit it on
a scratch branch. Do NOT use AWS's documentation example
(`AKIA` + `IOSFODNN7EXAMPLE`) — gitleaks allowlists it, so the hook will
silently pass and you will believe the check works when it does not.

Generate a test key shape with:
`echo "AKIA$(LC_ALL=C tr -dc A-Z0-9 </dev/urandom | head -c 16)"`

### 3.4 `make up` fails with "pull access denied for tmpmas/app"

Harmless. Docker checks for a pre-built image before building locally; if
none exists it builds. The message is informational.

### 3.5 Container build times out during pip install

Network issue. pip is configured with `PIP_DEFAULT_TIMEOUT=180` and
`PIP_RETRIES=10`. If it still fails:
```bash
make up     # retry; Docker caches completed layers
```
If failures persist across 3 retries, consider a PyPI mirror.

### 3.6 Branch protection blocks a merge

The `scripts/merge-pr.sh` guard refuses to merge if any CI check is not
green.
**Fix:** Wait for all checks to show ✓. Re-run `gh pr checks`.

### 3.7 PR is not mergeable but no checks are pending or failing

The branch is behind `main`. Rebase:
```bash
git fetch origin
git rebase origin/main
git push --force-with-lease
```

---

## 4. CI Pipeline Map

As of 2026-09-21, `.github/workflows/ci.yml` contains these jobs. Each is a
required status check on `main`.

| Job | Blocks merge | Purpose |
|-----|-------------|---------|
| `lint` | Yes | ruff |
| `format-check` | Yes | ruff format --check |
| `type-check` | Yes | mypy |
| `security` | Yes | gitleaks + pip-audit |
| `test` | Yes | pytest with coverage |

**Planned additions** (Pre-condition #3):
| Job | Blocks merge | Status |
|-----|-------------|--------|
| `codeql` | Yes | In progress (Phase 1) |
| `outbound-api-pattern` | Yes | Phase 2 |
| `constitutional-invariant` | Yes | Phase 2 |
| `traceability` | Warn-only → Yes | Phase 2 (blocking after RTM lands) |

---

## 5. Observability

| Service | URL | Credentials |
|---------|-----|-------------|
| Prometheus | http://localhost:9090 | None |
| Grafana | http://localhost:3000 | admin / admin (dev only) |
| OTel collector (metrics) | http://localhost:8888/metrics | None |

**Grafana dashboards:** Open `TMPMAS → Overview`.

**Retention:** Prometheus 30 days; Grafana indefinite; audit log indefinite.

---

## 6. Secrets Management

- All secrets in `.env` (gitignored)
- `.env.example` documents required variables
- gitleaks scans both pre-commit (container) and CI (native)
- GitHub secret scanning + push protection are enabled at the repo level

**Rotation:** Manual. Documented in `SECURITY.md`.

---

## 7. Emergency Procedures

### 7.1 CI is broken on main

1. Confirm the failure: `gh run list --branch main --limit 3`
2. Identify the failing job: `gh run view <run-id>`
3. If the failure is in a job (not the pipeline itself), fix-forward via a
   PR with the failing job's minimum required change
4. If the pipeline itself is broken (workflow syntax error), temporarily
   disable the workflow from the Actions tab, push the fix, re-enable

### 7.2 Branch protection must be temporarily relaxed

Only via `scripts/merge-pr.sh`, which restores protection atomically.
Never modify branch protection directly.

### 7.3 Docker Desktop not starting

Restart Docker Desktop. If it hangs:
1. Quit Docker Desktop
2. `wsl --shutdown` (from PowerShell as admin)
3. Restart Docker Desktop

---

## 8. Known Limitations

| Limitation | Impact | Workaround |
|-----------|--------|-----------|
| gitleaks blocked by Windows SAC natively | None — running in container | Containerised hook |
| `protect --staged` silently fails | Hidden secret commits | Use `detect --source` |
| Slow PyPI network | Build timeouts | Longer pip timeout, retries |
| OneDrive corrupts `.git` | Repo corruption | Repo lives at `/c/dev/tmpmas` |
| ADR-019/020/021/022/023/024 not yet in `docs/adr/` | ADRs only in Phase 4 pack | Migrate during Phase 2 |

---

## 9. Contacts

| Role | Contact |
|------|---------|
| DevOps Engineer | @bc-austine |
| Scrum Master | (TBD) |
| Project Owner | Best-Chinoziem, Austine C |
