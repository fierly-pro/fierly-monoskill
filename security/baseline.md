# Security Baseline

> Load: every implementation, review, architecture, and release task. This is the minimum lens; add attack-surface modules from `SKILL.md`.

## Principles

- **Security by design** — controls are part of the architecture, not a post-launch patch.
- **Secure by default** — deny by default, opt in explicitly, fail closed.
- **Defense in depth** — validate at the edge, authorize at the resource, constrain at the data layer.
- **Least privilege** — users, services, database roles, CI tokens, and containers get the minimum required.
- **Zero trust where it matters** — authenticate and authorize every request; network location is not identity.
- **Minimize attack surface** — fewer endpoints, ports, dependencies, permissions, and data retained.
- **Assume breach** — limit blast radius, log evidence, make recovery possible.

## Lightweight threat model (required for non-trivial changes)

1. **Assets** — credentials, tokens, personal data, money, admin capability, availability, code integrity.
2. **Actors** — anonymous internet, authenticated user, tenant admin, insider, compromised dependency, automated bot.
3. **Trust boundaries** — browser↔server, service↔service, app↔database, CI↔cloud, mobile app↔backend, human↔admin.
4. **Data flows** — where data enters, is transformed, stored, logged, exported.
5. **Questions per boundary** — spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege.
6. **Controls** — preventive, detective, corrective. Name the one that actually blocks the top risk.

Record the result with `templates/threat-model.md` for high-risk work; a short paragraph is enough otherwise.

## Data handling

| Class | Examples | Minimum handling |
|---|---|---|
| Public | marketing content | integrity only |
| Internal | logs, metrics, non-public docs | access control, no public buckets |
| Confidential | business data, source, contracts | encryption, least privilege, audit |
| Restricted | credentials, tokens, keys, payment data, health/PII | strong encryption, strict access, no logs, retention limits |

- Collect only data the feature needs. Define retention and deletion.
- Never use production personal data in development or tests.
- Redact secrets and personal data from logs, traces, crash reports, and error messages.
- Encrypt restricted data in transit and at rest; manage keys separately from data.

## Secrets

- Store in a secret manager or platform secret store, not in Git, images, logs, or client bundles.
- Use short-lived credentials and workload identity where available.
- Rotate after exposure; assume any committed secret is compromised even if the commit was deleted.
- Scan repositories and CI logs; block commits containing secrets.

## Errors, logging, and monitoring

- Return generic errors to users with a correlation ID; keep details in server logs.
- Log security events: authentication success/failure, authorization denial, privilege change, admin action, data export/delete, configuration change.
- Do not log passwords, tokens, session IDs, full payment data, or unnecessary PII.
- Alert on anomalies: credential stuffing, spikes in 401/403/429, unusual egress, repeated admin failures.
- Make logs tamper-resistant and retention-compliant.

## Verification level

Use OWASP ASVS 5.0 as the reference. Select a level by risk: L1 for low-risk internal tools, L2 for standard applications handling accounts or business data, L3 for high-value, regulated, or safety-critical systems. State the chosen level and the gaps; do not claim ASVS compliance without a full verification.

## Red flags

- Authorization enforced only in the UI.
- Secrets in `.env` committed to the repository.
- TLS verification disabled "temporarily".
- Untrusted data passed to a shell, SQL string, template compiler, or deserializer.
- Wildcard CORS with credentials, or CORS treated as authentication.
- Missing rate limits on login, reset, OTP, or expensive endpoints.
- Dependencies added without provenance or lockfile updates.
- A release approved because "the scanner found nothing".

## Severity and gate

Use the severity scale in `security/gate.md`. Confirmed critical issues block release. High issues block or require documented risk acceptance by the accountable owner. Medium/low are tracked with owners and deadlines.
