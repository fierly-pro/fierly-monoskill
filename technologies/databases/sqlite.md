# SQLite

> Load: embedded/local database in mobile, desktop, CLI, or small services.
> Pairs with: `technologies/languages/sql.md`, `security/database.md`, `platforms/android.md`/`ios.md`/`desktop.md`.

## Configuration that matters

```sql
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;      -- per connection, not persisted
PRAGMA busy_timeout = 5000;
PRAGMA synchronous = NORMAL;   -- WAL; use FULL for critical durability
```

- Enable foreign keys on **every** connection; SQLite defaults to off.
- WAL allows concurrent readers with one writer; still expect `SQLITE_BUSY` under write contention. Set a busy timeout and keep writes short.
- One writer at a time. For multi-process apps, serialize writes or use a single writer service; do not assume row-level concurrency.
- Use transactions for multi-statement writes; batch inserts in a transaction.

## Schema and queries

- SQLite types are affinities: use `INTEGER PRIMARY KEY`, `TEXT`, `REAL`, `BLOB`, and `CHECK` constraints for validation.
- `STRICT` tables (SQLite 3.37+) enforce types; use them for new schemas where supported.
- Index foreign keys and filter columns; verify with `EXPLAIN QUERY PLAN`.
- Avoid `SELECT *` on wide tables; paginate with keyset pagination.
- Dates: store UTC ISO-8601 text or integer epoch consistently; SQLite has no native timestamp type.

## Migrations and backup

- Version schema with the app/framework migration tool; test upgrades from every supported version.
- `PRAGMA user_version` or a migrations table for custom apps.
- Backup with the online backup API or `VACUUM INTO` while the DB is live; copying the file under WAL without care can corrupt it.
- Test restore; define what happens if the file is corrupted (recreate, sync, user notification).

## Security

- File permissions: owner-only; the DB is not encrypted by default. Use SQLCipher or platform file encryption for sensitive data.
- Do not store secrets in plaintext; use the platform keystore for keys.
- Parameterize queries; never interpolate input.
- Treat a local DB as untrusted input when opening files from users/other apps; validate schema/version.
- Exclude sensitive DBs from backups/cloud sync unless intended and encrypted.

## When not to use SQLite

- Many concurrent writers across processes/hosts.
- Network filesystems with unreliable locking.
- Large multi-tenant server workloads needing fine-grained concurrency, replication, or RLS.
  Use PostgreSQL or another client-server database.

## Checklist

- [ ] WAL, foreign keys, busy timeout configured per connection.
- [ ] Writes serialized/short; `SQLITE_BUSY` handled.
- [ ] Migrations tested from supported versions.
- [ ] Online backup/restore verified.
- [ ] Sensitive data encrypted; file permissions restricted.
