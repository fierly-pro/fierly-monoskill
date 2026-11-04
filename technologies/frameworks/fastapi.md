# FastAPI

> Load: FastAPI services.
> Pairs with: `platforms/backend.md`, `technologies/languages/python.md`, `security/api.md`, `security/auth.md`.

## Defaults

- Pydantic v2 models for request/response boundaries; set `response_model` to prevent accidental field exposure.
- Separate schemas (API) from ORM models and domain objects. Use `model_config = ConfigDict(extra="forbid")` where unknown fields are risky.
- Dependencies (`Depends`) for auth, DB sessions, pagination, and shared validation; keep them explicit and testable.
- Use `async def` only for non-blocking I/O. Synchronous DB drivers belong in `def` endpoints (run in a threadpool) or an async driver; never block the event loop.
- Manage DB sessions with a dependency that commits/rolls back and closes reliably. Do not share a session across requests.
- Central exception handlers for consistent error shapes; never leak stack traces.
- Configure CORS with exact origins; do not combine wildcard origins with credentials.
- Set timeouts on outbound HTTP; use a shared client with connection limits.

## Security

- Authentication as a dependency; authorization at the resource (check ownership/tenant), not only at the router.
- Validate path/query/body with constrained types (`conint`, `constr`, enums, `Literal`); enforce body size limits at the server/proxy.
- Rate-limit login, reset, OTP, and expensive endpoints (middleware or gateway).
- Do not log authorization headers, passwords, or tokens; redact request bodies.
- Store secrets in environment/secret manager; never in code or defaults.
- Use `secrets` for tokens; hash passwords with Argon2id/bcrypt.
- Serve docs/OpenAPI intentionally; restrict admin/internal routes.

## Operations

- Run with Uvicorn/Gunicorn workers behind a proxy; set `--proxy-headers` only for trusted proxies.
- Health endpoints: liveness vs readiness; do not expose dependency details publicly.
- Structured logs with request IDs; metrics for latency/errors.
- Graceful shutdown: finish in-flight requests, close pools/clients.
- Pin dependencies with a lockfile; build an immutable image.

## Testing

- `TestClient`/`httpx.AsyncClient` with dependency overrides for auth/DB; integration tests against a real test database for queries and transactions.
- Test authorization with multiple users/tenants, validation errors, and pagination bounds.
- Test OpenAPI schema compatibility for public APIs.
- Run migrations in tests; never rely on `create_all` for production parity.

## Checklist

- [ ] Request/response models prevent over-posting and field leaks.
- [ ] Authn/authz enforced per route and per object.
- [ ] Async endpoints do not block; sessions are request-scoped.
- [ ] Errors are consistent and non-leaky; CORS is explicit.
- [ ] Tests cover denial and validation paths.
