# Standards Exceptions Register

This document records every known deviation from the standards set out in
[`CONTRIBUTING.md`](CONTRIBUTING.md) and the TMPMAS Phase 4 Technical Standards.

The purpose of this register is **transparency**. Standards exist to be followed; when a
standard cannot be followed, the deviation is documented here — with a reason, an approver,
and a review date. Silent deviation is not permitted.

---

## How to Use This Register

### Adding an exception

1. **Open a PR** that both introduces the exception and updates this file in the same change.
2. **Add a row** to the table below, following the format.
3. **Justify the exception** in the PR description and in the register.
4. **Get approval** from a maintainer (or the Project Owner for material exceptions).
5. **Set a review date.** No exceptions are permanent. Choose a date when the exception
   will be re-evaluated.

### Reviewing an exception

At each review date, one of three things happens:

- **Extended** — the exception is still needed; extend with a new review date and updated reason.
- **Closed** — the exception is no longer needed; move it to the Closed Exceptions section.
- **Escalated** — the exception reveals a problem with the underlying standard; the standard
  should be changed via the normal standards process, and the exception closed once it is.

### Removing an exception

When an exception is resolved (the code now complies with the standard), move its row to the
**Closed Exceptions** section. Do not delete it — history is preserved.

---

## Active Exceptions

*No active exceptions.*

---

## Closed Exceptions

*No closed exceptions.*

---

## Exception Format Reference

When adding an exception, use this table format:

| ID | Date | Standard | Scope | Reason | Approver | Review date | Status |
|----|------|----------|-------|--------|----------|-------------|--------|
| EX-001 | 2026-04-01 | C-05 (max 50 lines/function) | `src/analytics/integration.py::solve` | Numerical integration; splitting obscures the algorithm | @maintainer | 2026-10-01 | Active |

### Field definitions

- **ID** — `EX-NNN`, sequentially assigned, never reused.
- **Date** — the date the exception was approved (ISO 8601, `YYYY-MM-DD`).
- **Standard** — the specific standard being excepted (e.g. `C-05`, `T-03`, `DS-05`).
- **Scope** — the exact file, function, or component where the exception applies. Be specific.
- **Reason** — a one or two sentence justification. "It was easier" is not a reason. "The
  algorithm's mathematical structure requires a single function to remain readable" is.
- **Approver** — who authorised the exception.
- **Review date** — when the exception will be re-evaluated. Maximum 12 months out.
- **Status** — `Active` or `Closed`.

---

## Rules for Exceptions

1. **Exception before the fact, not after.** If a code review reveals a standards violation
   that was intentional, it does not become an exception retroactively. The PR that
   introduced the violation should have updated this file. If it didn't, the standards
   governing future PRs apply — the code must be brought into compliance or the exception
   formally opened now.
2. **Every exception has a review date.** No exception is permanent. Reviews happen on
   or before the review date.
3. **Every exception has an approver.** Exceptions to critical standards (Security `S-NN`,
   Data `DS-NN`, Temporal `TM-NN`) require approval from a Governance user, not just the
   author's peer.
4. **Repeated exceptions to the same standard are a signal.** If you find yourself adding
   the third exception to the same rule, the rule is wrong. Propose a standards change.
5. **Some standards cannot be excepted.** The following are absolute and cannot appear in
   this register:
   - `S-16` (secrets via environment variables) and `S-17` (secrets never logged)
   - `DS-06` (every snapshot is hash-chained)
   - `DS-08` (every externally-sourced record carries provenance)
   - `DS-14` (historical records never silently rewritten)
   - `CM-06` (no secrets, credentials, or large binaries in commits)

   If you believe you need an exception to one of these, escalate to the Project Owner
   directly. These are invariants of the system, not guidelines.

---

## Maintenance

- This register is reviewed at each lifecycle gate (G5, G6, G7).
- It is also reviewed whenever a new standard is added or an existing standard changes.
- The Project Owner is the final authority on whether an exception is accepted.

---

*This file is part of the project's governance framework. If it becomes large, it will be
split into per-category registers (coding, testing, security, data). Until then, a single
file keeps the discipline visible.*
