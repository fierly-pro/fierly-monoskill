# MongoDB

> Load: MongoDB/Mongoose applications.
> Pairs with: `platforms/backend.md`, `security/database.md`, `security/input.md`.

## Schema design

- Design from access patterns, not entity diagrams. Embed bounded, co-read data; reference unbounded or independently accessed data.
- Keep documents well below the 16 MB limit; avoid unbounded arrays that grow with time.
- Duplicate data deliberately for read performance and define how it stays consistent.
- Use schema validation (`$jsonSchema`) for critical collections.
- Version documents when the shape evolves; write migrations/backfills as idempotent scripts.

## Queries and indexes

- Follow ESR for compound indexes: **E**quality fields, **S**ort fields, **R**ange fields.
- Index every frequent filter/sort; use `explain("executionStats")` to confirm `IXSCAN` and acceptable examined/returned ratio.
- Use projections to avoid returning large/unneeded fields; paginate with range queries, not deep `skip`.
- TTL indexes for expiring data; partial indexes for sparse predicates.
- Avoid `$where`, `$function`, and unbounded regex; they bypass index usage and can execute server-side JS.
- **Operator injection:** never pass a request body directly as a filter. Validate types; reject keys starting with `$` and dotted paths from user input.

## Consistency and transactions

- Single-document updates are atomic; design to keep invariants within one document where possible.
- Multi-document transactions require a replica set/sharded cluster; they have time and size limits — keep them short.
- Choose write concern (`majority` for critical writes) and read concern deliberately.
- Use idempotency keys/unique indexes to handle retries and duplicate delivery.
- Change streams for reactive flows; handle resume tokens and at-least-once delivery.

## Security

- Enable authentication and TLS; never expose MongoDB to the public internet.
- Least-privilege roles per service; separate admin credentials; rotate.
- Encrypt at rest; consider client-side field-level encryption for high-sensitivity fields.
- Enable audit logging where available; restrict access to logs.
- Validate all input; see operator injection above.
- Keep the server and drivers patched; monitor CVEs.

## Operations

- Replica set with monitored lag and tested failover; sharding only with a measured need and a good shard key (high cardinality, non-monotonic, query-aligned).
- Backups: snapshots/`mongodump` with consistency; test restore. Know the difference between logical and physical backups.
- Monitor connections, op counters, cache pressure, replication lag, and slow queries.
- Size connection pools per instance; do not create a client per request.

## Checklist

- [ ] Access patterns documented; embed/reference choices justified.
- [ ] Compound indexes match queries; explain checked.
- [ ] No raw request filters; operator injection blocked.
- [ ] Auth/TLS/least privilege enabled; network restricted.
- [ ] Backups and restore tested; transactions used sparingly.
