# Workflow: Testing

> Trigger: define a test strategy, close coverage gaps, or stabilize a flaky suite.
> Modules: `core/testing.md`, the stack's technology module, `security/testing.md` when security tests are in scope.

## Steps

1. **Inventory current evidence.** Test frameworks, commands, CI jobs, pass/fail baseline, runtime, coverage, known flakes.
2. **Map risk to coverage.** List critical behaviors and rank by blast radius: money, auth, data loss, public API, core workflow, edge features.
3. **Find the gaps.** For each critical behavior: covered? at which level? with which negative cases?
4. **Choose the cheapest reliable level.** Unit for logic, integration for DB/HTTP/authz, contract for services, few E2E for journeys.
5. **Add tests in risk order.** Success, denial, invalid input, duplicate/concurrent request, dependency failure.
6. **Make them deterministic.** Inject time/randomness, isolate data, bind ephemeral ports, avoid order dependence.
7. **Wire into CI.** Fast suite on every push; slower integration/nightly suites scheduled; fail on new flakes.
8. **Set a budget.** Keep the feedback loop fast; parallelize safe suites; cache dependencies; avoid redundant E2E.
9. **Document commands and ownership.** Update README/CI docs; define who fixes a quarantined test.
10. **Report** what is now covered, what remains, and the exact evidence.

## Exit criteria

- Critical behaviors have at least one automated check; security-sensitive denial paths are covered.
- The suite passes from a clean checkout in CI.
- Flaky tests are fixed, quarantined with an owner/deadline, or removed.
- Test commands and environment requirements are documented.

## Do not

- Chase a coverage percentage with assertion-free tests.
- Mock the behavior under test (e.g., mock the ORM when testing a query).
- Use sleeps to synchronize; use events, polling with timeout, or fakes.
- Add E2E tests for logic that a unit test can prove.
