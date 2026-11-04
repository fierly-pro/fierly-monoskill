# Workflow: Dependencies

> Trigger: add, upgrade, remove, or audit a dependency.
> Modules: `core/engineering.md`, `security/supply-chain.md`, `security/testing.md`, the stack's technology module.

## Add

1. **Justify the need.** What substantial code or risk does it replace? Could the platform or an existing dependency do it?
2. **Check provenance.** Official source, maintainer reputation, release cadence, open issues, download base, license compatibility.
3. **Check weight and risk.** Transitive dependencies, install scripts, native binaries, known CVEs, data access, telemetry.
4. **Pin it.** Add to the manifest and lockfile; use the ecosystem's exact/range policy consistently.
5. **Test** the integration path and failure behavior; document configuration and upgrade constraints.

## Update

1. **Inventory** direct and transitive dependencies, current versions, and end-of-life status.
2. **Read the changelog and migration notes** for every major/minor upgrade; identify breaking changes.
3. **Group safely:** security patches separately from routine updates; one major upgrade per change.
4. **Update the lockfile**, run the full test suite, typecheck, lint, and build.
5. **Check runtime behavior** for native, database, auth, serialization, and HTTP dependencies.
6. **Record** the reason, version delta, and rollback (revert the lockfile and manifest together).

## Remove

- Search for imports, dynamic loading, configuration, and infrastructure references.
- Remove the package, lockfile entries, unused configuration, and documentation.
- Verify the build and tests without it.

## Audit

- Run the ecosystem auditor plus `osv-scanner`/`trivy` where available.
- Triage by reachability and exploitability, not CVSS alone. Record accepted risk with owner and expiry.
- Check licenses against the project's distribution model.
- Prefer automated, reviewed update PRs (Dependabot/Renovate) with CI gates.

## Exit criteria

- The dependency is necessary, maintained, licensed compatibly, and pinned.
- Lockfile and manifest are consistent.
- Tests/build pass; breaking changes are handled.
- Security findings are fixed or explicitly accepted.
- No unrelated upgrades are mixed into the change.
