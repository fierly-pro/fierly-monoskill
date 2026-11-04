# Security Gate

> Load: before any release, production deploy, or publication.
> Pairs with: `security/baseline.md`, `security/testing.md`, `workflows/release.md`, `templates/security-gate.md`.

## Gate checklist

Record **pass / fail / not applicable / accepted risk** with evidence for each item.

### Code and design
- [ ] Trust boundaries and data flows reviewed for the changed surface.
- [ ] Authentication is present on every non-public entry point.
- [ ] Authorization is enforced server-side at the resource (object-level, tenant isolation).
- [ ] Input validation and context-aware output encoding cover all external data.
- [ ] Queries are parameterized; shell/process calls avoid untrusted interpolation.
- [ ] File uploads/paths are constrained; deserialization of untrusted data is avoided.
- [ ] Secrets are absent from code, images, logs, and client bundles.
- [ ] Errors do not leak stack traces, internal hosts, or sensitive data.

### Data
- [ ] Sensitive data is minimized, classified, encrypted in transit and at rest.
- [ ] Retention/deletion behavior is defined.
- [ ] Migrations are reviewed, backed up, and reversible or forward-fixable.
- [ ] Backup restore has been tested for the affected store.

### Dependencies and build
- [ ] Lockfiles are current; no unexplained new dependencies.
- [ ] SCA and secret scans are clean or findings are triaged.
- [ ] Critical/high vulnerabilities are fixed or explicitly accepted.
- [ ] CI permissions, action pinning, and environment protections are correct.
- [ ] Artifacts are built from the reviewed commit and signed/checksummed.

### Operations
- [ ] TLS and security headers are configured.
- [ ] Rate limits protect auth, reset, OTP, export, and expensive endpoints.
- [ ] Logging/alerting covers security events without sensitive payloads.
- [ ] Rollback and incident contacts are documented.

### Verification
- [ ] Security tests or manual abuse cases were executed for the changed surface.
- [ ] Findings were retested after fixes.
- [ ] Residual risk and untested areas are stated.

## Severity and blocking rules

| Severity | Examples | Release rule |
|---|---|---|
| Critical | RCE, auth bypass, mass data exposure, payment manipulation | **Block.** Fix and retest. No risk acceptance. |
| High | Privilege escalation, stored XSS, injectable query, exposed secret | **Block**, or approve only with documented risk acceptance by the accountable owner, compensating control, and expiry. |
| Medium | Limited disclosure, missing hardening, weak rate limit | Document, assign owner/deadline; may release with a tracked plan. |
| Low | Best-practice deviation, negligible exploitability | Document and prioritize. |

A confirmed critical vulnerability must not ship. "Accepted risk" is valid only when a named accountable human approves it, the rationale and blast radius are recorded, compensating controls exist, and an expiry/review date is set.

## Evidence standard

- Link each check to a command, test, artifact, or review note.
- A scanner result alone is insufficient; state manual verification for logic and authorization.
- Do not claim "no vulnerabilities" — state scope, what was tested, and residual risk.

## Decision

```text
Gate: PASS | PASS WITH ACCEPTED RISK | FAIL
Version/commit:
Scope:
Blocking findings:
Accepted risks (owner, rationale, control, expiry):
Untested areas:
Approver/date:
```

Re-run the gate after any fix that changes the build, dependencies, auth, data handling, or infrastructure.
