# SQL

> Load: schema design, queries, indexes, migrations, or performance.
> Pairs with: the database module (`postgresql`, `sqlite`, etc.), `security/database.md`, `security/input.md`.

## Queries

- Parameterize all values. Identifiers (table/column/sort direction) cannot be bound — map them through an allowlist.
- `NULL` is not `false` or `0`: use `IS NULL`, `COALESCE`, and be explicit about three-valued logic in `WHERE`/`NOT IN`.
- `NOT IN` with a nullable subquery returns no rows; prefer `NOT EXISTS` or filter nulls.
- Avoid `SELECT *` in application queries; select only needed columns, especially with large blobs/JSON.
- Paginate with keyset pagination (`WHERE (created_at, id) < (...)`), not large `OFFSET`.
- Avoid N+1 query loops; batch with `IN`/joins or a data loader, and verify query counts.
- Use `EXPLAIN (ANALYZE, BUFFERS)` on realistic data; an index that is not used is not an optimization.

## Schema and indexes

- Primary keys, foreign keys, `NOT NULL`, `UNIQUE`, and `CHECK` encode invariants in the database, not only in code.
- Index foreign keys and frequent filter/sort columns; prefer composite indexes ordered by equality then range/sort.
- Partial and covering indexes solve specific queries; verify with the planner and write cost.
- Avoid redundant indexes; each index slows writes and consumes storage.
- Use the correct type: `timestamptz` for instants, `numeric` for money, `uuid`/bigint per project convention, `jsonb` only for genuinely schemaless data.
- Normalize by default; denormalize with a measured read need and a consistency plan.

## Transactions and concurrency

- Keep transactions short; never hold one open across a network call or user interaction.
- Choose isolation deliberately; handle deadlocks/serialization failures with bounded retries.
- Lock only what is needed (`SELECT ... FOR UPDATE`); define lock order to avoid deadlocks.
- Make migrations compatible with rolling deploys: expand → backfill in batches → switch → contract.
- Set `lock_timeout`/`statement_timeout` for migrations; avoid long table rewrites on hot tables.

## Security and operations

- Application role: least privilege, no DDL, no superuser. Migrations use a separate role.
- Encrypt in transit; enable encryption at rest; restrict backups.
- Row-level security/tenant filters where applicable; test cross-tenant access.
- Audit sensitive access; do not log full rows or PII.
- Test restore, not just backup. Know RPO/RTO.

## Dialect notes

- PostgreSQL: rich types, `jsonb`, CTEs, window functions, partial indexes; `ILIKE`, arrays, and extensions vary by hosting.
- MySQL/MariaDB: index prefix rules, `utf8mb4`, storage-engine differences; verify `EXPLAIN` behavior.
- SQLite: single-writer, `PRAGMA foreign_keys=ON`, WAL mode; see `technologies/databases/sqlite.md`.

## Checklist

- [ ] Parameters bound; identifiers allowlisted.
- [ ] Plan checked for new/changed queries; indexes justified.
- [ ] Migration tested on production-like data with lock impact measured.
- [ ] Transactions short and retry-safe.
- [ ] Tenant/row access tested; backups and restore verified.
