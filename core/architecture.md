# Architecture

> Load: system design, boundaries, technology selection, structural change, or migration.
> Pairs with: `workflows/architecture.md`, `core/project-analysis.md`, `security/baseline.md`.

## Method

1. **State the problem and constraints** — users, scale, latency, consistency, budget, team, compliance, existing stack, deadlines.
2. **Rank quality attributes** — explicitly order the ones that trade off: simplicity, time-to-market, throughput, latency, availability, consistency, operability, cost, portability.
3. **Describe the current system** — even "greenfield" inherits organizational and platform constraints.
4. **Generate 2–3 viable options**, including the status quo or the simplest option.
5. **Compare on evidence** — prototype or measure the risky assumption; do not benchmark on intuition.
6. **Decide and record** — one ADR with context, options, decision, consequences, revisit trigger.
7. **Plan the migration** — reversible increments, compatibility window, rollback, data backfill, observability.

For small changes, this collapses to a short paragraph. Do not produce architecture theater for a one-file change.

## Defaults that age well

- **Modular monolith first.** Split services only for independent scaling, isolation, ownership, or deployment needs — not for résumé value.
- **Boring, supported technology.** Prefer the stack the team can operate. Novelty is a cost, not a feature.
- **One source of truth per datum.** Define ownership, write path, and read replicas explicitly.
- **Synchronous by default; async for decoupling.** Queues add ordering, duplication, and observability problems. Use them for real latency/throughput isolation.
- **Managed services for undifferentiated infrastructure**, unless regulation, cost, or control requires otherwise.
- **Stateless compute where possible.** Externalize sessions, uploads, and cache; make instances disposable.
- **Contracts at boundaries.** Version APIs and events; validate at ingress; never share internal models across trust boundaries.
- **Design for failure.** Timeouts, bounded retries with jitter, circuit breaking where it helps, idempotency keys, graceful degradation.
- **Observability is part of the design.** Define the signals (latency, errors, saturation, business events) before launch.

## Boundaries and dependencies

- Group by business capability, not by technical layer alone.
- Dependencies point inward toward domain rules; infrastructure implements ports.
- A module owns its data; cross-module access goes through a contract, not a shared table.
- Avoid cyclic dependencies. If two modules need each other, the boundary is wrong or a third module is missing.
- Keep framework code at the edges. Domain logic should be testable without a server or database.

## Data and consistency

- Choose consistency per operation: strong within a transaction, eventual across boundaries.
- Define transaction scope; never hold a transaction open across a network call.
- Use unique constraints and idempotency keys to make duplicate delivery safe.
- Migrations are code: versioned, reviewed, reversible or forward-fixable, and tested on production-like data.
- Large migrations use expand → backfill → switch → contract, with dual reads/writes where necessary.
- Define retention, deletion, and backup/restore requirements before storing data.

## Interfaces

- Validate input at the boundary; return stable error shapes.
- Version public APIs; add fields compatibly; never silently change semantics.
- Events are contracts: schema, producer, consumers, ordering, delivery guarantee, replay.
- Document rate limits, pagination, idempotency, and timeouts.
- Prefer explicit DTOs over exposing ORM entities or internal objects.

## Security architecture

- Draw trust boundaries and data flows; identify assets, actors, and entry points.
- Authenticate at the edge, authorize at the resource (object-level), and re-check in depth where risk warrants.
- Least privilege for users, services, database roles, and CI tokens.
- Segment networks; encrypt in transit; encrypt sensitive data at rest.
- Centralize secrets; rotate them; never bake them into images or code.
- Log security-relevant events with correlation IDs, without secrets or unnecessary PII.

## Review checklist

- [ ] Requirements and quality attributes are stated and prioritized.
- [ ] The simplest viable option was considered and rejected with reasons.
- [ ] Boundaries, ownership, and dependency direction are explicit.
- [ ] Failure modes, timeouts, retries, and idempotency are addressed.
- [ ] Data model, migrations, backup, and rollback are planned.
- [ ] Security trust boundaries and authorization points are defined.
- [ ] Observability and operational runbook are defined.
- [ ] Cost and team operability are realistic.
- [ ] An ADR captures the decision and revisit trigger.

## Anti-patterns

- Microservices without independent scaling, ownership, or deployment needs.
- Shared database across services with hidden coupling.
- Distributed transactions without a saga/compensation design.
- "Eventual consistency" used to avoid defining correctness.
- Architecture diagrams that omit the network, identity, and failure paths.
- Choosing technology before stating the constraint it solves.
