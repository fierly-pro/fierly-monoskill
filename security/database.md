# Database Security

> Load: persistent data, schema changes, migrations, backups, or personal data.
> Pairs with: `technologies/languages/sql.md`, the database module, `security/input.md`, `security/auth.md`.

## Access control

- Use a dedicated application role with only the required DML privileges; no `SUPERUSER`, no schema ownership, no `DROP`.
- Separate roles for migrations/DDL, read-only analytics, and background jobs.
- One database/user per environment; never share production credentials with staging or developers.
- Enforce tenant isolation in queries or row-level security; derive the tenant from the authenticated context.
- Rotate credentials through a secret manager; support short-lived credentials where available.

## Queries and integrity

- Parameterize every untrusted value; allowlist identifiers. See `security/input.md`.
- Add constraints that encode invariants: primary keys, foreign keys, unique, check, not-null, appropriate types.
- Use transactions for multi-step invariants; choose isolation consciously and handle serialization failures/retries.
- Avoid unbounded queries: paginate, limit, and index the access path. Verify with `EXPLAIN` on realistic data.
- Do not disable foreign-key checks or unique constraints to "fix" an application bug.

## Encryption and data minimization

- Encrypt in transit (TLS, verified certificates) and at rest (volume/disk encryption).
- For high-sensitivity fields, add application-level encryption with keys in a KMS/secret manager; plan rotation and key loss.
- Hash passwords with a password KDF, not general-purpose encryption. See `security/auth.md`.
- Store only necessary data; define retention, deletion, export, and legal-hold behavior.
- Mask or tokenize sensitive values in non-production environments.

## Migrations

- Version-control every schema change; review for lock time, table rewrites, and backfill cost.
- Use expand → backfill → switch → contract for zero-downtime changes; keep old and new code compatible during rollout.
- Test on a production-like dataset; measure lock duration; set statement/lock timeouts.
- Make data fixes idempotent, batched, resumable, and reversible or forward-fixable.
- Never run destructive migrations without a verified backup and a tested restore/rollback path.

## Backups and recovery

- Encrypt backups; restrict access; keep an offsite/immutable copy per retention policy.
- Test restore regularly, including point-in-time recovery; record the restore time objective.
- Protect against ransomware: immutable/offline copies and separate credentials.
- Verify that backups cover the actual data stores, including object storage and search indexes.

## Audit and monitoring

- Log privileged actions, schema changes, bulk exports, and access to restricted data.
- Do not log full sensitive rows or credentials; use identifiers and redaction.
- Alert on unusual volume, failed logins to the DB, replication lag, and backup failures.
- Retain audit logs according to policy and protect them from modification.

## Verification

- Attempt injection with quotes/operators; confirm parameterization.
- Test cross-tenant reads/writes and object-level access.
- Inspect `EXPLAIN` for the main queries; check index usage and unbounded scans.
- Verify restore from backup in a non-production environment before relying on it.
