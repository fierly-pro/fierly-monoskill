# Workflow: Architecture Decision

> Trigger: system design, technology selection, boundary change, scaling, or migration.
> Modules: `core/architecture.md`, `core/project-analysis.md`, `security/baseline.md`, relevant platform/technology modules.

## Steps

1. **Frame the decision.** What problem, for whom, under which constraints? What happens if nothing changes?
2. **List quality attributes in priority order.** Make tradeoffs explicit (e.g., consistency vs availability, speed vs operability).
3. **Map the current state.** Components, data ownership, interfaces, deployment, failure modes, team ownership.
4. **Generate 2–3 options**, including the simplest/status quo. For each: complexity, cost, risk, operability, migration effort, reversibility.
5. **Test the riskiest assumption** with a spike, benchmark, or vendor/API check. Time-box it and discard the spike code.
6. **Select and justify.** Prefer the option with the fewest irreversible commitments and the best fit for the team.
7. **Design the migration:** compatibility window, dual-write/read, backfill, feature flags, rollback, rollback trigger.
8. **Threat-model the target** and identify authorization, secret, and network boundaries.
9. **Record an ADR** using `templates/adr.md`. Include rejected options and revisit conditions.
10. **Define success metrics and observability** before implementation.
11. **Implement incrementally**; verify each stage; keep the old path until the new one is proven.

## Exit criteria

- The decision, alternatives, and consequences are recorded.
- Constraints and quality attributes are explicit.
- Security and data-migration risks are addressed.
- Rollback and compatibility are defined.
- The first implementation increment is small and verifiable.

## Avoid

- Choosing tools before stating constraints.
- A design that only works at 10× the current scale.
- Irreversible migrations without a tested rollback.
- Distributed systems complexity without an operational need.
