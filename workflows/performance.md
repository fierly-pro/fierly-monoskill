# Workflow: Performance

> Trigger: latency, throughput, memory, CPU, startup, or cost problem; or a change to a hot path.
> Modules: `core/engineering.md`, platform/technology modules, `core/testing.md`, `security/baseline.md`; add `security/database.md` for migrations or persistent-data changes.

## Steps

1. **Define the metric and target.** p50/p95/p99 latency, throughput, memory, CPU, query count, bundle size, cost per request. State the user-visible symptom.
2. **Reproduce with a realistic workload.** Capture dataset size, concurrency, hardware, versions, and configuration.
3. **Measure the baseline.** Use production-like profiling and tracing, not micro-benchmarks alone. Save the numbers.
4. **Locate the bottleneck with evidence.** Flame graph, query plan, allocation profile, network waterfall, lock contention.
5. **State a hypothesis** and the expected effect. Change one variable at a time.
6. **Optimize the dominant cost** — algorithm, query/index, allocation, N+1, payload, caching, batching, concurrency.
7. **Re-measure** with the same workload. Report the delta and variance. Revert changes that do not help.
8. **Protect correctness.** Run the full test suite; add a benchmark or performance regression guard where practical.
9. **Add observability** for the metric so regressions are visible (histogram, query timing, budget alert).
10. **Document** the change, tradeoffs (memory vs CPU, freshness vs cache), and rollback.

## Common causes

| Symptom | Check first |
|---|---|
| Slow endpoint | N+1 queries, missing index, serialization, synchronous I/O, payload size |
| High memory | Unbounded cache/queue, retained buffers, large object graphs, leaks |
| CPU saturation | Hot loops, regex backtracking, JSON/XML parsing, compression, GC pressure |
| Slow startup | Eager initialization, classpath scanning, large bundles, network calls at boot |
| Tail latency | GC pauses, lock contention, retries, connection pool exhaustion, noisy neighbors |

## Schema and data migrations

For a large or live table, use expand → backfill → contract, not a single blocking change.

1. **Expand.** Add nullable columns, new tables, or indexes without rewriting the table. In PostgreSQL use `CREATE INDEX CONCURRENTLY` outside a transaction; verify it did not leave an invalid index.
2. **Backfill.** Batch by primary key or time range, commit between batches, throttle, and make the job resumable/idempotent. Bound lock time and replication lag.
3. **Switch reads/writes.** Deploy dual-read or dual-write compatibility, then move traffic. Keep the old path until the new path is verified.
4. **Contract.** Only after backfill and verification, add `NOT NULL`/constraints (validate separately where supported) and drop the old column or index in a later release.
5. **Prove it.** Measure lock waits, latency, replication lag, and error rate on production-like data. State the rollback or forward-fix path; a backup alone is not a rollback plan. For a new non-null column with a default, check version-specific behavior before relying on it.

## Exit criteria

- The metric is measured before and after with the same workload.
- The improvement is material and correctness/security are preserved.
- A regression guard or observability metric is in place.
- The tradeoff and rollback are documented.

## Guardrails

- Do not optimize without a measured baseline.
- Do not trade correctness or security for speed without explicit approval.
- Do not add a cache before defining invalidation, consistency, and failure behavior.
- Do not benchmark with empty data or a single request.
