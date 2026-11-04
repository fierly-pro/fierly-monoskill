# PostgreSQL

> Load: PostgreSQL schema, queries, migrations, or operations.
> Pairs with: `technologies/languages/sql.md`, `security/database.md`, `platforms/backend.md`.

## Schema and queries

- Use `timestamptz` for instants, `numeric` for money, `text` with `CHECK` constraints where appropriate, `uuid`/`bigint` per project convention.
- Encode invariants with `NOT NULL`, `UNIQUE`, `FOREIGN KEY`, `CHECK`; add `DEFERRABLE` only when needed.
- `jsonb` for genuinely schemaless payloads; index with GIN only for real query patterns; do not use it to avoid schema design.
- Index foreign keys and frequent predicates. Composite order: equality columns first, then range/sort. Consider partial indexes for soft-delete/status filters.
- Verify with `EXPLAIN (ANALYZE, BUFFERS)` on realistic data; watch sequential scans on large tables and misestimates.
- Use keyset pagination for large sets; avoid deep `OFFSET`.
- `NULL` semantics: `NOT IN` with nullable subqueries is a trap; prefer `NOT EXISTS`.

## Transactions and concurrency

- Keep transactions short; never hold one across a network call.
- Choose isolation; handle serialization failures/deadlocks with bounded retries.
- `SELECT ... FOR UPDATE` only for rows that need locking; define a consistent lock order.
- Long-running transactions block vacuum; monitor `pg_stat_activity` and `pg_locks`.
- Use `lock_timeout` and `statement_timeout` for migrations and risky queries.

## Migrations

- Version every change (Flyway/Liquibase/Alembic/Rails/etc.); never edit applied migrations.
- Expand → backfill in batches → switch → contract for zero-downtime changes.
- Adding a column with a volatile default or changing a type can rewrite/lock the table; use the safe multi-step pattern.
- Create indexes concurrently (`CREATE INDEX CONCURRENTLY`) outside a transaction where supported.
- Test on a production-like snapshot; measure lock time and backfill duration.

## Operations

- Connection pooling: PgBouncer in transaction mode for many short connections; size pools from DB limits, not app instances blindly.
- Autovacuum tuning for high-churn tables; monitor bloat, dead tuples, and wraparound.
- Backups: base backup + WAL archiving/PITR; test restore; monitor failures.
- Replication: monitor lag; define failover and split-brain handling.
- Least-privilege roles: app DML only, separate migration/read-only roles; no superuser.
- Encryption in transit (TLS) and at rest; restrict `pg_hba.conf`; audit privileged access.
- Monitor slow queries (`pg_stat_statements`), locks, replication, disk, and connections.

## Security

- Parameterize queries; never concatenate input. Identifiers require allowlists.
- Row-level security for multi-tenant isolation where appropriate; test with multiple tenants.
- Do not log sensitive rows; restrict `pg_stat_activity` visibility if needed.
- Keep extensions minimal and patched; review `SECURITY DEFINER` functions.

## Checklist

- [ ] Constraints and indexes match query patterns.
- [ ] Plans checked on realistic data.
- [ ] Migration lock/backfill impact measured.
- [ ] Pooling and timeouts configured.
- [ ] Backups/PITR restore tested; roles least-privilege.
