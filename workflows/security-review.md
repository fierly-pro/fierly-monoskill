# Workflow: Security Review

> Trigger: security review, threat model, vulnerability report, or a change touching auth, data, payments, crypto, or infrastructure.
> Modules: `security/baseline.md`, matched security modules, `security/testing.md`, platform/technology modules.

## Steps

1. **Scope the system.** Components, data flows, assets, actors, entry points, deployment model, trust boundaries.
2. **Threat-model.** For each boundary: spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege. Rank by likelihood × impact.
3. **Review design controls.** Authentication, object-level authorization, least privilege, secrets, encryption, isolation, rate limits, audit.
4. **Review code by attack surface.** Input handling, queries, shell/process calls, file paths/uploads, deserialization, SSRF, templates, authz checks, error/log leakage.
5. **Review dependencies and supply chain.** Lockfiles, known CVEs, abandoned packages, install scripts, CI permissions, artifact signing.
6. **Run available scanners** (Semgrep, CodeQL, Gitleaks, Trivy, OSV-Scanner, ZAP) and triage results. Record tool versions and rulesets.
7. **Perform manual abuse cases.** IDOR with two accounts, privilege escalation, replay, CSRF, session fixation, upload bypass, injection payloads, rate-limit bypass.
8. **Classify findings** by severity with evidence, affected path, exploit preconditions, and remediation.
9. **Verify fixes** with a regression test or a repeatable manual check.
10. **Decide the gate** using `security/gate.md`; document accepted risk with an owner and expiry.

## Severity

- **Critical** — remote code execution, auth bypass, mass data exposure, payment manipulation. Blocks release.
- **High** — privilege escalation, stored XSS, SQL injection with limited impact, secret exposure. Blocks release or requires documented acceptance by the accountable owner.
- **Medium** — limited information disclosure, missing hardening, weak rate limiting. Fix or track with a deadline.
- **Low** — best-practice deviation with negligible exploitability. Track.

## Evidence standard

- A scanner finding is a lead, not a confirmed vulnerability. Validate exploitability and reachability.
- A clean scanner run does **not** mean the system is secure. Manual abuse cases and design review are required.
- Never include real secrets, personal data, or production payloads in reports. Use redacted reproductions.

## Exit criteria

- Assets, boundaries, and attack surface are documented.
- Confirmed critical/high findings are fixed or explicitly accepted with an owner and expiry.
- Security-relevant changes have tests or repeatable verification.
- Residual risk and unverified areas are stated.
