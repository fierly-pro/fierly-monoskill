# Workflow: Refactor

> Trigger: restructure code without changing observable behavior; reduce complexity or duplication.
> Modules: `core/engineering.md`, `core/testing.md`, `core/architecture.md` for boundary changes, `security/baseline.md`; add `security/auth.md`, `security/input.md`, or `security/database.md` when the refactor touches authentication/authorization, untrusted input, payments, or persistent data.

## Steps

1. **Define the behavior contract.** What must remain identical: outputs, errors, side effects, performance envelope, public APIs.
2. **Establish a safety net.** Run and, if needed, add characterization tests around the target. Record the baseline.
3. **Measure the problem.** Duplication, coupling, change frequency, or complexity — not aesthetics. State the target improvement.
4. **Choose the smallest structural change** that delivers it. Avoid a rewrite when an extraction or boundary move suffices.
5. **Refactor in small, compilable steps.** Each step preserves behavior and keeps tests green.
6. **Separate behavior changes.** If a bug is found, fix it in a separate commit with its own test.
7. **Preserve compatibility.** Public APIs, serialized formats, database schema, and configuration remain valid, or are versioned/migrated.
8. **Verify.** Full test suite, lint, typecheck, build; compare performance if the refactor touches hot paths.
9. **Review the diff for scope creep** — renames, formatting, and moved files should be explainable.
10. **Report** the structural change, evidence of behavior preservation, and measured effect.

## Exit criteria

- Observable behavior is unchanged (tests and manual checks demonstrate it).
- The stated structural goal is met; if not, report it rather than expanding scope.
- No unrelated files changed.
- Public contracts and data formats are preserved or deliberately migrated.
- The diff is reviewable in coherent steps.

## Guardrails

- Do not refactor and add features in the same change.
- Do not "clean up" code you do not need to touch.
- Do not replace a working abstraction with a fashionable one without measured benefit.
- Do not weaken tests to make a refactor pass.
