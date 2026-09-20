# Security Policy

## Supported Versions

TMPMAS is in pre-release development. There are currently no production releases.

| Version | Supported |
|---------|-----------|
| pre-release (main) | ✅ Security fixes applied |
| future releases    | ✅ See release notes for support window |

Once the project reaches its first production release, this table will list the specific
versions that receive security updates and the duration of each support window.

---

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you believe you have found a security vulnerability in TMPMAS, report it privately
using **GitHub's Private Vulnerability Reporting**:

1. Go to the [Security tab](https://github.com/bc-austine/tmpmas/security) of the repository.
2. Click **Report a vulnerability**.
3. Fill in the form with as much detail as you can.

This channel is private, authenticated, and visible only to repository maintainers. It is
the preferred method for all security disclosures.

If for any reason you cannot use the private reporting form, you may open a public issue
asking for a private contact channel — but **do not include any vulnerability details in
that issue**. A maintainer will follow up with a private channel.

---

## What to Include

A useful report usually contains:

- **Summary** — a one-sentence description of the vulnerability
- **Impact** — what an attacker could accomplish by exploiting it
- **Affected component(s)** — which part of the system is affected (e.g. authentication,
  ingestion adapters, model registry, audit log)
- **Reproduction steps** — as detailed as necessary to reliably trigger the issue
- **Proof of concept** — a minimal example or script, if applicable
- **Suggested fix or mitigation** — optional, but appreciated
- **Your contact information** — how you'd like to be reached for follow-up

You do not need to be exhaustive. A partial report is better than no report. If you're
unsure whether something counts as a vulnerability, err on the side of reporting.

---

## What to Expect

When you submit a report through GitHub's Private Vulnerability Reporting form:

| Timeframe | What happens |
|-----------|--------------|
| Within **3 business days** | Acknowledgment of receipt |
| Within **10 business days** | Initial assessment — validation or request for more information |
| Within **30 days** | Fix planned, or a documented decision on whether the report is in scope |
| Fix released | Coordinated disclosure — reporter notified before public announcement |

Timelines are best-effort. TMPMAS is currently maintained on a volunteer basis; complex
reports may take longer. We will keep you informed throughout the process.

---

## Disclosure Policy

We follow **coordinated disclosure**:

1. **Report received and validated.**
2. **Fix developed** — privately, in a non-public branch.
3. **Reporter notified** of the planned fix and anticipated release date.
4. **Fix released**, with a security advisory published on GitHub.
5. **Reporter credited** in the advisory, unless they prefer to remain anonymous.
6. **Public disclosure** — typically 90 days after the fix is released, or earlier if
   the reporter and maintainers agree.

If a vulnerability is being actively exploited in the wild, or if a fix is delayed
beyond 90 days, we will discuss a modified timeline with the reporter.

---

## Scope

### In scope

Security issues affecting:

- **Authentication and session management** — authentication bypass, session fixation,
  credential leakage, session hijacking
- **Authorisation** — privilege escalation, bypass of role-based access controls,
  bypass of approval separation
- **Data integrity** — tampering with prediction snapshots, audit log manipulation,
  bypass of hash-chain verification
- **Data privacy** — exposure of personal information, credentials, or source API keys
- **Temporal integrity** — injection of post-cut-off information into prediction-time data
- **Injection attacks** — SQL injection, command injection, template injection in any
  component that processes external data
- **Dependency vulnerabilities** — known CVEs in third-party packages that we have not
  yet patched (please report these; Dependabot often catches them first)
- **Supply chain** — malicious packages, compromised build artefacts, unauthorised
  changes to the CI/CD pipeline

### Out of scope

The following are **not** considered security vulnerabilities for the purposes of this
policy. They should be raised as regular GitHub issues instead:

- **Analytical accuracy** — the model produces a probability you disagree with
- **Ranking methodology** — you believe the ranking algorithm weights factors incorrectly
- **UI/UX issues** — the analyst workspace is confusing or hard to use
- **Feature requests** — "the system should also support doubles"
- **Theoretical vulnerabilities without demonstrated impact** — reports that require
  an attacker to already have administrative access
- **Denial of service via resource exhaustion** — the free-tier infrastructure has
  limited capacity; DoS is a known and accepted constraint (see AR-003 in the risk register)
- **Vulnerabilities in external data sources** — those should be reported to the
  respective source provider

If you're unsure whether something is in scope, **ask**. We'd rather receive a report
that turns out to be out of scope than miss a genuine issue.

---

## Acknowledgements

We are grateful to security researchers who help keep TMPMAS and its users safe.
Reporters who wish to be credited will be acknowledged in the relevant GitHub Security
Advisory and, where applicable, in release notes.

---

*This policy is maintained by the project maintainers. If something is unclear, or if
you would like to suggest an improvement, open a pull request.*