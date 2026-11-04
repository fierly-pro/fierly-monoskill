# Kubernetes

> Load: Kubernetes manifests, Helm charts, operators, or cluster operations.
> Pairs with: `technologies/infrastructure/docker.md`, `security/infrastructure.md`, `security/supply-chain.md`.

## Workloads

- Deployment for stateless services; StatefulSet for stable identity/storage; Job/CronJob for batch.
- Set CPU/memory requests and limits from measurements; requests affect scheduling, limits affect throttling/OOM.
- Liveness = process stuck; readiness = can serve traffic; startup probe for slow boot. Do not point liveness at dependencies.
- Use `strategy`/`maxSurge`/`maxUnavailable` and `PodDisruptionBudget` for safe rollouts and drains.
- Set `terminationGracePeriodSeconds` and handle `SIGTERM`; preStop hooks only when needed.
- Use HPA on meaningful metrics; cluster autoscaling needs correct requests.
- Keep images immutable (digest); avoid `latest`.

## Security

- `securityContext`: `runAsNonRoot`, `runAsUser`, `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem`, drop ALL capabilities.
- Enforce Pod Security Standards (restricted) and admission policies; block privileged, hostPath, hostNetwork, hostPID.
- NetworkPolicy: default deny ingress/egress, then allow required flows; remember DNS egress.
- RBAC: namespace-scoped roles, no cluster-admin for workloads/CI; audit bindings.
- Secrets: enable encryption at rest; prefer external secret stores/workload identity; do not commit SealedSecrets keys.
- Restrict API server access, dashboards, and kubelet; enable audit logs.
- Scan images/IaC and verify signatures at admission where supported.

## Configuration and traffic

- ConfigMaps for non-sensitive config; Secrets for sensitive (with the caveats above). Mount as files when possible.
- Ingress/Gateway with TLS; cert-manager or managed certificates; set timeouts, body limits, and rate limits at the edge.
- Service mesh only with a measured need; it adds operational and security complexity.
- Use namespaces/quotas/limit ranges to isolate teams and prevent noisy-neighbor issues.

## Operations

- Rollout status and automatic rollback on failed health; keep previous ReplicaSets for rollback.
- Monitor: pod restarts, OOMKills, pending pods, API latency, etcd health, node pressure, certificate expiry.
- Logs to a central store; metrics via Prometheus/OTel; traces with context propagation.
- Backups for PVs and cluster state (GitOps/IaC); test restore and disaster recovery.
- Cost: right-size requests, use HPA/cluster autoscaler, clean up orphaned volumes/load balancers.

## Local and CI

- Use kind/minikube/k3d for integration tests; keep manifests renderable (`helm template`/`kustomize build`).
- Validate with `kubeconform`/`kubeval`, policy tests, and server-side dry run in a disposable namespace.
- Diff against the live cluster (`kubectl diff`) and apply via GitOps with review.

## Checklist

- [ ] Requests/limits and probes configured.
- [ ] Restricted security context and NetworkPolicies.
- [ ] RBAC least privilege; secrets external/encrypted.
- [ ] Rollout/rollback and PDB tested.
- [ ] Manifests validated; images digest-pinned and signed.
- [ ] Monitoring, backups, and cost controls in place.
