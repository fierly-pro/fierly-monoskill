# CI/CD

> Load: pipelines, build automation, release workflows, or branch protection.
> Pairs with: `security/supply-chain.md`, `workflows/release.md`, `technologies/infrastructure/docker.md`.

## Pipeline stages

1. **Validate** — format/lint, typecheck, static analysis.
2. **Test** — unit, integration, contract; fast suites first; fail fast.
3. **Build** — immutable artifact/container from the reviewed commit; generate SBOM.
4. **Scan** — dependencies, secrets, image, IaC; fail on policy thresholds.
5. **Publish** — sign artifacts; push to an access-controlled registry.
6. **Deploy** — staged/canary to an environment with approvals and secrets scoped to it.
7. **Verify** — smoke tests, health, key metrics; automatic rollback on failure thresholds.

## Security

- Default token permissions to read-only; elevate per job only when required.
- Pin third-party actions by full commit SHA; pin container images by digest.
- Never run untrusted PR code with secrets or a privileged token. Avoid `pull_request_target` unless the workflow is designed for it.
- Store secrets in the CI secret store/environment, not in workflow files; mask logs.
- Use OIDC/workload identity for cloud access instead of long-lived keys.
- Protect branches/environments: required reviews, status checks, signed commits where policy requires, restricted who can change workflows.
- Separate build and deploy credentials; production approvals by an accountable owner.

## Reliability and speed

- Cache dependencies and build layers keyed by lockfile; do not cache secrets or mutable artifacts.
- Run independent jobs in parallel; use a matrix for supported versions/platforms.
- Keep the critical path short; move slow E2E/security scans to scheduled or pre-release pipelines with clear gates.
- Make pipelines deterministic: pin tool versions, use clean workspaces, avoid network flakiness.
- Publish test reports and artifacts for debugging; retain logs per policy.

## Deployment

- Build once, promote the same artifact through environments.
- Use blue/green, canary, or rolling deploys with health checks and automatic rollback.
- Run migrations as a separate, backward-compatible step; never require atomic app+DB upgrades.
- Feature-flag risky changes; keep a rollback path for code, config, and data.
- Record the deployed commit, artifact digest, and migration version.

## Anti-patterns

- `latest` images/tags in production.
- Long-lived cloud keys in CI.
- Secrets echoed in logs or passed as build args.
- A pipeline that deploys on every push to main without gates.
- Ignoring flaky tests or retrying until green.
- Mutable artifacts rebuilt per environment.

## Checklist

- [ ] Permissions least-privilege; actions/images pinned.
- [ ] Tests, scans, and build are required checks.
- [ ] Artifacts signed, digest recorded, SBOM stored.
- [ ] Production requires approval and scoped secrets.
- [ ] Rollback and migration compatibility tested.
