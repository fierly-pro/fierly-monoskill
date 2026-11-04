# Workflow: Release

> Trigger: prepare, deploy, or publish a version.
> Modules: `core/engineering.md`, `security/gate.md`, `security/supply-chain.md`, platform module, release-related technology modules.

## Steps

1. **Freeze scope.** Confirm included changes, excluded changes, known issues, and the version number (semantic versioning where applicable).
2. **Run the full verification.** Tests, lint, typecheck, build, migrations check, and the security gate from `security/gate.md`.
3. **Review the diff since the last release.** Look for debug code, feature flags left on, secrets, and unintended dependency changes.
4. **Update release artifacts.** Changelog, version files, API docs, migration notes, configuration examples, support matrix.
5. **Build reproducibly.** Clean environment, pinned toolchain, locked dependencies. Produce checksums and an SBOM.
6. **Sign and verify artifacts.** Code signing, package signatures, container image digests, provenance attestations where supported.
7. **Prepare data changes.** Test migrations on a production-like copy; verify rollback or forward-fix; estimate lock time and backfill impact.
8. **Configure production.** Secrets from the secret manager, safe defaults, feature flags, resource limits, health checks, alerts.
9. **Deploy progressively.** Canary or staged rollout; watch error rate, latency, saturation, and business metrics. Define abort thresholds.
10. **Verify after deploy.** Smoke test critical journeys; check logs, metrics, and traces; confirm the version and migrations.
11. **Keep rollback ready.** Document the exact command and data implications. Do not roll back a destructive migration blindly.
12. **Announce and monitor.** Publish notes, monitor for a defined window, and record incidents or follow-ups.

## Exit criteria

- Security gate passed or risks explicitly accepted with an owner and expiry.
- All checks pass on the exact artifact being released.
- Artifacts are signed/checksummed and traceable to a commit.
- Migration and rollback were tested or the risk is documented.
- Post-deploy verification passed.
- Changelog and version are published.

## Mobile and desktop additions

- Verify signing identities, provisioning profiles, entitlements, and store metadata.
- Test on the minimum supported OS version and a current device/emulator.
- Stage the rollout; keep a phased-release halt plan.
- For desktop, verify auto-update signing, notarization, and installer/uninstaller behavior.

## Never

- Release from an uncommitted working tree or an untested local build.
- Skip the gate because the change "looks small".
- Store release credentials in CI logs or repository variables without protection.
