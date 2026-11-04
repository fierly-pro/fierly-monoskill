# Workflow: New Project

> Trigger: greenfield project, prototype that will be maintained, or a new service/app.
> Modules: `core/engineering.md`, `core/architecture.md`, `core/testing.md`, platform module, selected technology modules, `security/baseline.md` + matched security modules.

## Steps

1. **Define the outcome.** Users, core jobs, acceptance criteria, non-goals, constraints (budget, deadline, compliance, team skills, deployment target).
2. **Choose the stack from constraints.** Prefer the team's operable, supported stack. Record a short ADR if the choice is non-obvious.
3. **Design the smallest coherent architecture.** Boundaries, data ownership, interfaces, auth model, failure behavior. Avoid services you cannot operate.
4. **Threat-model before code.** Assets, actors, trust boundaries, entry points; select security modules.
5. **Bootstrap the repository.** Version control, `.gitignore`, formatter, linter, typecheck, test runner, CI, environment template, README, run instructions.
6. **Build a vertical slice first.** One end-to-end path through UI/API/data/auth, with tests — not all layers half-built.
7. **Add quality gates early.** Tests, lint, typecheck, build, secret scan, dependency scan in CI. Make the default branch protected.
8. **Iterate in small increments.** Each increment: acceptance test → implementation → verification → docs/migration.
9. **Prepare operations.** Config, migrations, health check, logs/metrics, backup, deploy and rollback procedure.
10. **Run the release workflow** when the first deployable version exists.

## Exit criteria

- The app/service starts from a clean checkout using documented commands.
- The critical path works end-to-end and is covered by at least one automated test.
- Lint, typecheck, build, and tests pass in CI.
- No secrets in the repository; `.env.example` documents required configuration.
- Auth, input handling, and data access follow the matched security modules.
- README states purpose, setup, run, test, and deploy commands.

## Avoid

- Scaffolding every layer before proving one user journey.
- Adding microservices, queues, or caches without a measured need.
- Deferring auth, validation, and migrations "until later".
- Choosing a stack because it is new rather than because it fits the constraints.
