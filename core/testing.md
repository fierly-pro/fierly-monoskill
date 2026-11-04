# Testing

> Load: test strategy, TDD, coverage gaps, flaky tests, or verification planning.
> Pairs with: `workflows/testing.md`, the stack's technology module, `security/testing.md` for security tests.

## Strategy: risk first

Match test depth to blast radius, not to a fixed ratio.

| Risk | Minimum evidence |
|---|---|
| Pure logic, parsers, calculations | Unit tests, edge cases, property/fuzz for untrusted input |
| Service behavior, DB queries, authz | Integration tests against a real dependency (container/emulator where practical) |
| Cross-service contracts | Contract tests or schema validation in CI |
| Critical user journeys | A small number of end-to-end tests, stable and fast |
| Money, auth, data deletion | Explicit negative tests, idempotency, concurrency, and audit checks |

Do not test framework internals, generated code, or trivial getters. Do test your decisions, boundaries, and failure paths.

## Test behavior, not implementation

- Assert observable outcomes: return values, state transitions, emitted events, HTTP responses, persisted rows.
- Avoid asserting private method calls or internal structure; refactors should not break tests.
- One logical behavior per test; a clear arrange–act–assert shape.
- Name tests by behavior: `rejects_expired_reset_token`, not `test_reset_2`.
- Cover the unhappy paths: invalid input, missing permission, duplicate request, timeout, partial failure.

## TDD and bug fixes

- For new behavior: write a failing test, implement the minimum, then refactor with the test green.
- For bugs: reproduce with a failing test first. If the environment makes that impossible, document the manual reproduction and add the closest automated guard.
- Keep the red → green → refactor cycle small; do not batch unrelated behavior.

## Determinism

Tests must not depend on wall-clock time, randomness, network access, filesystem order, shared mutable state, or execution order.

- Inject clocks, ID generators, and randomness; freeze time in tests.
- Use ephemeral databases/schemas and clean up per test.
- Bind test servers to port 0; never rely on a developer's local service.
- Isolate environment variables; restore them after the test.
- Run tests in parallel only when isolation is proven.
- Treat a flaky test as a defect: fix, quarantine with an owner and deadline, or delete. Never normalize retries.

## Test data

- Build data with factories/builders near the test; avoid giant shared fixtures.
- Use realistic values for formats and constraints, synthetic values for PII.
- Test boundary values: empty, one, max, max+1, Unicode, null/absent, duplicate.
- For security-sensitive parsers, add malformed and adversarial inputs (see `security/input.md`).

## Coverage

Coverage is a signal for untested paths, not a target to game. Prefer branch coverage on changed code and risk-based gaps over a global percentage. A high-coverage suite with no negative cases can still miss the failures that matter.

## Verification contract

Before claiming completion:

1. Run the project's own test, lint, typecheck, and build commands.
2. Run the narrowest relevant suite during development, then the full suite before handoff.
3. Report exact commands and outcomes; include failing/skipped tests and why.
4. For UI or integration changes, exercise the changed path manually when automation is missing.
5. If a check cannot run, say so and provide the command for the user; do not mark it passed.
