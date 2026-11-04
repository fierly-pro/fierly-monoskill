# Redis

> Load: Redis/Valkey caching, sessions, queues, rate limits, or locks.
> Pairs with: `platforms/backend.md`, `security/infrastructure.md`, `technologies/databases/postgresql.md`.

## Role

Redis is an in-memory data store, not a system of record unless persistence and durability are explicitly designed. Keep the source of truth in a durable database; treat cache loss as recoverable.

## Caching

- Cache-aside: read through the cache, load from the source, set with a TTL. Define invalidation on writes.
- Always set a TTL; avoid unbounded keys. Add jitter to prevent synchronized expiry.
- Prevent stampedes with a short lock/`SET NX` or stale-while-revalidate; bound the number of concurrent rebuilds.
- Namespace keys (`app:entity:id:version`); version keys for schema changes.
- Never use `KEYS` in production; use `SCAN` with a cursor, or maintain indexes/sets.
- Cache only what is safe to be stale; never cache authorization decisions without scope and invalidation.

## Data structures and atomicity

- Use the right type: strings for counters, hashes for objects, sets for membership, sorted sets for rankings/queues, streams for event logs.
- Atomic single commands (`INCR`, `SET NX`, `HSET`) avoid races. For multi-step logic use Lua scripts or `MULTI/EXEC`; keep them short.
- Distributed locks: `SET key token NX PX ttl`, release only if the token matches (Lua), and use fencing tokens for correctness. Do not treat a lock as a guarantee under partitions.
- Rate limiting: fixed/sliding window or token bucket in Lua; define behavior when Redis is unavailable (fail open vs closed).

## Memory and persistence

- Set `maxmemory` and an eviction policy appropriate to the use case (`allkeys-lru` for cache; `noeviction` for critical queues).
- Watch big keys and hot keys; split or shard them. Monitor fragmentation and memory usage.
- RDB snapshots vs AOF: choose durability; `appendfsync everysec` is a common tradeoff. Test recovery.
- Replication is asynchronous by default; failover can lose recent writes. Do not rely on Redis for data that cannot be lost unless configured accordingly.

## Security

- Bind to private interfaces; never expose Redis to the internet.
- Require TLS and ACLs; disable/rename dangerous commands (`FLUSHALL`, `CONFIG`, `KEYS`) for application users.
- Separate credentials per service; least privilege per key pattern.
- Do not store secrets/PII unencrypted unless the threat model accepts it; Redis has no built-in field encryption.
- Monitor unauthorized access attempts and anomalous commands.

## Operations

- Connection pooling; timeouts and retries with backoff; circuit breakers for cache outages.
- Cluster: hash tags for multi-key operations; avoid cross-slot transactions.
- Monitor latency, evictions, hit rate, memory, connections, replication lag, and persistence errors.
- Backups/restore for any data you cannot rebuild.

## Checklist

- [ ] TTLs and eviction policy defined.
- [ ] Invalidation and stampede protection implemented.
- [ ] No `KEYS`; big/hot keys monitored.
- [ ] Locks have tokens, TTLs, and fencing where correctness matters.
- [ ] Private network, TLS, ACLs; dangerous commands restricted.
