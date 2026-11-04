# Workflow: Feature

> Trigger: add or change behavior in an existing system.
> Modules: `core/engineering.md`, `core/testing.md`, platform + technology modules, `security/baseline.md` + matched modules.

## Steps

1. **Define acceptance criteria.** Inputs, outputs, permissions, error cases, non-goals. Resolve ambiguity that changes behavior.
2. **Locate the seam.** Find the closest existing pattern and the smallest set of files to change. Identify affected APIs, events, schema, and UI states.
3. **Check contracts.** Who consumes the changed interface? Is a version, migration, feature flag, or compatibility window required?
4. **Design the data and failure path.** Validation, authorization, transactions, idempotency, timeouts, partial failure.
5. **Write the test first** for the main behavior and the most important negative case.
6. **Implement one coherent slice.** Keep the build green; avoid opportunistic refactors.
7. **Handle the edges.** Empty/oversized input, duplicate requests, concurrency, permissions, localization, accessibility where relevant.
8. **Update artifacts.** Docs, OpenAPI/schema, migrations, configuration examples, changelog.
9. **Verify.** Run focused tests, then the full suite, lint, typecheck, and build. Exercise the UI/API path manually when automation is missing.
10. **Report** the behavior change, verification evidence, and any follow-up.

## Exit criteria

- Acceptance criteria are demonstrably met.
- Tests cover success, denial, and at least one failure path.
- Authorization is enforced server-side at the resource, not only in the UI.
- Backward compatibility is preserved or migrated deliberately.
- Docs and contracts match the implementation.

## Guardrails

- No drive-by renames or dependency upgrades.
- No new abstraction for a single caller.
- No client-side-only validation for security decisions.
- No silent behavior change hidden inside a refactor.
