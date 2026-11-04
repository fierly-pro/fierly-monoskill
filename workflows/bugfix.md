# Workflow: Bug Fix

> Trigger: crash, incorrect result, regression, failing test, or reported defect.
> Modules: `core/engineering.md`, `core/testing.md`, the affected platform/technology modules, `security/baseline.md`.

## Steps

1. **Reproduce reliably.** Capture exact input, environment, version, and observed vs expected output. Do not fix from a description alone.
2. **Preserve evidence.** Save the stack trace, failing test, logs (redact secrets/PII), or a minimal reproduction.
3. **Find the root cause.** Trace the data and control flow to the first incorrect assumption. Distinguish symptom from cause.
4. **Check blast radius.** Search for the same pattern elsewhere; identify other callers and data already corrupted.
5. **Write a failing regression test** at the lowest level that reproduces the defect.
6. **Apply the smallest fix** at the correct layer. Do not patch the UI to hide a backend error or catch-and-ignore.
7. **Verify the fix and the neighborhood.** Run the regression test, related tests, and the full suite. Test the original reproduction.
8. **Assess security impact.** Could the defect expose data, bypass authorization, corrupt state, or cause a denial of service? If yes, load the security module and check for exploitation evidence.
9. **Handle existing damage.** Provide a data repair or migration plan when the bug wrote bad state; make it idempotent and reversible.
10. **Report** root cause, fix, tests, affected versions, and any residual risk.

## Exit criteria

- The original reproduction now passes.
- A regression test fails without the fix and passes with it.
- No unrelated behavior changed.
- Security and data-integrity impact is assessed.
- The fix is documented for release notes when user-visible.

## Anti-patterns

- Fixing the symptom (null check everywhere) without the invariant that failed.
- Adding a retry to hide nondeterminism.
- Disabling or skipping the failing test.
- Mixing the fix with refactoring or dependency updates.
