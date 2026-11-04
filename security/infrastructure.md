# Infrastructure Security

> Load: containers, Kubernetes, cloud, network, deployment, secrets, monitoring, or incident response.
> Pairs with: `security/supply-chain.md`, `security/database.md`, `technologies/infrastructure/*`.

## Network and TLS

- TLS 1.2+ everywhere, modern cipher suites, valid certificates, automated renewal.
- HSTS with a deliberate max-age; redirect HTTP to HTTPS.
- Segment networks: public edge, application, data, management. Default-deny between segments.
- Restrict egress; allow only required destinations (prevents SSRF/exfiltration).
- Do not expose databases, caches, admin panels, or metrics endpoints to the public internet.
- Use a WAF/rate limiter at the edge for coarse protection; do not treat it as the primary auth control.

## Compute and containers

- Minimal base images, pinned by digest; rebuild regularly for patches.
- Run as non-root, read-only root filesystem where possible, drop Linux capabilities, set `no-new-privileges`.
- Do not bake secrets into images or layers; mount them at runtime.
- Limit CPU/memory/PIDs; set health checks and graceful shutdown.
- Scan images and IaC; block critical vulnerabilities by policy.
- Keep orchestrator and runtime versions supported; patch the host and control plane.

## Kubernetes

- Enable RBAC with least privilege; avoid cluster-admin for workloads and CI.
- Use namespaces and NetworkPolicies; deny by default.
- Enforce Pod Security Standards (restricted where possible); block privileged, hostPath, hostNetwork, and privilege escalation.
- Encrypt secrets at rest; prefer an external secret manager with short-lived credentials.
- Set resource requests/limits, PodDisruptionBudgets, and rollout strategies.
- Restrict access to the API server, kubelet, and dashboards; audit logs enabled.
- Use admission policies (OPA/Gatekeeper/Kyverno) to enforce invariants.

## Secrets and identity

- Central secret manager with audit, rotation, and least privilege.
- Workload identity/OIDC for cloud access instead of long-lived keys.
- Separate credentials per environment and service; never reuse production secrets.
- Rotate on exposure and on a schedule; revoke old versions.
- Do not put secrets in environment variables if the platform exposes them broadly (process listings, crash dumps); prefer mounted files/short-lived tokens where practical.

## Backups and resilience

- Encrypt backups, restrict access, keep immutable/offsite copies, and test restores.
- Define RPO/RTO; monitor backup failures.
- Protect against destructive automation: approvals, soft-delete/retention, and separate credentials for deletion.
- Plan for dependency failure: timeouts, retries with jitter, circuit breakers, and degraded modes.

## Observability and incident response

- Centralize logs, metrics, and traces with retention and access control.
- Alert on: auth failures, privilege changes, unusual egress, error/latency spikes, disk/DB saturation, certificate expiry, backup failure.
- Keep an incident runbook: contacts, severity, containment, evidence preservation, credential rotation, customer communication, postmortem.
- Do not log secrets or sensitive payloads; redact at the source.
- Practice a restore and an incident tabletop at least annually.

## CI/CD and IaC

- Least-privilege pipeline identities; short-lived OIDC credentials.
- Protect production environments with approvals and branch/environment rules.
- Review infrastructure plans (`terraform plan`) before apply; detect drift.
- Scan IaC for public buckets, open security groups, wildcard IAM, and unencrypted storage.
- Keep deploy and rollback automated and tested.

## Verification

- Attempt access to data/admin endpoints from an untrusted network position.
- Inspect running workloads for root, privileged mode, mounted secrets, and excessive capabilities.
- Confirm backups restore and secrets rotate.
- Review IAM policies for wildcards and unused permissions.
- Confirm alerts fire for a simulated auth-failure spike.
