# Platform: Backend

> Load: server, API, service, worker, CLI daemon, or scheduled jobs.
> Pairs with: `security/api.md`, `security/auth.md`, `security/database.md`, `technologies/infrastructure/*`.

## Architecture defaults

- Separate transport (HTTP/gRPC), application/use cases, domain rules, and infrastructure. Keep domain logic testable without a server.
- Validate at the edge; authorize at the resource; keep business invariants in the domain/data layer.
- Configuration from the environment/secret manager, validated at startup. No silent fallback to insecure defaults.
- Stateless request handling where possible; externalize sessions, uploads, and cache. Make instances disposable.
- Define timeouts, retries (idempotent only, with jitter), circuit breaking, and backpressure for every dependency.
- Background jobs: idempotency keys, at-least-once handling, dead-letter queue, visibility timeout, metrics.
- Graceful shutdown: stop accepting, drain in-flight requests, close pools, finish or requeue jobs.

## API and data

- Version public contracts; use explicit DTOs; never expose ORM entities.
- Enforce pagination, payload limits, and query complexity limits.
- Use transactions for invariants; never hold a transaction across a network call.
- Migrations are versioned and compatible with the rolling deploy (expand/contract).
- Cache with a defined key, TTL, invalidation, and failure behavior; never cache authorization decisions without scope.

## Observability and operations

- Structured logs with correlation/request IDs; no secrets or unnecessary PII.
- Metrics: request rate, errors, latency histograms, saturation, dependency health, queue depth, job failures.
- Health endpoints: liveness (process) and readiness (dependencies); do not leak internals publicly.
- Traces across service boundaries where the system is distributed.
- Runbooks for common failures; alerts tied to user impact, not every error log.

## Security

- Authenticate every non-public endpoint; authorize per object with tenant isolation.
- Rate-limit auth, reset, OTP, search, export, and expensive operations.
- Parameterize queries; avoid shell interpolation; constrain outbound requests (SSRF).
- Secrets from a manager; least-privilege DB/service accounts; rotate.
- Generic error responses; detailed logs server-side.
- CORS allowlist; CSRF protection for cookie-authenticated writes; security headers at the edge.

## Testing

- Unit tests for domain rules; integration tests against real DB/queue/HTTP dependencies (containers/emulators) for queries, transactions, and authz.
- Contract tests for service boundaries; a few end-to-end tests for critical flows.
- Load test the critical endpoints with realistic payloads and data volume; verify timeouts and backpressure.
- Test migrations against a production-like snapshot, including rollback/forward-fix.

## Release

- Build an immutable artifact; deploy progressively; verify readiness and key metrics.
- Keep migrations backward-compatible during rollout; never require all instances to upgrade atomically.
- Document rollback and data implications; feature-flag risky behavior.

## Checklist

- [ ] Every route has explicit authn/authz and input validation.
- [ ] Timeouts, retries, and idempotency are defined for dependencies and writes.
- [ ] Logs/metrics/traces cover the new path without sensitive data.
- [ ] Migrations are compatible with the deploy strategy.
- [ ] Graceful shutdown and readiness behave correctly.
- [ ] Rate limits and resource bounds are in place.
