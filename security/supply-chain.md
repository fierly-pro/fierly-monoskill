# Supply Chain Security

> Load: dependencies, CI/CD, build artifacts, package publishing, or release signing.
> Pairs with: `security/infrastructure.md`, `workflows/dependencies.md`, `workflows/release.md`.

## Inventory and provenance

- Maintain a lockfile for every ecosystem; review lockfile diffs, not just manifests.
- Generate an SBOM (CycloneDX or SPDX) per release; store it with the artifact.
- Know the source of each dependency: registry, repository, maintainer, license, release cadence.
- Prefer signed/tagged releases and official registries. Verify checksums/signatures where available.
- Avoid unmaintained or end-of-life packages; track a replacement plan.

## Dependency risk

- Run SCA (OSV-Scanner, Trivy, Dependabot/Renovate) in CI; triage by reachability and exploitability, not CVSS alone.
- Watch for dependency confusion: scope private packages, pin registries, and avoid falling back to public registries for internal names.
- Watch for typosquatting and unexpected post-install scripts; review new dependencies before adding.
- Do not auto-merge major upgrades or security updates without tests.
- Record accepted vulnerabilities with owner, rationale, compensating control, and expiry.

## CI/CD

- Grant the minimum token permissions. For GitHub Actions, set `permissions: contents: read` by default and elevate per job.
- Pin third-party actions by full commit SHA, not a mutable tag. Pin container images by digest.
- Never run untrusted pull-request code with secrets or a privileged token (`pull_request_target` is a common trap).
- Require review and status checks on protected branches; restrict who can change workflows.
- Use OIDC/workload identity for cloud access instead of long-lived credentials.
- Protect production environments with manual approval and environment-scoped secrets.
- Keep build logs free of secrets; mask and restrict access.

## Artifacts

- Build once, promote the same artifact through environments.
- Produce checksums and sign artifacts (Sigstore/cosign, platform signing). Verify signatures before deploy.
- Generate provenance/attestations where supported; do not claim SLSA compliance without verification.
- Store artifacts in an access-controlled registry with retention and immutability where possible.
- Verify container image digests at deploy time; reject mutable tags.

## Secrets in the supply chain

- Scan repositories and history (Gitleaks), plus CI logs and artifacts.
- Use pre-commit hooks and server-side push protection.
- Revoke and rotate any exposed credential immediately; deleting the commit is not enough.
- Keep signing keys in an HSM/KMS or hardware token; restrict access and audit use.

## Verification

- Reproduce a build from a clean checkout with pinned tooling; compare artifact hashes where the ecosystem allows.
- Confirm CI permissions, action pinning, and environment protections.
- Check the SBOM against the deployed artifact.
- Test that a tampered artifact or unsigned image is rejected by deployment policy.
